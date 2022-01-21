from datetime import datetime

from messages import *

def test_help_request():
    message_body = HelpRequestBody(
        time=datetime(2022, 1, 1, 12, 0, 0),
        position=Coordinates(
            x= 10.0,
            y=20.0,
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
            x=-10.0,
            y=20.0,
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


def test_replying():
    message_body = HelpOfferBody(
        time=datetime(2022, 1, 1, 12, 0, 30),
        position=Coordinates(
            x=-10.0,
            y=20.0,
        ),
        eta=180.0,
    )
    message = message_body.make_message("recv3@localhost", "sender3@localhost")

    response_body = HelpResponseBody(help_accepted=True)
    response = response_body.make_response(message)

    assert str(response.to) == "sender3@localhost"
    assert str(response.sender) == "recv3@localhost"


def test_sector_cleared_report():
    message_body = SectorClearedReportBody(
        count=2,
        position=Coordinates(
            x=10,
            y=1,
        ),
        seconds_spent=120,
    )

    message = message_body.make_message("recv@localhost", "sender@localhost")

    assert str(message.to) == "recv@localhost"
    assert str(message.sender) == "sender@localhost"
    assert message.metadata == {
        "performative": "inform",
        'language': 'aasd_boarder_lang',
        'ontology': 'aasd_drones_boarder',
        "body_type": "SectorClearedReportBody",
    }
    
    after_deserialization = SectorClearedReportBody.parse_raw(message.body)
    assert message_body == after_deserialization


def test_sector_cleared_recieved():
    message_body = SectorClearedRecievedBody(
        accepted=True,
    )

    message = message_body.make_message("recv@localhost", "sender@localhost")

    assert str(message.to) == "recv@localhost"
    assert str(message.sender) == "sender@localhost"
    assert message.metadata == {
        "performative": "agree",
        'language': 'aasd_boarder_lang',
        'ontology': 'aasd_drones_boarder',
        "body_type": "SectorClearedRecievedBody",
    }
    
    after_deserialization = SectorClearedRecievedBody.parse_raw(message.body)
    assert message_body == after_deserialization


def test_searching_status():
    message_body = SearchingStatusBody(
        actual_position=Coordinates(x=2, y=3),
        searching_range_meters=10,
        boars_positions=[
            Coordinates(x=3, y=3),
            Coordinates(x=3, y=4),
            Coordinates(x=3, y=5),
        ],
        heading_towards=Coordinates(x=3, y=4.5),
    )
    message = message_body.make_message("recv@localhost", "sender@localhost")

    assert message.metadata == {
        "performative": "inform",
        'language': 'aasd_boarder_lang',
        'ontology': 'aasd_drones_boarder',
        "body_type": "SearchingStatusBody",
    }
    after_deserialization = SearchingStatusBody.parse_raw(message.body)
    assert message_body == after_deserialization
    assert len(after_deserialization.boars_positions) == 3


def test_searching_status_no_boars():
    message_body = SearchingStatusBody(
        actual_position=Coordinates(x=2, y=3),
        searching_range_meters=10,
        boars_positions=[],
        heading_towards=Coordinates(x=3, y=4.5),
    )
    message = message_body.make_message("recv@localhost", "sender@localhost")

    after_deserialization = SearchingStatusBody.parse_raw(message.body)
    assert message_body == after_deserialization
    assert len(after_deserialization.boars_positions) == 0


def test_searching_directives():
    message_body = SearchingDirectivesBody(
        keep_schedule=True,
    )
    message = message_body.make_message("recv@localhost", "sender@localhost")
    assert message.metadata == {
        "performative": "inform",
        'language': 'aasd_boarder_lang',
        'ontology': 'aasd_drones_boarder',
        "body_type": "SearchingDirectivesBody",
    }
    after_deserialization = SearchingDirectivesBody.parse_raw(message.body)
    assert after_deserialization.keep_schedule is True


def test_searching_directives_with_new_coords():
    message_body = SearchingDirectivesBody(
        keep_schedule=False,
        change_direction=Coordinates(x=20, y=10),
    )
    message = message_body.make_message("recv@localhost", "sender@localhost")
    assert message.metadata == {
        "performative": "inform",
        'language': 'aasd_boarder_lang',
        'ontology': 'aasd_drones_boarder',
        "body_type": "SearchingDirectivesBody",
    }
    after_deserialization = SearchingDirectivesBody.parse_raw(message.body)
    assert after_deserialization.keep_schedule is False
    assert after_deserialization.change_direction == Coordinates(x=20, y=10)


def test_dock_occupation_report():
    message_body = DockOccupationReportBody(
        total_docks=2,
        status=[
            Dock(occupied=False, number=0),
            Dock(
                occupied=True,
                number=1,
                occupied_by=Drone(id=2137),
            ),
        ]
    )
    message = message_body.make_message("recv@localhost", "sender@localhost")

    assert message.metadata == {
        "performative": "inform",
        'language': 'aasd_boarder_lang',
        'ontology': 'aasd_drones_boarder',
        "body_type": "DockOccupationReportBody",
    }
    after_deserialization = DockOccupationReportBody.parse_raw(message.body)
    assert message_body == after_deserialization


def test_charging_request():
    message_body = ChargingRequestBody(
        remaining_time_on_battery=100.3,
        distance_in_seconds=20.5,
    )
    message = message_body.make_message("recv@localhost", "sender@localhost")

    assert message.metadata == {
        "performative": "request",
        'language': 'aasd_boarder_lang',
        'ontology': 'aasd_drones_boarder',
        "body_type": "ChargingRequestBody",
    }
    after_deserialization = ChargingRequestBody.parse_raw(message.body)
    assert message_body == after_deserialization


def test_charging_response():
    message_body = ChargingResponseBody(
        charging_available=True,
        allocated_dock=Dock(occupied=False, number=1),
    )
    message = message_body.make_message("recv@localhost", "sender@localhost")

    assert message.metadata == {
        "performative": "agree",
        'language': 'aasd_boarder_lang',
        'ontology': 'aasd_drones_boarder',
        "body_type": "ChargingResponseBody",
    }
    after_deserialization = ChargingResponseBody.parse_raw(message.body)
    assert message_body == after_deserialization
