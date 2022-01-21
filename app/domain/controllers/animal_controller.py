from typing import Tuple

from domain.controllers.controller import AbstractController
from domain.environment import AbstractEnvironment


class AnimalController(AbstractController):
    def __init__(self, env: AbstractEnvironment, x: float, y: float) -> None:
        self.env = env
        self.id = self.env.add_animal(x, y)

    def get_position(self) -> Tuple[float, float]:
        return self.env.get_animal_position(self.id)

    def move(self, x: float, y: float) -> None:
        self.env.move_animal(self.id, x, y)
