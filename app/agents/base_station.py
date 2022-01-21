from typing import Iterator

from aioxmpp import JID

from agents.agent import Agent, Behaviour, CyclicBehaviour, PeriodicBehaviour
from domain.controllers.controller import AbstractController
from loggers import Logger, NullLogger

SENDING_REPORT_PERIOD = 60


class BaseStationAgent(Agent):
    # TODO change AbstractController to BaseStationController
    def __init__(
            self,
            jid: str,
            password: str,
            controller: AbstractController,
            logger: Logger = NullLogger()
    ) -> None:
        super().__init__(jid, password, logger)
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
            return NotImplemented

    class SendReportToServer(CyclicBehaviour):
        def __init__(
                self,
                jid: JID,
                controller: AbstractController,
                logger: Logger
        ) -> None:
            super().__init__(jid, logger)
            self.controller = controller

        async def run(self) -> None:
            # TODO add periodic checking if slots availability has changed
            return NotImplemented

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
            return NotImplemented
