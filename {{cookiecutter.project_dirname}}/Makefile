.DEFAULT_GOAL := help

.PHONY: behave
behave:  ## Run behave test
	./scripts/behave.sh

.PHONY: check
check:  ## Check code formatting and import sorting
	./scripts/check.sh

.PHONY: collectstatic
collectstatic:  ## Django collectstatic
	python3 manage.py collectstatic --clear --noinput

.PHONY: compilemessages
compilemessages:  ## Django compilemessages
	python3 manage.py compilemessages

.PHONY: coverage
coverage:  ## Run coverage
	./scripts/coverage.sh

.PHONY: createsuperuser
createsuperuser:  ## Django createsuperuser
	python3 manage.py createsuperuser --noinput

.PHONY: dumpgroups
dumpgroups:  ## Django dump auth.Group data
	python3 manage.py dumpdata auth.Group --natural-foreign --natural-primary -o fixtures/auth_groups.json

.PHONY: fix
fix:  ## Fix code formatting, linting and sorting imports
	black .
	isort .
	flake8
	mypy .
	bandit -r -q -x tests .

.PHONY: flush
flush:  ## Django flush
	python manage.py flush --noinput

.PHONY: graph_models
graph_models:  ## Django generate graph models
	python3 manage.py graph_models -o models.svg

.PHONY: loadgroups
loadgroups:  ## Django load auth.Group data
	python3 manage.py loaddata fixtures/auth_groups.json

.PHONY: local
local: pip_update  ## Install local requirements and dependencies
	pip-sync requirements/local.txt

.PHONY: messages
messages:  ## Django makemessages
	python3 manage.py makemessages --add-location file --ignore requirements --ignore htmlcov --ignore features --ignore gunicorn.conf.py -l it

.PHONY: migrate
migrate:  ## Django migrate
	python3 manage.py migrate --noinput

.PHONY: migrations
migrations: ## Django makemigrations
	python3 manage.py makemigrations --no-header

.PHONY: outdated
outdated:  ## Check outdated requirements and dependencies
	python3 -m pip list --outdated

.PHONY: pip
pip: pip_update  ## Compile requirements
	pip-compile -q -U -o requirements/base.txt requirements/base.in
	pip-compile -q -U -o requirements/common.txt requirements/common.in
	pip-compile -q -U -o requirements/local.txt requirements/local.in
	pip-compile -q -U -o - requirements/remote.in | grep == > requirements/remote.txt 
	pip-compile -q -U -o requirements/test.txt requirements/test.in

.PHONY: pip_update
pip_update:  ## Update requirements and dependencies
	python3 -m pip install -q -U pip~=21.2.0 pip-tools~=6.3.0 setuptools~=58.2.0 wheel~=0.37.0

.PHONY: remote
remote: pip_update  ## Install remote requirements and dependencies
	pip-sync requirements/remote.txt

.PHONY: report
report:  ## Run coverage report
	./scripts/report.sh

ifeq (simpletest,$(firstword $(MAKECMDGOALS)))
  simpletestargs := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
  $(eval $(simpletestargs):;@true)
endif

.PHONY: simpletest
simpletest:  ## Run debugging test
	# You can pass more arguments as follows:
	# make simpletest -- --keepdb --failfast --pdb --debug-sql --verbosity 2 path.to.TestClass
	python3 manage.py test --configuration=Testing $(simpletestargs)

.PHONY: test
test:  ## Run test
	./scripts/test.sh

.PHONY: help
help:
	@echo "[Help] Makefile list commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
