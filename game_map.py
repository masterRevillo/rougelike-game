from __future__ import annotations

from typing import Iterable, TYPE_CHECKING, Optional, Iterator, Tuple
import numpy as np
from tcod import Console

from camera import Camera
from entity import Actor, Item
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Chunk:
    def __init__(
            self, engine: Engine, chunk_x: int, chunk_y: int, entities: Iterable[Entity] = ()
    ):
        self.size = 20
        self.visible = []
        self.explored = []
        self.tiles = []
        self.chunk_x, self.chunk_y = chunk_x, chunk_y

        self.engine = engine
        self.entities = set(entities)

    def coords_in_chunk(self, entity: Entity) -> Tuple[int, int]:
        return entity.x - self.size*self.chunk_x, entity.y - self.size*self.chunk_y

    def distance_from_entity(self, entity: Entity) -> Tuple[int, int]:
        return abs(self.size*self.chunk_x - entity.x), abs(self.size*self.chunk_y - entity.y)

class GameMap:
    def __init__(
            self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
    ):
        self.visible = []
        self.explored = []
        self.tiles = []

        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)

    @property
    def game_map(self) -> GameMap:
        return self

    @property
    def actors(self) -> Iterable[Actor]:
        """iterate over this maps living actors"""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    @property
    def items(self) -> Iterator[Item]:
        yield from (entity for entity in self.entities if isinstance(entity, Item))

    def get_blocking_entity_at_location(
            self, location_x: int, location_y: int
    ) -> Optional[Entity]:
        for entity in self.entities:
            if (
                    entity.blocks_movement
                    and entity.x == location_x
                    and entity.y == location_y
            ):
                return entity

        return None

    def get_actor_at_location(self, x: int, y: int):
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map"""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console, camera: Camera) -> None:
        """
        renders the map
        If a tile is in the visible array, draw it with its "light" colors
        If it isn't, but it's in the explored array, draw it with its "dark" colors
        Default to SHROUD, meaning its not visible AND not explored
        """

        console.tiles_rgb[0 : camera.width, 0 : camera.height] = np.full(
            (camera.width, camera.height), fill_value=tile_types.SHROUD2, order="F"
        )

        to_print = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )

        for y in range(self.height):
            for x in range(self.width):
                x_in_camera, y_in_camera = camera.apply(x, y)
                if camera.in_bounds(x_in_camera, y_in_camera) and self.in_bounds(x, y):
                    console.tiles_rgb[x_in_camera, y_in_camera] = to_print[x][y]

        # np.roll(to_print, camera.y, axis=0)
        # np.roll(to_print, camera.x, axis=1)
        #
        # console.tiles_rgb[0 : self.width, 0 : self.height] = to_print

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )

        for entity in entities_sorted_for_rendering:
            # only print entities that are in the FOV
            if self.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x + camera.x, y=entity.y + camera.y, string=entity.char, fg= entity.color
                )

class DungeonGameMap(GameMap):
    def __init__(
            self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
    ):
        super().__init__(engine, width, height, entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full(
            (width, height), fill_value=False, order="F"
        ) # tiles player can currently see
        self.explored = np.full(
            (width, height), fill_value=False, order="F"
        ) # tiles player has seen before

        self.downstairs_location = (0, 0)

class WorldGameMap(DungeonGameMap):
    def __init__(
            self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
    ):
        super().__init__(engine, width, height, entities)
        self.tiles = np.full((width, height), fill_value=tile_types.water, order="F")

        self.visible = np.full(
            (width, height), fill_value=False, order="F"
        )  # tiles player can currently see
        self.explored = np.full(
            (width, height), fill_value=True, order="F"
        )  # tiles player has seen before

        self.downstairs_location = (0, 0)
        self.chunks = {}

    def get_chunk(self, coordinates: Tuple[int, int]) -> Chunk:
        chunk = self.chunks.get(coordinates)
        if chunk:
            return chunk
        else:
            pass
#             genereate it


class GameWorld:
    """
    Holds the settings for the GameMap, and generates new maps when moving down stairs
    """

    def __init__(
            self,
            *,
            engine: Engine,
            map_width: int,
            map_height: int,
            max_rooms: int,
            room_max_size: int,
            room_min_size: int,
            current_floor: int = 0
    ):
        self.engine = engine
        self.map_width = map_width
        self.map_height = map_height
        self.max_rooms = max_rooms
        self.room_max_size = room_max_size
        self.room_min_size = room_min_size
        self.current_floor = current_floor

    def generate_floor(self) -> None:
        from dungeon_procgen import generate_dungeon

        self.current_floor += 1

        self.engine.game_map = generate_dungeon(
            max_rooms=self.max_rooms,
            room_max_size=self.room_max_size,
            room_min_size=self.room_min_size,
            map_width=self.map_width,
            map_height=self.map_height,
            engine=self.engine
        )

    def generate_overworld(self) -> None:
        from world_procgen import generate_world

        self.engine.game_map = generate_world(
            world_width=self.map_width,
            world_height=self.map_height,
            engine=self.engine,
        )
