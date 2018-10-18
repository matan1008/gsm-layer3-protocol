from gsm_layer3_protocol import parse, build
from gsm_layer3_protocol.enums import *
from gsm_layer3_protocol.l3_message import L3Message
from gsm_layer3_protocol.sms_protocol.cp_data import CpData
from gsm_layer3_protocol.sms_protocol.rp_data import RpDataNToMs
from gsm_layer3_protocol.sms_protocol.sms_status_report import SmsStatusReport
from gsm_layer3_protocol.enums import bcd_number_plan as plan, \
    bcd_type_of_number as number_type
from gsm_layer3_protocol.sms_protocol.called_party_bcd_address import \
    AddressField
from gsm_layer3_protocol.sms_protocol.tp_user_data import TpUserData, \
    TpUserDataHeader, TpUserDataHeaderElement
from gsm_layer3_protocol.sms_protocol.tpdu_parameters import TpScts, \
    TpDcsGeneralDataCodingIndicationNoMessageClass, TpDt


def test_building_sms_status_report_with_data_header():
    sms_status_report = SmsStatusReport(
        tp_srq.SMS_SUBMIT,
        tp_lp.NOT_FORWARDED_OR_SPAWNED,
        tp_mms.NO_MORE_MESSAGES_ARE_WAITING,
        0xcc,
        AddressField(
            number_type.INTERNATIONAL_NUMBER,
            plan.UNKNOWN,
            "*3639"
        ),
        TpScts(18, 9, 1, 23, 6, 0, 2),
        TpDt(18, 9, 1, 23, 0, 0, 2),
        tp_st.SHORT_MESSAGE_RECEIVED_BY_THE_SME,
        tp_pid.DEFAULT,
        TpDcsGeneralDataCodingIndicationNoMessageClass(),
        TpUserData(
            "Deliver us!",
            TpUserDataHeader(TpUserDataHeaderElement(
                tp_udh_elements.CONCATENATED_SHORT_MESSAGES_8_BIT,
                b"\x03\x02\x01"
            ))
        )
    )
    assert build(L3Message(
        3,
        protocol_discriminator.SMS,
        CpData(rp_mti.RP_DATA_N_TO_MS, RpDataNToMs(
            1,
            AddressField(
                number_type.INTERNATIONAL_NUMBER,
                plan.UNKNOWN,
                "123456"
            ),
            sms_status_report
        ))
    )) == (b"\x39\x01\x33\x01\x01\x04\x90\x21\x43\x65\x00\x2a\x46\xcc\x05\x90"
           b"\x3a\x36\xf9\x81\x90\x10\x32\x60\x00\x80\x81\x90\x10\x32\x00\x00"
           b"\x80\x00\x07\x00\x00\x12\x05\x00\x03\x03\x02\x01\x88\x65\x76\xda"
           b"\x5e\x96\x83\xea\xf3\x10")


def test_parsing_sms_status_report_with_data_header():
    assert parse(b"\x39\x01\x33\x01\x01\x04\x90\x21\x43\x65\x00\x2a\x46\xcc"
                 b"\x05\x90\x3a\x36\xf9\x81\x90\x10\x32\x60\x00\x80\x81\x90"
                 b"\x10\x32\x00\x00\x80\x00\x07\x00\x00\x12\x05\x00\x03\x03"
                 b"\x02\x01\x88\x65\x76\xda\x5e\x96\x83\xea\xf3\x10") == {
               "transaction_identifier": 3,
               "protocol_discriminator": protocol_discriminator.SMS,
               "l3_protocol": {
                   "message_type": message_type.CP_DATA,
                   "cp_layer_protocol": {
                       "spare": None,
                       "mti": rp_mti.RP_DATA_N_TO_MS,
                       "rp": {
                           "message_reference": 1,
                           "rp_originator_address": {
                               "ext": None,
                               "number": "123456",
                               "number_plan": plan.UNKNOWN,
                               "type_of_number": number_type.INTERNATIONAL_NUMBER
                           },
                           "rp_destination_address": 0,
                           "rp_user_data": {"tpdu": {
                               "tp_udhi": True,
                               "tp_srq": tp_srq.SMS_SUBMIT,
                               "tp_lp": tp_lp.NOT_FORWARDED_OR_SPAWNED,
                               "tp_mms": tp_mms.NO_MORE_MESSAGES_ARE_WAITING,
                               "tp_mti": tp_mti.SMS_STATUS_OR_COMMAND,
                               "tp_mr": 0xcc,
                               "tp_ra": {
                                   "ext": None,
                                   "number": "*3639",
                                   "number_plan": plan.UNKNOWN,
                                   "type_of_number": number_type.INTERNATIONAL_NUMBER
                               },
                               "tp_scts": {
                                   "day": 1,
                                   "gmt": 2.0,
                                   "hour": 23,
                                   "minute": 6,
                                   "month": 9,
                                   "second": 0,
                                   "year": 18
                               },
                               "tp_dt": {
                                   "day": 1,
                                   "gmt": 2.0,
                                   "hour": 23,
                                   "minute": 0,
                                   "month": 9,
                                   "second": 0,
                                   "year": 18
                               },
                               "tp_st": tp_st.SHORT_MESSAGE_RECEIVED_BY_THE_SME,
                               "tp_pi": {
                                   "tp_udl": True,
                                   "tp_dcs": True,
                                   "tp_pid": True,
                               },
                               "tp_pid": tp_pid.DEFAULT,
                               "tp_dcs": {
                                   "coding_group": dcs_coding_groups.GENERAL_DATA_CODING_INDICATION,
                                   "character_set": dcs_character_set.GSM_7,
                               },
                               "tp_ud": {
                                   "user_data_header": [
                                       {
                                           "element_type": tp_udh_elements.CONCATENATED_SHORT_MESSAGES_8_BIT,
                                           "element_data": b"\x03\x02\x01"
                                       }
                                   ],
                                   "user_data": "Deliver us!"
                               }
                           }}
                       }
                   }
               }
           }


