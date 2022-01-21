from typing import Iterator

from agents.agent import Agent, Behaviour, CyclicBehaviour
from messages.messages import MessageBody


class ServerAgent(Agent):
    def get_behaviours(self) -> Iterator[Behaviour]:
        return [
            self.ProcessReports(self.get_jid(), self.get_logger())
        ]

    class ProcessReports(CyclicBehaviour):
        async def run(self) -> None:
            message = await self.receive(timeout=60)
            if message:
                content = MessageBody.parse(message)
                self.log(
                    f"New report from {message.sender}:\n{content.pretty_print()}"
                )
