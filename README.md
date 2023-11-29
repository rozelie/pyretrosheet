# pyretrosheet

Load and analyze retrosheet.org MLB data.

# Usage
**TODO**

# Contributing
## `Makefile` targets
```
help: Show this help.
setup: Install the package and dev dependencies into a virtualenv.
run:  Run the package.
test:  Run pytest on the tests dir.
format: Run black and isort on package and tests dirs.
lint:  Run ruff and mypy on package files.
docker_build: Build a Docker image for the package.
docker_run:  Run the Docker image for the package.
publish_to_testpypi:  Publish the package to test.pypi.org.
publish_to_pypi:  Publish the package to pypi.org.
```

## TODO
- Parse out 'info' fields into `Game` properties

# Credits
- Project skeleton generated via `cookiecutter https://github.com/rozelie/Python-Project-Cookiecutter`