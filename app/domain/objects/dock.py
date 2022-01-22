from typing import Optional


class Dock:
    occupied_by: Optional[int] = None

    @property
    def occupied(self) -> bool:
        return self.occupied_by is not None

    def occupy(self, drone_id: int) -> None:
        self.occupied_by = drone_id

    def deoccupy(self) -> None:
        self.occupied_by = None
