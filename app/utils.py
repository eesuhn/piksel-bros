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


def load_sprites_sheet(
    relative_path: str | Path,
    width: int,
    height: int,
    scale: int = 1,
    direction: bool = False
) -> dict:

    sheet = {}
    path = get_file_path(relative_path)

    for file in sorted(path.glob('*.png')):
        file_name = file.stem
        sheet_surface = pygame.image.load(str(file)).convert_alpha()

        raw_sprites = [
            pygame.transform.scale(
                sheet_surface.subsurface(pygame.Rect(
                    width * i,
                    0,
                    width,
                    height
                )),
                (width * scale, height * scale)
            )
            for i in range(sheet_surface.get_width() // width)
        ]

        if direction:
            sheet[f'{file_name}_left'] = [
                pygame.transform.flip(sprite, True, False) for sprite in raw_sprites
            ]
            sheet[f'{file_name}_right'] = raw_sprites
        else:
            sheet[file_name] = raw_sprites

    return sheet
