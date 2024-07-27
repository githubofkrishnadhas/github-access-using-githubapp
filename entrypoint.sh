#! /bin/bash

# installng pipenv and creating pipenv venv
cd /app && pipenv install --skip-lock

# Capture arguments
GITHUB_APP_ID="$1"
GITHUB_APP_PRIVATE_KEY="$2"
OWNER="$3"
REPOSITORIES="$4"

# Build the command based on available parameters
CMD="pipenv run python3 /app/generate_jwt.py --github_app_id \"$GITHUB_APP_ID\" --github_app_private_key \"$GITHUB_APP_PRIVATE_KEY\""

if [ -n "$OWNER" ]; then
    CMD="$CMD --owner \"$OWNER\""
fi

if [ -n "$REPOSITORIES" ]; then
    CMD="$CMD --repositories \"$REPOSITORIES\""
fi

# Print and execute the command
echo "Executing command: $CMD"
eval "$CMD"

## run python program to generate token
#pipenv run python3 /app/generate_jwt.py --github_app_id "$1" --github_app_private_key "$2" --owner "$3" --repositories "$4"


