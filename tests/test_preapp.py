import pytest
import json
import subprocess
from github import Github
from typing import Dict, Any
import os


def run_config(config_file: str) -> None:
    process = subprocess.Popen(
        f"python -m preapp --preset {config_file} --credentials {os.getcwd()}/tests/credentials.json",
        shell=True,
        stdout=subprocess.PIPE,
    )
    stdout, _ = process.communicate()


def cleanup(github_object: Github) -> None:
    # delete github repo
    github_object.get_user().get_repo("test").delete()

    # delete local folder
    process = subprocess.Popen(f"rm -rf {os.getcwd()}/test", shell=True, stdout=subprocess.PIPE,)
    stdout, _ = process.communicate()


def get_github_object() -> Github:
    credentials_fp: TextIOWrapper = open("tests/credentials.json", "r")
    credentials: Dict[str, Any] = json.load(credentials_fp)
    credentials_fp.close()

    github_username: str = credentials["username"]
    github_auth: str = credentials["oauth_token"]

    return Github(github_auth)


def __test_web_framework(framework: str):
    run_config(f"{os.getcwd()}/tests/{framework}-config.json")
    assert os.path.isdir(f"{os.getcwd()}/test")
    github_object = get_github_object()
    assert github_object.get_user().get_repo("test")
    cleanup(github_object)


def test_preapp_react():
    __test_web_framework("react")


def test_preapp_angular():
    __test_web_framework("angular")


def test_preapp_vue():
    __test_web_framework("vue")
