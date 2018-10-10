from gsm_layer3_protocol import parse, build
from gsm_layer3_protocol.enums import *
from gsm_layer3_protocol.l3_message import L3Message
from gsm_layer3_protocol.sms_protocol.cp_data import CpData
from gsm_layer3_protocol.sms_protocol.rp_ack import RpAck
from gsm_layer3_protocol.sms_protocol.sms_submit_report_rp_ack import \
    RpAckSmsSubmitReport
from gsm_layer3_protocol.sms_protocol.sms_deliver_report_rp_ack import \
    RpAckSmsDeliverReport
from gsm_layer3_protocol.sms_protocol.tp_user_data import TpUserData, \
    TpUserDataHeader, TpUserDataHeaderElement
from gsm_layer3_protocol.sms_protocol.tpdu_parameters import TpScts, \
    TpDcsGeneralDataCodingIndicationNoMessageClass


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
                "rp": {"message_reference": 4, "rp_user_data": None}
            }
        }
    }


def test_building_rp_ack_to_n():
    assert build(
        L3Message(
            3,
            protocol_discriminator.SMS,
            CpData(rp_mti.RP_ACK_MS_TO_N, RpAck(1))
        )
    ) == b"\x39\x01\x02\x02\x01"


def test_parsing_rp_ack_to_ms():
    assert parse(b"\x29\x01\x02\x03\x04") == {
        "transaction_identifier": 2,
        "protocol_discriminator": protocol_discriminator.SMS,
        "l3_protocol": {
            "message_type": message_type.CP_DATA,
            "cp_layer_protocol": {
                "length_indicator": 2,
                "spare": None,
                "mti": rp_mti.RP_ACK_N_TO_MS,
                "rp": {"message_reference": 4, "rp_user_data": None}
            }
        }
    }


def test_building_rp_ack_to_ms():
    assert build(L3Message(
        3,
        protocol_discriminator.SMS,
        CpData(rp_mti.RP_ACK_N_TO_MS, RpAck(1))
    )) == b"\x39\x01\x02\x03\x01"


def test_parsing_rp_ack_with_short_rp_user_data_deliver():
    assert parse(b"\x29\x01\x06\x02\x04\x41\x02\x00\x00") == {
        "transaction_identifier": 2,
        "protocol_discriminator": protocol_discriminator.SMS,
        "l3_protocol": {
            "message_type": message_type.CP_DATA,
            "cp_layer_protocol": {
                "length_indicator": 6,
                "spare": None,
                "mti": rp_mti.RP_ACK_MS_TO_N,
                "rp": {
                    "message_reference": 4,
                    "rp_user_data": {
                        "rp_user_data_iei": 0x41,
                        "tpdu": {
                            "tp_udhi": False,
                            "tp_mti": tp_mti.SMS_DELIVER_OR_REPORT,
                            "tp_pi": {
                                "tp_udl": False,
                                "tp_dcs": False,
                                "tp_pid": False
                            },
                            "tp_scts": None,
                            "tp_dcs": None,
                            "tp_pid": None,
                            "tp_ud": None,
                        }
                    }
                }
            }
        }
    }


def test_building_rp_ack_with_short_rp_user_data_deliver():
    assert build(L3Message(
        3,
        protocol_discriminator.SMS,
        CpData(
            rp_mti.RP_ACK_MS_TO_N,
            RpAck(1, RpAckSmsDeliverReport())
        )
    )) == b"\x39\x01\x06\x02\x01\x41\x02\x00\x00"


