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

local:
	python3 -m pip install -q -U pip~=21.0.0 pip-tools~=5.5.0
	pip-sync requirements/local.txt

dumpgroups:
	python3 manage.py dumpdata auth.Group --indent 2 --natural-foreign --natural-primary -o fixtures/auth_groups.json

fix:
	black .
	isort .
	flake8
	mypy .

graph_models:
	python3 manage.py graph_models -o models.svg

loadgroups:
	python3 manage.py loaddata fixtures/auth_groups.json

messages:
	python3 manage.py makemessages --add-location file --ignore requirements --ignore htmlcov --ignore features --all

migrate:
	python3 manage.py migrate --noinput

migrations:
	python3 manage.py makemigrations --no-header

outdated:
	python3 -m pip list --outdated

pip:
	python3 -m pip install -q -U pip~=21.0.0 pip-tools~=5.5.0
	pip-compile -q -U -o requirements/base.txt requirements/base.in
	pip-compile -q -U -o requirements/common.txt requirements/common.in
	pip-compile -q -U -o requirements/local.txt requirements/local.in
	pip-compile -q -U -o requirements/remote.txt requirements/remote.in
	pip-compile -q -U -o requirements/test.txt requirements/test.in

remote:
	python3 -m pip install -q -U pip~=21.0.0 pip-tools~=5.5.0
	pip-sync requirements/remote.txt

report:
	./scripts/report.sh

ifeq (simpletest,$(firstword $(MAKECMDGOALS)))
  simpletestargs := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
  $(eval $(simpletestargs):;@true)
endif

simpletest:
	# You can pass more arguments as follow:
	# $ make simpletest -- --keepdb --failfast --pdb --debug-sql --verbosity 2 path.to.TestClass
	python3 manage.py test --configuration=Testing $(simpletestargs)

test:
	./scripts/test.sh
