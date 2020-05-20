from preapp import Node, ConfirmQuestion
from typing import List, Dict, Any
import subprocess
import os
from preapp.utils import commit_and_push
import json
from preapp.utils.fileio import copy_file, file_to_json, raw_to_json_file
from preapp.utils.miscellaneous import bash


class GithubActionsNode(Node):
    """Checks if the user wants to use github actions"""

    def __init__(self):
        super(GithubActionsNode, self).__init__(
            "github_actions",
            [ConfirmQuestion("use", "Do you want to add github actions?", True)],
            parents=["github", "github_repository", "github_credentials", "framework",],
        )

    def post_process(self, responses):
        if responses["use"] == True:
            frameworks: List[str] = self.get_full_response()["framework"]
            if "web" in frameworks:
                project_name: str = self.get_full_response()["metadata"]["name"]
                github_username: str = self.get_full_response()["github_credentials"]["username"]
                github_auth: str = ""

                if "password" in self.get_full_response()["github_credentials"]:
                    github_auth = self.get_full_response()["github_credentials"]["password"]
                if "oauth_token" in self.get_full_response()["github_credentials"]:
                    github_auth = self.get_full_response()["github_credentials"]["oauth_token"]

                bash(f"cd {project_name} && mkdir .github && cd .github && mkdir workflows")

                dirname, _ = os.path.split(os.path.abspath(__file__))

                if frameworks["web"] == "react":
                    commit_actions_file(
                        f"{dirname}/../../assets/react/nodejs.yml",
                        project_name,
                        github_username,
                        github_auth,
                    )

                if frameworks["web"] == "angular":
                    # add additional library for github actions testing
                    bash(f"cd {project_name}/website && npm install puppeteer --save-dev")

                    # update karma.conf file
                    dirname, filename = os.path.split(os.path.abspath(__file__))
                    copy_file(
                        f"{dirname}/../../assets/angular/karma.conf.js",
                        f"{os.getcwd()}/{project_name}/website/karma.conf.js",
                    )

                    # update package.json
                    raw_json: Dict[str, Any] = file_to_json(
                        f"{os.getcwd()}/{project_name}/website/package.json"
                    )

                    raw_json["scripts"]["clean"] = "rimraf ./dist"
                    raw_json["scripts"]["build:prod"] = "ng build --prod"
                    raw_json["scripts"][
                        "test"
                    ] = "ng test --watch=false --browsers=ChromeHeadlessCustom"
                    raw_json["scripts"][
                        "build:ci"
                    ] = "npm run clean && npm run test && npm run build:prod"

                    raw_to_json_file(f"{os.getcwd()}/{project_name}/website/package.json", raw_json)

                    commit_actions_file(
                        f"{dirname}/../../assets/angular/nodejs.yml",
                        project_name,
                        github_username,
                        github_auth,
                    )

                if frameworks["web"] == "vue":
                    commit_actions_file(
                        f"{dirname}/../../assets/vue/nodejs.yml",
                        project_name,
                        github_username,
                        github_auth,
                    )


Node.register(GithubActionsNode())


def commit_actions_file(
    actions_filepath: str, project_name: str, github_username: str, github_password: str
) -> None:
    copy_file(actions_filepath, f"{os.getcwd()}/{project_name}/.github/workflows/nodejs.yml")

    commit_and_push(
        "Setup Github Actions",
        project_name,
        github_username,
        github_password,
        directory=project_name,
    )
