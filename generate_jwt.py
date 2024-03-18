from jwt import JWT, jwk_from_pem
import time
import argparse
import os
import requests


def create_jwt(private_key, app_id):
    """
    function to create JWT from GitHub app id and pvt key
    :param private_key:
    :param app_id:
    :return:
    """
    # Open PEM
    # with open(pem_path, 'rb') as pem_file:
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
    os.environ["GITHUB_JWT"] = encoded_jwt

    print(f"JWT set as environment variable: JWT={encoded_jwt}")
    return encoded_jwt

def main():
    """
    to test the code
    :return:
    """
    parser = argparse.ArgumentParser(description="Create JWT for GitHub App authentication")
    parser.add_argument("--github_app_private_key",required=True, type=str, help="Github App Private key")
    parser.add_argument("--github_app_id",required=True, type=str, help="Your GitHub App ID")
    args = parser.parse_args()

    private_key = args.github_app_private_key
    app_id = args.github_app_id

    # function call
    create_jwt(private_key, app_id)

if __name__ == "__main__":
    main()
