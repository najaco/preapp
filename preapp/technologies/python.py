from preapp.hooks import action_hook
from preapp.node import Node
from preapp.utils.miscellaneous import bash
from preapp.utils.githubio import commit_and_push, get_gitignore_file
from preapp.utils import __assets_directory__
import os
from preapp.utils.fileio import (
    append_text_to_file,
    copy_file,
    file_to_text,
    text_to_file,
)


@action_hook("framework", "web_backend", "python")
def setup_module():
    _setup()

    project_name: str = Node.get_full_response()["metadata"]["name"]

    # backend/<project_name> directory
    bash(f"cd {project_name}/backend && mkdir {project_name}")
    bash(f'cd {project_name}/backend/{project_name} && echo "" > __init__.py')
    copy_file(
        f"{__assets_directory__}/python/module/__main__.py",
        f"{os.getcwd()}/{project_name}/backend/{project_name}/__main__.py",
    )

    _setup_devops()

    _commit("Initialized Python backend")


@action_hook("framework", "web_backend", "python-flask")
def setup_flask():
    _setup()

    project_name: str = Node.get_full_response()["metadata"]["name"]

    copy_file(
        f"{__assets_directory__}/python/flask/api.py",
        f"{os.getcwd()}/{project_name}/backend/api.py",
    )

    copy_file(
        f"{__assets_directory__}/python/flask/.flaskenv",
        f"{os.getcwd()}/{project_name}/backend/.flaskenv",
    )

    copy_file(
        f"{__assets_directory__}/python/flask/requirements.txt",
        f"{os.getcwd()}/{project_name}/backend/requirements.txt",
    )

    _setup_devops()

    _commit("Initialized Python Flask backend")


@action_hook("github_actions", "web_backend", "python")
def setup_python_actions():
    _setup_actions()


@action_hook("github_actions", "web_backend", "python-flask")
def setup_python_flask_actions():
    _setup_actions()


def _setup_actions():
    project_name: str = Node.get_full_response()["metadata"]["name"]

    copy_file(
        f"{__assets_directory__}/python/devops/python.yml",
        f"{os.getcwd()}/{project_name}/.github/workflows/python.yml",
    )

    _commit("Setup Github Actions")


def _setup():
    project_name: str = Node.get_full_response()["metadata"]["name"]

    bash(f"cd {project_name} && mkdir backend")
    # setup the virtual environment
    bash(f"cd {project_name}/backend && python -m venv {project_name}-env")

    gitignore_source: str = get_gitignore_file("python")
    append_text_to_file(gitignore_source, f"{os.getcwd()}/{project_name}/backend/.gitignore")


def _setup_devops():
    project_name: str = Node.get_full_response()["metadata"]["name"]
    version: str = Node.get_full_response()["metadata"]["version"]
    description: str = Node.get_full_response()["metadata"]["description"]
    author: str = Node.get_full_response()["metadata"]["owner"]
    email: str = Node.get_full_response()["metadata"]["owner_email"]
    project_license: str = Node.get_full_response()["metadata"]["license"]
    project_license = project_license[1:].partition("]")[0].upper()

    copy_file(
        f"{__assets_directory__}/python/devops/setup.py",
        f"{os.getcwd()}/{project_name}/backend/setup.py",
    )

    source: str = file_to_text(f"{os.getcwd()}/{project_name}/backend/setup.py")
    source = source.replace("__NAME__", project_name)
    source = source.replace("__VERSION__", version)
    source = source.replace("__DESCRIPTION__", description)
    source = source.replace("__AUTHOR__", author)
    source = source.replace("__EMAIL__", email)
    source = source.replace("__LICENSE__", project_license)

    text_to_file(source, f"{os.getcwd()}/{project_name}/backend/setup.py")

    copy_file(
        f"{__assets_directory__}/python/devops/noxfile.py",
        f"{os.getcwd()}/{project_name}/backend/noxfile.py",
    )

    # backend/tests directory
    bash(f"cd {project_name}/backend && mkdir tests")
    copy_file(
        f"{__assets_directory__}/python/devops/__test_util.py",
        f"{os.getcwd()}/{project_name}/backend/tests/test_util.py",
    )

    bash(f"cd {project_name}/backend && python -m pip install nox")


def _commit(message: str):
    project_name: str = Node.get_full_response()["metadata"]["name"]
    github_username: str = Node.get_full_response()["github_credentials"]["username"]
    github_auth: str = ""
    if "password" in Node.get_full_response()["github_credentials"]:
        github_auth = Node.get_full_response()["github_credentials"]["password"]
    if "oauth_token" in Node.get_full_response()["github_credentials"]:
        github_auth = Node.get_full_response()["github_credentials"]["oauth_token"]

    commit_and_push(
        message, project_name, github_username, github_auth, directory=project_name,
    )
