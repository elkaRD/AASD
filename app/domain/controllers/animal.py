from typing import Tuple

from domain.controllers.controller import AbstractMovableController
from domain.environment import AbstractEnvironment


class AnimalController(AbstractMovableController):
    def __init__(self, env: AbstractEnvironment, x: float, y: float) -> None:
        self.env = env
        self.id = self.env.add_animal(x, y)
        self.chased_away = False

    def get_position(self) -> Tuple[float, float]:
        return self.env.get_animal_position(self.id)

    def move(self, x: float, y: float) -> None:
        if not self.chased_away:
            self.env.move_animal(self.id, x, y)

    def chase_away(self):
        if not self.chased_away:
            self.chased_away = True
            self.env.chase_away_animal(self.id)
