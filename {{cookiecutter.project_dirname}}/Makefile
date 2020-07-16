# Develop

check:
	black --check .
	isort --check-only --recursive
	flake8
	mypy .

collectstatic:
	python manage.py collectstatic --clear --noinput

compilemessages:
	python manage.py compilemessages -i .tox

dev:
	pip install -q -U pip~=20.1.0 pip-tools~=5.2.0
	pip-sync requirements/dev.txt

fix:
	black .
	isort --recursive -y
	flake8
	mypy .

graph_models:
	python manage.py graph_models -o models.svg

messages:
	python manage.py makemessages --add-location file

migrate:
	python manage.py migrate --noinput

migrations:
	python manage.py makemigrations --no-header

pip:
	pip install -q -U pip~=20.1.0 pip-tools~=5.2.0
	pip-compile -q -U -o requirements/common.txt requirements/common.ini
	pip-compile -q -U -o requirements/dev.txt requirements/dev.ini
	pip-compile -q -U -o requirements/prod.txt requirements/prod.ini
	pip-compile -q -U -o requirements/tests.txt requirements/tests.ini

test:
	tox -e coverage,reporthtml,report
