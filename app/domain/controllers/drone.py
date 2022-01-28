from typing import Collection, Tuple

from domain.controllers.controller import AbstractMovableController
from domain.environment import AbstractEnvironment


class DroneController(AbstractMovableController):
    def __init__(self, env: AbstractEnvironment, drone_id: int) -> None:
        self.env = env
        self.drone_id = drone_id

    def get_position(self) -> Tuple[float, float]:
        return self.env.get_drone_position(self.drone_id)

    def move(self, x: float, y: float) -> None:
        self.env.move_drone(self.drone_id, x, y)

    def detect_wild_animals(
        self, radius: float
    ) -> Collection[Tuple[float, float]]:
        return self.env.detect_wild_animals(self.drone_id, radius)

    def get_battery_status(self) -> float:
        return NotImplemented
