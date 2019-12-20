[uwsgi]

project_name = {{cookiecutter.project_slug}}
venv_name = {{cookiecutter.project_slug}}
py_version = PYVERSION

workarea_root = WORKAREA_ROOT

project_root = %(workarea_root)/%(project_name)
venvs_dir = VENV_ROOT

# Set environment variables
for-readline = WORKAREA_ROOT/{{cookiecutter.project_slug}}/.env
  env = %(_)
endfor =

ini = %dglobal.ini
ini = %dstatic.ini

# Not required if uwsgi was installed with pip
plugin = python3

http-socket = :8080

processes = 1
threads = 1

# Reload the app if any py module or this config file change (debug only)
py-auto-reload = 1
touch-reload = %p
