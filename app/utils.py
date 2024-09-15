import json

from pathlib import Path
from typing import Any


def get_package_root() -> Path:
    return Path(__file__).parent


def get_file_path(relative_path: str | Path) -> Path:
    return get_package_root() / relative_path


def load_json(relative_path: str | Path) -> dict[str, Any]:
    with get_file_path(relative_path).open('r') as f:
        return json.load(f)
