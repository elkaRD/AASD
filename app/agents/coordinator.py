import math
import random
from typing import Iterator, Union

from aioxmpp import JID

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

    def get_behaviours(self) -> Iterator[Behaviour]:
        return [
            self.Coordinate(self.get_jid(), self.controller, self.get_logger())
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
                self.log(
                    f"New report from {message.sender}:\n{content.pretty_print()}"
                )
                theta = random.random() * 2 * math.pi
                reply = SearchingDirectivesBody(
                    keep_schedule=False,
                    change_direction=Coordinates(
                        x=content.actual_position.x
                        + math.cos(theta) * content.searching_range_meters,
                        y=content.actual_position.y
                        + math.sin(theta) * content.searching_range_meters,
                    ),
                ).make_response(message)
                await self.send(reply)