def test_building_sms_status_report_without_data_header():
    sms_status_report = SmsStatusReport(
        tp_srq.SMS_SUBMIT,
        tp_lp.NOT_FORWARDED_OR_SPAWNED,
        tp_mms.NO_MORE_MESSAGES_ARE_WAITING,
        0xcc,
        AddressField(
            number_type.INTERNATIONAL_NUMBER,
            plan.UNKNOWN,
            "*3639"
        ),
        TpScts(18, 9, 1, 23, 6, 0, 2),
        TpDt(18, 9, 1, 23, 0, 0, 2),
        tp_st.SHORT_MESSAGE_RECEIVED_BY_THE_SME,
        tp_pid.DEFAULT,
        TpDcsGeneralDataCodingIndicationNoMessageClass(),
        TpUserData(
            "Deliver us!"
        )
    )
    assert build(L3Message(
        3,
        protocol_discriminator.SMS,
        CpData(rp_mti.RP_DATA_N_TO_MS, RpDataNToMs(
            1,
            AddressField(
                number_type.INTERNATIONAL_NUMBER,
                plan.UNKNOWN,
                "123456"
            ),
            sms_status_report
        ))
    )) == (b"\x39\x01\x2d\x01\x01\x04\x90\x21\x43\x65\x00\x24\x06\xcc\x05\x90"
           b"\x3a\x36\xf9\x81\x90\x10\x32\x60\x00\x80\x81\x90\x10\x32\x00\x00"
           b"\x80\x00\x07\x00\x00\x0b\xc4\x32\x3b\x6d\x2f\xcb\x41\xf5\x79\x08")


def test_parsing_sms_status_report_without_data_header():
    assert parse(b"\x39\x01\x2d\x01\x01\x04\x90\x21\x43\x65\x00\x24\x06\xcc"
                 b"\x05\x90\x3a\x36\xf9\x81\x90\x10\x32\x60\x00\x80\x81\x90"
                 b"\x10\x32\x00\x00\x80\x00\x07\x00\x00\x0b\xc4\x32\x3b\x6d"
                 b"\x2f\xcb\x41\xf5\x79\x08") == {
               "transaction_identifier": 3,
               "protocol_discriminator": protocol_discriminator.SMS,
               "l3_protocol": {
                   "message_type": message_type.CP_DATA,
                   "cp_layer_protocol": {
                       "spare": None,
                       "mti": rp_mti.RP_DATA_N_TO_MS,
                       "rp": {
                           "message_reference": 1,
                           "rp_originator_address": {
                               "ext": None,
                               "number": "123456",
                               "number_plan": plan.UNKNOWN,
                               "type_of_number": number_type.INTERNATIONAL_NUMBER
                           },
                           "rp_destination_address": 0,
                           "rp_user_data": {"tpdu": {
                               "tp_udhi": False,
                               "tp_srq": tp_srq.SMS_SUBMIT,
                               "tp_lp": tp_lp.NOT_FORWARDED_OR_SPAWNED,
                               "tp_mms": tp_mms.NO_MORE_MESSAGES_ARE_WAITING,
                               "tp_mti": tp_mti.SMS_STATUS_OR_COMMAND,
                               "tp_mr": 0xcc,
                               "tp_ra": {
                                   "ext": None,
                                   "number": "*3639",
                                   "number_plan": plan.UNKNOWN,
                                   "type_of_number": number_type.INTERNATIONAL_NUMBER
                               },
                               "tp_scts": {
                                   "day": 1,
                                   "gmt": 2.0,
                                   "hour": 23,
                                   "minute": 6,
                                   "month": 9,
                                   "second": 0,
                                   "year": 18
                               },
                               "tp_dt": {
                                   "day": 1,
                                   "gmt": 2.0,
                                   "hour": 23,
                                   "minute": 0,
                                   "month": 9,
                                   "second": 0,
                                   "year": 18
                               },
                               "tp_st": tp_st.SHORT_MESSAGE_RECEIVED_BY_THE_SME,
                               "tp_pi": {
                                   "tp_udl": True,
                                   "tp_dcs": True,
                                   "tp_pid": True,
                               },
                               "tp_pid": tp_pid.DEFAULT,
                               "tp_dcs": {
                                   "coding_group": dcs_coding_groups.GENERAL_DATA_CODING_INDICATION,
                                   "character_set": dcs_character_set.GSM_7,
                               },
                               "tp_ud": {
                                   "user_data_header": None,
                                   "user_data": "Deliver us!"
                               }
                           }}
                       }
                   }
               }
           }


