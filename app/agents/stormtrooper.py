from typing import Iterator, Optional, Tuple, Union

from aioxmpp import JID
from spade.template import Template

from agents.agent import Agent, Behaviour, OneShotBehaviour
from domain.controllers.controller import AbstractMovableController
from domain.controllers.drone import DroneController
from loggers import Logger


class StormtrooperAgent(Agent):
    def __init__(
        self, jid: Union[str, JID], password: str, controller: DroneController
    ) -> None:
        super().__init__(jid, password)
        self.controller = controller

    def get_behaviours(self) -> Iterator[Tuple[Behaviour, Optional[Template]]]:
        return [
            (
                self.MockBehaviour(
                    self.get_jid(), self.controller, self.get_logger()
                ),
                None,
            )
        ]

    class MockBehaviour(OneShotBehaviour):
        def __init__(
            self,
            jid: JID,
            controller: AbstractMovableController,
            logger: Logger,
        ) -> None:
            super().__init__(jid, logger)
            self.controller = controller

        async def run(self) -> None:
            return NotImplemented
