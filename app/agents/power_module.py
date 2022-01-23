from typing import Iterator, Union

from aioxmpp import JID

from agents.agent import Agent, Behaviour, CyclicBehaviour, FSMBehaviour, State
from domain.controllers.drone import DroneController
from loggers import Logger, NullLogger

CHECK_BATTERY_STATUS_STATE = "CHECK_BATTERY_STATUS_STATE"
CHECK_AVAILABILITY_OF_CHARGERS_STATE = "CHECK_AVAILABILITY_OF_CHARGERS_STATE"
FLY_TO_STATION_STATE = "FLY_TO_STATION_STATE"
CHARGE_BATTERY_STATE = "CHARGE_BATTERY_STATE"
STATE_TWO = "STATE_TWO"
STATE_THREE = "STATE_THREE"
LOW_BATTERY_THRESHOLD = 10
CHARGED_BATTERY_THRESHOLD = 95


class PowerModuleAgent(Agent):
    def __init__(
        self,
        jid: Union[str, JID],
        password: str,
        controller: DroneController,
        logger: Logger = NullLogger(),
    ) -> None:
        super().__init__(jid, password, logger)
        self.controller = controller

    def get_behaviours(self) -> Iterator[Behaviour]:
        return [
            self.ReceiveReportFromStation(
                self.get_jid(), self.controller, self.get_logger()
            ),
            self.BatteryBehaviour(self.get_jid(), self.controller, self.get_logger()),
        ]

    class ReceiveReportFromStation(CyclicBehaviour):
        def __init__(
            self, jid: JID, controller: DroneController, logger: Logger
        ) -> None:
            super().__init__(jid, logger)
            self.controller = controller

        async def run(self) -> None:
            # TODO add periodic checking for messages from base
            return NotImplemented

    class BatteryBehaviour(FSMBehaviour):
        def __init__(
            self, jid: JID, controller: DroneController, logger: Logger
        ) -> None:
            super().__init__(jid, logger)
            self.controller = controller
            self.add_state(
                name=CHECK_BATTERY_STATUS_STATE,
                state=self.CheckBatteryStatus(
                    self.get_jid(), controller, self.get_logger()
                ),
                initial=True,
            )
            self.add_state(
                name=CHECK_AVAILABILITY_OF_CHARGERS_STATE,
                state=self.CheckAvailabilityOfChargers(
                    self.get_jid(), controller, self.get_logger()
                ),
            )
            self.add_state(
                name=FLY_TO_STATION_STATE,
                state=self.FlyToStation(self.get_jid(), controller, self.get_logger()),
            )
            self.add_state(
                name=CHARGE_BATTERY_STATE,
                state=self.ChargeBattery(self.get_jid(), controller, self.get_logger()),
            )
            self.add_transition(
                source=CHECK_BATTERY_STATUS_STATE, dest=CHECK_BATTERY_STATUS_STATE
            )
            self.add_transition(
                source=CHECK_BATTERY_STATUS_STATE,
                dest=CHECK_AVAILABILITY_OF_CHARGERS_STATE,
            )
            self.add_transition(
                source=CHECK_AVAILABILITY_OF_CHARGERS_STATE,
                dest=CHECK_AVAILABILITY_OF_CHARGERS_STATE,
            )
            self.add_transition(
                source=CHECK_AVAILABILITY_OF_CHARGERS_STATE, dest=FLY_TO_STATION_STATE
            )
            self.add_transition(source=FLY_TO_STATION_STATE, dest=FLY_TO_STATION_STATE)
            self.add_transition(source=FLY_TO_STATION_STATE, dest=CHARGE_BATTERY_STATE)
            self.add_transition(
                source=CHARGE_BATTERY_STATE, dest=CHECK_BATTERY_STATUS_STATE
            )

        async def run(self) -> None:
            # TODO add periodic checking for messages from base
            return NotImplemented

        class CheckBatteryStatus(State):
            def __init__(self, jid: JID, controller: DroneController, logger: Logger):
                super().__init__(jid, logger)
                self.controller = controller

            async def run(self) -> None:
                # TODO sleep then check battery status
                if self.controller.get_battery_status() > LOW_BATTERY_THRESHOLD:
                    self.set_next_state(CHECK_BATTERY_STATUS_STATE)
                else:
                    self.set_next_state(CHECK_AVAILABILITY_OF_CHARGERS_STATE)

        class CheckAvailabilityOfChargers(State):
            def __init__(self, jid: JID, controller: DroneController, logger: Logger):
                super().__init__(jid, logger)
                self.controller = controller

            async def run(self) -> None:
                # TODO send request to base for available charger slots
                CHARGER_SLOTS_AVAILABLE = True
                if CHARGER_SLOTS_AVAILABLE:
                    self.set_next_state(FLY_TO_STATION_STATE)
                else:
                    # TODO sleep
                    self.set_next_state(CHECK_AVAILABILITY_OF_CHARGERS_STATE)

        class FlyToStation(State):
            def __init__(self, jid: JID, controller: DroneController, logger: Logger):
                super().__init__(jid, logger)
                self.controller = controller

            async def run(self) -> None:
                # TODO move to station location, until you get there
                YOU_ARE_AT_STATION = True
                if YOU_ARE_AT_STATION:
                    self.set_next_state(CHARGE_BATTERY_STATE)
                else:
                    # TODO move
                    self.set_next_state(FLY_TO_STATION_STATE)

        class ChargeBattery(State):
            def __init__(self, jid: JID, controller: DroneController, logger: Logger):
                super().__init__(jid, logger)
                self.controller = controller

            async def run(self) -> None:
                if self.controller.get_battery_status() > CHARGED_BATTERY_THRESHOLD:
                    self.set_next_state(CHECK_BATTERY_STATUS_STATE)
                else:
                    # TODO sleep
                    self.set_next_state(CHARGE_BATTERY_STATE)
