from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel
from spade.message import Message

ONTOLOGY = "aasd_drones_boarder"
LANGUAGE = "JSON"


class MessageBase(BaseModel):
    def make_message(self, to: str, sender: str) -> Message:
        return Message(
            to=to,
            sender=sender,
            body=self.json(),
            metadata=self.metadata
        )

    def make_response(self, message: Message) -> Message:
        return self.make_message(
            to=str(message.sender),
            sender=str(message.to)
        )

    @property
    @abstractmethod
    def performative(self) -> str:
        pass

    @property
    def metadata(self) -> Dict[str, str]:
        return {
            "ontology"    : ONTOLOGY,
            "language"    : LANGUAGE,
            "performative": self.performative,
            "body_type"   : self.__class__.__name__
        }


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


# Pierwszy diagram kolaboracji


class HelpRequestBody(MessageBase):
    """Prośba o pomoc"""

    time: datetime
    position: Coordinates
    urgency: UrgencyEnum

    @property
    def performative(self) -> str:
        return "request"


class HelpOfferBody(MessageBase):
    """Propozycja pomocy"""

    time: datetime
    position: Coordinates
    eta: float

    @property
    def performative(self) -> str:
        return "agree"


class HelpResponseBody(MessageBase):
    """Zaakceptowanie lub odrzucenie pomocy"""

    help_accepted: bool

    @property
    def performative(self) -> str:
        return "inform"


# Drugi diagram kolaboracji


class SectorClearedReportBody(MessageBase):
    """Powiadomienie o przegonieniu zwierząt"""

    count: int
    position: Coordinates
    seconds_spent: float

    @property
    def performative(self) -> str:
        return "inform"


class SectorClearedRecievedBody(MessageBase):
    """Powiadomienie o odebraniu raportu"""

    accepted: bool

    @property
    def performative(self) -> str:
        return "agree"


# Trzeci diagram kolaboracji


class SearchingStatusBody(MessageBase):
    """Powiadomienie o stanie przeszukiwania"""

    actual_position: Coordinates
    searching_range_meters: float
    boars_positions: List[Coordinates]
    heading_towards: Coordinates

    @property
    def performative(self) -> str:
        return "inform"


class SearchingDirectivesBody(MessageBase):
    """Powiadomienie o odebraniu raportu"""

    keep_schedule: bool
    change_direction: Optional[Coordinates]

    @property
    def performative(self) -> str:
        return "inform"


# Czwarty i piąty diagram kolaboracji


class DockOccupationReportBody(MessageBase):
    """Powiadomienie o zmianie zajętości stacji dokującej"""

    total_docks: int
    status: List[Dock]

    @property
    def performative(self) -> str:
        return "inform"


# Szósty diagram kolaboracji

class ChargingRequestBody(MessageBase):
    """Powiadomienie o chęci ładowania"""

    remaining_time_on_battery: float
    distance_in_seconds: float

    @property
    def performative(self) -> str:
        return "request"


class ChargingResponseBody(MessageBase):
    """Powiadomienie o dostępnym miejscu do ładowania"""

    charging_available: bool
    allocated_dock: Optional[Dock]

    @property
    def performative(self) -> str:
        return "agree"
