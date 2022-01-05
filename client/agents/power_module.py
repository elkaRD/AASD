from spade.agent import Agent
from spade.behaviour import OneShotBehaviour

from client.domain.controllers.controller import AbstractController
from client.domain.controllers.drone_controller import DroneController


class PowerModuleAgent(Agent):

    def __init__(self, jid: str, password: str, controller: DroneController) -> None:
        super().__init__(jid, password)
        self.controller = controller

    class MockBehaviour(OneShotBehaviour):
        def __init__(self, controller: AbstractController) -> None:
            super().__init__()
            self.controller = controller

        async def run(self):
            return NotImplemented

    async def setup(self):
        print("PowerModuleAgent started")
        b = self.MockBehaviour(self.controller)
        self.add_behaviour(b)