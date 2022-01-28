from abc import ABC, abstractmethod
from math import sqrt
from typing import Collection, List, Optional, Tuple

from domain.objects.animal import Animal
from domain.objects.dock import Dock
from domain.objects.drone import Drone


class AbstractEnvironment(ABC):
    @abstractmethod
    def add_drone(self, x: float, y: float) -> int:
        pass

    @abstractmethod
    def add_animal(self, x: float, y: float) -> int:
        pass

    @abstractmethod
    def add_base_station_dock(self) -> int:
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
    def chase_away_animal(self, animal_id: int) -> None:
        pass

    @abstractmethod
    def distance_between(self, obj1: Tuple, obj2: Tuple) -> float:
        pass

    @abstractmethod
    def detect_wild_animals(
        self, drone_id: int, radius: float = 10
    ) -> Collection[Tuple[float, float]]:
        pass

    @abstractmethod
    def chase_away_wild_animals(self, radius: float = 5) -> None:
        pass

    @abstractmethod
    def get_base_station_docks_occupation(self) -> List[Optional[int]]:
        pass

    @abstractmethod
    def get_drones_positions_list(self) -> List[Tuple[float, float]]:
        pass

    @abstractmethod
    def get_field_scope(
        self,
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        pass

    @abstractmethod
    def get_animals_positions_list(self) -> List[Tuple[float, float]]:
        pass

    @abstractmethod
    def get_drone_battery(self, drone_id: int) -> float:
        pass

    @abstractmethod
    def step(self) -> None:
        pass


class Environment(AbstractEnvironment):
    def __init__(
        self,
        x_field_scope: Tuple[float, float] = (0, 10),
        y_field_scope: Tuple[float, float] = (0, 10),
    ) -> None:
        self.drones: List[Drone] = []
        self.animals: List[Animal] = []
        self.base_station_docks: List[Dock] = []
        self.x_field_scope = x_field_scope
        self.y_field_scope = y_field_scope

    def add_drone(self, x: float, y: float) -> int:
        drone_id = len(self.drones)
        drone = Drone(
            max(self.x_field_scope[0], min(self.x_field_scope[1], x)),
            max(self.y_field_scope[0], min(self.y_field_scope[1], y)),
        )
        self.drones.append(drone)
        return drone_id

    def add_animal(self, x: float, y: float) -> int:
        animal_id = len(self.animals)
        animal = Animal(
            max(self.x_field_scope[0], min(self.x_field_scope[1], x)),
            max(self.y_field_scope[0], min(self.y_field_scope[1], y)),
        )
        self.animals.append(animal)
        return animal_id

    def add_base_station_dock(self) -> int:
        slot_id = len(self.base_station_docks)
        slot = Dock()
        self.base_station_docks.append(slot)
        return slot_id

    def get_drone_position(self, drone_id: int) -> Tuple[float, float]:
        return self.drones[drone_id].get_position()

    def move_drone(self, drone_id: int, x: float, y: float) -> None:
        self.drones[drone_id].move(
            max(self.x_field_scope[0], min(self.x_field_scope[1], x)),
            max(self.y_field_scope[0], min(self.y_field_scope[1], y)),
        )

    def get_animal_position(self, animal_id: int) -> Tuple[float, float]:
        return self.animals[animal_id].get_position()

    def move_animal(self, animal_id: int, x: float, y: float) -> None:
        self.animals[animal_id].move(x, y)

    def chase_away_animal(self, animal_id: int) -> None:
        self.animals.pop(animal_id)

    def distance_between(self, obj1: Tuple, obj2: Tuple) -> float:
        return sqrt((obj1[0] - obj2[0]) ** 2 + (obj1[1] - obj2[1]) ** 2)

    def detect_wild_animals(
        self, drone_id: int, radius: float = 10
    ) -> Collection[Tuple[float, float]]:
        drone_pos = self.get_drone_position(drone_id)
        return [
            animal.get_position()
            for animal in self.animals
            if self.distance_between(drone_pos, animal.get_position())
            <= radius
        ]

    def chase_away_wild_animals(self, radius: float = 1) -> None:
        for drone in self.drones:
            for i, animal in enumerate(self.animals):
                if (
                    self.distance_between(
                        drone.get_position(), animal.get_position()
                    )
                    <= radius
                ):
                    self.chase_away_animal(i)

    def get_base_station_docks_occupation(self) -> List[Optional[int]]:
        return [slot.occupied_by for slot in self.base_station_docks]

    def get_field_scope(
        self,
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        return self.x_field_scope, self.y_field_scope

    def step(self) -> None:
        self.chase_away_wild_animals()

    def get_drones_positions_list(self) -> List[Tuple[float, float]]:
        return [drone.get_position() for drone in self.drones]

    def get_animals_positions_list(self) -> List[Tuple[float, float]]:
        return [animal.get_position() for animal in self.animals]

    def get_drone_battery(self, drone_id: int) -> float:
        return self.drones[drone_id].get_battery()
