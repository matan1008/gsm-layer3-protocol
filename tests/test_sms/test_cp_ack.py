from gsm_layer3_protocol import parse, build
from gsm_layer3_protocol.l3_message import L3Message, protocol_discriminator
from gsm_layer3_protocol.sms import CpAck, message_type


def test_parsing_cp_ack():
    assert parse(b"\x29\x04") == {
        "transaction_identifier": 2,
        "protocol_discriminator": protocol_discriminator.SMS,
        "l3_protocol": {
            "message_type": message_type.CP_ACK
        }
    }


def test_building_cp_ack():
    assert build(L3Message(1, protocol_discriminator.SMS, CpAck())) == b"\x19\x04"
