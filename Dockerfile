# Container image that runs your code
FROM python:3.13-slim-bullseye

WORKDIR /app
# Copies your code file from your action repository to the filesystem path `/` of the container
COPY . /app/

# Install uv
RUN chmod +x entrypoint.sh &&  apt-get update -y && pip install uv
# Add uv to PATH
ENV PATH="/root/.local/bin:$PATH"

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/app/entrypoint.sh"]
