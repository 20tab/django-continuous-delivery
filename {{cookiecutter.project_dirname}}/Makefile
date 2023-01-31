.DEFAULT_GOAL := help

.PHONY: behave
behave:  ## Run behave test
	./scripts/behave.sh

.PHONY: check
check:  ## Check code formatting and import sorting
	./scripts/check.sh

.PHONY: collectstatic
collectstatic:  ## Django collectstatic
	python3 -m manage collectstatic --clear --link --noinput

.PHONY: compilemessages
compilemessages:  ## Django compilemessages
	python3 -m manage compilemessages

.PHONY: coverage
coverage:  ## Run coverage
	./scripts/coverage.sh

.PHONY: createsuperuser
createsuperuser:  ## Django createsuperuser
	python3 -m manage createsuperuser --noinput

.PHONY: dumpgroups
dumpgroups:  ## Django dump auth.Group data
	python3 -m manage dumpdata auth.Group --natural-foreign --natural-primary --output fixtures/auth_groups.json

.PHONY: fix
fix:  ## Fix code formatting, linting and sorting imports
	python3 -m black .
	ruff --fix .
	python3 -m mypy --no-site-packages .

.PHONY: flush
flush:  ## Django flush
	python3 -m manage flush --noinput

.PHONY: graph_models
graph_models:  ## Django generate graph models
	python3 -m manage graph_models --output models.svg

.PHONY: loadgroups
loadgroups:  ## Django load auth.Group data
	python3 -m manage loaddata fixtures/auth_groups.json

.PHONY: local
local: pip_update  ## Install local requirements and dependencies
	python3 -m piptools sync requirements/local.txt

.PHONY: messages
messages:  ## Django makemessages
	python3 -m manage makemessages --add-location file --ignore requirements --ignore htmlcov --ignore features --ignore gunicorn.conf.py --locale it

.PHONY: migrate
migrate:  ## Django migrate
	python3 -m manage migrate --noinput

.PHONY: migrations
ifeq ($(name),)
migrations: ## Django makemigrations with optional `name="migration_name app_name"`
	python3 -m manage makemigrations --no-header
else
migrations:
	python3 -m manage makemigrations --no-header --name $(name)
endif

.PHONY: outdated
outdated:  ## Check outdated requirements and dependencies
	python3 -m pip list --outdated

.PHONY: pip
pip: pip_update  ## Compile requirements
	python3 -m piptools compile --generate-hashes --no-header --quiet --resolver=backtracking --upgrade --output-file requirements/base.txt requirements/base.in
	python3 -m piptools compile --generate-hashes --no-header --quiet --resolver=backtracking --upgrade --output-file requirements/common.txt requirements/common.in
	python3 -m piptools compile --generate-hashes --no-header --quiet --resolver=backtracking --upgrade --output-file requirements/local.txt requirements/local.in
	python3 -m piptools compile --generate-hashes --no-header --quiet --resolver=backtracking --upgrade --output-file requirements/remote.txt requirements/remote.in
	python3 -m piptools compile --generate-hashes --no-header --quiet --resolver=backtracking --upgrade --output-file requirements/test.txt requirements/test.in

.PHONY: pip_update
pip_update:  ## Update requirements and dependencies
	python3 -m pip install --quiet --upgrade pip~=23.0.0 pip-tools~=6.12.0 setuptools~=67.0.0 wheel~=0.38.0

.PHONY: precommit
precommit:  ## Fix code formatting, linting and sorting imports
	python3 -m pre_commit run --all-files

.PHONY: precommit_update
precommit_update:  ## Update pre_commit
	python3 -m pre_commit autoupdate

.PHONY: pytest
pytest:  ## Run debugging test
	python3 -m pytest --capture=no --dc=Testing --durations 10

.PHONY: remote
remote: pip_update  ## Install remote requirements and dependencies
	python3 -m piptools sync requirements/remote.txt

.PHONY: report
report:  ## Run coverage report
	./scripts/report.sh

.PHONY: runserver
runserver:  ## Django run
	python3 -m manage runserver 0:8000

.PHONY: shellplus
shellplus:  ## Run shell_plus
	python3 -m manage shell_plus

ifeq (simpletest,$(firstword $(MAKECMDGOALS)))
  simpletestargs := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
  $(eval $(simpletestargs):;@true)
endif

.PHONY: simpletest
simpletest:  ## Run debugging test
	# You can pass more arguments as follows:
	# make simpletest -- --debug-sql --failfast --keepdb --pdb --verbosity 2 path.to.TestClass
	python3 -m manage test --configuration=Testing --shuffle --timing $(simpletestargs)

.PHONY: test
test:  ## Run test
	./scripts/test.sh

.PHONY: update
update: pip precommit_update ## Run update

CURRENT_BRANCH=`git rev-parse --abbrev-ref HEAD`

.PHONY: verifybranchpacts
verifybranchpacts:  ## Verify pact for the current branch consumer tag
	./scripts/pact_verify.sh --verbose --capture=no --pact-verify-consumer-tag="branch:"$(CURRENT_BRANCH)

.PHONY: verifypacts
verifypacts:  ## Verify pact for all environments consumer tags
	./scripts/pact_verify.sh --verbose --capture=no --pact-verify-consumer-tag="branch:"$(CURRENT_BRANCH)
	./scripts/pact_verify.sh --verbose --capture=no --pact-verify-consumer-tag="env:dev"
	./scripts/pact_verify.sh --verbose --capture=no --pact-verify-consumer-tag="env:stage"
	./scripts/pact_verify.sh --verbose --capture=no --pact-verify-consumer-tag="env:prod"

.PHONY: help
help:
	@echo "[Help] Makefile list commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
