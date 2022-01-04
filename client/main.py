import os

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

from domain.controllers.animal_controller import AnimalController
from domain.controllers.drone_controller import DroneController
from domain.environment import Environment

SERVER_HOST = os.getenv("SERVER_HOST", "localhost")


class SenderAgent(Agent):
    class InformBehav(OneShotBehaviour):
        async def run(self):
            print("InformBehav running")
            msg = Message(
                to=f"receiver@{SERVER_HOST}"
            )  # Instantiate the message
            msg.set_metadata(
                "performative",
                "inform"
            )  # Set the "inform" FIPA performative
            msg.body = "Hello World"  # Set the message content

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
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)


if __name__ == "__main__":
    # receiveragent = ReceiverAgent(f"receiver@{SERVER_HOST}", "password")
    # future = receiveragent.start()
    # future.result()  # wait for receiver agent to be prepared.
    # senderagent = SenderAgent(f"sender@{SERVER_HOST}", "password")
    # senderagent.start()

    # while receiveragent.is_alive():
    #     try:
    #         time.sleep(1)
    #     except KeyboardInterrupt:
    #         senderagent.stop()
    #         receiveragent.stop()
    #         break
    # print("Agents finished")
    environment = Environment()

    drone1 = DroneController(environment, 0, 0)
    drone2 = DroneController(environment, 10, 10)

    animal1 = AnimalController(environment, 5, 5)
    animal2 = AnimalController(environment, 4, 4)

    print(drone1.detect_wild_animals(5))

    drone1.move(3, 3)

    print(drone1.detect_wild_animals(5))
