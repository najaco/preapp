from .. import Node
import json
from typing import Dict, Any


class RootNode(Node):
    """ The root node of the preapp application, All required entry point nodes are defined here """

    def __init__(self, preset: str, credentials: str):
        super(RootNode, self).__init__(
            "root", [], children=["metadata", "github", "platform", "output"], serializable=False,
        )
        self.preset = preset
        self.credentials = credentials

    def pre_process(self):
        if self.preset != None:
            config_fp: TextIOWrapper = open(self.preset, "r")
            config_json: Dict[str, Any] = json.load(config_fp)
            config_fp.close()

            for key, value in config_json.items():
                Node._full_response[key] = value

        if self.credentials != None:
            credentials_fp = open(self.credentials, "r")
            credentials_json: Dict[str, Any] = json.load(credentials_fp)
            credentials_fp.close()

            Node._full_response["github_credentials"] = credentials_json
