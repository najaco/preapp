import pytest
import json
import subprocess
from github import Github
from typing import Dict, Any
import os


def setup(config_file: str) -> None:
    process = subprocess.Popen(
        f"python -m preapp --preset {config_file} --credentials {os.getcwd()}/tests/credentials.json",
        shell=True,
        stdout=subprocess.PIPE,
    )
    stdout, _ = process.communicate()


def teardown(github_object: Github) -> None:
    # delete github repo
    github_object.get_user().get_repo("test").delete()

    # delete local folder
    process = subprocess.Popen(
        f"rm -rf {os.getcwd()}/test", shell=True, stdout=subprocess.PIPE,
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
    setup(f"{os.getcwd()}/tests/{request.param}-config.json")
    yield web_framework
    teardown(get_github_object())


def test_web(web_framework):
    # checks for initial git files
    assert os.path.isdir(f"{os.getcwd()}/test")
    assert os.path.isfile(f"{os.getcwd()}/test/README.md")
    assert os.path.isfile(f"{os.getcwd()}/test/LICENSE")
    assert os.path.isfile(f"{os.getcwd()}/test/.gitignore")

    # checks for website folder
    assert os.path.isdir(f"{os.getcwd()}/test/website")

    # checks for github actions file
    assert os.path.isfile(f"{os.getcwd()}/test/.github/workflows/nodejs.yml")

    # checks for repository
    github_object = get_github_object()
    assert (
        github_object.get_user().get_repo("test").get_commits(sha="master").totalCount
        == 5
    )
