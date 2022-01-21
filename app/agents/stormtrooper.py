from typing import Iterator, Union

from aioxmpp import JID

from agents.agent import Agent, Behaviour, OneShotBehaviour
from domain.controllers.controller import AbstractController
from domain.controllers.drone_controller import DroneController
from loggers import Logger


class StormtrooperAgent(Agent):
    def __init__(
            self,
            jid: Union[str, JID],
            password: str,
            controller: DroneController
    ) -> None:
        super().__init__(jid, password)
        self.controller = controller

    def get_behaviours(self) -> Iterator[Behaviour]:
        return [
            self.MockBehaviour(
                self.get_jid(),
                self.controller,
                self.get_logger()
            )
        ]

    class MockBehaviour(OneShotBehaviour):
        def __init__(
                self,
                jid: JID,
                controller: AbstractController,
                logger: Logger
        ) -> None:
            super().__init__(jid, logger)
            self.controller = controller

        async def run(self) -> None:
            return NotImplemented
