import os
import json
from typing import Dict, Any

__assets_directory__: str = f"{os.path.split(os.path.abspath(__file__))[0]}/../assets"


def file_to_json(file_path: str) -> Dict[str, Any]:
    fp = open(file_path, "r")
    raw_json: Dict[str, Any] = json.load(fp)
    fp.close()
    return raw_json
