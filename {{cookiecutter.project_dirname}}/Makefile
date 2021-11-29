.DEFAULT_GOAL := help

.PHONY: behave
behave:  ## Run behave test
	./scripts/behave.sh --reverse

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
	python3 -m black .
	python3 -m isort .
	python3 -m flake8
	python3 -m mypy .

.PHONY: flush
flush:  ## Django flush
	python3 manage.py flush --noinput

.PHONY: graph_models
graph_models:  ## Django generate graph models
	python3 manage.py graph_models -o models.svg

.PHONY: loadgroups
loadgroups:  ## Django load auth.Group data
	python3 manage.py loaddata fixtures/auth_groups.json

.PHONY: local
local: pip_update  ## Install local requirements and dependencies
	python3 -m piptools sync requirements/local.txt

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
	python3 -m piptools compile --no-header --quiet --upgrade --output-file requirements/base.txt requirements/base.in
	python3 -m piptools compile --no-header --quiet --upgrade --output-file requirements/common.txt requirements/common.in
	python3 -m piptools compile --no-header --quiet --upgrade --output-file requirements/local.txt requirements/local.in
	python3 -m piptools compile --no-header --quiet --upgrade --output-file requirements/remote.txt requirements/remote.in
	python3 -m piptools compile --no-header --quiet --upgrade --output-file requirements/test.txt requirements/test.in

.PHONY: pip_update
pip_update:  ## Update requirements and dependencies
	python3 -m pip install -q -U pip~=21.3.0 pip-tools~=6.4.0 setuptools~=59.4.0 wheel~=0.37.0

.PHONY: precommit
precommit:  ## Fix code formatting, linting and sorting imports
	python3 -m pre_commit run --all-files

.PHONY: precommit_update
precommit_update:  ## Update pre_commit
	python3 -m pre_commit autoupdate

.PHONY: pytest
pytest:  ## Run debugging test
	python3 -m pytest --durations 10

.PHONY: remote
remote: pip_update  ## Install remote requirements and dependencies
	python3 -m piptools sync requirements/remote.txt

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
	python3 manage.py test --configuration=Testing --timing $(simpletestargs)

.PHONY: test
test:  ## Run test
	./scripts/test.sh

.PHONY: update
update: pip precommit_update ## Run update

.PHONY: help
help:
	@echo "[Help] Makefile list commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