def test_building_sms_status_report_without_dcs():
    sms_status_report = SmsStatusReport(
        tp_srq.SMS_SUBMIT,
        tp_lp.NOT_FORWARDED_OR_SPAWNED,
        tp_mms.NO_MORE_MESSAGES_ARE_WAITING,
        0xcc,
        AddressField(
            number_type.INTERNATIONAL_NUMBER,
            plan.UNKNOWN,
            "*3639"
        ),
        TpScts(18, 9, 1, 23, 6, 0, 2),
        TpDt(18, 9, 1, 23, 0, 0, 2),
        tp_st.SHORT_MESSAGE_RECEIVED_BY_THE_SME,
        tp_pid=tp_pid.DEFAULT,
        tp_ud=TpUserData(
            "Deliver us!",
            TpUserDataHeader(TpUserDataHeaderElement(
                tp_udh_elements.CONCATENATED_SHORT_MESSAGES_8_BIT,
                b"\x03\x02\x01"
            ))
        )
    )
    assert build(L3Message(
        3,
        protocol_discriminator.SMS,
        CpData(rp_mti.RP_DATA_N_TO_MS, RpDataNToMs(
            1,
            AddressField(
                number_type.INTERNATIONAL_NUMBER,
                plan.UNKNOWN,
                "123456"
            ),
            sms_status_report
        ))
    )) == (b"\x39\x01\x32\x01\x01\x04\x90\x21\x43\x65\x00\x29\x46\xcc\x05\x90"
           b"\x3a\x36\xf9\x81\x90\x10\x32\x60\x00\x80\x81\x90\x10\x32\x00\x00"
           b"\x80\x00\x05\x00\x12\x05\x00\x03\x03\x02\x01\x88\x65\x76\xda\x5e"
           b"\x96\x83\xea\xf3\x10")


def test_parsing_sms_status_report_without_dcs():
    assert parse(b"\x39\x01\x32\x01\x01\x04\x90\x21\x43\x65\x00\x29\x46\xcc"
                 b"\x05\x90\x3a\x36\xf9\x81\x90\x10\x32\x60\x00\x80\x81\x90"
                 b"\x10\x32\x00\x00\x80\x00\x05\x00\x12\x05\x00\x03\x03\x02"
                 b"\x01\x88\x65\x76\xda\x5e\x96\x83\xea\xf3\x10") == {
               "transaction_identifier": 3,
               "protocol_discriminator": protocol_discriminator.SMS,
               "l3_protocol": {
                   "message_type": message_type.CP_DATA,
                   "cp_layer_protocol": {
                       "spare": None,
                       "mti": rp_mti.RP_DATA_N_TO_MS,
                       "rp": {
                           "message_reference": 1,
                           "rp_originator_address": {
                               "ext": None,
                               "number": "123456",
                               "number_plan": plan.UNKNOWN,
                               "type_of_number": number_type.INTERNATIONAL_NUMBER
                           },
                           "rp_destination_address": 0,
                           "rp_user_data": {"tpdu": {
                               "tp_udhi": True,
                               "tp_srq": tp_srq.SMS_SUBMIT,
                               "tp_lp": tp_lp.NOT_FORWARDED_OR_SPAWNED,
                               "tp_mms": tp_mms.NO_MORE_MESSAGES_ARE_WAITING,
                               "tp_mti": tp_mti.SMS_STATUS_OR_COMMAND,
                               "tp_mr": 0xcc,
                               "tp_ra": {
                                   "ext": None,
                                   "number": "*3639",
                                   "number_plan": plan.UNKNOWN,
                                   "type_of_number": number_type.INTERNATIONAL_NUMBER
                               },
                               "tp_scts": {
                                   "day": 1,
                                   "gmt": 2.0,
                                   "hour": 23,
                                   "minute": 6,
                                   "month": 9,
                                   "second": 0,
                                   "year": 18
                               },
                               "tp_dt": {
                                   "day": 1,
                                   "gmt": 2.0,
                                   "hour": 23,
                                   "minute": 0,
                                   "month": 9,
                                   "second": 0,
                                   "year": 18
                               },
                               "tp_st": tp_st.SHORT_MESSAGE_RECEIVED_BY_THE_SME,
                               "tp_pi": {
                                   "tp_udl": True,
                                   "tp_dcs": False,
                                   "tp_pid": True,
                               },
                               "tp_pid": tp_pid.DEFAULT,
                               "tp_dcs": {
                                   "character_set": dcs_character_set.GSM_7,
                               },
                               "tp_ud": {
                                   "user_data_header": [
                                       {
                                           "element_type": tp_udh_elements.CONCATENATED_SHORT_MESSAGES_8_BIT,
                                           "element_data": b"\x03\x02\x01"
                                       }
                                   ],
                                   "user_data": "Deliver us!"
                               }
                           }}
                       }
                   }
               }
           }


