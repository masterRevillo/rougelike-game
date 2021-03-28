from typing import Tuple

import numpy as np

graphic_dt = np.dtype(
    [
        ("ch", np.int32), # unicode codepoint
        ("fg", "3B"), # 3 unsigned bytes for rgb color
        ("bg", "3B")
    ]
)

tile_dt = np.dtype(
    [
        ("walkable", np.bool_), # true if tile can be walked on
        ("transparent", np.bool_), # true if tile doesnt block FOV
        ("dark", graphic_dt), # Graphics for when this tile is not in FOV
        ("light", graphic_dt), # Graphics for when this tile is in FOV
    ]
)

def new_tile(
        *, # enforce the use of keywords, so parameter order doesnt matter
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types"""
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (5, 5, 5)), dtype=graphic_dt)
SHROUD2 = np.array((ord(" "), (255, 255, 255), (5, 100, 5)), dtype=graphic_dt)

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (35, 35, 60)),
    light=(ord(" "), (255, 255, 255), (200, 200, 200))
)

wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (25, 25, 45)),
    light=(ord(" "), (255, 255, 255), (160, 110, 50))
)

down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(">"), (0, 0, 100), (50, 50, 150)),
    light=(ord(">"), (255, 255, 255), (200, 180, 50))
)

water = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (5, 5, 150)),
    light=(ord(" "), (255, 255, 255), (5, 5, 230))
)

sand = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (100, 105, 20)),
    light=(ord(" "), (255, 255, 255), (230, 205, 48))
)

grass = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (5, 100, 15)),
    light=(ord(" "), (255, 255, 255), (5, 230, 15))
)

brush = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (20, 80, 7)),
    light=(ord(" "), (255, 255, 255), (30, 130, 7))
)