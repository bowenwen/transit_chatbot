# Extend the official Rasa Core SDK image
ARG BASE_CONTAINER=rasa/rasa_core_sdk:0.12.1
FROM $BASE_CONTAINER

LABEL maintainer="Bo Wen"

## Add a custom system library (e.g. git)
#RUN apt-get update && \
#    apt-get install -y git

# Upgrade pip
RUN pip install --upgrade pip

# Add a custom python library
RUN pip install --no-cache-dir \
    setuptools NumPy python-dateutil pytz pandas