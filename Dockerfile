FROM python:3.9-buster
ENV APPLICATION_SERVICE=/app

# set work directory
RUN mkdir -p $APPLICATION_SERVICE

# where the code lives
WORKDIR $APPLICATION_SERVICE

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY pyproject.toml ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry lock && \
    poetry install --no-dev

# copy project
COPY . $APPLICATION_SERVICE

CMD alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000  --reload