def test_building_sms_status_report_without_optionals():
    sms_status_report = SmsStatusReport(
        tp_srq.SMS_SUBMIT,
        tp_lp.NOT_FORWARDED_OR_SPAWNED,
        tp_mms.NO_MORE_MESSAGES_ARE_WAITING,
        0xcc,
        AddressField(
            number_type.INTERNATIONAL_NUMBER,
            plan.UNKNOWN,
            "*3639"
        ),
        TpScts(18, 9, 1, 23, 6, 0, 2),
        TpDt(18, 9, 1, 23, 0, 0, 2),
        tp_st.SHORT_MESSAGE_RECEIVED_BY_THE_SME
    )
    assert build(L3Message(
        3,
        protocol_discriminator.SMS,
        CpData(rp_mti.RP_DATA_N_TO_MS, RpDataNToMs(
            1,
            AddressField(
                number_type.INTERNATIONAL_NUMBER,
                plan.UNKNOWN,
                "123456"
            ),
            sms_status_report
        ))
    )) == (b"\x39\x01\x20\x01\x01\x04\x90\x21\x43\x65\x00\x17\x06\xcc\x05\x90"
           b"\x3a\x36\xf9\x81\x90\x10\x32\x60\x00\x80\x81\x90\x10\x32\x00\x00"
           b"\x80\x00\x00")


def test_parsing_sms_status_report_without_optionals():
    assert parse(b"\x39\x01\x20\x01\x01\x04\x90\x21\x43\x65\x00\x17\x06\xcc"
                 b"\x05\x90\x3a\x36\xf9\x81\x90\x10\x32\x60\x00\x80\x81\x90"
                 b"\x10\x32\x00\x00\x80\x00\x00") == {
               "transaction_identifier": 3,
               "protocol_discriminator": protocol_discriminator.SMS,
               "l3_protocol": {
                   "message_type": message_type.CP_DATA,
                   "cp_layer_protocol": {
                       "spare": None,
                       "mti": rp_mti.RP_DATA_N_TO_MS,
                       "rp": {
                           "message_reference": 1,
                           "rp_originator_address": {
                               "ext": None,
                               "number": "123456",
                               "number_plan": plan.UNKNOWN,
                               "type_of_number": number_type.INTERNATIONAL_NUMBER
                           },
                           "rp_destination_address": 0,
                           "rp_user_data": {"tpdu": {
                               "tp_udhi": False,
                               "tp_srq": tp_srq.SMS_SUBMIT,
                               "tp_lp": tp_lp.NOT_FORWARDED_OR_SPAWNED,
                               "tp_mms": tp_mms.NO_MORE_MESSAGES_ARE_WAITING,
                               "tp_mti": tp_mti.SMS_STATUS_OR_COMMAND,
                               "tp_mr": 0xcc,
                               "tp_ra": {
                                   "ext": None,
                                   "number": "*3639",
                                   "number_plan": plan.UNKNOWN,
                                   "type_of_number": number_type.INTERNATIONAL_NUMBER
                               },
                               "tp_scts": {
                                   "day": 1,
                                   "gmt": 2.0,
                                   "hour": 23,
                                   "minute": 6,
                                   "month": 9,
                                   "second": 0,
                                   "year": 18
                               },
                               "tp_dt": {
                                   "day": 1,
                                   "gmt": 2.0,
                                   "hour": 23,
                                   "minute": 0,
                                   "month": 9,
                                   "second": 0,
                                   "year": 18
                               },
                               "tp_st": tp_st.SHORT_MESSAGE_RECEIVED_BY_THE_SME,
                               "tp_pi": {
                                   "tp_udl": False,
                                   "tp_dcs": False,
                                   "tp_pid": False,
                               },
                               "tp_pid": None,
                               "tp_dcs": {
                                   "character_set": dcs_character_set.GSM_7,
                               },
                               "tp_ud": None
                           }}
                       }
                   }
               }
           }
