from abc import ABC, abstractmethod
from math import sqrt
from typing import Collection, List, Tuple

from domain.objects.animal import Animal
from domain.objects.drone import Drone


class AbstractEnvironment(ABC):
    @abstractmethod
    def add_drone(self, x: float, y: float) -> int:
        pass

    @abstractmethod
    def add_animal(self, x: float, y: float) -> int:
        pass

    @abstractmethod
    def get_drone_position(self, drone_id: int) -> Tuple[float, float]:
        pass

    @abstractmethod
    def move_drone(self, drone_id: int, x: float, y: float) -> None:
        pass

    @abstractmethod
    def get_animal_position(self, animal_id: int) -> Tuple[float, float]:
        pass

    @abstractmethod
    def move_animal(self, animal_id: int, x: float, y: float) -> None:
        pass

    @abstractmethod
    def detect_wild_animals(
            self,
            drone_id: int,
            radius: float
    ) -> Collection[Tuple[float, float]]:
        pass


class Environment(AbstractEnvironment):
    def __init__(self) -> None:
        self.drones: List[Drone] = []
        self.animals: List[Animal] = []

    def add_drone(self, x: float, y: float) -> int:
        drone_id = len(self.drones)
        drone = Drone(x, y)
        self.drones.append(drone)
        return drone_id

    def add_animal(self, x: float, y: float) -> int:
        animal_id = len(self.animals)
        animal = Animal(x, y)
        self.animals.append(animal)
        return animal_id

    def get_drone_position(self, drone_id: int) -> Tuple[float, float]:
        return self.drones[drone_id].get_position()

    def move_drone(self, drone_id: int, x: float, y: float) -> None:
        self.drones[drone_id].move(x, y)

    def get_animal_position(self, animal_id: int) -> Tuple[float, float]:
        return self.animals[animal_id].get_position()

    def move_animal(self, animal_id: int, x: float, y: float) -> None:
        self.animals[animal_id].move(x, y)

    def detect_wild_animals(
            self,
            drone_id: int,
            radius: float
    ) -> Collection[Tuple[float, float]]:
        drone_pos = self.get_drone_position(drone_id)
        return [
            animal.get_position()
            for animal in self.animals
            if sqrt(
                (drone_pos[0] - animal.get_position()[0]) ** 2 +
                (drone_pos[1] - animal.get_position()[1]) ** 2
            ) <= radius
        ]
