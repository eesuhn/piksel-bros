import json

from pathlib import Path
from typing import Union, Dict, Any


def get_package_root() -> Path:
    return Path(__file__).parent


def get_file_path(relative_path: Union[str, Path]) -> Path:
    return get_package_root() / relative_path


def load_json(relative_path: Union[str, Path]) -> Dict[str, Any]:
    with get_file_path(relative_path).open('r') as f:
        return json.load(f)
