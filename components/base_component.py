from __future__ import annotations

from typing import TYPE_CHECKING

from game_map import GameMap

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class BaseComponent:
    parent: Entity # owning entity instance

    @property
    def game_map(self) -> GameMap:
        return self.parent.game_map

    @property
    def engine(self) -> Engine:
        return self.game_map.engine