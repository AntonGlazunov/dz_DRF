FROM python:3

WORKDIR /app

COPY ./pyproject.toml .

COPY ./poetry.lock .

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN ~/.local/share/pypoetry/venv/bin/poetry install

RUN ~/.local/share/pypoetry/venv/bin/poetry add django

COPY . .