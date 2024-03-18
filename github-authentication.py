
import requests
import os
# from generate_jwt import create_jwt

## use this function in order to pass the jwt manually and do the github api call

def make_github_api_request():
    url = "https://api.github.com/app"
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
def make_github_api_request():
    url = "https://api.github.com/app"
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
    # jwt = create_jwt()
    make_github_api_request()
