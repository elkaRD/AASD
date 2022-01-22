from asyncio import sleep
from typing import Iterator, Sequence, Union

from aioxmpp import JID

from agents.agent import Agent, Behaviour, CyclicBehaviour, PeriodicBehaviour
from domain.controllers.station import BaseStationController
from loggers import Logger, NullLogger
from messages import Dock, DockOccupationReportBody, Drone
from messages.messages import ChargingResponseBody, MessageBody

SENDING_REPORT_PERIOD = 10


class BaseStationAgent(Agent):
    def __init__(
        self,
        jid: Union[str, JID],
        password: str,
        server_jid: Union[str, JID],
        power_module_jids: Sequence[Union[str, JID]],
        controller: BaseStationController,
        logger: Logger = NullLogger(),
    ) -> None:
        super().__init__(jid, password, logger)
        self.server_jid = JID.fromstr(str(server_jid))
        self.power_module_jids = [
            JID.fromstr(str(jid)) for jid in power_module_jids
        ]
        self.controller = controller

    def get_behaviours(self) -> Iterator[Behaviour]:
        return [
            self.CheckAvailabilityOfChargers(
                self.get_jid(), self.controller, self.get_logger()
            ),
            self.SendReportToServer(
                self.get_jid(),
                self.server_jid,
                SENDING_REPORT_PERIOD,
                self.controller,
                self.get_logger(),
            ),
            self.SendReportToPowerModules(
                self.get_jid(),
                self.power_module_jids,
                SENDING_REPORT_PERIOD,
                self.controller,
                self.get_logger(),
            ),
        ]

    class CheckAvailabilityOfChargers(CyclicBehaviour):
        def __init__(
            self, jid: JID, controller: BaseStationController, logger: Logger
        ) -> None:
            super().__init__(jid, logger)
            self.controller = controller

        async def run(self) -> None:
            message = await self.receive(60)
            if message:
                content = MessageBody.parse(message)
                self.log(
                    f"New request from {message.sender}:\n{content.pretty_print()}"
                )
                reply = ChargingResponseBody(
                    charging_available=True
                ).make_response(message)
                await self.send(reply)
                self.log(f"Reply sent to {reply.to}")

    class SendReportToServer(PeriodicBehaviour):
        def __init__(
            self,
            jid: JID,
            server_jid: JID,
            period: float,
            controller: BaseStationController,
            logger: Logger,
        ) -> None:
            super().__init__(jid, period, logger)
            self.server_jid = server_jid
            self.controller = controller
            self.last_occupation = self.controller.get_docks_occupation()

        async def run(self) -> None:
            occupation = self.controller.get_docks_occupation()
            if occupation != self.last_occupation:
                self.log("Docks occupation changed")
                body = DockOccupationReportBody(
                    total_docks=len(occupation),
                    status=[
                        Dock(
                            occupied=occ is not None,
                            number=i,
                            occupied_by=None if occ is None else Drone(id=occ),
                        )
                        for i, occ in enumerate(occupation)
                    ],
                )
                message = body.make_message(self.server_jid, self.get_jid())
                await self.send(message)
                self.log(f"Sent docks occupation report to {self.server_jid}")
            self.last_occupation = occupation
            await sleep(10)

    class SendReportToPowerModules(PeriodicBehaviour):
        def __init__(
            self,
            jid: JID,
            power_module_jids: Sequence[JID],
            period: float,
            controller: BaseStationController,
            logger: Logger,
        ) -> None:
            super().__init__(jid, period, logger)
            self.power_module_jids = power_module_jids
            self.controller = controller
            self.last_occupation = self.controller.get_docks_occupation()

        async def run(self) -> None:
            occupation = self.controller.get_docks_occupation()
            if occupation != self.last_occupation:
                self.log("Docks occupation changed")
                body = DockOccupationReportBody(
                    total_docks=len(occupation),
                    status=[
                        Dock(
                            occupied=occ is not None,
                            number=i,
                            occupied_by=None if occ is None else Drone(id=occ),
                        )
                        for i, occ in enumerate(occupation)
                    ],
                )
                for jid in self.power_module_jids:
                    message = body.make_message(jid, self.get_jid())
                    await self.send(message)
                    self.log(f"Sent docks occupation report to {jid}")
            self.last_occupation = occupation
