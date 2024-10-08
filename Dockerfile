FROM python:3

WORKDIR /app

COPY ./pyproject.toml .

COPY ./poetry.lock .

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .