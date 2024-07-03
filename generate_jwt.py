from jwt import JWT, jwk_from_pem
import time
import argparse
import os
import requests
from dotenv import load_dotenv
from label import create_github_label

def create_jwt(private_key, app_id):
    """
    function to create JWT from GitHub app id and pvt key
    :param private_key:
    :param app_id:
    :return:
    """
    # Open PEM
    with open(private_key, 'rb') as pem_file:
        signing_key = jwk_from_pem(pem_file.read())
    # signing_key = jwk_from_pem(private_key.encode('utf-8'))

    payload = {
        # Issued at time
        'iat': int(time.time()),
        # JWT expiration time (10 minutes maximum)
        'exp': int(time.time()) + 600,
        # GitHub App's identifier
        'iss': app_id
    }

    # Create JWT
    jwt_instance = JWT()
    encoded_jwt = jwt_instance.encode(payload, signing_key, alg='RS256')

    # Set JWT as environment variable
    # os.environ["GITHUB_JWT"] = encoded_jwt

    # print(f"JWT token created successfully")
    return encoded_jwt

def get_app_installation_id(jwt:str, github_account_type:str):
    """
    returns github app installation id on user and org accounts
    :param jwt:
    :return:
    """
    GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')
    GITHUB_REPOSITORY_OWNER =  os.getenv('GITHUB_REPOSITORY_OWNER')
    org_url = f'https://api.github.com/repos/{GITHUB_REPOSITORY}/installation'
    user_url = f'https://api.github.com/users/{GITHUB_REPOSITORY_OWNER}/installation'
    if github_account_type == 'user':
        url = user_url
    else:
        url = org_url
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {jwt}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    response = requests.get(url= url, headers=headers)

    if response.status_code == 200:
        print(f'Okay. Received proper response.Got installation id')
        response_json = response.json()
    elif response.status_code == 301:
        print(f'Moved permanently. Cant get a response')
    else:
        print(f'Resource Not Found!')

    # Installation id of github app
    installation_id = response_json['id']
    return installation_id

def generate_token_by_post_call(installation_id:int, jwt:str):
    """
    create a app installation token by doing a rest api post call with permissions for application
    :return:
    """
    url = f'https://api.github.com/app/installations/{installation_id}/access_tokens'
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {jwt}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    response = requests.post(url=url, headers=headers)
    response_json = response.json()
    if response.status_code == 201:
        print(f'Github app installation token generate succcessfully, expires at {response_json["expires_at"]}')
    os.environ['GH_APP_TOKEN'] = response_json['token']

def main():
    """
    to test the code
    :return:
    """
    load_dotenv()
    parser = argparse.ArgumentParser(description="Create JWT for GitHub App authentication")
    parser.add_argument("--github_app_private_key",required=True, type=str, help="Github App Private key")
    parser.add_argument("--github_account_type",required=True, choices=['user','organization'], help="Github account whether user account ot github org")
    parser.add_argument("--github_app_id",required=True, type=str, help="Your GitHub App ID")
    args = parser.parse_args()

    private_key = args.github_app_private_key
    app_id = args.github_app_id
    github_account_type = args.github_account_type

    # function call
    jwt = create_jwt(private_key=private_key, app_id=app_id)
    installation_id = get_app_installation_id(jwt=jwt, github_account_type=github_account_type)
    generate_token_by_post_call(installation_id=installation_id, jwt=jwt)



if __name__ == "__main__":
    main()
