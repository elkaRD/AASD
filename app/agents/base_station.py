from asyncio import sleep
from typing import Iterator, Union

from aioxmpp import JID

from agents.agent import Agent, Behaviour, CyclicBehaviour, PeriodicBehaviour
from domain.controllers.controller import AbstractController
from loggers import Logger, NullLogger
from messages import Dock, DockOccupationReportBody

SENDING_REPORT_PERIOD = 60


class BaseStationAgent(Agent):
    # TODO change AbstractController to BaseStationController
    def __init__(
            self,
            jid: Union[str, JID],
            password: str,
            server_jid: Union[str, JID],
            controller: AbstractController,
            logger: Logger = NullLogger()
    ) -> None:
        super().__init__(jid, password, logger)
        self.server_jid = JID.fromstr(str(server_jid))
        self.controller = controller

    def get_behaviours(self) -> Iterator[Behaviour]:
        return [
            self.CheckAvailabilityOfChargers(
                self.get_jid(),
                self.controller,
                self.get_logger()
            ),
            self.SendReportToServer(
                self.get_jid(),
                self.server_jid,
                self.controller,
                self.get_logger()
            ),
            self.SendReportToPowerModule(
                self.get_jid(),
                SENDING_REPORT_PERIOD,
                self.controller,
                self.get_logger()
            )
        ]

    class CheckAvailabilityOfChargers(CyclicBehaviour):
        def __init__(
                self,
                jid: JID,
                controller: AbstractController,
                logger: Logger
        ) -> None:
            super().__init__(jid, logger)
            self.controller = controller

        async def run(self) -> None:
            # TODO add periodic checking for messages
            pass

    class SendReportToServer(CyclicBehaviour):
        def __init__(
                self,
                jid: JID,
                server_jid: JID,
                controller: AbstractController,
                logger: Logger
        ) -> None:
            super().__init__(jid, logger)
            self.server_jid = server_jid
            self.controller = controller

        async def run(self) -> None:
            # TODO add periodic checking if slots availability has changed
            body = DockOccupationReportBody(
                total_docks=1,
                status=[Dock(occupied=False, number=0)]
            )
            message = body.make_message(self.server_jid, self.get_jid())
            await self.send(message)
            await sleep(10)

    class SendReportToPowerModule(PeriodicBehaviour):
        def __init__(
                self,
                jid: JID,
                period: float,
                controller: AbstractController,
                logger: Logger
        ) -> None:
            super().__init__(jid, period, logger)
            self.controller = controller

        async def run(self) -> None:
            # TODO add periodic checking if slots availability has changed
            pass
