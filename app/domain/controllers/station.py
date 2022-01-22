from typing import Optional, Sequence

from domain.environment import AbstractEnvironment


class BaseStationController:
    def __init__(self, environment: AbstractEnvironment) -> None:
        self.environment = environment

    def get_docks_occupation(self) -> Sequence[Optional[int]]:
        return self.environment.get_base_station_docks_occupation()
