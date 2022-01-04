from abc import ABC, abstractmethod
from typing import Collection, Tuple

from domain.objects.drone import AbstractDrone, Drone


class AbstractEnvironment(ABC):
    @abstractmethod
    def add_drone(x: float, y: float,) -> int:
        return NotImplemented
    
    @abstractmethod
    def get_drone_position(id: int) -> Tuple[float, float]:
        return NotImplemented

    @abstractmethod
    def move_drone(id: int, x: float, y: float) -> None:
        return NotImplemented
    
    @abstractmethod
    def detect_wild_animals(x: float, y: float, radius: float) -> Collection[Tuple[float, float]]:
        return NotImplemented


class Environment(AbstractEnvironment):
    def __init__(self) -> None:
        self.drones: AbstractDrone = []
        # self.animals: AbstractAnimal = []
    
    def add_drone(self, x: float, y: float,) -> int:
        id = len(self.drones)
        drone = Drone(x, y)
        self.drones.append(drone)
        return id
    
    def get_drone_position(self, id: int) -> Tuple[float, float]:
        return self.drones[id].get_position()

    def move_drone(self, id: int, x: float, y: float) -> None:
        self.drones[id].move(x, y)
    
    def detect_wild_animals(x: float, y: float, radius: float) -> Collection[Tuple[float, float]]:
        pass
