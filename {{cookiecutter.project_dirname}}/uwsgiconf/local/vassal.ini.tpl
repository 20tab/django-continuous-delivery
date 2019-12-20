[uwsgi]

project_name = {{cookiecutter.project_slug}}
venv_name = {{cookiecutter.project_slug}}
py_version = PYVERSION
uid = USERNAME
gid = USERNAME

workarea_root = WORKAREA_ROOT

project_root = %(workarea_root)/%(project_name)
venvs_dir = VENV_ROOT

# Set environment variables
for-readline = WORKAREA_ROOT/{{cookiecutter.project_slug}}/.env
  env = %(_)
endfor =

ini = WORKAREA_ROOT/{{cookiecutter.project_slug}}/uwsgiconf/local/global.ini
ini = WORKAREA_ROOT/{{cookiecutter.project_slug}}/uwsgiconf/local/static.ini

# Not required if uwsgi was installed using pip
plugin = python3

socket = 127.0.0.1:0
subscribe-to = 127.0.0.1:5005:%(project_name).local

# Logging
plugin = logfile
logger = file:logfile=/%(project_root)/%(project_name).log
# Parsable date/time
log-date = %%Y-%%m-%%dT%%H:%%M:%%S
logformat-strftime = true
# JSON lines format
log-format = {"timestamp": "%(ftime)", "method": "%(method)", "uri": "%(uri)", "proto": "%(proto)", "status": %(status), "referer": "%(referer)", "user_agent": "%(uagent)", "remote_addr": "%(addr)", "user_id": "%(userid)", "http_host": "%(host)", "pid": %(pid), "worker_id": %(wid), "core": %(core), "async_switches": %(switches), "io_errors": %(ioerr), "rq_size": %(cl), "rs_time_ms": %(msecs), "rs_size": %(size), "rs_header_size": %(hsize), "rs_header_count": %(headers)}
req-logger = file:logfile=/%(project_root)/%(project_name)_access.log
logfile-chown = %U:%G

# Zeroconf
plugin = ZEROCONF
ZEROCONF-register = ZEROOPTS

processes = 1
threads = 1
