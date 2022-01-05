from datetime import datetime
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.template import Template

from client.messages import HelpOfferBody, Coordinates
from client.properties import SERVER_HOST


class SenderAgent(Agent):
    class InformBehav(OneShotBehaviour):
        async def run(self):
            print("InformBehav running")
            body = HelpOfferBody(
                time=datetime.now(),
                position=Coordinates(lat=10.0, long=4.4),
                eta=20,
            )
            msg = body.make_message(to=f"receiver@{SERVER_HOST}", sender=f"sender@{SERVER_HOST}")

            await self.send(msg)
            print("Message sent!")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("SenderAgent started")
        b = self.InformBehav()
        self.add_behaviour(b)


class ReceiverAgent(Agent):
    class RecvBehav(OneShotBehaviour):
        async def run(self):
            print("RecvBehav running")

            msg = await self.receive(
                timeout=10
            )  # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
            else:
                print("Did not received any message after 10 seconds")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "agree")
        self.add_behaviour(b, template)

