import os
import json
from typing import Dict, Any

__assets_directory__: str = f"{os.path.split(os.path.abspath(__file__))[0]}/../assets"


def file_to_json(file_path: str) -> Dict[str, Any]:
    fp = open(file_path, "r")
    raw_json: Dict[str, Any] = json.load(fp)
    fp.close()
    return raw_json


def raw_to_json_file(file_path: str, raw_json: Dict[str, Any]) -> None:
    fp: TextIOWrapper = open(file_path, "w+")
    json.dump(raw_json, fp, indent=4)
    fp.close()


def str_to_json_file(file_path: str, raw_json: str) -> None:
    raw_to_json_file(file_path, json.loads(raw_json))


def copy_file(src_file: str, dest_file: str) -> None:
    src_fp: TextIOWrapper = open(src_file, "r")
    dest_fp: TextIOWrapper = open(dest_file, "w")
    dest_fp.write("".join(src_fp.readlines()))
    src_fp.close()
    dest_fp.close()
