import requests
import os
import argparse
from dotenv import load_dotenv


def create_github_label(repo:str):
    url = f"https://api.github.com/repos/{repo}/labels"
    headers = {
        "Authorization": f"token {os.getenv('GH_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "name": 'label_name',
        "color": "f29513",  # Default color for the label, you can change this
        "description": f"Label 123"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print(f"Label  created successfully in repository '{repo}'!")
    else:
        print(f"Failed to create label in repository '{repo}'.")
        print("Response:", response.json())


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description='Create a GitHub label in a repository.')
    # parser.add_argument('--repo', type=str, help='GitHub repository name in the format "owner/repo".')
    # parser.add_argument('--label_name', type=str, help='Name of the label to create.')

    args = parser.parse_args()
    repo = os.getenv('GITHUB_REPOSITORY_OWNER')/os.getenv('GITHUB_REPOSITORY')
    # label_name = args.label_name
    # Get the GitHub token from environment variable or argument
    # github_token = os.getenv('GITHUB_TOKEN')

    create_github_label(repo=repo)