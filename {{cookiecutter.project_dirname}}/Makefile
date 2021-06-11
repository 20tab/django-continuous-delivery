behave:
	./scripts/behave.sh

check:
	./scripts/check.sh

collectstatic:
	python3 manage.py collectstatic --clear --noinput

compilemessages:
	python3 manage.py compilemessages

coverage:
	./scripts/coverage.sh

createsuperuser:
	python3 manage.py createsuperuser --noinput

dumpgroups:
	python3 manage.py dumpdata auth.Group --natural-foreign --natural-primary -o fixtures/auth_groups.json

fix:
	black .
	isort .
	flake8
	mypy .

flush:
	python manage.py flush --noinput

graph_models:
	python3 manage.py graph_models -o models.svg

loadgroups:
	python3 manage.py loaddata fixtures/auth_groups.json

local: pip_update
	pip-sync requirements/local.txt

messages:
	python3 manage.py makemessages --add-location file --ignore requirements --ignore htmlcov --ignore features --ignore gunicorn.conf.py -l it

migrate:
	python3 manage.py migrate --noinput

migrations:
	python3 manage.py makemigrations --no-header

outdated:
	python3 -m pip list --outdated

pip: pip_update
	pip-compile -q -U -o requirements/base.txt requirements/base.in
	pip-compile -q -U -o requirements/common.txt requirements/common.in
	pip-compile -q -U -o requirements/local.txt requirements/local.in
	pip-compile -q -U -o requirements/remote.txt requirements/remote.in
	pip-compile -q -U -o requirements/test.txt requirements/test.in

pip_update:
	python3 -m pip install -q -U pip~=21.1.0 pip-tools~=6.1.0 setuptools~=57.0.0 wheel~=0.36.0

remote: pip_update
	pip-sync requirements/remote.txt

report:
	./scripts/report.sh

ifeq (simpletest,$(firstword $(MAKECMDGOALS)))
  simpletestargs := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
  $(eval $(simpletestargs):;@true)
endif

simpletest:
	# You can pass more arguments as follows:
	# $ make simpletest -- --keepdb --failfast --pdb --debug-sql --verbosity 2 path.to.TestClass
	python3 manage.py test --configuration=Testing $(simpletestargs)

test:
	./scripts/test.sh
