from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour

from client.domain.controllers.controller import AbstractController
from client.domain.controllers.drone_controller import DroneController


class ScoutAgent(Agent):

    def __init__(self, jid: str, password: str, controller: DroneController) -> None:
        super().__init__(jid, password)
        self.controller = controller

    def get_behaviours(self):
        return [
            self.CheckReportsFromStormtroopers()
        ]

    async def setup(self):
        print("ScoutAgent started")
        for behaviour in self.get_behaviours():
            self.add_behaviour(behaviour)

    class CheckReportsFromStormtroopers(CyclicBehaviour):
        async def run(self):
            # TODO check if there are reports from stormtroopers

            return NotImplemented
