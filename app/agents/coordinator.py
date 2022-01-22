from typing import Iterator, Union

from aioxmpp import JID

from agents.agent import Agent, Behaviour, CyclicBehaviour
from domain.controllers.drone_controller import DroneController
from loggers import Logger, NullLogger


class CoordinatorAgent(Agent):
    def __init__(
        self,
        jid: Union[str, JID],
        password: str,
        controller: DroneController,
        logger: Logger = NullLogger(),
    ) -> None:
        super().__init__(jid, password, logger)
        self.controller = controller

    def get_behaviours(self) -> Iterator[Behaviour]:
        return [self.Coordinate(self.get_jid(), self.controller, self.get_logger())]

    class Coordinate(CyclicBehaviour):
        def __init__(
            self, jid: JID, controller: DroneController, logger: Logger
        ) -> None:
            super().__init__(jid, logger)
            self.controller = controller

        async def run(self) -> None:
            # TODO add periodic checking for messages from scouts
            return NotImplemented
