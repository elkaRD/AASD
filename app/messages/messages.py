import json
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

from aioxmpp import JID
from spade.message import Message as SpadeMessage

from utils import BaseModel, Typable

ONTOLOGY = "aasd_drones_boarder"
LANGUAGE = "JSON"


class Coordinates(BaseModel):
    x: float
    y: float


class UrgencyEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Drone(BaseModel):
    id: int


class Dock(BaseModel):
    occupied: bool
    number: int
    occupied_by: Optional[Drone]


class MessageBody(BaseModel, Typable):
    @classmethod
    def parse(cls, message: SpadeMessage):
        subclass = cls.for_type(message.metadata["type"])
        params = json.loads(message.body)
        return subclass.__call__(**params)

    def make_message(
        self, to: Union[str, JID], sender: Union[str, JID]
    ) -> SpadeMessage:
        return SpadeMessage(
            to=str(to),
            sender=str(sender),
            body=self.json(),
            metadata=self.metadata(),
        )

    def make_response(self, message: SpadeMessage) -> SpadeMessage:
        return self.make_message(
            to=str(message.sender), sender=str(message.to)
        )

    @classmethod
    @abstractmethod
    def performative(cls) -> str:
        pass

    @classmethod
    def type(cls) -> str:
        return cls.__name__

    @classmethod
    def metadata(cls) -> Dict[str, str]:
        return {
            "ontology": ONTOLOGY,
            "language": LANGUAGE,
            "performative": cls.performative(),
            "type": cls.type(),
        }


# Pierwszy diagram kolaboracji


class HelpRequestBody(MessageBody):
    """Prośba o pomoc"""

    time: datetime
    position: Coordinates
    urgency: UrgencyEnum

    @classmethod
    def performative(cls) -> str:
        return "request"


class HelpOfferBody(MessageBody):
    """Propozycja pomocy"""

    time: datetime
    position: Coordinates
    eta: float

    @classmethod
    def performative(cls) -> str:
        return "agree"


class HelpResponseBody(MessageBody):
    """Zaakceptowanie lub odrzucenie pomocy"""

    help_accepted: bool

    @classmethod
    def performative(cls) -> str:
        return "inform"


# Drugi diagram kolaboracji


class SectorClearedReportBody(MessageBody):
    """Powiadomienie o przegonieniu zwierząt"""

    count: int
    position: Coordinates
    seconds_spent: float

    @classmethod
    def performative(cls) -> str:
        return "inform"


class SectorClearedRecievedBody(MessageBody):
    """Powiadomienie o odebraniu raportu"""

    accepted: bool

    @classmethod
    def performative(cls) -> str:
        return "agree"


# Trzeci diagram kolaboracji


class SearchingStatusBody(MessageBody):
    """Powiadomienie o stanie przeszukiwania"""

    actual_position: Coordinates
    searching_range_meters: float
    boars_positions: List[Coordinates]
    heading_towards: Coordinates

    @classmethod
    def performative(cls) -> str:
        return "inform"


class SearchingDirectivesBody(MessageBody):
    """Powiadomienie o odebraniu raportu"""

    keep_schedule: bool
    change_direction: Optional[Coordinates]

    @classmethod
    def performative(cls) -> str:
        return "inform"


# Czwarty i piąty diagram kolaboracji


class DockOccupationReportBody(MessageBody):
    """Powiadomienie o zmianie zajętości stacji dokującej"""

    total_docks: int
    status: List[Dock]

    @classmethod
    def performative(cls) -> str:
        return "inform"


# Szósty diagram kolaboracji


class ChargingRequestBody(MessageBody):
    """Powiadomienie o chęci ładowania"""

    remaining_time_on_battery: float
    distance_in_seconds: float

    @classmethod
    def performative(cls) -> str:
        return "request"


class ChargingResponseBody(MessageBody):
    """Powiadomienie o dostępnym miejscu do ładowania"""

    charging_available: bool
    allocated_dock: Optional[Dock]

    @classmethod
    def performative(cls) -> str:
        return "agree"
