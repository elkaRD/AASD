from abc import ABC, abstractmethod
from math import sqrt
from typing import Collection, Tuple

from domain.objects.animal import Animal
from domain.objects.drone import Drone


class AbstractEnvironment(ABC):
    @abstractmethod
    def add_drone(x: float, y: float,) -> int:
        return NotImplemented
    
    @abstractmethod
    def add_animal(x: float, y: float,) -> int:
        return NotImplemented
    
    @abstractmethod
    def get_drone_position(id: int) -> Tuple[float, float]:
        return NotImplemented

    @abstractmethod
    def move_drone(id: int, x: float, y: float) -> None:
        return NotImplemented
    
    @abstractmethod
    def get_animal_position(self, id: int) -> Tuple[float, float]:
        return NotImplemented
    
    @abstractmethod
    def move_animal(self, id: int, x: float, y: float) -> None:
        return NotImplemented
    
    @abstractmethod
    def detect_wild_animals(self, x: float, y: float, radius: float) -> Collection[Tuple[float, float]]:
        return NotImplemented


class Environment(AbstractEnvironment):
    def __init__(self) -> None:
        self.drones: Drone = []
        self.animals: Animal = []
    
    def add_drone(self, x: float, y: float) -> int:
        id = len(self.drones)
        drone = Drone(x, y)
        self.drones.append(drone)
        return id
    
    def add_animal(self, x: float, y: float) -> int:
        id = len(self.animals)
        animal = Animal(x, y)
        self.animals.append(animal)
        return id
    
    def get_drone_position(self, id: int) -> Tuple[float, float]:
        return self.drones[id].get_position()

    def move_drone(self, id: int, x: float, y: float) -> None:
        self.drones[id].move(x, y)
    
    def get_animal_position(self, id: int) -> Tuple[float, float]:
        return self.animals[id].get_position()
    
    def move_animal(self, id: int, x: float, y: float) -> None:
        self.animals[id].move(x, y)
    
    def detect_wild_animals(self, id: int, radius: float) -> Collection[Tuple[float, float]]:
        drone_pos = self.get_drone_position(id)
        return [animal.get_position() for animal in self.animals if sqrt(((drone_pos[0]-animal.get_position()[0])**2)+((drone_pos[1]-animal.get_position()[0])**2)) < radius]
