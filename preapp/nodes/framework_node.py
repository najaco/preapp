import subprocess
from .. import Node, ListQuestion
from ..utils import commit_and_push, __assets_directory__
from preapp.utils.miscellaneous import bash
from preapp.utils.fileio import copy_file, file_to_text, text_to_file
import os
from preapp.hooks import call_hook


class FrameworkNode(Node):
    """Selects a Framework for the project """

    def __init__(self):
        super(FrameworkNode, self).__init__(
            "framework",
            [],
            parents=["nodejs", "python_interpreter", "platform", "github", "github_clone",],
        )

    def pre_process(self):
        if "web" in self.get_full_response()["platform"]["software"]:
            self.add_question(
                ListQuestion(
                    "web_frontend", "Select a frontend web framework", ["react", "angular", "vue"],
                ),
            )
            self.add_question(
                ListQuestion("web_backend", "Select a backend web framework", ["python"])
            )

    def post_process(self, responses):
        if "web_frontend" in responses:
            call_hook("framework", "web_frontend", responses["web_frontend"])

        if "web_backend" in responses:
            call_hook("framework", "web_backend", responses["web_backend"])

        # if "web_frontend" in responses and responses["web_frontend"] == "react":
        # project_name: str = self.get_full_response()["metadata"]["name"]
        # if not self.get_full_response()["github"]["use"]:
        #     bash(f"npx create-react-app {project_name}")
        # else:
        #     github_username: str = self.get_full_response()["github_credentials"]["username"]
        #     github_auth: str = ""
        #     if "password" in self.get_full_response()["github_credentials"]:
        #         github_auth = self.get_full_response()["github_credentials"]["password"]
        #     if "oauth_token" in self.get_full_response()["github_credentials"]:
        #         github_auth = self.get_full_response()["github_credentials"]["oauth_token"]

        #     bash(f"cd {project_name} && npx create-react-app website")

        #     commit_and_push(
        #         "Initialized React",
        #         project_name,
        #         github_username,
        #         github_auth,
        #         directory=project_name,
        #     )

        # if "web_frontend" in responses and responses["web_frontend"] == "angular":
        #     project_name: str = self.get_full_response()["metadata"]["name"]
        #     bash("sudo npm install -g @angular/cli")

        #     if not self.get_full_response()["github"]["use"]:
        #         bash(f"ng new {project_name}")
        #     else:
        #         github_username: str = self.get_full_response()["github_credentials"]["username"]
        #         github_auth: str = ""
        #         if "password" in self.get_full_response()["github_credentials"]:
        #             github_auth = self.get_full_response()["github_credentials"]["password"]
        #         if "oauth_token" in self.get_full_response()["github_credentials"]:
        #             github_auth = self.get_full_response()["github_credentials"]["oauth_token"]

        #         bash(f"cd {project_name} && ng new website")

        #         commit_and_push(
        #             "Initialized Angular",
        #             project_name,
        #             github_username,
        #             github_auth,
        #             directory=project_name,
        #         )

        # if "web_frontend" in responses and responses["web_frontend"] == "vue":
        #     project_name: str = self.get_full_response()["metadata"]["name"]
        #     # assert that vue is installed
        #     bash("sudo npm install -g vue")

        #     # assert the vue cli is installed
        #     bash("sudo npm install -g @vue/cli")

        #     if not self.get_full_response()["github"]["use"]:
        #         bash(f"vue create -d {project_name}")
        #     else:
        #         github_username: str = self.get_full_response()["github_credentials"]["username"]
        #         github_auth: str = ""
        #         if "password" in self.get_full_response()["github_credentials"]:
        #             github_auth = self.get_full_response()["github_credentials"]["password"]
        #         if "oauth_token" in self.get_full_response()["github_credentials"]:
        #             github_auth = self.get_full_response()["github_credentials"]["oauth_token"]

        #         bash(f"cd {project_name} && vue create -d website")

        #         commit_and_push(
        #             "Initialized Vue",
        #             project_name,
        #             github_username,
        #             github_auth,
        #             directory=project_name,
        #         )

        # if "web_backend" in responses and responses["web_backend"] == "python":
        #     # backend directory
        #     project_name: str = self.get_full_response()["metadata"]["name"]

        #     bash(f"cd {project_name} && mkdir backend")
        #     copy_file(
        #         f"{__assets_directory__}/python/module/requirements.txt",
        #         f"{os.getcwd()}/{project_name}/backend/requirements.txt",
        #     )
        #     copy_file(
        #         f"{__assets_directory__}/python/module/setup.py",
        #         f"{os.getcwd()}/{project_name}/backend/setup.py",
        #     )

        #     source: str = file_to_text(f"{os.getcwd()}/{project_name}/backend/setup.py")
        #     source = source.replace("__NAME__", self.get_full_response()["metadata"]["name"])
        #     source = source.replace("__VERSION__", self.get_full_response()["metadata"]["version"])
        #     source = source.replace(
        #         "__DESCRIPTION__", self.get_full_response()["metadata"]["description"]
        #     )
        #     source = source.replace("__AUTHOR__", self.get_full_response()["metadata"]["owner"])
        #     source = source.replace(
        #         "__EMAIL__", self.get_full_response()["metadata"]["owner_email"]
        #     )
        #     source = source.replace(
        #         "__LICENSE__",
        #         self.get_full_response()["metadata"]["license"][1:].partition("]")[0].upper(),
        #     )

        #     text_to_file(source, f"{os.getcwd()}/{project_name}/backend/setup.py")

        #     copy_file(
        #         f"{__assets_directory__}/python/module/noxfile.py",
        #         f"{os.getcwd()}/{project_name}/backend/noxfile.py",
        #     )

        #     # backend/<project_name> directory
        #     bash(f"cd {project_name}/backend && mkdir {project_name}")
        #     bash(f'cd {project_name}/backend/{project_name} && echo "" > __init__.py')
        #     copy_file(
        #         f"{__assets_directory__}/python/module/__main__.py",
        #         f"{os.getcwd()}/{project_name}/backend/{project_name}/__main__.py",
        #     )

        #     # backend/tests directory
        #     bash(f"cd {project_name}/backend && mkdir tests")
        #     copy_file(
        #         f"{__assets_directory__}/python/module/__test_util.py",
        #         f"{os.getcwd()}/{project_name}/backend/tests/test_util.py",
        #     )

        #     # setup the virtual environment
        #     bash(f"cd {project_name}/backend && python -m venv {project_name}-env")
        #     bash(f"cd {project_name}/backend && python -m pip install nox")

        #     github_username: str = self.get_full_response()["github_credentials"]["username"]
        #     github_auth: str = ""
        #     if "password" in self.get_full_response()["github_credentials"]:
        #         github_auth = self.get_full_response()["github_credentials"]["password"]
        #     if "oauth_token" in self.get_full_response()["github_credentials"]:
        #         github_auth = self.get_full_response()["github_credentials"]["oauth_token"]

        #     commit_and_push(
        #         "Initialized Python backend",
        #         project_name,
        #         github_username,
        #         github_auth,
        #         directory=project_name,
        #     )


Node.register(FrameworkNode())
