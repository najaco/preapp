import subprocess
from .. import Node, ListQuestion
from ..utils import commit_and_push, __assets_directory__
from preapp.utils.miscellaneous import bash


class FrameworkNode(Node):
    """Selects a Framework for the project """

    def __init__(self):
        super(FrameworkNode, self).__init__(
            "framework", [], parents=["nodejs", "platform", "github", "github_clone"],
        )

    def pre_process(self):
        if "web" in self.get_full_response()["platform"]["software"]:
            self.add_question(
                ListQuestion("web", "Select a web framework", ["react", "angular", "vue"])
            )

    def post_process(self, responses):
        if "web" in responses and responses["web"] == "react":
            project_name: str = self.get_full_response()["metadata"]["name"]
            if not self.get_full_response()["github"]["use"]:
                bash(f"npx create-react-app {project_name}")
            else:
                github_username: str = self.get_full_response()["github_credentials"]["username"]
                github_auth: str = ""
                if "password" in self.get_full_response()["github_credentials"]:
                    github_auth = self.get_full_response()["github_credentials"]["password"]
                if "oauth_token" in self.get_full_response()["github_credentials"]:
                    github_auth = self.get_full_response()["github_credentials"]["oauth_token"]

                bash(f"cd {project_name} && npx create-react-app website")

                commit_and_push(
                    "Initialized React",
                    project_name,
                    github_username,
                    github_auth,
                    directory=project_name,
                )

        if "web" in responses and responses["web"] == "angular":
            project_name: str = self.get_full_response()["metadata"]["name"]
            bash("npm install -g @angular/cli")

            if not self.get_full_response()["github"]["use"]:
                bash(f"ng new {project_name}")
            else:
                github_username: str = self.get_full_response()["github_credentials"]["username"]
                github_auth: str = self.get_full_response()["github_credentials"]["password"]

                bash(f"cd {project_name} && ng new website")

                commit_and_push(
                    "Initialized Angular",
                    project_name,
                    github_username,
                    github_auth,
                    directory=project_name,
                )

        if "web" in responses and responses["web"] == "vue":
            project_name: str = self.get_full_response()["metadata"]["name"]
            # assert that vue is installed
            bash("npm install -g vue")

            # assert the vue cli is installed
            bash("npm install -g @vue/cli")

            if not self.get_full_response()["github"]["use"]:
                bash(f"vue create -d {project_name}")
            else:
                github_username: str = self.get_full_response()["github_credentials"]["username"]
                github_auth: str = self.get_full_response()["github_credentials"]["password"]

                bash(f"cd {project_name} && vue create -d website")

                commit_and_push(
                    "Initialized Vue",
                    project_name,
                    github_username,
                    github_auth,
                    directory=project_name,
                )


Node.register(FrameworkNode())
