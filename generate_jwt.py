from jwt import JWT, jwk_from_pem
import time
import argparse
import os
import sys
import requests
from dotenv import load_dotenv

def create_jwt(private_key, app_id):
    """
    Function to create JWT from GitHub app id and private key.
    :param private_key: Path to the PEM file containing the private key.
    :param app_id: GitHub App ID.
    :return: Encoded JWT.
    """
    # Open PEM
    # with open(private_key, 'rb') as pem_file:
    #     signing_key = jwk_from_pem(pem_file.read())
    signing_key = jwk_from_pem(private_key.encode('utf-8'))


    payload = {
        'iat': int(time.time()),  # Issued at time
        'exp': int(time.time()) + 600,  # JWT expiration time (10 minutes maximum)
        'iss': app_id  # GitHub App's identifier
    }

    # Create JWT
    jwt_instance = JWT()
    encoded_jwt = jwt_instance.encode(payload, signing_key, alg='RS256')

    return encoded_jwt

def get_app_installation_id(jwt: str, owner: str):
    """
    Get GitHub app installation ID on user and org accounts.
    :param jwt: JWT token.
    :param owner: GitHub owner (user or organization).
    :return: Installation ID.
    """
    results = []
    per_page = 50
    page = 1
    url = 'https://api.github.com/app/installations'
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {jwt}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    while True:
        params = {'per_page': per_page, 'page': page}
        response = requests.get(url=url, headers=headers, params=params)

        if response.status_code == 200:
            response_json = response.json()
        elif response.status_code == 301:
            print('Moved permanently. Cannot get a response.')
            sys.exit(1)
        else:
            print('Resource not found!')
            sys.exit(1)

        results.extend(response_json)

        if len(response_json) < per_page:
            break
        page += 1

    for result in results:
        result_owner = result['account']['login']
        if owner == result_owner:
            installation_id = result['id']
            print(f'Installation ID is {installation_id} - {owner} {result["target_type"]}')
            return installation_id

    print(f'Installation ID for owner {owner} not found.')
    sys.exit(1)

def generate_token_by_post_call(installation_id: int, jwt: str, repositories: str):
    """
    Create an app installation token by making a POST request with permissions for the application.
    :param installation_id: Installation ID of the GitHub App.
    :param jwt: JWT token.
    :param repositories: Comma-separated list of repositories.
    """
    input_repositories = [item.strip() for item in repositories.split(',')]
    print(f'Input repos - {input_repositories}')
    url = f'https://api.github.com/app/installations/{installation_id}/access_tokens'
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {jwt}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    data = {
        "repositories": input_repositories
    }
    response = requests.post(url=url, headers=headers, json=data)
    response_json = response.json()

    if response.status_code == 201:
        print(f'GitHub app installation token generated successfully for scope {repositories} - expires at {response_json["expires_at"]}')
    elif response.status_code == 401:
        print('Authentication is required')
    elif response.status_code == 403:
        print('Forbidden action')
    elif response.status_code == 404:
        print('Resource not found')
    else:
        print(f"Validation failed, {response_json.get('message', 'Unknown error')} or the endpoint has been spammed.")
        print(f'Aborting GitHub App installation token generation')
        sys.exit(1)

    os.environ['GH_APP_TOKEN'] = response_json['token']
    with open(os.environ['GITHUB_ENV'], 'a') as fh:
        fh.write(f"GH_APP_TOKEN={response_json['token']}\n")

def main():
    """
    Main function to run the script.
    """
    load_dotenv()
    parser = argparse.ArgumentParser(description="Create JWT for GitHub App authentication")
    parser.add_argument("--github_app_private_key", required=True, type=str, help="GitHub App Private key")
    parser.add_argument("--github_app_id", required=True, type=str, help="Your GitHub App ID")
    parser.add_argument("--owner", required=False, type=str, help="Target GitHub owner")
    parser.add_argument("--repositories", required=False, type=str, help="Repos to which token will be generated, for multiple separate by comma")
    args = parser.parse_args()

    private_key = args.github_app_private_key
    app_id = args.github_app_id

    # Handle --owner argument
    if args.owner is None:
        print("No owner specified. Considering current repository owner as Owner.")
        owner = os.getenv('GITHUB_REPOSITORY_OWNER')  # Assign a default or dynamically determined value
        print(f"Taking owner as {owner}")
    else:
        owner = args.owner
        print(f"Owner: {owner}")

    # Handle --repositories argument
    if args.repositories is None:
        if args.owner is not None:
            # If owner is provided but repositories are not
            print(f"No repositories specified for the provided owner: {owner}.")
            repositories = 'all'  # You can decide on a default behavior here, e.g., an empty list or a specific action
            print(f"Selecting all repos under owner {owner}")
        else:
            # If neither owner nor repositories are specified
            print("No repositories & owner specified. Considering current repository as repositories.")
            os_repositories = os.getenv('GITHUB_REPOSITORY')  # Get the current repository
            if os_repositories:
                parts = os_repositories.split('/')
                repositories = parts[1]
                print(f"Taking repositories as {repositories}")
            else:
                print("Current repository information is not available.")
                sys.exit(1)
    else:
        repositories = args.repositories
        print(f"Will generate tokens for {repositories}")

    # Function calls
    jwt = create_jwt(private_key=private_key, app_id=app_id)
    installation_id = get_app_installation_id(jwt=jwt, owner=owner)
    generate_token_by_post_call(installation_id=installation_id, jwt=jwt, repositories=repositories)

if __name__ == "__main__":
    main()
