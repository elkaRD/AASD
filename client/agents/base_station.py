from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour

from client.domain.controllers.controller import AbstractController

SENDING_REPORT_PERIOD = 60


class BaseStationAgent(Agent):
    # TODO change AbstractController to BaseStationController
    def __init__(self, jid: str, password: str, controller: AbstractController) -> None:
        super().__init__(jid, password)
        self.controller = controller

    def get_behaviours(self):
        return [
            self.CheckAvailabilityOfChargers(self.controller),
            self.SendReportToServer(self.controller),
            self.SendReportToPowerModule(SENDING_REPORT_PERIOD, self.controller)
        ]

    async def setup(self):
        print("BaseStationAgent started")
        for behaviour in self.get_behaviours():
            self.add_behaviour(behaviour)

    class CheckAvailabilityOfChargers(CyclicBehaviour):
        def __init__(self, controller: AbstractController) -> None:
            super().__init__()
            self.controller = controller

        async def run(self):
            # TODO add periodic checking for messages

            return NotImplemented

    class SendReportToServer(CyclicBehaviour):
        def __init__(self, controller: AbstractController) -> None:
            super().__init__()
            self.controller = controller

        async def run(self):
            # TODO add periodic checking if slots availability has changed

            return NotImplemented

    class SendReportToPowerModule(PeriodicBehaviour):
        def __init__(self, period: float, controller: AbstractController) -> None:
            super().__init__(period)
            self.controller = controller

        async def run(self):
            # TODO add periodic checking if slots availability has changed

            return NotImplemented