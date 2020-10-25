[uwsgi]

project_name = {{cookiecutter.project_slug}}
venv_name = {{cookiecutter.project_slug}}
py_version = __PYVERSION__

workarea_root = __WORKAREA_ROOT__

project_root = %(workarea_root)/%(project_name)
venvs_dir = __VENV_ROOT__

# Set environment variables
for-readline = __WORKAREA_ROOT__/{{cookiecutter.project_slug}}/.env
  env = %(_)
endfor =

ini = %dglobal.ini
ini = %dstatic.ini

# Not required if uwsgi was installed with pip
plugin = __PYTHON__

http-socket = :8080

processes = 1
threads = 1

# Reload the app if any py module or this config file change (debug only)
py-auto-reload = 1
touch-reload = %p
