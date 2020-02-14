DATABASE_URL=postgres://postgres:postgres@postgres:5432/{{cookiecutter.project_slug}}
DJANGO_ADMINS={{cookiecutter.project_slug}},errors@{{cookiecutter.project_slug}}.com
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_CONFIGURATION=Local
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=secretkey
DJANGO_SERVER_EMAIL=info@{{cookiecutter.project_slug}}.com
EMAIL_URL=console:///
