ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
SRC_DIR := ${ROOT_DIR}/pyretrosheet
TESTS_DIR := ${ROOT_DIR}/tests
VENV_BIN := ${ROOT_DIR}/venv/bin
PYTHON := ${VENV_BIN}/python

help: ## Show this help.
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

setup: ## Install the package and dev dependencies into a virtualenv.
	python3 -m venv venv
	${PYTHON} -m pip install .
	${PYTHON} -m pip install .[dev]

test:  ## Run pytest on the tests dir.
	PYTHONPATH="${ROOT_DIR}" PYTHONUNBUFFERED=1 ${PYTHON} -m pytest ${TESTS_DIR} --numprocesses auto

test_all_data:  ## Run pytest on all Retrosheet data.
	PYRETROSHEET_TEST_ALL_DATA=true PYTHONPATH="${ROOT_DIR}" PYTHONUNBUFFERED=1 ${PYTHON} -m pytest ${TESTS_DIR} --exitfirst --capture=no --numprocesses auto

format: ## Run black and isort on package and tests dirs.
	${VENV_BIN}/black ${SRC_DIR} ${TESTS_DIR}
	${VENV_BIN}/isort ${SRC_DIR} ${TESTS_DIR}

lint:  ## Run ruff and mypy on package files.
	${VENV_BIN}/ruff ${SRC_DIR}
	${VENV_BIN}/mypy ${SRC_DIR}

coverage:  ## Run test coverage and update coverage badge
	${VENV_BIN}/coverage run -m pytest tests
	${VENV_BIN}/coverage report -m
	pip install coverage-badge
	coverage-badge -f -o assets/coverage.svg

bump_version:  ## Increment patch version references in the project
	${PYTHON} -m pip install --upgrade bumpversion
	bumpversion patch

publish_to_testpypi:  ## Publish the package to test.pypi.org.
	# register account at https://test.pypi.org/account/register/
	${PYTHON} -m pip install --upgrade build twine
	${PYTHON} -m build

publish_to_pypi:  ## Publish the package to pypi.org.
	# register account at https://pypi.org/account/register/
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) bump_version
	${PYTHON} -m pip install --upgrade build twine
	${PYTHON} -m build
	${PYTHON} -m twine upload --repository pypi dist/*
	git push --tags
	rm -rf dist
