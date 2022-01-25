import time
import threading

from pythonosc.udp_client import SimpleUDPClient

from domain.environment import AbstractEnvironment


SLEEP_FOR = 1
ADDRS = "host.docker.internal"
PORT = 1337


class OSCClientThread(threading.Thread):
    def __init__(self, env: AbstractEnvironment) -> None:
        threading.Thread.__init__(self)
        self.running = False
        self.env = env
        self.client = SimpleUDPClient(ADDRS, PORT)
    
    def run(self) -> None:
        while True:
            self.send_data()
            time.sleep(SLEEP_FOR)

    def send_data(self):
        drones_positions = self.env.get_drones_positions_list()
        animals_positions = self.env.get_animals_positions_list()
        for i, drone in enumerate(drones_positions):
            self.client.send_message(f"/drone/{i}/pos", list(drone))
        for i, animal in enumerate(animals_positions):
            self.client.send_message(f"/animal/{i}/pos", list(animal))
