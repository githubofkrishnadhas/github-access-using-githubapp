# Container image that runs your code
FROM python:3.11-slim-bullseye

WORKDIR /app
# Copies your code file from your action repository to the filesystem path `/` of the container
COPY . /app/

# Install pipenv
RUN chmod +x entrypoint.sh &&  apt-get update -y && pip install pipenv

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/app/entrypoint.sh"]
