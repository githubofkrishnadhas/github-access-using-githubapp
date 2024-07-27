# github-access-using-githubapp

Once your GitHub App is installed on an account, you can make it authenticate as an app installation for API requests.
This allows the app to access resources owned by that installation, as long as the app was granted the necessary repository access and permissions.
API requests made by an app installation are attributed to the app.

:pushpin:  This action will help in creating GitHub app installation token for both **user accounts** and **Github organizations**

> [!IMPORTANT]  
> An installation access token expires after 1 hour. Please find suitable alternative approaches if you have long-running processes..

# Parameters of action
| Parameter name | Description                                                                                                    | Required          |
|----------------|----------------------------------------------------------------------------------------------------------------|-------------------|
| github_app_private_key | Github App Private key                                                                                         | :heavy_check_mark: |
| github_app_id | Your GitHub App ID                                                                                             | :heavy_check_mark: |
| owner | Github account owner name. if not specified takes owner of current repository where action is ran              | ❌ |
| repositories | List of github repositores to generte token for. if not specified takes current repository where action is ran. | ❌ |

* Store your `Github App Id` and `Github App Private key` as github secret and pass the secret names as inputs for action.

* ❌ 👉 Means optional values

> [!NOTE]  
> If the owner is set but repositories are empty, access will include all repositories for that owner.
> If both the owner and repositories are empty, access will be limited to the current repository.

# What's New

Please refer to the [release](https://github.com/githubofkrishnadhas/github-access-using-githubapp/releases) page for the latest release notes.

# Usage 
```commandline
- uses: githubofkrishnadhas/github-access-using-githubapp@v2
  id: token-generation
  with:
    # Your GitHub App ID - interger value
    github_app_id: 1234567

    # GitHub App Private key 
    github_app_private_key : ''

    # GitHub account Owner name - Optional
    owner: ''
    
    # GitHub repositories names seperated by comma if more than 1 - optional
    repositories: ''
```

# output

* The token generated will be available as a ${{ steps.token-generation.outputs.token }}  which can be used in later stages as required

# Example usages

## Create a token for the current repository

```commandline
uses: githubofkrishnadhas/github-access-using-githubapp@v2
  id: token-generation
  with:
    github_app_id: ${{ secrets.APP_ID }}
    github_app_private_key : ${{ secrets.PRIVATE_KEY }}
```
* To create a Token in the scope of current repository where action is run, you do not need to specify `owner` or `repositores` 
* Assuming both GitHub App ID and Private key are present as github secrets with names `APP_ID` and `PRIVATE_KEY`
* You can substitute your secrets names with above
* The token generated will be available as a ${{ steps.token-generation.outputs.token }}  which can be used in later stages as required


## Create a token for the current user or organization level

```commandline
uses: githubofkrishnadhas/github-access-using-githubapp@v2
  id: token-generation
  with:
    github_app_id: ${{ secrets.APP_ID }}
    github_app_private_key : ${{ secrets.PRIVATE_KEY }}
    owner: 'github'
```
* To create a Token in the scope of current user or organization where your Github app has access, you need only to specify `owner`
* Assuming both GitHub App ID and Private key are present as github secrets with names `APP_ID` and `PRIVATE_KEY`
* You can substitute your secrets names with above
* The token generated will be available as a ${{ steps.token-generation.outputs.token }}  which can be used in later stages as required


## Create a token for a differnt user or organization scoped to specific repos

```commandline
uses: githubofkrishnadhas/github-access-using-githubapp@v2
  id: token-generation
  with:
    github_app_id: ${{ secrets.APP_ID }}
    github_app_private_key : ${{ secrets.PRIVATE_KEY }}
    owner: 'github'
    repositories: 'test1,test2,test3'
```
* To create a Token in the scope of provided repositories and owner where your Github app has access you need only to specify `owner` and `repositories`
* The above will generate token which are scoped to repositores named `test1, test2, test3` on `github` org
* Assuming both GitHub App ID and Private key are present as github secrets with names `APP_ID` and `PRIVATE_KEY`
* You can substitute your secrets names with above
* The token generated will be available as a ${{ steps.token-generation.outputs.token }}  which can be used in later stages as required


## Using the token generated with other actions

```commandline
name: Clone Repository

on:
  workflow_dispatch:

jobs:
  clone:
    runs-on: ubuntu-latest

    steps:

    - name: Token generator
      uses: githubofkrishnadhas/github-access-using-githubapp@v2
      id: token-generation
      with:
        github_app_id: ${{ secrets.APP_ID }}
        github_app_private_key : ${{ secrets.PRIVATE_KEY }}

    - name: Checkout Repository
      uses: actions/checkout@v4
      with:
        repository: 'devwithkrishna/azure-terraform-modules'
        token: ${{ steps.token-generation.outputs.token }}
        fetch-depth: 1
```
* The above workflow generates a github app installation access token using the action - `githubofkrishnadhas/github-access-using-githubapp@v2`
* The token generated will be available as a ${{ steps.token-generation.outputs.token }}  which can be used in later stages as shown above
* The workflow is to clone a repository named `azure-terraform-modules` inside `devwithkrishna` organization


# References

* [generating-an-installation-access-token](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app#generating-an-installation-access-token)
* [get-a-user-installation-for-the-authenticated-app](https://docs.github.com/en/rest/apps/apps?apiVersion=2022-11-28#get-a-user-installation-for-the-authenticated-app)
* [get-a-repository-installation-for-the-authenticated-app](https://docs.github.com/en/rest/apps/apps?apiVersion=2022-11-28#get-a-repository-installation-for-the-authenticated-app)

All the above API's uses [JWT](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app#authenticating-as-a-github-app) as access token.
