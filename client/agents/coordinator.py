from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

from domain.controllers.drone_controller import DroneController


class CoordinatorAgent(Agent):

    def __init__(
            self,
            jid: str,
            password: str,
            controller: DroneController
    ) -> None:
        super().__init__(jid, password)
        self.controller = controller

    def get_behaviours(self):
        return [
            self.Coordinate(self.controller)
        ]

    async def setup(self):
        print("CoordinatorAgent started")
        for behaviour in self.get_behaviours():
            self.add_behaviour(behaviour)

    class Coordinate(CyclicBehaviour):
        def __init__(self, controller: DroneController) -> None:
            super().__init__()
            self.controller = controller

        async def run(self):
            # TODO add periodic checking for messages from scouts

            return NotImplemented
