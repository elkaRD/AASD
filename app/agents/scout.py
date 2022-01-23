from datetime import datetime
from typing import Iterator, Optional, Union

from aioxmpp import JID

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
SEARCH_PERIOD = 10


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

    def get_behaviours(self) -> Iterator[Behaviour]:
        return [
            self.CheckReportsFromStormtroopers(
                self.get_jid(), self.get_logger()
            ),
            self.Search(
                self.get_jid(),
                self.coordinator_jid,
                self.controller,
                SEARCH_RADIUS,
                SEARCH_PERIOD,
                self.get_logger(),
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
                pass  # TODO: what now? what if there are multiple detections?

    class CheckReportsFromStormtroopers(CyclicBehaviour):
        async def run(self) -> None:
            message = await self.receive(timeout=60)
            if message:
                content: SectorClearedReportBody = MessageBody.parse(message)
                self.log(
                    f"New report from {message.sender}:\n{content.pretty_print()}"
                )
                reply = SectorClearedRecievedBody(accepted=True).make_response(
                    message
                )
                await self.send(reply)
                self.log(f"Sent reply to {reply.to}")

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
            self.log(f"Sent searching report to {self.coordinator_jid}")
            message = await self.receive(timeout=10)
            if message:
                content: SearchingDirectivesBody = MessageBody.parse(message)
                self.log(f"Received reply from {message.sender}")
                if not content.keep_schedule:
                    xt, yt = (
                        content.change_direction.x,
                        content.change_direction.y,
                    )
                self.controller.move(xt, yt)
                self.log(f"Moving to ({xt:.3f}, {yt:.3f})")
