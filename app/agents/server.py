from spade.agent import Agent
from spade.behaviour import CyclicBehaviour


class ServerAgent(Agent):

    def get_behaviours(self):
        return [
            self.ProcessReports()
        ]

    async def setup(self):
        print("ServerAgent started")
        for behaviour in self.get_behaviours():
            self.add_behaviour(behaviour)

    class ProcessReports(CyclicBehaviour):
        async def run(self):
            # TODO add periodic checking for messages from scouts and base station

            return NotImplemented
