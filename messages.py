from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from spade.message import Message


ONTOLOGY = "aasd_drones_boarder"
LANGUAGE = "aasd_boarder_lang"


def set_default_metadata(msg: Message) -> None:
    msg.set_metadata("ontology", ONTOLOGY)
    msg.set_metadata("language", LANGUAGE)


class MessageBase(BaseModel):
    def make_message(self, to: str, sender: str) -> Message:
        pass


class Coordinates(BaseModel):
    lat: float
    long: float


class UrgencyEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class HelpRequestBody(MessageBase):
    time: datetime
    position: Coordinates
    urgency: UrgencyEnum

    def make_message(self, to: str, sender: str) -> Message:
        message = Message(to=to, sender=sender)
        message.set_metadata("performative", "request")
        set_default_metadata(message)
        message.body = self.json()

        return message


class HelpOfferBody(MessageBase):
    time: datetime
    position: Coordinates
    eta: float

    def make_message(self, to: str, sender: str) -> Message:
        message = Message(to=to, sender=sender)
        message.set_metadata("performative", "agree")
        set_default_metadata(message)
        message.body = self.json()

        return message


class HelpOfferResponse(MessageBase):
    help_accepted: bool

    def make_message(self, to: str, sender: str) -> Message:
        message = Message(to=to, sender=sender)
        message.set_metadata("performative", "inform")
        set_default_metadata(message)
        message.body = self.json()

        return message
