FROM python:3.10-slim-buster
# Prevents Python from writing pyc files to disc 
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr 
ENV PYTHONUNBUFFERED=1
# Install packages needed to run the application:
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -ex \
    && DEPS=" \
    mime-support \
    netcat \
    telnet \
    postgresql-client \
    libcairo2 \
    python3-cffi \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libmagic1 \
    shared-mime-info \
    build-essential \
    python3-dev \
    libpq-dev \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get dist-upgrade -y && apt-get install -y --no-install-recommends $DEPS \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV APP_DIR=/opt/recon
WORKDIR $APP_DIR

COPY . $APP_DIR

RUN pip install  --no-cache-dir -r requirements/base.txt

RUN sed -i 's/\r$//g' $APP_DIR/entrypoint.sh
RUN chmod +x $APP_DIR/entrypoint.sh
