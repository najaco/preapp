import pytest
import json
import subprocess
from github import Github
from typing import Dict, Any
import os


# @pytest.mark.skip()
def test_preapp_react():
    # run command
    process = subprocess.Popen(
        f"python -m preapp --preset {os.getcwd()}/tests/preapp-config.json --credentials {os.getcwd()}/tests/credentials.json",
        shell=True,
        stdout=subprocess.PIPE,
    )
    stdout, _ = process.communicate()
    # assert local folder exists
    assert os.path.isdir(f"{os.getcwd()}/test")

    # assert github repository exists
    credentials_fp: TextIOWrapper = open("tests/credentials.json", "r")
    credentials: Dict[str, Any] = json.load(credentials_fp)
    credentials_fp.close()

    github_username: str = credentials["username"]
    github_auth: str = credentials["oauth_token"]

    github_object = Github(github_auth)

    assert github_object.get_user().get_repo("test")

    # delete github repo
    github_object.get_user().get_repo("test").delete()

    # delete local folder
    process = subprocess.Popen(f"rm -rf {os.getcwd()}/test", shell=True, stdout=subprocess.PIPE,)
    stdout, _ = process.communicate()
