from preapp.hooks import action_hook
from preapp.node import Node
from preapp.utils.miscellaneous import bash
from preapp.utils.githubio import commit_and_push
from preapp.utils import __assets_directory__
import os
from preapp.utils.fileio import append_file_to_file, copy_file, delete_file


@action_hook("framework", "web_frontend", "vue")
def setup():
    project_name: str = Node.get_full_response()["metadata"]["name"]
    # assert that vue is installed
    bash("sudo npm install -g vue")

    # assert the vue cli is installed
    bash("sudo npm install -g @vue/cli")

    if not Node.get_full_response()["github"]["use"]:
        bash(f"vue create -d {project_name}")
    else:
        github_username: str = Node.get_full_response()["github_credentials"]["username"]
        github_auth: str = ""
        if "password" in Node.get_full_response()["github_credentials"]:
            github_auth = Node.get_full_response()["github_credentials"]["password"]
        if "oauth_token" in Node.get_full_response()["github_credentials"]:
            github_auth = Node.get_full_response()["github_credentials"]["oauth_token"]

        bash(f"cd {project_name} && vue create -d website")

        # gitignore_file_path: str = f"{os.getcwd()}/{project_name}/website/.gitignore"
        # append_file_to_file(gitignore_file_path, f"{os.getcwd()}/{project_name}/.gitignore")
        # delete_file(gitignore_file_path)

        commit_and_push(
            "Initialized Vue", project_name, github_username, github_auth, directory=project_name,
        )


@action_hook("github_actions", "web_frontend", "vue")
def setup_actions():
    project_name: str = Node.get_full_response()["metadata"]["name"]
    github_username: str = Node.get_full_response()["github_credentials"]["username"]
    github_auth: str = ""

    if "password" in Node.get_full_response()["github_credentials"]:
        github_auth = Node.get_full_response()["github_credentials"]["password"]
    if "oauth_token" in Node.get_full_response()["github_credentials"]:
        github_auth = Node.get_full_response()["github_credentials"]["oauth_token"]

    copy_file(
        f"{__assets_directory__}/vue/nodejs.yml",
        f"{os.getcwd()}/{project_name}/.github/workflows/nodejs.yml",
    )

    commit_and_push(
        "Setup Github Actions", project_name, github_username, github_auth, directory=project_name,
    )
