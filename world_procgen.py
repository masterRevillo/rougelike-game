from perlin_noise import PerlinNoise

import tile_types
from engine import Engine
from game_map import WorldGameMap


def generate_world(world_width: int, world_height: int, engine: Engine):
    player = engine.player
    dungeon = WorldGameMap(engine, world_width, world_height, entities=[player])

    noise = PerlinNoise(octaves=10, seed=1)

    for x in range(world_width):
        for y in range(world_height):
            noise_val = noise([x/world_width, y/world_height]) + .5
            if noise_val > 0.65:
                dungeon.tiles[x, y] = tile_types.brush
            elif noise_val > 0.35:
                dungeon.tiles[x, y] = tile_types.grass
            elif noise_val > 0.30:
                dungeon.tiles[x, y] = tile_types.sand



    player.place(int(world_width/2), int(world_height/2), dungeon)

    return dungeon