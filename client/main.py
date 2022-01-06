import time

from client.agents.example import ReceiverAgent, SenderAgent
from client.properties import SERVER_HOST
from domain.controllers.animal_controller import AnimalController
from domain.controllers.drone_controller import DroneController
from domain.environment import Environment


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
    environment = Environment()

    drone1 = DroneController(environment, 0, 0)
    drone2 = DroneController(environment, 10, 10)

    animal1 = AnimalController(environment, 5, 5)
    animal2 = AnimalController(environment, 4, 4)

    print(drone1.detect_wild_animals(5))

    drone1.move(3, 3)

    print(drone1.detect_wild_animals(5))
