import time

from agents.base_station import BaseStationAgent
from agents.server import ServerAgent
from domain.controllers.station import BaseStationController
from domain.environment import Environment
from loggers import ConsoleLogger
from properties import SERVER_DOMAIN
from xmpp import JIDGenerator, XMPPServer

if __name__ == "__main__":
    xmpp_server = XMPPServer(SERVER_DOMAIN)
    xmpp_server.wait_until_available()

    jid_generator = JIDGenerator(xmpp_server.domain)

    environment = Environment()
    controller = BaseStationController(environment)

    environment.add_drone(0.0, 0.0)
    environment.add_base_station_dock()

    logger = ConsoleLogger()

    server = ServerAgent(jid_generator.generate(), "password", logger)
    station = BaseStationAgent(
        jid_generator.generate(),
        "password",
        server.jid,
        [],
        controller,
        logger,
    )

    server.start().result()
    station.start()

    while server.is_alive():
        try:
            environment.step()
            time.sleep(1)
        except KeyboardInterrupt:
            server.stop()
            station.stop()
            break

    logger.log("Finished")
