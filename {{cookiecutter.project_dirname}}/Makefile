# Develop

check:
	black --check .
	flake8
	isort --check-only --recursive
	mypy .

checkcommit:
	black .
	flake8
	isort --recursive
	mypy .

collectstatic:
	python manage.py collectstatic --clear --noinput

dev:
	pip install -q -U pip~=20.0.1 pip-tools~=4.4.0
	pip-sync requirements/dev.txt

migrate:
	python manage.py migrate --noinput

migrations:
	python manage.py makemigrations --no-header

pip:
	pip install -q -U pip~=20.0.1 pip-tools~=4.4.0
	pip-compile $(p) requirements/common.ini > requirements/common.txt
	pip-compile $(p) requirements/dev.ini > requirements/dev.txt
	pip-compile $(p) requirements/prod.ini > requirements/prod.txt
	pip-compile $(p) requirements/tests.ini > requirements/tests.txt
	pip-compile $(p) requirements/local.ini > requirements/local.txt

test:
	tox -e coverage,reporthtml,report
