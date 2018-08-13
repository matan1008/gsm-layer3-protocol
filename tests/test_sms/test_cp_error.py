from gsm_layer3_protocol import parse, build
from gsm_layer3_protocol.l3_message import L3Message, protocol_discriminator
from gsm_layer3_protocol.sms import CpError, cp_cause, message_type


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
    assert build(L3Message(1, protocol_discriminator.SMS, CpError(cp_cause.NETWORK_FAILURE))) == b"\x19\x10\x11"
