from __future__ import annotations
from typing import Tuple, TypeVar, TYPE_CHECKING, Optional

import copy

if TYPE_CHECKING:
    from game_map import GameMap

T = TypeVar("T", bound="Entity")

class Entity:
    """
    Generic object representing any entity within game
    """
    def __init__(
            self,
            game_map: Optional[GameMap] = None,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed",
            blocks_movement: bool = False,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        if game_map:
            # if game_map isnt provided, it will get set later
            self.game_map = game_map
            game_map.entities.add(self)

    def spawn(self: T, game_map: GameMap, x: int, y: int) -> T:
        """spawn a copy of this instance at the given location"""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.game_map = game_map
        game_map.entities.add(clone)
        return clone

    def place(self, x: int, y: int, game_map: Optional[GameMap] = None) -> None:
        """place this entity at a new location. Handles moving across game maps"""
        self.x = x
        self.y = y
        if game_map:
            if hasattr(self, "game_map"): # if game map is passed in and this entity already has one
                # remove this entity from the old board; it will get added to the newly supplied one
                self.game_map.entities.remove(self)
            self.game_map = game_map
            game_map.entities.add(self)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy