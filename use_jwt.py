import os
import requests


def make_github_api_request():
    url = "  https://api.github.com/repositories"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.getenv('GITHUB_JWT')}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()

    if response.status_code == 200:
        print("API request successful:")
        print(response_json)
    else:
        print(f"API request failed with status code {response.status_code}:")
        print(response_json)

if __name__ == "__main__":
    make_github_api_request()