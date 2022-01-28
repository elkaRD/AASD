from domain.objects.movable import AbstractMovable


class Drone(AbstractMovable):
    def __init__(self, x: float, y: float, battery: float = 100.0) -> None:
        super().__init__(x, y)
        self.battery = battery

    def get_battery(self) -> float:
        return self.battery

    def change_battery(self, amount: float) -> None:
        self.battery += amount
