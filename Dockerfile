FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --no-dev --locked

COPY ./docs ./docs
RUN uv run --only-group docs sphinx-build -M html docs/source /opt/kora-docs

COPY . /app
COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