def test_parsing_rp_ack_with_short_rp_user_data_submit():
    assert parse(b"\x29\x01\x0d\x03\x04\x41\x09\x01\x00\x81\x90\x10\x32\x60"
                 b"\x00\x8a") == {
               "transaction_identifier": 2,
               "protocol_discriminator": protocol_discriminator.SMS,
               "l3_protocol": {
                   "message_type": message_type.CP_DATA,
                   "cp_layer_protocol": {
                       "length_indicator": 2,
                       "spare": None,
                       "mti": rp_mti.RP_ACK_N_TO_MS,
                       "rp": {
                           "message_reference": 4,
                           "rp_user_data": {
                               "rp_user_data_iei": 0x41,
                               "tpdu": {
                                   "tp_udhi": False,
                                   "tp_mti": tp_mti.SMS_SUBMIT_OR_REPORT,
                                   "tp_pi": {
                                       "tp_udl": False,
                                       "tp_dcs": False,
                                       "tp_pid": False
                                   },
                                   "tp_scts": {
                                       "year": 18,
                                       "month": 9,
                                       "day": 1,
                                       "hour": 23,
                                       "minute": 6,
                                       "second": 0,
                                       "gmt": -7
                                   },
                                   "tp_dcs": None,
                                   "tp_pid": None,
                                   "tp_ud": None,
                               }
                           }
                       }
                   }
               }
           }


def test_building_rp_ack_with_short_rp_user_data_submit():
    assert build(L3Message(
        3,
        protocol_discriminator.SMS,
        CpData(
            rp_mti.RP_ACK_N_TO_MS,
            RpAck(1, RpAckSmsSubmitReport(TpScts(18, 9, 1, 23, 6, 0, 2)))
        )
    )) == b"\x39\x01\x0d\x03\x01\x41\x09\x01\x00\x81\x90\x10\x32\x60\x00\x80"


def test_parsing_rp_ack_full():
    assert parse(
        b"\x29\x01\x1b\x02\x04\x41\x17\x40\x07\x20\x15\x12\x04\x01\x02"
        b"\xff\xff\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d") == {
               "transaction_identifier": 2,
               "protocol_discriminator": protocol_discriminator.SMS,
               "l3_protocol": {
                   "message_type": message_type.CP_DATA,
                   "cp_layer_protocol": {
                       "length_indicator": 2,
                       "spare": None,
                       "mti": rp_mti.RP_ACK_MS_TO_N,
                       "rp": {
                           "message_reference": 4,
                           "rp_user_data": {
                               "rp_user_data_iei": 0x41,
                               "tpdu": {
                                   "tp_udhi": True,
                                   "tp_mti": tp_mti.SMS_DELIVER_OR_REPORT,
                                   "tp_pi": {
                                       "tp_udl": True,
                                       "tp_dcs": True,
                                       "tp_pid": True
                                   },
                                   "tp_pid": tp_pid.IMPLICIT,
                                   "tp_dcs": {
                                       "coding_group": dcs_coding_groups.GENERAL_DATA_CODING_INDICATION,
                                       "compressed": False,
                                       "character_set": dcs_character_set.DATA_8BIT,
                                       "message_class": 1
                                   },
                                   "tp_ud": {
                                       "user_data_header": [
                                           {
                                               "element_type": tp_udh_elements.SPECIAL_SMS_MESSAGE,
                                               "element_data": b"\xff\xff"}
                                       ],
                                       "user_data": (b"\x01\x02\x03\x04\x05"
                                                     b"\x06\x07\x08\x09\x0a"
                                                     b"\x0b\x0c\x0d")
                                   }
                               }
                           }
                       }
                   }
               }
           }


def test_building_rp_ack_full():
    a = build(L3Message(
        3,
        protocol_discriminator.SMS,
        CpData(rp_mti.RP_ACK_MS_TO_N, RpAck(
            1,
            RpAckSmsDeliverReport(
                tp_pid.X_400_BASED,
                TpDcsGeneralDataCodingIndicationNoMessageClass(),
                TpUserData(
                    "This is Part 1.",
                    TpUserDataHeader(
                        TpUserDataHeaderElement(
                            tp_udh_elements.CONCATENATED_SHORT_MESSAGES_8_BIT,
                            b"\x03\x02\x01"
                        )
                    )
                )
            )
        ))
    ))
    assert a == (b"\x39\x01\x1d\x02\x01\x41\x19\x40\x07\x31\x00\x16\x05\x00"
                 b"\x03\x03\x02\x01\xa8\xe8\xf4\x1c\x94\x9e\x83\xa0\x61\x39"
                 b"\x1d\x14\x73\x01")
