import time

from agents.base_station import BaseStationAgent
from agents.server import ServerAgent
from domain.controllers.drone_controller import DroneController
from domain.environment import Environment
from loggers import ConsoleLogger
from properties import SERVER_DOMAIN
from utils import JIDGenerator
from xmpp import Server

if __name__ == "__main__":
    xmpp_server = Server(SERVER_DOMAIN)
    xmpp_server.wait_until_available()

    jid_generator = JIDGenerator(xmpp_server.domain)

    environment = Environment()
    controller = DroneController(environment, 0, 0)

    logger = ConsoleLogger()

    server = ServerAgent(
        jid_generator.generate(), "password", logger
    )
    station = BaseStationAgent(
        jid_generator.generate(), "password", server.jid, controller, logger
    )

    server.start().result()
    station.start()

    while server.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            server.stop()
            station.stop()
            break

    logger.log("Finished")
