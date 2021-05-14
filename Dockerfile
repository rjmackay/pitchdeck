# pull official base image
FROM python:3.9.2
ARG PIPENV_SYSTEM=1

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Combine apt-get update and apt-get install to avoid caching issues see:
# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#run
RUN apt-get update \
    && apt-get --no-install-recommends install -y \
    wait-for-it \
    # extra libs
    poppler-utils \
    # Cleanup after installation
    && apt-get clean -y \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -fr /var/lib/apt/lists/*

# install dependencies
RUN pip install --upgrade pip pipenv
ENV PIPENV_SYSTEM=$PIPENV_SYSTEM
COPY ./Pipfile .
COPY ./Pipfile.lock .
RUN pipenv sync --dev

# copy project
COPY . .
