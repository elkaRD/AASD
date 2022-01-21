from typing import Iterator

from agents.agent import Agent, Behaviour, CyclicBehaviour
from domain.controllers.drone_controller import DroneController
from loggers import Logger, NullLogger


class ScoutAgent(Agent):
    def __init__(
            self,
            jid: str,
            password: str,
            controller: DroneController,
            logger: Logger = NullLogger()
    ) -> None:
        super().__init__(jid, password, logger)
        self.controller = controller

    def get_behaviours(self) -> Iterator[Behaviour]:
        return [self.CheckReportsFromStormtroopers(
            self.get_jid(), self.get_logger()
        )]

    class CheckReportsFromStormtroopers(CyclicBehaviour):
        async def run(self) -> None:
            # TODO check if there are reports from stormtroopers
            return NotImplemented
