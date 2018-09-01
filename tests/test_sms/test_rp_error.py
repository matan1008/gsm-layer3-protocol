from gsm_layer3_protocol import parse, build
from gsm_layer3_protocol.enums import *
from gsm_layer3_protocol.l3_message import L3Message
from gsm_layer3_protocol.sms_protocol.cp_data import CpData
from gsm_layer3_protocol.sms_protocol.rp_error import RpError
from gsm_layer3_protocol.sms_protocol.rp_cause import RpCause
from gsm_layer3_protocol.sms_protocol.sms_deliver_report import RpErrorSmsDeliverReport
from gsm_layer3_protocol.sms_protocol.tp_user_data import TpUserData, TpUserDataHeader, TpUserDataHeaderElement


def test_parsing_minimal_rp_error():
    assert parse(b"\x29\x01\x04\x05\x04\x01\x29") == {
        "transaction_identifier": 2,
        "protocol_discriminator": protocol_discriminator.SMS,
        "l3_protocol": {
            "message_type": message_type.CP_DATA,
            "cp_layer_protocol": {
                "length_indicator": 2,
                "spare": None,
                "mti": rp_mti.RP_ERROR_N_TO_MS,
                "rp": {
                    "message_reference": 4,
                    "rp_cause": {
                        "ext": None,
                        "cause_value": rp_cause.TEMPORARY_FAILIURE,
                        "diagnostic_field": None
                    },
                    "rp_user_data": None
                }
            }
        }
    }


def test_building_minimal_rp_error():
    assert build(L3Message(
        3,
        protocol_discriminator.SMS,
        CpData(rp_mti.RP_ERROR_MS_TO_N, RpError(1, rp_cause.INTERWORKING))
    )) == b"\x39\x01\x04\x04\x01\x01\x7f"


def test_parsing_rp_error_with_diagnostic_field():
    assert parse(b"\x29\x01\x05\x05\x04\x02\x01\x80") == {
        "transaction_identifier": 2,
        "protocol_discriminator": protocol_discriminator.SMS,
        "l3_protocol": {
            "message_type": message_type.CP_DATA,
            "cp_layer_protocol": {
                "length_indicator": 2,
                "spare": None,
                "mti": rp_mti.RP_ERROR_N_TO_MS,
                "rp": {
                    "message_reference": 4,
                    "rp_cause": {
                        "ext": None,
                        "cause_value": rp_cause.UNASSIGNED_NUMBER,
                        "diagnostic_field": 0x80
                    },
                    "rp_user_data": None
                }
            }
        }
    }


def test_building_rp_error_with_diagnostic_field():
    assert build(L3Message(
        3,
        protocol_discriminator.SMS,
        CpData(rp_mti.RP_ERROR_MS_TO_N, RpError(1, RpCause(rp_cause.CALL_BARRED, 0xaa)))
    )) == b"\x39\x01\x05\x04\x01\x02\x0a\xaa"


def test_parsing_rp_error_with_short_rp_user_data():
    assert parse(b"\x29\x01\x09\x05\x04\x01\x01\x41\x03\x00\xd2\x00") == {
        "transaction_identifier": 2,
        "protocol_discriminator": protocol_discriminator.SMS,
        "l3_protocol": {
            "message_type": message_type.CP_DATA,
            "cp_layer_protocol": {
                "length_indicator": 2,
                "spare": None,
                "mti": rp_mti.RP_ERROR_N_TO_MS,
                "rp": {
                    "message_reference": 4,
                    "rp_cause": {
                        "ext": None,
                        "cause_value": rp_cause.UNASSIGNED_NUMBER,
                        "diagnostic_field": None
                    },
                    "rp_user_data": {
                        "rp_user_data_iei": 0x41,
                        "tpdu": {
                            "tp_udhi": False,
                            "tp_mti": tp_mti.SMS_DELIVER_OR_REPORT,
                            "tp_fcs": tp_fcs.ERROR_IN_MS,
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


def test_building_rp_error_with_short_rp_user_data():
    assert build(L3Message(
        3,
        protocol_discriminator.SMS,
        CpData(
            rp_mti.RP_ERROR_MS_TO_N,
            RpError(1, rp_cause.CALL_BARRED, RpErrorSmsDeliverReport(tp_fcs.SC_BUSY))
        )
    )) == b"\x39\x01\x09\x04\x01\x01\x0a\x41\x03\x00\xc0\x00"


def test_parsing_rp_error_full():
    assert parse(
        b"\x29\x01\x1c\x05\x04\x02\x01\x81\x41\x15\x40\xc3\x07\x20\x80\x0f\x03\x01\x01\xff\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b") == {
               "transaction_identifier": 2,
               "protocol_discriminator": protocol_discriminator.SMS,
               "l3_protocol": {
                   "message_type": message_type.CP_DATA,
                   "cp_layer_protocol": {
                       "length_indicator": 2,
                       "spare": None,
                       "mti": rp_mti.RP_ERROR_N_TO_MS,
                       "rp": {
                           "message_reference": 4,
                           "rp_cause": {
                               "ext": None,
                               "cause_value": rp_cause.UNASSIGNED_NUMBER,
                               "diagnostic_field": 0x81
                           },
                           "rp_user_data": {
                               "rp_user_data_iei": 0x41,
                               "tpdu": {
                                   "tp_udhi": True,
                                   "tp_mti": tp_mti.SMS_DELIVER_OR_REPORT,
                                   "tp_fcs": tp_fcs.INVALID_SME_ADDRESS,
                                   "tp_pi": {
                                       "tp_udl": True,
                                       "tp_dcs": True,
                                       "tp_pid": True
                                   },
                                   "tp_scts": None,
                                   "tp_dcs": 0x80,
                                   "tp_pid": tp_pid.IMPLICIT,
                                   "tp_ud": {
                                       "user_data_header": [
                                           {"element_type": tp_udh_elements.SPECIAL_SMS_MESSAGE,
                                            "element_data": b"\xff"}
                                       ],
                                       "user_data": b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b"
                                   }
                               }
                           }
                       }
                   }
               }
           }


def test_building_rp_error_full():
    assert build(L3Message(
        3,
        protocol_discriminator.SMS,
        CpData(
            rp_mti.RP_ERROR_MS_TO_N,
            RpError(
                1,
                RpCause(rp_cause.PROTOCOL_ERROR, 0x44),
                RpErrorSmsDeliverReport(tp_fcs.SIM_APPLICATION_TOOLKIT_BUSY, tp_pid.X_400_BASED, 0x00,
                                        TpUserData(
                                            b"\xdd\xcc\xbb\xaa",
                                            TpUserDataHeader(TpUserDataHeaderElement(
                                                tp_udh_elements.SMALL_ANIMATION,
                                                b"\x11\x22\x33"
                                            ))
                                        )
                                        )
            )
        )
    )) == b"\x39\x01\x17\x04\x01\x02\x6f\x44\x41\x10\x40\xd4\x07\x31\x00\x0a\x05\x0f\x03\x11\x22\x33\xdd\xcc\xbb\xaa"
