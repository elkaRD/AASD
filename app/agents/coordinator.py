import math
import random
from typing import Iterator, Optional, Tuple, Union

from aioxmpp import JID
from spade.template import Template

from agents.agent import Agent, Behaviour, CyclicBehaviour
from domain.controllers.drone import DroneController
from loggers import Logger, NullLogger
from messages.messages import (
    Coordinates,
    MessageBody,
    SearchingDirectivesBody,
    SearchingStatusBody,
)


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

    def get_behaviours(self) -> Iterator[Tuple[Behaviour, Optional[Template]]]:
        return [
            (
                self.Coordinate(
                    self.get_jid(), self.controller, self.get_logger()
                ),
                Template(metadata=SearchingStatusBody.metadata()),
            )
        ]

    class Coordinate(CyclicBehaviour):
        def __init__(
            self, jid: JID, controller: DroneController, logger: Logger
        ) -> None:
            super().__init__(jid, logger)
            self.controller = controller

        async def run(self) -> None:
            message = await self.receive(timeout=60)
            if message:
                content: SearchingStatusBody = MessageBody.parse(message)
                # self.log(f"New report from {message.sender}")
                theta = random.random() * 2 * math.pi
                x = (
                    content.actual_position.x
                    + math.cos(theta) * content.searching_range_meters
                )
                y = (
                    content.actual_position.y
                    + math.sin(theta) * content.searching_range_meters
                )
                reply = SearchingDirectivesBody(
                    keep_schedule=False,
                    change_direction=Coordinates(x=x, y=y),
                ).make_response(message)
                self.log(f"New search position: ({x:.3f}, {y:.3f})")
                await self.send(reply)
