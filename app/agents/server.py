from typing import Iterator, Optional, Tuple

from spade.template import Template

from agents.agent import Agent, Behaviour, CyclicBehaviour
from messages.messages import MessageBody


class ServerAgent(Agent):
    def get_behaviours(self) -> Iterator[Tuple[Behaviour, Optional[Template]]]:
        return [(self.ProcessReports(self.get_jid(), self.get_logger()), None)]

    class ProcessReports(CyclicBehaviour):
        async def run(self) -> None:
            message = await self.receive(timeout=60)
            if message:
                content = MessageBody.parse(message)
                self.log(
                    f"New report from {message.sender}:\n{content.pretty_print()}"
                )
