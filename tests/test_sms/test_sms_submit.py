from gsm_layer3_protocol import parse, build
from gsm_layer3_protocol.enums import *
from gsm_layer3_protocol.l3_message import L3Message
from gsm_layer3_protocol.sms_protocol.cp_data import CpData
from gsm_layer3_protocol.sms_protocol.rp_data import RpDataMsToN
from gsm_layer3_protocol.sms_protocol.sms_submit import SmsSubmit
from gsm_layer3_protocol.enums import bcd_number_plan as plan, \
    bcd_type_of_number as number_type
from gsm_layer3_protocol.sms_protocol.called_party_bcd_address import \
    AddressField
from gsm_layer3_protocol.sms_protocol.tp_user_data import TpUserData, \
    TpUserDataHeader, TpUserDataHeaderElement
from gsm_layer3_protocol.sms_protocol.tpdu_parameters import TpVpEnhanced, \
    TpDcsGeneralDataCodingIndicationNoMessageClass, TpVpAbsolute, \
    TpVpEnhancedSemiOctet


def test_building_sms_submit_with_data_header():
    destination_address = AddressField(
        number_type.INTERNATIONAL_NUMBER,
        plan.UNKNOWN,
        "*3639"
    )
    sms_submit = SmsSubmit(
        False,
        tp_srr.STATUS_REPORT_NOT_REQUESTED,
        tp_rd.ACCEPT,
        0xcc,
        destination_address,
        tp_pid.DEFAULT,
        TpDcsGeneralDataCodingIndicationNoMessageClass(),
        TpVpAbsolute(18, 9, 1, 23, 6, 0, 2),
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
        CpData(rp_mti.RP_DATA_MS_TO_N, RpDataMsToN(
            1,
            destination_address,
            sms_submit
        ))
    )) == (b"\x39\x01\x2a\x00\x01\x00\x04\x90\x3a\x36\xf9\x21\x59\xcc\x05\x90"
           b"\x3a\x36\xf9\x00\x00\x81\x90\x10\x32\x60\x00\x80\x12\x05\x00\x03"
           b"\x03\x02\x01\x88\x65\x76\xda\x5e\x96\x83\xea\xf3\x10")


