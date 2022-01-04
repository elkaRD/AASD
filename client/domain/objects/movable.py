from abc import ABC
from typing import Tuple


class AbstractMovable(ABC):
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def get_position(self) -> Tuple[float, float]:
        return (self.x, self.y)
    
    def move(self, x: float, y: float) -> None:
        self.x += x
        self.y += y
