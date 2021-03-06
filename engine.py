from __future__ import annotations
import lzma
import pickle
from typing import TYPE_CHECKING, Any, Iterable

from tcod import Console
from tcod.map import compute_fov

import exceptions
from camera import Camera
from message_log import MessageLog
import render_functions
from sound_manager import SoundManager

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld

class Engine:
    game_map: GameMap
    game_world: GameWorld
    sound_manager: SoundManager

    def __init__(self, player: Actor, camera: Camera):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player
        self.camera = camera

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass # ignore impossible exceptions from enemy actions

    def update_fov(self) -> None:
        """recomputes the visible area based on the players point of view"""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8
        )
        # if a tile is visible, it should be added to explored
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        self.camera.update(self.player)
        self.game_map.render(console, self.camera)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20
        )

        render_functions.render_dungeon_level(
            console=console,
            dungeon_level=self.game_world.current_floor,
            location=(0, 47)
        )

        render_functions.render_names_at_mouse_location(
            console=console,
            x=21,
            y=44,
            engine=self
        )

        render_functions.render_player_coords(
            console=console,
            player=self.player,
            location=(0, 48)
        )


    def save_as(self, filename: str) -> None:
        """save this engine instance as a compressed file"""
        self.sound_manager.pauseBgm()
        self.sound_manager.clearSfxCache()
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)