def test_parsing_sms_submit_with_data_header():
    assert parse(b"\x39\x01\x2a\x00\x01\x00\x04\x90\x3a\x36\xf9\x21\x59\xcc"
                 b"\x05\x90\x3a\x36\xf9\x00\x00\x81\x90\x10\x32\x60\x00\x80"
                 b"\x12\x05\x00\x03\x03\x02\x01\x88\x65\x76\xda\x5e\x96\x83"
                 b"\xea\xf3\x10") == {
               "transaction_identifier": 3,
               "protocol_discriminator": protocol_discriminator.SMS,
               "l3_protocol": {
                   "message_type": message_type.CP_DATA,
                   "cp_layer_protocol": {
                       "spare": None,
                       "mti": rp_mti.RP_DATA_MS_TO_N,
                       "rp": {
                           "message_reference": 1,
                           "rp_destination_address": {
                               "ext": None,
                               "number": "*3639",
                               "number_plan": plan.UNKNOWN,
                               "type_of_number": number_type.INTERNATIONAL_NUMBER
                           },
                           "rp_originator_address": 0,
                           "rp_user_data": {"tpdu": {
                               "tp_rp": False,
                               "tp_udhi": True,
                               "tp_srr": tp_srr.STATUS_REPORT_NOT_REQUESTED,
                               "tp_vpf": tp_vpf.ABSOLUTE_FORMAT,
                               "tp_rd": tp_rd.ACCEPT,
                               "tp_mti": tp_mti.SMS_SUBMIT_OR_REPORT,
                               "tp_mr": 0xcc,
                               "tp_da": {
                                   "ext": None,
                                   "number": "*3639",
                                   "number_plan": plan.UNKNOWN,
                                   "type_of_number": number_type.INTERNATIONAL_NUMBER
                               },
                               "tp_pid": tp_pid.DEFAULT,
                               "tp_dcs": {
                                   "coding_group": dcs_coding_groups.GENERAL_DATA_CODING_INDICATION,
                                   "character_set": dcs_character_set.GSM_7,
                               },
                               "tp_vp": {
                                   "day": 1,
                                   "gmt": 2.0,
                                   "hour": 23,
                                   "minute": 6,
                                   "month": 9,
                                   "second": 0,
                                   "year": 18
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


def test_building_sms_submit_without_data_header():
    destination_address = AddressField(
        number_type.INTERNATIONAL_NUMBER,
        plan.UNKNOWN,
        "123456"
    )
    sms_submit = SmsSubmit(
        False,
        tp_srr.STATUS_REPORT_NOT_REQUESTED,
        tp_rd.ACCEPT,
        0xcc,
        destination_address,
        tp_pid.DEFAULT,
        TpDcsGeneralDataCodingIndicationNoMessageClass(),
        TpVpEnhanced(False, False, TpVpEnhancedSemiOctet(3, 4, 5)),
        TpUserData(
            "Deliver us!"
        )
    )
    assert build(L3Message(
        3,
        protocol_discriminator.SMS,
        CpData(rp_mti.RP_DATA_MS_TO_N, RpDataMsToN(
            1,
            destination_address,
            sms_submit
        ))
    )) == (b"\x39\x01\x24\x00\x01\x00\x04\x90\x21\x43\x65\x1b\x09\xcc\x06\x90"
           b"\x21\x43\x65\x00\x00\x03\x30\x40\x50\x00\x00\x00\x0b\xc4\x32\x3b"
           b"\x6d\x2f\xcb\x41\xf5\x79\x08")


def test_parsing_sms_submit_without_data_header():
    assert parse(b"\x39\x01\x24\x00\x01\x00\x04\x90\x21\x43\x65\x1b\x09\xcc"
                 b"\x06\x90\x21\x43\x65\x00\x00\x03\x30\x40\x50\x00\x00\x00"
                 b"\x0b\xc4\x32\x3b\x6d\x2f\xcb\x41\xf5\x79\x08") == {
               "transaction_identifier": 3,
               "protocol_discriminator": protocol_discriminator.SMS,
               "l3_protocol": {
                   "message_type": message_type.CP_DATA,
                   "cp_layer_protocol": {
                       "spare": None,
                       "mti": rp_mti.RP_DATA_MS_TO_N,
                       "rp": {
                           "message_reference": 1,
                           "rp_destination_address": {
                               "ext": None,
                               "number": "123456",
                               "number_plan": plan.UNKNOWN,
                               "type_of_number": number_type.INTERNATIONAL_NUMBER
                           },
                           "rp_originator_address": 0,
                           "rp_user_data": {"tpdu": {
                               "tp_rp": False,
                               "tp_udhi": False,
                               "tp_srr": tp_srr.STATUS_REPORT_NOT_REQUESTED,
                               "tp_vpf": tp_vpf.ENHANCED_FORMAT,
                               "tp_rd": tp_rd.ACCEPT,
                               "tp_mti": tp_mti.SMS_SUBMIT_OR_REPORT,
                               "tp_mr": 0xcc,
                               "tp_da": {
                                   "ext": None,
                                   "number": "123456",
                                   "number_plan": plan.UNKNOWN,
                                   "type_of_number": number_type.INTERNATIONAL_NUMBER
                               },
                               "tp_pid": tp_pid.DEFAULT,
                               "tp_dcs": {
                                   "coding_group": dcs_coding_groups.GENERAL_DATA_CODING_INDICATION,
                                   "character_set": dcs_character_set.GSM_7,
                               },
                               "tp_vp": {
                                   "extension_bit": False,
                                   "single_shot_sm": False,
                                   "validity_period_format": tp_vp_enhanced_format.SEMI_OCTET,
                                   "validity_period": {
                                       "hour": 3,
                                       "minute": 4,
                                       "second": 5
                                   }
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
