import pygame
import json

from pathlib import Path
from typing import Any


def get_package_root() -> Path:
    return Path(__file__).parent


def get_file_path(relative_path: str | Path) -> Path:
    return get_package_root() / relative_path


def load_json(relative_path: str | Path) -> dict[str, Any]:
    with get_file_path(f'{relative_path}.json').open('r') as f:
        return json.load(f)


def load_image(
    relative_path: str | Path,
    file_extension: str = 'png',
    scale: int = 1
) -> pygame.Surface:
    """
    Load an image from the given path and scale it by the given factor.
    """

    image = pygame.image.load(get_file_path(f'{relative_path}.{file_extension}'))
    return pygame.transform.scale(
        image,
        (image.get_width() * scale, image.get_height() * scale)
    )
