"""Define invoke tasks."""

import getpass
import os
import sys
from pathlib import Path

import dj_database_url
from django.core.management.utils import get_random_secret_key
from dotenv import find_dotenv, load_dotenv
from invoke import task

BASE_DIR = os.path.dirname(__file__)
BASE_DIRNAME = os.path.dirname(BASE_DIR)
PROJECT_DIRNAME = os.path.basename(os.path.dirname(__file__))
EMPEROR_MODE = True
VASSALS = f"{BASE_DIRNAME}/vassals"
USERNAME = os.getlogin()
ENV_FILE = f"{BASE_DIR}/.env"
SECRET_KEY = get_random_secret_key()


@task
def init(c):
    """Initialize project."""
    try:
        VENV_ROOT = str(Path(os.getenv("VIRTUAL_ENV")).parent).replace(
            "/", "\/"
        )  # noqa
    except TypeError:
        print("Activate your virtualenv and run the inv command again")
        return
    EMPEROR_MODE = confirm(
        "Do you want to configure your uWSGI vassal in emperor mode? (no=stand-alone)"
    )
    if EMPEROR_MODE:
        vassals = (
            input(
                f"We will use '{VASSALS}' as the vassal directory or specify the path: "
            )
            or VASSALS
        )
        bonjour = confirm(
            "Do you want to use Bonjour for OSX (Yes) or Avahi for Linux (No)? "
        )
        if bonjour:
            ZEROCONF = "bonjour"
            ZEROOPTS = "name=%(project_name).local,cname=localhost"
        else:
            ZEROCONF = "avahi"
            ZEROOPTS = "%(project_name).local"
    python_plugin = (
        input(f"Specify python plugin to configure uwsgi (default: python3): ")
        or "python3"
    )
    database = (
        input(f"We'll use '{PROJECT_DIRNAME}' as database name or specify the name: ")
        or PROJECT_DIRNAME
    )
    username = input(f"Enter the database user name: ")
    password = getpass.getpass(f"Enter the database user password: ")
    print("Compiling pip file in requirements")
    c.run("make pip")
    print("Installing libraries in requirements")
    c.run("make dev")
    if not os.path.exists("static"):
        print("Making static directory")
        c.run("mkdir static")
    if not os.path.exists("media"):
        print("Making media directory")
        c.run("mkdir media")
    ini_dir = f"{BASE_DIR}/uwsgiconf/local"
    PYVERSION = f"{sys.version_info[0]}.{sys.version_info[1]}"
    WORKAREA_ROOT = BASE_DIRNAME.replace("/", "\/")  # noqa
    print("Generating uwsgi user file")
    if EMPEROR_MODE and not os.path.exists(f"{vassals}/{PROJECT_DIRNAME}.ini"):
        c.run(f"cp {ini_dir}/vassal.ini.tpl {ini_dir}/{USERNAME}.ini")
        c.run(
            (
                f'sed -i".bak" -e "s/USERNAME/{USERNAME}/g;s/ZEROCONF/{ZEROCONF}/g;'
                f's/ZEROOPTS/{ZEROOPTS}/g;" {ini_dir}/{USERNAME}.ini'
            )
        )
        c.run(
            f"ln -s "
            f"{BASE_DIR}/uwsgiconf/local/{USERNAME}.ini "
            f"{vassals}/{PROJECT_DIRNAME}.ini"
        )
    else:
        c.run(f"cp {ini_dir}/standalone.ini.tpl {ini_dir}/{USERNAME}.ini")
    c.run(
        f'sed -i".bak" -e "s/plugin = python3/plugin = {python_plugin}/g;"'
        f" {ini_dir}/{USERNAME}.ini"
    )
    c.run(
        f'sed -i".bak" -e "s/WORKAREA_ROOT/{WORKAREA_ROOT}/g;" {ini_dir}/{USERNAME}.ini'
    )
    c.run(f'sed -i".bak" -e "s/PYVERSION/{PYVERSION}/g;" {ini_dir}/{USERNAME}.ini')
    c.run(f'sed -i".bak" -e "s/VENV_ROOT/{VENV_ROOT}/g;" {ini_dir}/{USERNAME}.ini')
    print("Create env file")
    if not os.path.exists(f"{ENV_FILE}"):
        c.run(f"cp {ENV_FILE}.tpl {ENV_FILE}")
    c.run(
        (
            f'sed -i".bak" -e '
            f'"s/database/{database}/g;s/password/{password}/g;'
            f's/secretkey/{SECRET_KEY}/g;s/username/{username}/g"'
            f" {ENV_FILE}"
        )
    )
    print("Collect static files")
    c.run("make collectstatic")
    createdb(c)
    print("*** Next steps ***")
    print(f"a) Check the uwsgiconf/local/{USERNAME}.ini and verify the python plugin")
    print(f"b) Configure the file by {PROJECT_DIRNAME}/settings.py")
    if EMPEROR_MODE:
        c.run(f"python -m webbrowser -t http://{PROJECT_DIRNAME}.local/")


