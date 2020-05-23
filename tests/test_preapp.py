import pytest
import json
import subprocess
from github import Github
from typing import Dict, Any
import os


PROJECT_NAME: str = "test"


def _setup_web(web_framework: str, config_file: str) -> None:
    # update the config file to have the correct information
    config_fp: TextIOWrapper = open(config_file, "r")
    config_file_source: str = config_fp.read()
    config_fp.close()

    config_file_source = config_file_source.replace("__WEB_FRAMEWORK__", web_framework)
    config_file_source = config_file_source.replace("__PROJECT_NAME__", PROJECT_NAME)

    new_config_file: str = f"tests/{web_framework}-test-config.json"
    config_fp: TextIOWrapper = open(new_config_file, "w")
    config_fp.write(config_file_source)
    config_fp.close()

    process = subprocess.Popen(
        f"python -m preapp --preset {new_config_file} --credentials {os.getcwd()}/tests/credentials.json",
        shell=True,
        stdout=subprocess.PIPE,
    )
    stdout, _ = process.communicate()


def _teardown_web(github_object: Github) -> None:
    # delete github repo
    github_object.get_user().get_repo(PROJECT_NAME).delete()

    # delete local folder
    process = subprocess.Popen(
        f"rm -rf {os.getcwd()}/{PROJECT_NAME}", shell=True, stdout=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    # delete generated test files
    process = subprocess.Popen(
        f"rm -rf {os.getcwd()}/tests/*test-config.json", shell=True, stdout=subprocess.PIPE,
    )
    stdout, _ = process.communicate()


def get_github_object() -> Github:
    credentials_fp: TextIOWrapper = open("tests/credentials.json", "r")
    credentials: Dict[str, Any] = json.load(credentials_fp)
    credentials_fp.close()

    github_username: str = credentials["username"]
    github_auth: str = credentials["oauth_token"]

    return Github(github_auth)


@pytest.fixture(scope="function", params=["react", "angular", "vue"])
def web_framework(request):
    _setup_web(request.param, f"{os.getcwd()}/tests/web-config.json")
    yield web_framework
    _teardown_web(get_github_object())


def test_web(web_framework):
    # check for initial git files
    assert os.path.isdir(f"{os.getcwd()}/{PROJECT_NAME}")
    assert os.path.isfile(f"{os.getcwd()}/{PROJECT_NAME}/README.md")
    assert os.path.isfile(f"{os.getcwd()}/{PROJECT_NAME}/LICENSE")
    assert os.path.isfile(f"{os.getcwd()}/{PROJECT_NAME}/.gitignore")

    # check for website folder
    assert os.path.isdir(f"{os.getcwd()}/{PROJECT_NAME}/website")

    # check for github actions file
    assert os.path.isfile(f"{os.getcwd()}/{PROJECT_NAME}/.github/workflows/nodejs.yml")

    # check for backend
    assert os.path.isdir(f"{os.getcwd()}/{PROJECT_NAME}/backend")
    assert os.path.isfile(f"{os.getcwd()}/{PROJECT_NAME}/backend/requirements.txt")
    assert os.path.isfile(f"{os.getcwd()}/{PROJECT_NAME}/backend/noxfile.py")
    assert os.path.isfile(f"{os.getcwd()}/{PROJECT_NAME}/backend/setup.py")

    setup_fp: TextIOWrapper = open(f"{os.getcwd()}/{PROJECT_NAME}/backend/setup.py", "r")
    setup_source: str = setup_fp.read()

    assert setup_source.find(f'name="{PROJECT_NAME}"') != -1
    assert setup_source.find('description="test"') != -1
    assert setup_source.find('version="0.0.1"') != -1
    assert setup_source.find('email="test"') != -1
    assert setup_source.find('license="MIT"') != -1
    assert setup_source.find('author="test"') != -1

    setup_fp.close()

    assert os.path.isdir(f"{os.getcwd()}/{PROJECT_NAME}/backend/tests")
    assert os.path.isfile(f"{os.getcwd()}/{PROJECT_NAME}/backend/tests/test_util.py")

    assert os.path.isdir(f"{os.getcwd()}/{PROJECT_NAME}/backend/{PROJECT_NAME}")
    assert os.path.isfile(f"{os.getcwd()}/{PROJECT_NAME}/backend/{PROJECT_NAME}/__init__.py")
    assert os.path.isfile(f"{os.getcwd()}/{PROJECT_NAME}/backend/{PROJECT_NAME}/__main__.py")

    # check for repository
    github_object = get_github_object()
    assert github_object.get_user().get_repo(PROJECT_NAME).get_commits(sha="master").totalCount == 5
