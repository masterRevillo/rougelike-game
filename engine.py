from typing import Set, Any, Iterable

from tcod import Console
from tcod.context import Context
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    def __init__(self, event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            print(f"The {entity.name} is impatiently waiting for a real turn (gotta smash dat player)")

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is not None:
                action.perform(self, self.player)
                self.handle_enemy_turns()
                self.update_fov() # update fov before next action

    def update_fov(self) -> None:
        """recomputes the visible area based on the players point of view"""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8
        )
        # if a tile is visible, it should be added to explored
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        context.present(console)
        console.clear()