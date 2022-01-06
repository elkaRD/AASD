from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, FSMBehaviour, State

from client.domain.controllers.drone_controller import DroneController

CHECK_BATTERY_STATUS_STATE = "CHECK_BATTERY_STATUS_STATE"
CHECK_AVAILABILITY_OF_CHARGERS_STATE = "CHECK_AVAILABILITY_OF_CHARGERS_STATE"
FLY_TO_STATION_STATE = "FLY_TO_STATION_STATE"
CHARGE_BATTERY_STATE = "CHARGE_BATTERY_STATE"
STATE_TWO = "STATE_TWO"
STATE_THREE = "STATE_THREE"
LOW_BATTERY_THRESHOLD = 10
CHARGED_BATTERY_THRESHOLD = 95


class PowerModuleAgent(Agent):

    def __init__(self, jid: str, password: str, controller: DroneController) -> None:
        super().__init__(jid, password)
        self.controller = controller

    def get_behaviours(self):
        return [
             self.ReceiveReportFromStation(self.controller),
             self.BatteryBehaviour(self.controller)
        ]

    async def setup(self):
        print("PowerModuleAgent started")
        for behaviour in self.get_behaviours():
            self.add_behaviour(behaviour)

    class ReceiveReportFromStation(CyclicBehaviour):
        def __init__(self, controller: DroneController) -> None:
            super().__init__()
            self.controller = controller

        async def run(self):
            # TODO add periodic checking for messages from base

            return NotImplemented

    class BatteryBehaviour(FSMBehaviour):
        def __init__(self, controller: DroneController) -> None:
            super().__init__()
            self.controller = controller
            self.add_state(name=CHECK_BATTERY_STATUS_STATE, state=self.CheckBatteryStatus(controller), initial=True)
            self.add_state(name=CHECK_AVAILABILITY_OF_CHARGERS_STATE, state=self.CheckAvailabilityOfChargers(controller))
            self.add_state(name=FLY_TO_STATION_STATE, state=self.FlyToStation(controller))
            self.add_state(name=CHARGE_BATTERY_STATE, state=self.ChargeBattery(controller))
            self.add_transition(source=CHECK_BATTERY_STATUS_STATE, dest=CHECK_BATTERY_STATUS_STATE)
            self.add_transition(source=CHECK_BATTERY_STATUS_STATE, dest=CHECK_AVAILABILITY_OF_CHARGERS_STATE)
            self.add_transition(source=CHECK_AVAILABILITY_OF_CHARGERS_STATE, dest=CHECK_AVAILABILITY_OF_CHARGERS_STATE)
            self.add_transition(source=CHECK_AVAILABILITY_OF_CHARGERS_STATE, dest=FLY_TO_STATION_STATE)
            self.add_transition(source=FLY_TO_STATION_STATE, dest=FLY_TO_STATION_STATE)
            self.add_transition(source=FLY_TO_STATION_STATE, dest=CHARGE_BATTERY_STATE)
            self.add_transition(source=CHARGE_BATTERY_STATE, dest=CHECK_BATTERY_STATUS_STATE)

        async def run(self):
            # TODO add periodic checking for messages from base

            return NotImplemented

        class CheckBatteryStatus(State):
            def __init__(self, controller: DroneController):
                super().__init__()
                self.controller = controller

            async def run(self):
                # TODO sleep then check battery status

                if self.controller.battery_status() > LOW_BATTERY_THRESHOLD:
                    self.set_next_state(CHECK_BATTERY_STATUS_STATE)
                else:
                    self.set_next_state(CHECK_AVAILABILITY_OF_CHARGERS_STATE)

        class CheckAvailabilityOfChargers(State):
            def __init__(self, controller: DroneController):
                super().__init__()
                self.controller = controller

            async def run(self):
                # TODO send request to base for available charger slots
                CHARGER_SLOTS_AVAILABLE = True
                if CHARGER_SLOTS_AVAILABLE:
                    self.set_next_state(FLY_TO_STATION_STATE)
                else:
                    # TODO sleep
                    self.set_next_state(CHECK_AVAILABILITY_OF_CHARGERS_STATE)

        class FlyToStation(State):
            def __init__(self, controller: DroneController):
                super().__init__()
                self.controller = controller

            async def run(self):
                # TODO move to station location, until you get there
                YOU_ARE_AT_STATION = True
                if YOU_ARE_AT_STATION:
                    self.set_next_state(CHARGE_BATTERY_STATE)
                else:
                    # TODO move
                    self.set_next_state(FLY_TO_STATION_STATE)

        class ChargeBattery(State):
            def __init__(self, controller: DroneController):
                super().__init__()
                self.controller = controller

            async def run(self):
                if self.controller.get_battery_status() > CHARGED_BATTERY_THRESHOLD:
                    self.set_next_state(CHECK_BATTERY_STATUS_STATE)
                else:
                    # TODO sleep
                    self.set_next_state(CHARGE_BATTERY_STATE)