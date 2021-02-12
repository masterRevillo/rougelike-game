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
    ]
)

def new_tile(
        *, # enforce the use of keywords, so parameter order doesnt matter
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types"""
    return np.array((walkable, transparent, dark), dtype=tile_dt)

floor = new_tile(
    walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255), (50, 50, 150))
)

wall = new_tile(
    walkable=False, transparent=False, dark=(ord(" "), (255, 255, 255), (0, 0, 100))
)