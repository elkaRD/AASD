from spade.agent import Agent
from spade.behaviour import OneShotBehaviour


class ServerAgent(Agent):
    class MockBehaviour(OneShotBehaviour):
        async def run(self):
            return NotImplemented

    async def setup(self):
        print("ServerAgent started")
        b = self.MockBehaviour()
        self.add_behaviour(b)