from perlin_noise import PerlinNoise

import tile_types
from engine import Engine
from game_map import WorldGameMap


def generate_world(world_width: int, world_height: int, engine: Engine):
    player = engine.player
    dungeon = WorldGameMap(engine, world_width, world_height, entities=[player])
    generate_world_at(
        start_x=0,
        start_y=0,
        len_x=world_width,
        len_y=world_height,
        dungeon=dungeon
    )
    player.place(int(world_width / 2), int(world_height / 2), dungeon)
    return dungeon

def generate_world_at(start_x: int, start_y: int, len_x: int, len_y: int, dungeon: WorldGameMap):
    noise = PerlinNoise(octaves=10, seed=1)

    for x in range(start_x, len_x):
        for y in range(start_y, len_y):
            noise_val = noise([x/len_x, y/len_y]) + .5
            if noise_val > 0.65:
                dungeon.tiles[x, y] = tile_types.brush
            elif noise_val > 0.35:
                dungeon.tiles[x, y] = tile_types.grass
            elif noise_val > 0.30:
                dungeon.tiles[x, y] = tile_types.sand