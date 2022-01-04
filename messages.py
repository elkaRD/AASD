from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
from spade.message import Message


ONTOLOGY = "aasd_drones_boarder"
LANGUAGE = "aasd_boarder_lang"


class MessageBase(BaseModel):
    def make_message(self, to: str, sender: str) -> Message:
        message = Message(to=to, sender=sender)
        self.set_default_metadata(message)
        message.body = self.json()
        return message

    def make_response(self, message: Message) -> Message:
        return self.make_message(to=str(message.sender), sender=str(message.to))
    
    def set_default_metadata(self, msg: Message) -> None:
        msg.set_metadata("ontology", ONTOLOGY)
        msg.set_metadata("language", LANGUAGE)
        msg.set_metadata("body_type", self.__class__.__name__)

class Coordinates(BaseModel):
    lat: float
    long: float


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


class HelpRequestBody(MessageBase):  # Prośba o pomoc
    time: datetime
    position: Coordinates
    urgency: UrgencyEnum

    def make_message(self, to: str, sender: str) -> Message:
        message = super().make_message(to, sender)
        message.set_metadata("performative", "request")

        return message


class HelpOfferBody(MessageBase):  # Propozycja pomocy
    time: datetime
    position: Coordinates
    eta: float

    def make_message(self, to: str, sender: str) -> Message:
        message = super().make_message(to, sender)
        message.set_metadata("performative", "agree")

        return message


class HelpResponseBody(MessageBase):  # Zaakceptowanie lub odrzucenie pomocy
    help_accepted: bool

    def make_message(self, to: str, sender: str) -> Message:
        message = super().make_message(to, sender)
        message.set_metadata("performative", "inform")

        return message


# Drugi diagram kolaboracji


class SectorClearedReportBody(MessageBase):  # Powiadomienie o przegonieniu zwierząt
    count: int
    position: Coordinates
    seconds_spent: float

    def make_message(self, to: str, sender: str) -> Message:
        message = super().make_message(to, sender)
        message.set_metadata("performative", "inform")

        return message


class SectorClearedRecievedBody(MessageBase):  # Powiadomienie o odebraniu raportu
    accepted: bool

    def make_message(self, to: str, sender: str) -> Message:
        message = super().make_message(to, sender)
        message.set_metadata("performative", "agree")

        return message


# Trzeci diagram kolaboracji


class SearchingStatusBody(MessageBase):  # Powiadomienie o stanie przeszukiwania
    actual_position: Coordinates
    searching_range_meters: float
    boars_positions: List[Coordinates]
    heading_towards: Coordinates

    def make_message(self, to: str, sender: str) -> Message:
        message = super().make_message(to, sender)
        message.set_metadata("performative", "inform")

        return message


class SearchingDirectivesBody(MessageBase):  # Powiadomienie o odebraniu raportu
    keep_schedule: bool
    change_direction: Optional[Coordinates]

    def make_message(self, to: str, sender: str) -> Message:
        message = super().make_message(to, sender)
        message.set_metadata("performative", "inform")

        return message


# Czwarty i piąty diagram kolaboracji


class DockOccupationReportBody(MessageBase):  # Powiadomienie o zmianie zajętości stacji dokującej
    total_docks: int
    status: List[Dock]

    def make_message(self, to: str, sender: str) -> Message:
        message = super().make_message(to, sender)
        message.set_metadata("performative", "inform")

        return message


# Szósty diagram kolaboracji

class ChargingRequestBody(MessageBase):  # Powiadomienie o chęci ładowania
    remaining_time_on_battery: float
    distance_in_seconds: float

    def make_message(self, to: str, sender: str) -> Message:
        message = super().make_message(to, sender)
        message.set_metadata("performative", "request")

        return message


class ChargingResponseBody(MessageBase):  # Powiadomienie o dostępnym miejscu do ładowania
    charging_available: bool
    allocated_dock: Optional[Dock]

    def make_message(self, to: str, sender: str) -> Message:
        message = super().make_message(to, sender)
        message.set_metadata("performative", "agree")

        return message
