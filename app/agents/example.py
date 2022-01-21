from datetime import datetime
from typing import Iterator

from spade.template import Template

from agents.agent import Agent, Behaviour, OneShotBehaviour
from messages import Coordinates, HelpOfferBody
from properties import SERVER_DOMAIN


class SenderAgent(Agent):
    def get_behaviours(self) -> Iterator[Behaviour]:
        return [
            self.InformBehaviour(self.get_jid(), self.get_logger())
        ]

    class InformBehaviour(OneShotBehaviour):
        async def run(self):
            self.log("Running")
            body = HelpOfferBody(
                time=datetime.now(),
                position=Coordinates(x=10.0, y=4.4),
                eta=20,
            )
            msg = body.make_message(
                to=f"receiver@{SERVER_DOMAIN}",
                sender=f"sender@{SERVER_DOMAIN}"
            )

            await self.send(msg)
            self.log("MessageBody sent!")

            # stop agent from behaviour
            await self.agent.stop()


class ReceiverAgent(Agent):
    def get_behaviours(self) -> Iterator[Behaviour]:
        b = self.RecvBehaviour(self.get_jid(), self.get_logger())
        template = Template()
        template.set_metadata("performative", "agree")
        self.add_behaviour(b, template)
        return [b]

    class RecvBehaviour(OneShotBehaviour):
        async def run(self):
            self.log("Running")

            msg = await self.receive(
                timeout=10
            )  # wait for a message for 10 seconds
            if msg:
                self.log("MessageBody received with content: {}".format(msg.body))
            else:
                self.log("Did not received any message after 10 seconds")

            # stop agent from behaviour
            await self.agent.stop()
