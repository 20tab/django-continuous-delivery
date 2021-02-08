behave:
	python manage.py behave --configuration=Testing --simple

check:
	black -q --check .
	isort -q --check .
	flake8
	mypy .

collectstatic:
	python manage.py collectstatic --clear --noinput

compilemessages:
	python manage.py compilemessages

coverage:
	coverage run --concurrency=multiprocessing manage.py test --configuration=Testing --noinput --parallel --debug-sql
	coverage combine
	coverage html
	coverage report

dev:
	pip install -q -U pip~=21.0.0 pip-tools~=5.5.0
	pip-sync requirements/dev.txt

dumpgroups:
	python manage.py dumpdata auth.Group --indent 2 --natural-foreign --natural-primary -o fixtures/auth_groups.json

fix:
	black .
	isort .
	flake8
	mypy .

graph_models:
	python manage.py graph_models -o models.svg

loadgroups:
	python manage.py loaddata fixtures/auth_groups.json

messages:
	python manage.py makemessages --add-location file

migrate:
	python manage.py migrate --noinput

migrations:
	python manage.py makemigrations --no-header

pip:
	pip install -q -U pip~=21.0.0 pip-tools~=5.5.0
	pip-compile -q -U -o requirements/common.txt requirements/common.in
	pip-compile -q -U -o requirements/dev.txt requirements/dev.in
	pip-compile -q -U -o requirements/prod.txt requirements/prod.in
	pip-compile -q -U -o requirements/tests.txt requirements/tests.in

prod:
	pip install -q -U pip~=21.0.0 pip-tools~=5.5.0
	pip-sync requirements/prod.txt

ifeq (simpletest,$(firstword $(MAKECMDGOALS)))
  simpletestargs := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
  $(eval $(simpletestargs):;@true)
endif

simpletest:
	python manage.py test --configuration=Testing --debug-sql $(simpletestargs)

test: check behave coverage
