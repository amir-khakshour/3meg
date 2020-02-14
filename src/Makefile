VENV = venv
PYTEST = $(PWD)/$(VENV)/bin/py.test

.PHONY: build test clean venv

all: clean_py build server

clean_py:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -Rf *.egg-info
	rm -Rf dist/
	rm -Rf build/

##################
# Install commands
##################
install: install-base ## Install requirements for local development and production
install_dev: install install-dev ## Install requirements for local development and production
install_test: install install-test ## Install requirements for local development and production

install-base: ## Install python base requirements
	pip install -r requirements/base.txt

install-test: ## Install test requirements
	pip install -e .[test]

install-dev: ## Install dev requirements
	pip install -r requirements/dev.txt

venv: ## Create a virtual env and install test and production requirements
	$(shell which python3) -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements/base.txt
	$(VENV)/bin/pip install -r requirements/test.txt

check_venv:
ifeq ($(VIRTUAL_ENV),)
	$(error "Run frost from a virtualenv (try 'make venv && source venv/bin/activate')")
endif
#############################
# Sandbox management commands
#############################
build: clean load_data statics

clean:
	# Remove media
	-rm -rf src/files/media/images
	-rm -rf src/files/media/cache
	-rm -rf src/files/static
	-rm -f src/db.sqlite
	# Create database
	./manage.py migrate

load_data:
	./manage.py loaddata ./files/fixtures/all_data.json

statics:
	./manage.py collectstatic --noinput

image:
	docker build -t 3megawat:latest .

server:
	./manage.py runserver 127.0.0.1:8080
	
##################
# Tests and checks
##################
test: check_venv ## Run tests
	$(PYTEST)

retest: check_venv ## Run failed tests only
	$(PYTEST) --lf

coverage: check_venv ## Generate coverage report
	$(PYTEST) --cov=apps

lint: check_venv ## Run flake8 and isort checks
	flake8 --max-line-length 120 --exclude */migrations/* $(shell git ls-files | grep \.py$$)
	isort -c -q --recursive --diff apps/
	isort -c -q --recursive --diff tests/

##################
# Misc
##################
shell:
	pipenv shell

