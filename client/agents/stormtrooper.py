from spade.agent import Agent
from spade.behaviour import OneShotBehaviour

from client.domain.controllers.controller import AbstractController
from client.domain.controllers.drone_controller import DroneController


class StormtrooperAgent(Agent):

    def __init__(self, jid: str, password: str, controller: DroneController) -> None:
        super().__init__(jid, password)
        self.controller = controller

    def get_behaviours(self):
        return [
            self.MockBehaviour(self.controller)
        ]

    async def setup(self):
        print("ScoutAgent started")
        for behaviour in self.get_behaviours():
            self.add_behaviour(behaviour)

    class MockBehaviour(OneShotBehaviour):
        def __init__(self, controller: AbstractController) -> None:
            super().__init__()
            self.controller = controller

        async def run(self):
            return NotImplemented
