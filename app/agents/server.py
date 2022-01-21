from typing import Iterator

from agents.agent import Agent, Behaviour, CyclicBehaviour


class ServerAgent(Agent):
    def get_behaviours(self) -> Iterator[Behaviour]:
        return [
            self.ProcessReports(self.get_jid(), self.get_logger())
        ]

    class ProcessReports(CyclicBehaviour):
        async def run(self) -> None:
            # TODO add periodic checking for messages from scouts and base station
            return NotImplemented
