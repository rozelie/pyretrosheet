FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
COPY README.md ./
COPY ./pyretrosheet ./pyretrosheet

RUN python -m pip install .

CMD ["python", "-m", "pyretrosheet"]