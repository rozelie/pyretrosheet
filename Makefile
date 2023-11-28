ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
SRC_DIR := ${ROOT_DIR}/pyretrosheet
TESTS_DIR := ${ROOT_DIR}/tests
VENV_BIN := ${ROOT_DIR}/venv/bin
PYTHON := ${VENV_BIN}/python
ENTRYPOINT := ${SRC_DIR}/__main__.py
DOCKER_IMAGE := pyretrosheet:local

help: ## Show this help.
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

setup: ## Install the package and dev dependencies into a virtualenv.
	python3 -m venv venv
	${PYTHON} -m pip install .
	${PYTHON} -m pip install .[dev]

run:  ## Run the package.
	PYTHONPATH="${ROOT_DIR}" PYTHONUNBUFFERED=1 ${PYTHON} ${ENTRYPOINT}

test:  ## Run pytest on the tests dir.
	PYTHONPATH="${ROOT_DIR}" PYTHONUNBUFFERED=1 ${PYTHON} -m pytest ${TESTS_DIR}

format: ## Run black and isort on package and tests dirs.
	${VENV_BIN}/black ${SRC_DIR} ${TESTS_DIR}
	${VENV_BIN}/isort ${SRC_DIR} ${TESTS_DIR}

lint:  ## Run ruff and mypy on package files.
	${VENV_BIN}/ruff ${SRC_DIR}
	${VENV_BIN}/mypy ${SRC_DIR}

docker_build: ## Build a Docker image for the package.
	docker build -t ${DOCKER_IMAGE} .

docker_run:  ## Run the Docker image for the package.
	docker run -it --rm ${DOCKER_IMAGE}

publish_to_testpypi:  ## Publish the package to test.pypi.org.
	# register account at https://test.pypi.org/account/register/
	${PYTHON} -m pip install --upgrade build twine
	${PYTHON} -m build
	${PYTHON} -m twine upload --repository testpypi dist/*
	rm -rf dist

publish_to_pypi:  ## Publish the package to pypi.org.
	# register account at https://pypi.org/account/register/
	${PYTHON} -m pip install --upgrade build twine
	${PYTHON} -m build
	${PYTHON} -m twine upload --repository pypi dist/*
	rm -rf dist
