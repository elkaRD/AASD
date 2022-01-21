import time

from agents.example import ReceiverAgent, SenderAgent
from domain.controllers.animal_controller import AnimalController
from domain.controllers.drone_controller import DroneController
from domain.environment import Environment
from loggers import ConsoleLogger
from properties import SERVER_DOMAIN
from xmpp import Server

if __name__ == "__main__":
    server = Server(SERVER_DOMAIN)
    server.wait_until_available()

    logger = ConsoleLogger()

    receiver = ReceiverAgent(
        f"receiver@{server.domain}",
        "password",
        logger=logger
    )
    future = receiver.start()
    future.result()  # wait for receiver agent to be prepared.
    sender = SenderAgent(
        f"sender@{server.domain}",
        "password",
        logger=logger
    )
    sender.start()

    while receiver.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            sender.stop()
            receiver.stop()
            break
    print("Agents finished")
    environment = Environment()

    drone1 = DroneController(environment, 0, 0)
    drone2 = DroneController(environment, 10, 10)

    animal1 = AnimalController(environment, 5, 5)
    animal2 = AnimalController(environment, 4, 4)

    print(drone1.detect_wild_animals(5))

    drone1.move(3, 3)

    print(drone1.detect_wild_animals(5))
