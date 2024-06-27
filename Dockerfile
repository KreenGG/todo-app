FROM python:3.12.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update

ADD pyproject.toml /app

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-root --no-interaction --no-ansi --no-dev

COPY . /app/

# CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]