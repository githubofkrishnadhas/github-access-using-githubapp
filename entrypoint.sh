#! /bin/bash

# installng pipenv and creating pipenv venv
cd /app && pipenv install --skip-lock

# run python program to generate token
pipenv run python3 /app/generate_jwt.py --github_app_id "$1" --github_app_private_key "$2" --github_account_type "$3"


