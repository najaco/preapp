import pytest
import json
import subprocess
from github import Github
from typing import Dict, Any
import os
from flaky import flaky


def __setup(project_name: str, framework: str, env_variable: str, config_file: str):
    config_fp: TextIOWrapper = open(config_file, "r")
    config_file_source: str = config_fp.read()
    config_fp.close()

    config_file_source = config_file_source.replace(env_variable, framework)
    config_file_source = config_file_source.replace("__PROJECT_NAME__", project_name)

    new_config_file: str = f"tests/{framework}-test-config.json"
    config_fp: TextIOWrapper = open(new_config_file, "w")
    config_fp.write(config_file_source)
    config_fp.close()

    process = subprocess.Popen(
        f"python -m preapp --preset {new_config_file} --credentials {os.getcwd()}/tests/credentials.json",
        shell=True,
        stdout=subprocess.PIPE,
    )
    stdout, _ = process.communicate()


def _setup_web(project_name: str, web_framework: str) -> None:
    __setup(
        project_name, web_framework, "__WEB_FRAMEWORK__", f"{os.getcwd()}/tests/web-config.json",
    )


def _setup_python(project_name: str, python_framework: str) -> None:
    __setup(
        project_name,
        python_framework,
        "__PYTHON_FRAMEWORK__",
        f"{os.getcwd()}/tests/python-config.json",
    )


def _teardown(project_name: str, github_object: Github) -> None:
    # delete github repo
    github_object.get_user().get_repo(project_name).delete()

    # delete local folder
    process = subprocess.Popen(
        f"rm -rf {os.getcwd()}/{project_name}", shell=True, stdout=subprocess.PIPE,
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


@pytest.fixture()
def name(pytestconfig):
    return pytestconfig.getoption("name")


@pytest.mark.parametrize("name", ["name"])
@pytest.fixture(scope="function", params=["react", "angular", "vue"])
def web_framework(name, request):
    project_name: str = f"{name}-{request.param}"

    _setup_web(project_name, request.param)
    yield project_name
    _teardown(project_name, get_github_object())


@pytest.mark.parametrize("name", ["name"])
@pytest.fixture(scope="function", params=["python", "python-flask"])
def python_framework(name, request):
    project_name: str = f"{name}-{request.param}"

    _setup_python(project_name, request.param)
    yield project_name
    _teardown(project_name, get_github_object())


@flaky
def test_web(web_framework):
    # check for initial git files
    assert os.path.isdir(f"{os.getcwd()}/{web_framework}")
    assert os.path.isfile(f"{os.getcwd()}/{web_framework}/README.md")
    assert os.path.isfile(f"{os.getcwd()}/{web_framework}/LICENSE")
    assert os.path.isfile(f"{os.getcwd()}/{web_framework}/.gitignore")

    # check for website folder
    assert os.path.isdir(f"{os.getcwd()}/{web_framework}/website")

    # check for github actions file
    assert os.path.isfile(f"{os.getcwd()}/{web_framework}/.github/workflows/nodejs.yml")
    assert os.path.isfile(f"{os.getcwd()}/{web_framework}/.github/workflows/python.yml")

    # check for repository
    github_object = get_github_object()
    assert (
        github_object.get_user().get_repo(web_framework).get_commits(sha="master").totalCount == 6
    )

    assert github_object.get_user().get_repo(web_framework).get_issues().totalCount == 4


@flaky
def test_python(python_framework):
    # check for initial git files
    assert os.path.isdir(f"{os.getcwd()}/{python_framework}")
    assert os.path.isfile(f"{os.getcwd()}/{python_framework}/README.md")
    assert os.path.isfile(f"{os.getcwd()}/{python_framework}/LICENSE")
    assert os.path.isfile(f"{os.getcwd()}/{python_framework}/.gitignore")

    # check for github actions file
    assert os.path.isfile(f"{os.getcwd()}/{python_framework}/.github/workflows/python.yml")

    # check for backend
    assert os.path.isdir(f"{os.getcwd()}/{python_framework}/backend")
    assert os.path.isfile(f"{os.getcwd()}/{python_framework}/backend/noxfile.py")
    assert os.path.isfile(f"{os.getcwd()}/{python_framework}/backend/setup.py")
    assert os.path.isfile(f"{os.getcwd()}/{python_framework}/backend/.gitignore")

    setup_fp: TextIOWrapper = open(f"{os.getcwd()}/{python_framework}/backend/setup.py", "r")
    setup_source: str = setup_fp.read()

    assert setup_source.find(f'name="{python_framework}"') != -1
    assert setup_source.find('description="test"') != -1
    assert setup_source.find('version="0.0.1"') != -1
    assert setup_source.find('email="test"') != -1
    assert setup_source.find('license="MIT"') != -1
    assert setup_source.find('author="test"') != -1

    setup_fp.close()

    assert os.path.isdir(f"{os.getcwd()}/{python_framework}/backend/tests")
    assert os.path.isfile(f"{os.getcwd()}/{python_framework}/backend/tests/test_util.py")

    if python_framework == "python-flask":
        assert os.path.isfile(f"{os.getcwd()}/{python_framework}/backend/api.py")
        assert os.path.isfile(f"{os.getcwd()}/{python_framework}/backend/.flaskenv")
        assert os.path.isfile(f"{os.getcwd()}/{python_framework}/backend/requirements.txt")
    if python_framework == "python":
        assert os.path.isdir(f"{os.getcwd()}/{python_framework}/backend/{python_framework}")
        assert os.path.isfile(
            f"{os.getcwd()}/{python_framework}/backend/{python_framework}/__main__.py"
        )
        assert os.path.isfile(
            f"{os.getcwd()}/{python_framework}/backend/{python_framework}/__init__.py"
        )

    # check for repository
    github_object = get_github_object()
    assert (
        github_object.get_user().get_repo(python_framework).get_commits(sha="master").totalCount
        == 6
    )

    assert github_object.get_user().get_repo(python_framework).get_issues().totalCount == 4
