FROM python:3.12-slim

# Minimal set of common packages to download
ARG package_args="--allow-downgrades --allow-remove-essential --allow-change-held-packages --no-install-recommends"
RUN echo "debconf debconf/frontend select noninteractive" | debconf-set-selections \
  && export DEBIAN_FRONTEND=noninteractive \
  && apt-get -q $package_args update \
  && apt-get -y $package_args upgrade \
  && apt-get -y $package_args install \
        ca-certificates \
        # CLI tool for transferring data from or to a server
        curl \
        # C libraries required for building psycopg[binary]
        libpq-dev \
        # Meta-package for compiling Python packages with C extensions
        build-essential \
        # C headers/libraries for some Python packages (e.g. stdlib.h)
        libc-dev \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 - --version 1.8.4
ENV PATH=$PATH:/etc/poetry/venv/bin

WORKDIR /TripNestArmenia-backend

COPY pyproject.toml poetry.lock entrypoint.sh ./

RUN poetry config virtualenvs.create false && poetry check --lock && poetry env use system && poetry install --only main

ADD . /TripNestArmenia-backend/
ENV PYTHONPATH=/TripNestArmenia-backend

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["sh", "./entrypoint.sh"]

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "3", "--reload"]
