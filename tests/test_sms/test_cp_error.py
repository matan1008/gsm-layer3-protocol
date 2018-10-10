from gsm_layer3_protocol import parse, build
from gsm_layer3_protocol.enums import protocol_discriminator, message_type, \
    cp_cause
from gsm_layer3_protocol.l3_message import L3Message
from gsm_layer3_protocol.sms_protocol.cp_error import CpError


def test_parsing_cp_error():
    assert parse(b"\x29\x10\x51") == {
        "transaction_identifier": 2,
        "protocol_discriminator": protocol_discriminator.SMS,
        "l3_protocol": {
            "message_type": message_type.CP_ERROR,
            "cp_layer_protocol": {
                "cp_cause": cp_cause.INVALID_TID
            }
        }
    }


def test_building_cp_error():
    assert build(L3Message(1, protocol_discriminator.SMS, CpError(
        cp_cause.NETWORK_FAILURE))) == b"\x19\x10\x11"
