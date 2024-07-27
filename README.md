# github-access-using-githubapp
github-access-using-githubapp

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
- uses: githubofkrishnadhas/github-access-using-githubapp@v1
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

The token generated will be available as a Environment variable `GH_APP_TOKEN` which can be used while running api calls

# References

[generating-an-installation-access-token](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app#generating-an-installation-access-token)
[get-a-user-installation-for-the-authenticated-app](https://docs.github.com/en/rest/apps/apps?apiVersion=2022-11-28#get-a-user-installation-for-the-authenticated-app)
[get-a-repository-installation-for-the-authenticated-app](https://docs.github.com/en/rest/apps/apps?apiVersion=2022-11-28#get-a-repository-installation-for-the-authenticated-app)

All the above API's uses [JWT](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app#authenticating-as-a-github-app) as access token.
