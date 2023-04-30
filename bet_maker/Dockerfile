FROM python:3.11 AS bet_maker_api

ARG POETRY_HOME=/etc/poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python - --version 1.2.2
ENV PATH="${PATH}:${POETRY_HOME}/bin"

COPY pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --without=dev --no-interaction

COPY . .

CMD ["/bin/bash", "-c", "alembic upgrade head; poetry run uvicorn --reload app.main:app --port 8001 --timeout-keep-alive 1000"]


FROM python:3.11 AS bet_proccessing

ARG POETRY_HOME=/etc/poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python - --version 1.2.2
ENV PATH="${PATH}:${POETRY_HOME}/bin"

COPY pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --without=dev --no-interaction

WORKDIR app
COPY . .

CMD ["/bin/bash", "-c", "python run -m app.services.bet_processing"]
