import math
import random
import time
from datetime import datetime
from typing import Iterator, Optional, Tuple, Union

from aioxmpp import JID
from spade.template import Template

from agents.agent import Agent, Behaviour, CyclicBehaviour, PeriodicBehaviour
from domain.controllers.drone import DroneController
from loggers import Logger, NullLogger
from messages import Coordinates, SearchingStatusBody
from messages.messages import (
    MessageBody,
    SearchingDirectivesBody,
    SectorClearedRecievedBody,
    SectorClearedReportBody,
)

SEARCH_RADIUS = 5
SEARCH_PERIOD = 1


class ScoutAgent(Agent):
    def __init__(
        self,
        jid: Union[str, JID],
        coordinator_jid: Union[str, JID],
        password: str,
        controller: DroneController,
        logger: Logger = NullLogger(),
    ) -> None:
        super().__init__(jid, password, logger)
        self.coordinator_jid = JID.fromstr(str(coordinator_jid))
        self.controller = controller

    def get_behaviours(self) -> Iterator[Tuple[Behaviour, Optional[Template]]]:
        return [
            (
                self.CheckDetection(
                    self.get_jid(),
                    SEARCH_RADIUS,
                    SEARCH_PERIOD,
                    self.controller,
                    self.get_logger(),
                ),
                None,
            ),
            (
                self.CheckReportsFromStormtroopers(
                    self.get_jid(), self.get_logger()
                ),
                Template(metadata=SectorClearedReportBody.metadata()),
            ),
            (
                self.Search(
                    self.get_jid(),
                    self.coordinator_jid,
                    self.controller,
                    SEARCH_RADIUS,
                    SEARCH_PERIOD,
                    self.get_logger(),
                ),
                Template(metadata=SearchingDirectivesBody.metadata()),
            ),
        ]

    class CheckDetection(PeriodicBehaviour):
        def __init__(
            self,
            jid: JID,
            radius: float,
            period: float,
            controller: DroneController,
            logger: Logger = NullLogger(),
            start_at: Optional[datetime] = None,
        ):
            super().__init__(jid, period, logger, start_at)
            self.radius = radius
            self.controller = controller

        async def run(self) -> None:
            detection = self.controller.detect_wild_animals(self.radius)
            if detection:
                x, y = random.choice(tuple(detection))
                self.log(f"Animal detected at: ({x:.3f}, {y:.3f})")
                while (x, y) in self.controller.detect_wild_animals(
                    self.radius
                ):
                    self.log(
                        f"Distance to animal: {math.sqrt((x - self.controller.get_position()[0]) ** 2 + (y - self.controller.get_position()[1]) ** 2)}"
                    )
                    self.controller.move(
                        self.controller.get_position()[0]
                        + 0.5 * (x - self.controller.get_position()[0]),
                        self.controller.get_position()[1]
                        + 0.5 * (y - self.controller.get_position()[1]),
                    )
                    time.sleep(0.5)
                self.log(f"Animal at ({x:.3f}, {y:.3f}) scared away")

    class CheckReportsFromStormtroopers(CyclicBehaviour):
        async def run(self) -> None:
            message = await self.receive(timeout=60)
            if message:
                _ = MessageBody.parse(message)
                # self.log(f"New report from {message.sender}")
                reply = SectorClearedRecievedBody(accepted=True).make_response(
                    message
                )
                await self.send(reply)
                # self.log(f"Sent reply to {reply.to}")

    class Search(PeriodicBehaviour):
        def __init__(
            self,
            jid: JID,
            coordinator_jid: JID,
            controller: DroneController,
            radius: float,
            period: float,
            logger: Logger = NullLogger(),
            start_at: Optional[datetime] = None,
        ):
            super().__init__(jid, period, logger, start_at)
            self.coordinator_jid = coordinator_jid
            self.controller = controller
            self.radius = radius

        async def run(self) -> None:
            x, y = self.controller.get_position()
            xt, yt = 0, 0
            detections = self.controller.detect_wild_animals(self.radius)
            message = SearchingStatusBody(
                actual_position=Coordinates(x=x, y=y),
                searching_range_meters=self.radius,
                boars_positions=[Coordinates(x=x, y=y) for x, y in detections],
                heading_towards=Coordinates(x=xt, y=yt),
            ).make_message(self.coordinator_jid, self.get_jid())
            await self.send(message)
            # self.log(f"Sent searching report to {self.coordinator_jid}")
            message = await self.receive(timeout=10)
            if message:
                content: SearchingDirectivesBody = MessageBody.parse(message)
                # self.log(f"Received reply from {message.sender}")
                if not content.keep_schedule:
                    xt, yt = (
                        content.change_direction.x,
                        content.change_direction.y,
                    )
                self.controller.move(xt, yt)
                self.log(f"Moving to ({xt:.3f}, {yt:.3f})")
