from abc import ABC, abstractmethod
from typing import Collection, Tuple

from domain.controllers.controller import AbstractController
from domain.environment import AbstractEnvironment


class AbstractDroneController(ABC):
    @abstractmethod
    def detect_wild_animals(self, radius: float) -> Collection[Tuple[float, float]]:
        return NotImplemented


class DroneController(AbstractController, AbstractDroneController):
    def __init__(self, env: AbstractEnvironment, x: float, y: float) -> None:
        self.env = env
        self.id = self.env.add_drone(x, y)
    
    def get_position(self) -> Tuple[float, float]:
        return self.env.get_drone_position(self.id)
    
    def move(self, x: float, y: float) -> None:
        self.env.move_drone(self.id, x, y)
    
    def detect_wild_animals(self, radius: float) -> Collection[Tuple[float, float]]:
        return self.env.detect_wild_animals(self.id, radius)

    def get_battery_status(self) -> float:
        return NotImplemented
