from jwt import JWT, jwk_from_pem
import time
import argparse
import os
import sys
import requests
from dotenv import load_dotenv

def create_jwt(private_key, app_id):
    """
    function to create JWT from GitHub app id and pvt key
    :param private_key:
    :param app_id:
    :return:
    """
    # Open PEM
    # with open(private_key, 'rb') as pem_file:
    #     signing_key = jwk_from_pem(pem_file.read())
    signing_key = jwk_from_pem(private_key.encode('utf-8'))

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

def get_app_installation_id(jwt:str, owner:str, repositories:str):
    """
    returns github app installation id on user and org accounts
    github app can be installed on scope of org providing permission to all repos or hand picked ones.
    in either case github app is installed on organization has a unique installation id. same for user accounts as well.
    :param jwt:
    :return:
    """
    results = []
    # Pagination query params
    per_page = 50
    page = 1
    # Api call url
    url = f'https://api.github.com/app/installations'
    # header
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {jwt}",
        "X-GitHub-Api-Version": "2022-11-28"
        }
    while True:
        params = {'per_page': per_page, 'page': page}
        response = requests.get(url= url, headers=headers, params=params)

        if response.status_code == 200:
            response_json = response.json()
        elif response.status_code == 301:
            print(f'Moved permanently. Cant get a response')
        else:
            print(f'Resource Not Found!')

        # Add the current page of results to the results list
        results.extend(response_json)

        # Check if there are more results
        if len(response_json) < per_page:
            break
        page += 1

    # Iterating through all installations
    for result in results:
        result_owner = result['account']['login']
        if owner == result_owner:
            installation_id = result['id']
            print(f'Installation id is {installation_id} - {owner} {result["target_type"]} ')
            print(f'Okay. Received proper response.Got installation id')
    return installation_id


def generate_token_by_post_call(installation_id:int, jwt:str, repositories: str):
    """
    create a app installation token by doing a rest api post call with permissions for application
    :return:
    """
    input_repositories = [item.strip() for item in repositories.split(',')]
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
        print(f'Github app installation token generated successfully for scope {repositories} - expires at {response_json["expires_at"]}')
    elif response.status_code == 401:
        print(f'Authentication is required')
    elif response.status_code == 403:
        print(f'Forbidden action')
    elif response.status_code == 404:
        print(f'Resource not found')
    else:
        print(f"Validation failed, {response_json['message']} or the endpoint has been spammed. Provided input repositories are {repositories}")
        print(f'Aborting GitHub App installation token generation')
        sys.exit(1) # Exiting as rest api cant process the req 422 error code
    os.environ['GH_APP_TOKEN'] = response_json['token']
    # Write the token to GITHUB_ENV to be available in subsequent steps
    with open(os.environ['GITHUB_ENV'], 'a') as fh:
        fh.write(f"GH_APP_TOKEN={response_json['token']}\n")

def main():
    """
    to test the code
    :return:
    """
    load_dotenv()
    parser = argparse.ArgumentParser(description="Create JWT for GitHub App authentication")
    parser.add_argument("--github_app_private_key",required=True, type=str, help="Github App Private key")
    parser.add_argument("--github_app_id",required=True, type=str, help="Your GitHub App ID")
    parser.add_argument("--owner", required=False, type=str, help="Target github owner")
    parser.add_argument("--repositories", required=False, type=str, help="Repos to which token will be generated, for multiple seperate by comma")
    args = parser.parse_args()

    private_key = args.github_app_private_key
    app_id = args.github_app_id

    # Handle --owner argument
    if args.owner is None:
        print("No owner specified. Considering current repository owner as Owner")
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
            print("No repositories specified. Considering current repository as repositories")
            repositories = os.getenv('GITHUB_REPOSITORY')  # Assign a default or dynamically determined value
    else:
        repositories = args.repositories
        print(f"Will generate tokens for {repositories}")

    # function call
    jwt = create_jwt(private_key=private_key, app_id=app_id)
    installation_id = get_app_installation_id(jwt=jwt, owner=owner, repositories=repositories)
    generate_token_by_post_call(installation_id=installation_id, jwt=jwt, repositories=repositories)



if __name__ == "__main__":
    main()
