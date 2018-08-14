from gsm_layer3_protocol import parse, build
from gsm_layer3_protocol.enums import protocol_discriminator, message_type, rp_mti
from gsm_layer3_protocol.l3_message import L3Message
from gsm_layer3_protocol.sms_protocol.cp_data import CpData
from gsm_layer3_protocol.sms_protocol.rp_ack import RpAck


def test_parsing_rp_ack_to_n():
    assert parse(b"\x29\x01\x02\x02\x04") == {
        "transaction_identifier": 2,
        "protocol_discriminator": protocol_discriminator.SMS,
        "l3_protocol": {
            "message_type": message_type.CP_DATA,
            "cp_layer_protocol": {
                "length_indicator": 2,
                "spare": None,
                "mti": rp_mti.RP_ACK_MS_TO_N,
                "rp": {"message_reference": 4}
            }
        }
    }


def test_building_rp_ack_to_n():
    assert build(
        L3Message(3, protocol_discriminator.SMS, CpData(rp_mti.RP_ACK_MS_TO_N, RpAck(1)))) == b"\x39\x01\x02\x02\x01"
