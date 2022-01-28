import os
import time

from agents.base_station import BaseStationAgent
from agents.coordinator import CoordinatorAgent
from agents.power_module import PowerModuleAgent
from agents.scout import ScoutAgent
from agents.server import ServerAgent
from domain.controllers.drone import DroneController
from domain.controllers.station import BaseStationController
from domain.environment import Environment
from domain.osc_client import OSCClientThread
from loggers import ConsoleLogger
from properties import SERVER_DOMAIN
from xmpp import JIDGenerator, XMPPServer

if __name__ == "__main__":
    xmpp_server = XMPPServer(SERVER_DOMAIN)
    xmpp_server.wait_until_available()

    jid_generator = JIDGenerator(xmpp_server.domain)

    environment = Environment()

    if os.getenv("BOARDER_VISUALIZATION"):
        osc_client = OSCClientThread(environment)
        osc_client.start()

    drone_id = environment.add_drone(5.0, 5.0)
    environment.add_animal(1.0, 1.0)
    environment.add_animal(7.0, 8.0)
    environment.add_animal(9.0, 9.0)
    environment.add_base_station_dock()

    drone_controller = DroneController(environment, drone_id)
    base_station_controller = BaseStationController(environment)

    logger = ConsoleLogger()

    server_jid = jid_generator.generate()
    base_station_jid = jid_generator.generate()
    power_module_jid = jid_generator.generate()
    coordinator_jid = jid_generator.generate()
    scout_jid = jid_generator.generate()

    agents = [
        ServerAgent(server_jid, "password", logger),
        BaseStationAgent(
            base_station_jid,
            "password",
            server_jid,
            [],
            base_station_controller,
            logger,
        ),
        PowerModuleAgent(
            power_module_jid, "password", drone_controller, logger
        ),
        CoordinatorAgent(
            coordinator_jid, "password", drone_controller, logger
        ),
        ScoutAgent(
            scout_jid, coordinator_jid, "password", drone_controller, logger
        ),
    ]

    for agent in agents:
        agent.start().result()

    while True:
        try:
            environment.step()
            time.sleep(0.1)
        except KeyboardInterrupt:
            for agent in agents:
                agent.stop()
            break

    logger.log("Finished")
