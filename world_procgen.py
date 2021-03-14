import perlin_noise

from engine import Engine
from game_map import WorldGameMap


def generate_world(world_width: int, world_height: int, engine: Engine):
    player = engine.player
    dungeon = WorldGameMap(engine, world_width, world_height, entities=[player])

    player.place(int(world_width/2), int(world_height/2), dungeon)

    return dungeon
    # map = [][]
    # for x in range(world_width):
    #     for y in range(world_height):