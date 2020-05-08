from preapp import Node, ConfirmQuestion
from typing import List
import subprocess
import os
from preapp.utils import commit_and_push


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
                # we can add the web github actions file
                project_name: str = self.get_full_response()["metadata"]["name"]
                github_username: str = self.get_full_response()["github_credentials"]["username"]
                github_password: str = self.get_full_response()["github_credentials"]["password"]
                process = subprocess.Popen(
                    f"cd {project_name} && mkdir .github && cd .github && mkdir workflows",
                    shell=True,
                    stdout=subprocess.PIPE,
                )
                stdout, _ = process.communicate()
                dirname, filename = os.path.split(os.path.abspath(__file__))
                actions_src_file: TextIOWrapper = open(f"{dirname}/../../assets/nodejs.yml", "r")
                actions_dest_file: TextIOWrapper = open(
                    f"{os.getcwd()}/{project_name}/.github/workflows/nodejs.yml", "w+"
                )
                actions_dest_file.write("".join(actions_src_file.readlines()))
                actions_src_file.close()
                actions_dest_file.close()

                commit_and_push(
                    "Setup Github Actions",
                    project_name,
                    github_username,
                    github_password,
                    directory=project_name,
                )


Node.register(GithubActionsNode())
