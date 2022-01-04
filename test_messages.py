from datetime import datetime

from messages import HelpRequestBody, HelpOfferBody, HelpResponseBody, Coordinates, UrgencyEnum

def test_help_request():
    message_body = HelpRequestBody(
        time=datetime(2022, 1, 1, 12, 0, 0),
        position=Coordinates(
            lat= 10.0,
            long=20.0,
        ),
        urgency=UrgencyEnum.LOW,
    )

    message = message_body.make_message("recv@localhost", "sender@localhost")

    assert str(message.to) == "recv@localhost"
    assert str(message.sender) == "sender@localhost"
    assert message.metadata == {
        "performative": "request",
        'language': 'aasd_boarder_lang',
        'ontology': 'aasd_drones_boarder',
        "body_type": "HelpRequestBody",
    }
    
    after_deserialization = HelpRequestBody.parse_raw(message.body)
    assert message_body == after_deserialization


def test_help_offer():
    message_body = HelpOfferBody(
        time=datetime(2022, 1, 1, 12, 0, 30),
        position=Coordinates(
            lat=-10.0,
            long=20.0,
        ),
        eta=180.0,
    )

    message = message_body.make_message("recv1@localhost", "sender1@localhost")

    assert str(message.to) == "recv1@localhost"
    assert str(message.sender) == "sender1@localhost"
    assert message.metadata == {
        "performative": "agree",
        'language': 'aasd_boarder_lang',
        'ontology': 'aasd_drones_boarder',
        "body_type": "HelpOfferBody",
    }
    
    after_deserialization = HelpOfferBody.parse_raw(message.body)
    assert message_body == after_deserialization


def test_help_offer_response():
    message_body = HelpResponseBody(
        help_accepted=True,
    )

    message = message_body.make_message("recv2@localhost", "sender2@localhost")

    assert str(message.to) == "recv2@localhost"
    assert str(message.sender) == "sender2@localhost"
    assert message.metadata == {
        "performative": "inform",
        'language': 'aasd_boarder_lang',
        'ontology': 'aasd_drones_boarder',
        "body_type": "HelpResponseBody",
    }
    
    after_deserialization = HelpResponseBody.parse_raw(message.body)
    assert message_body == after_deserialization
