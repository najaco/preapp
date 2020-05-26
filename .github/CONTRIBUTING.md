# Contributing to preapp
Thanks for your interest in contributing to preapp. Pull requests for both bugs and new features are always welcome. 

Our goal is that contributing to preapp is as easy as possible. These guidelines are intended to help contributions as painless as possible.

## Reporting Bugs
Please use the github issue tracker to report any bugs. Before doing so, make sure to search the current issues for your bug before to prevent duplicate issues.

## Requesting New Features
Please use the github issue tracker to request any new features. Before doing so, make sure to search the current issues for your feature before to prevent duplicate issues. 

When requesting a new feature please provide the following
- what you are trying to accomplish
- why this feature is needed
- why current solutions (if they exist) are not viable
- code snippets of how this feature will be used once implemented

## Setting up your Development Environment
here is a list of what you'll need before you can start development

- your own fork of [preapp](https://github.com/stephend017/preapp)
- [python](https://www.python.org/downloads/) version 3.6 or higher
- [nox](https://nox.thea.codes/en/stable/)

## Contributing a Feature or Bug Fix
If you've chosen to contribute thats awesome. Here is our recommended workflow for efficiently and effectively contributing.

1. claim an open issue. this is so everyone knows what you're working on and its a feature or bug fix we want implemented.
2. rebase your fork with master. this is to keep our git history clean and prevent as many merge conflicts as possible
3. implement your feature or bug fix. when doing so please try and make as few changes as possible and stay in scope of your change.
4. test your changes. see [testing](#testing-preapp-locally) for more information
5. open a pull request. someone will review your code after it has passed the automated test cases via github actions.

## Testing preapp Locally
to test preapp locally you'll need to create a github personal access token which can be done [here](https://github.com/settings/tokens). This token must have the following permissions.

- `admin:gpg_key`
- `admin:org`
- `admin:org_hook`
- `admin:public_key`
- `admin:repo_hook`
- `delete:packages` 
- `delete_repo`
- `gist`
- `notifications`
- `read:packages`
- `repo`
- `user`
- `workflow`
- `write:discussion`
- `write:packages`

this token can then be placed into a local file `tests/credentials.json` which should look like this

```json
{
    "username": "<YOUR_GITHUB_USERNAME>",
    "oauth_token": "<YOUR_GITHUB_OAUTH_TOKEN>"
}
```

> Note: you should never commit or share this file with anyone

Now you should be able to run `nox` and it will test preapp locally for you 