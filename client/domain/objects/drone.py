from abc import ABC, abstractmethod
from typing import Tuple


class AbstractDrone(ABC):
    @abstractmethod
    def get_position(self) -> Tuple[float, float]:
        return NotImplemented

    @abstractmethod
    def move(self, x: float, y: float) -> None:
        return NotImplemented


class Drone(AbstractDrone):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def get_position(self):
        return (self.x, self.y)
    
    def move(self, x: float, y: float) -> None:
        self.x += x
        self.y += y
