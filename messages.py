from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from spade.message import Message


ONTOLOGY = "aasd_drones_boarder"
LANGUAGE = "aasd_boarder_lang"


class MessageBase(BaseModel):
    def make_message(self, to: str, sender: str) -> Message:
        pass

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


class HelpRequestBody(MessageBase):
    time: datetime
    position: Coordinates
    urgency: UrgencyEnum

    def make_message(self, to: str, sender: str) -> Message:
        message = Message(to=to, sender=sender)
        message.set_metadata("performative", "request")
        self.set_default_metadata(message)
        message.body = self.json()

        return message


class HelpOfferBody(MessageBase):
    time: datetime
    position: Coordinates
    eta: float

    def make_message(self, to: str, sender: str) -> Message:
        message = Message(to=to, sender=sender)
        message.set_metadata("performative", "agree")
        self.set_default_metadata(message)
        message.body = self.json()

        return message


class HelpResponseBody(MessageBase):
    help_accepted: bool

    def make_message(self, to: str, sender: str) -> Message:
        message = Message(to=to, sender=sender)
        message.set_metadata("performative", "inform")
        self.set_default_metadata(message)
        message.body = self.json()

        return message
