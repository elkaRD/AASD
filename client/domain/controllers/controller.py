from abc import ABC, abstractmethod
from typing import Tuple


class AbstractController(ABC):
    @abstractmethod
    def get_position(self) -> Tuple[float, float]:
        return NotImplemented
    
    @abstractmethod
    def move(self, x: float, y: float) -> None:
        return NotImplemented
