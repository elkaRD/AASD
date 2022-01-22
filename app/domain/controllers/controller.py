from abc import ABC, abstractmethod
from typing import Tuple


class AbstractMovableController(ABC):
    @abstractmethod
    def get_position(self) -> Tuple[float, float]:
        pass

    @abstractmethod
    def move(self, x: float, y: float) -> None:
        pass
