from spade.agent import Agent
from spade.behaviour import OneShotBehaviour

from client.domain.controllers.controller import AbstractController


class BaseStationAgent(Agent):
    # TODO change AbstractController to BaseStationController
    def __init__(self, jid: str, password: str, controller: AbstractController) -> None:
        super().__init__(jid, password)
        self.controller = controller

    class MockBehaviour(OneShotBehaviour):
        def __init__(self, controller: AbstractController) -> None:
            super().__init__()
            self.controller = controller

        async def run(self):
            return NotImplemented

    async def setup(self):
        print("BaseStationAgent started")
        b = self.MockBehaviour(self.controller)
        self.add_behaviour(b)
