"""Define invoke tasks."""

import getpass
import os
import secrets
import sys
from pathlib import Path

from invoke import task

EMPEROR_MODE = True
USERNAME = getpass.getuser()
PROJECT_PATH = Path(__file__).parent
PROJECT_NAME = PROJECT_PATH.name
ENV_FILE = PROJECT_PATH / ".env"
ENV_TEMPLATE = PROJECT_PATH / ".env_template"
WORKAREA_ROOT = PROJECT_PATH.parent
VASSAL_DIR = WORKAREA_ROOT / "vassals"


@task
def init(c):
    """Initialize project."""
    try:
        VENV_ROOT = Path(os.getenv("VIRTUAL_ENV")).parent
    except TypeError:
        sys.exit("Activate your virtualenv and run the inv command again.")
    EMPEROR_MODE = confirm(
        "Do you want to configure your uWSGI vassal in emperor mode? (no=stand-alone)"
    )
    vassal_path = str(VASSAL_DIR)
    if EMPEROR_MODE:
        vassal_path = (
            input(
                f"We will use '{vassal_path}' as vassal directory or specify the path: "
            )
            or vassal_path
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
        input("Specify python plugin to configure uwsgi (default: python3): ")
        or "python3"
    )
    INI_DIR = PROJECT_PATH / "uwsgiconf" / "local"
    PYVERSION = f"{sys.version_info.major}.{sys.version_info.minor}"
    print("Generating uwsgi user file")
    vassal_project = Path(vassal_path) / f"{PROJECT_NAME}.ini"
    vassal_file = INI_DIR / f"{USERNAME}.ini"
    if EMPEROR_MODE and not vassal_project.exists():
        vassal_template = INI_DIR / "vassal.ini_template"
        vassal_text = vassal_template.read_text()
        vassal_text = (
            vassal_text.replace("__USERNAME__", USERNAME)
            .replace("__ZEROCONF__", ZEROCONF)
            .replace("__ZEROOPTS__", ZEROOPTS)
        )
        vassal_file.write_text(vassal_text)
        vassal_project.symlink_to(vassal_file)
    else:
        vassal_template = INI_DIR / "standalone.ini_template"
        vassal_file.write_text(vassal_template.read_text())
    vassal_text = vassal_file.read_text()
    vassal_text = (
        vassal_text.replace("__PYTHON__", python_plugin)
        .replace("__WORKAREA_ROOT__", f"{WORKAREA_ROOT}")
        .replace("__PYVERSION__", PYVERSION)
        .replace("__VENV_ROOT__", f"{VENV_ROOT}")
    )
    vassal_file.write_text(vassal_text)
    db_name = (
        input(f"We'll use '{PROJECT_NAME}' as database name or specify the name: ")
        or PROJECT_NAME
    )
    db_user = (
        input("We'll use 'postgres' as database user name or specify the user name: ")
        or "postgres"
    )
    db_host = (
        input("We'll use '127.0.0.1' as database host or specify the host: ")
        or "127.0.0.1"
    )
    db_port = (
        input("We'll use '5432' as database posrt or specify the port: ") or "5432"
    )
    db_password = getpass.getpass("Enter the database user password: ")
    print("Create env file")
    if not ENV_FILE.exists():
        ENV_FILE.write_text(ENV_TEMPLATE.read_text())
    env_text = ENV_FILE.read_text()
    env_text = (
        env_text.replace("__NAME__", db_name)
        .replace("__PASSWORD__", db_password)
        .replace("__USERNAME__", db_user)
        .replace("__HOST__", db_host)
        .replace("__PORT__", db_port)
        .replace("__SECRETKEY__", secrets.token_urlsafe(40))
    )
    ENV_FILE.write_text(env_text)
    print("Compiling pip file in requirements")
    c.run("make pip")
    print("Installing libraries in requirements")
    c.run("make dev")
    print("Creating static and media empty directories")
    Path("static").mkdir(exist_ok=True)
    Path("media").mkdir(exist_ok=True)
    print("Collect static files")
    c.run("make collectstatic")
    createdb(c)
    print("Install pre-commit")
    c.run("black .")
    c.run("pre-commit install")
    print("*** Next steps ***")
    print(f"a) Check the uwsgiconf/local/{USERNAME}.ini and verify the python plugin")
    print(f"b) Configure the file by {PROJECT_NAME}/settings.py")


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
        "bzip2 -9 > backup/dump.sql.bz2"
    )


@task
def restoredb(c, dump_filename):
    """Restore database."""
    db_name, db_host, db_port, db_user = get_db()
    c.run(
        f"bzip2 -c -d {dump_filename} | "
        f"psql -q -o /dev/null -h {db_host} -p {db_port} -U {db_user} {db_name}"
    )


@task
def gitinit(c, git_repository_url):
    """Initialize git repository."""
    c.run(f'sed -i".bak" -e "s,GIT_REPOSITORY_URL,{git_repository_url},g;" README.md')
    c.run("git init")
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
    from dj_database_url import parse
    from dotenv import find_dotenv, load_dotenv

    load_dotenv(find_dotenv())
    db_url = os.getenv("DATABASE_URL")
    db_default = parse(db_url)
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
        response = input(f"{question} [{suffix}] ")
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