@task
def createdb(c):
    """Create database."""
    if confirm(
        "Attention: you are creating the PostgreSQL DB. Do you want to proceed?"
    ):
        db_name, db_host, db_port, db_user = get_db()
        c.run(
            f"createdb -e -h {db_host} -p {db_port} -U {db_user} -O {db_user} {db_name}"
        )
        if confirm("Attention: you are applying migrations. Do you want to proceed?"):
            c.run("make migrate")


@task
def dropdb(c):
    """Drop database."""
    if confirm("Warning, you are deleting the db. Are you sure you want to proceed?"):
        db_name, db_host, db_port, db_user = get_db()
        c.run(f"dropdb -e -h {db_host} -p {db_port} -U {db_user} {db_name}")


@task
def dumpdb(c):
    """Dump database."""
    db_name, db_host, db_port, db_user = get_db()
    c.run(
        f"pg_dump -h {db_host} -p {db_port} -U {db_user} {db_name} | "
        "bzip2 -9 > deploy/dump.sql.bz2"
    )


@task
def gitinit(c, git_repository_url):
    """Initialize git repository."""
    c.run(f'sed -i".bak" -e "s,GIT_REPOSITORY_URL,{git_repository_url},g;" README.md')
    c.run("git init")
    c.run("pre-commit install")
    c.run("git add -A")
    c.run("git commit -m 'Initial commit'")
    c.run(f"git remote add origin {git_repository_url}")
    c.run("git push -u origin master")


@task
def restart(c):
    """Restart uWSGI instance."""
    c.run(f"touch uwsgiconf/local/{USERNAME}.ini")


def get_db():
    """Fetch database credentials."""
    load_dotenv(find_dotenv())
    db_url = os.getenv("DATABASE_URL")
    db_default = dj_database_url.parse(db_url)
    db_name = db_default["NAME"]
    db_host = db_default["HOST"]
    db_port = db_default["PORT"]
    db_user = db_default["USER"]
    return db_name, db_host, db_port, db_user


# NOTE: originally cribbed from fab 1's contrib.console.confirm
def confirm(question, assume_yes=True):
    """
    Ask user a yes/no question and return their response as a boolean.

    ``question`` should be a simple, grammatically complete question such as
    "Do you wish to continue?", and will have a string similar to ``" [Y/n] "``
    appended automatically. This function will *not* append a question mark for
    you.

    By default, when the user presses Enter without typing anything, "yes" is
    assumed. This can be changed by specifying ``affirmative=False``.

    .. note::
        If the user does not supplies input that is (case-insensitively) equal
        to "y", "yes", "n" or "no", they will be re-prompted until they do.

    :param str question: The question part of the input.
    :param bool assume_yes:
        Whether to assume the affirmative answer by default. Default value:
        ``True``.

    :returns: A `bool`.
    """
    # Set up suffix
    if assume_yes:
        suffix = "Y/n"
    else:
        suffix = "y/N"
    # Loop till we get something we like
    # TODO: maybe don't do this? It can be annoying. Turn into 'q'-for-quit?
    while True:
        # TODO: ensure that this is Ctrl-C friendly, ISTR issues with
        # raw_input/input on some Python versions blocking KeyboardInterrupt.
        response = input("{0} [{1}] ".format(question, suffix))
        response = response.lower().strip()  # Normalize
        # Default
        if not response:
            return assume_yes
        # Yes
        if response in ["y", "yes"]:
            return True
        # No
        if response in ["n", "no"]:
            return False
        # Didn't get empty, yes or no, so complain and loop
        err = "I didn't understand you. Please specify '(y)es' or '(n)o'."
        print(err, file=sys.stderr)
