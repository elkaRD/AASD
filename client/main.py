import os
from datetime import datetime
import time

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

SERVER_HOST = os.getenv("SERVER_HOST", "localhost")
import messages as messages


class SenderAgent(Agent):
    class InformBehav(OneShotBehaviour):
        async def run(self):
            print("InformBehav running")
            body = messages.HelpRequestBody(
                time=datetime.now(),
                position=messages.Coordinates(lat=1.0, long=2.0),
                urgency=messages.UrgencyEnum.HIGH,
            )
            msg = body.make_message("receiver@{SERVER_HOST}", "sender@{SERVER_HOST}")

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
        template.set_metadata("performative", "request")
        self.add_behaviour(b, template)


if __name__ == "__main__":
    receiveragent = ReceiverAgent(f"receiver@{SERVER_HOST}", "password")
    future = receiveragent.start()
    future.result()  # wait for receiver agent to be prepared.
    senderagent = SenderAgent(f"sender@{SERVER_HOST}", "password")
    senderagent.start()

    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            receiveragent.stop()
            break
    print("Agents finished")
