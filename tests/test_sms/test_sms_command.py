from gsm_layer3_protocol import parse, build
from gsm_layer3_protocol.enums import *
from gsm_layer3_protocol.l3_message import L3Message
from gsm_layer3_protocol.sms_protocol.cp_data import CpData
from gsm_layer3_protocol.sms_protocol.rp_data import RpDataMsToN
from gsm_layer3_protocol.sms_protocol.sms_command import SmsCommand
from gsm_layer3_protocol.enums import bcd_number_plan as plan, \
    bcd_type_of_number as number_type
from gsm_layer3_protocol.sms_protocol.called_party_bcd_address import \
    AddressField
from gsm_layer3_protocol.sms_protocol.tp_user_data import TpUserData, \
    TpUserDataHeader, TpUserDataHeaderElement


def test_building_sms_command_with_data_header():
    destination_address = AddressField(
        number_type.INTERNATIONAL_NUMBER,
        plan.UNKNOWN,
        "123456"
    )
    sms_command = SmsCommand(
        tp_srr.STATUS_REPORT_REQUESTED,
        0xcd,
        tp_pid.DEFAULT,
        tp_ct.DELETE_PREVIOUSLY_SUBMITTED_SM,
        0xcc,
        destination_address,
        TpUserData(
            b"Deliver us!",
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
            sms_command
        ))
    )) == (b"\x39\x01\x25\x00\x01\x00\x04\x90\x21\x43\x65\x1c\x62\xcd\x00\x02"
           b"\xcc\x06\x90\x21\x43\x65\x11\x05\x00\x03\x03\x02\x01\x44\x65\x6c"
           b"\x69\x76\x65\x72\x20\x75\x73\x21")


def test_parsing_sms_command_with_data_header():
    assert parse(b"\x39\x01\x25\x00\x01\x00\x04\x90\x21\x43\x65\x1c\x62\xcd"
                 b"\x00\x02\xcc\x06\x90\x21\x43\x65\x11\x05\x00\x03\x03\x02"
                 b"\x01\x44\x65\x6c\x69\x76\x65\x72\x20\x75\x73\x21") == {
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
                               "tp_udhi": True,
                               "tp_srr": tp_srr.STATUS_REPORT_REQUESTED,
                               "tp_mti": tp_mti.SMS_STATUS_OR_COMMAND,
                               "tp_mr": 0xcd,
                               "tp_pid": tp_pid.DEFAULT,
                               "tp_ct": tp_ct.DELETE_PREVIOUSLY_SUBMITTED_SM,
                               "tp_mn": 0xcc,
                               "tp_da": {
                                   "ext": None,
                                   "number": "123456",
                                   "number_plan": plan.UNKNOWN,
                                   "type_of_number": number_type.INTERNATIONAL_NUMBER
                               },
                               "tp_cd": {
                                   "user_data_header": [
                                       {
                                           "element_type": tp_udh_elements.CONCATENATED_SHORT_MESSAGES_8_BIT,
                                           "element_data": b"\x03\x02\x01"
                                       }
                                   ],
                                   "user_data": b"Deliver us!"
                               }
                           }}
                       }
                   }
               }
           }

def test_building_sms_command_without_data_header():
    destination_address = AddressField(
        number_type.INTERNATIONAL_NUMBER,
        plan.UNKNOWN,
        "123456"
    )
    sms_command = SmsCommand(
        tp_srr.STATUS_REPORT_REQUESTED,
        0xcd,
        tp_pid.DEFAULT,
        tp_ct.DELETE_PREVIOUSLY_SUBMITTED_SM,
        0xcc,
        destination_address,
        TpUserData(
            b"Deliver us!"
        )
    )
    assert build(L3Message(
        3,
        protocol_discriminator.SMS,
        CpData(rp_mti.RP_DATA_MS_TO_N, RpDataMsToN(
            1,
            destination_address,
            sms_command
        ))
    )) == (b"\x39\x01\x1f\x00\x01\x00\x04\x90\x21\x43\x65\x16\x22\xcd\x00\x02"
           b"\xcc\x06\x90\x21\x43\x65\x0b\x44\x65\x6c\x69\x76\x65\x72\x20\x75"
           b"\x73\x21")


def test_parsing_sms_command_without_data_header():
    assert parse(b"\x39\x01\x1f\x00\x01\x00\x04\x90\x21\x43\x65\x16\x22\xcd"
                 b"\x00\x02\xcc\x06\x90\x21\x43\x65\x0b\x44\x65\x6c\x69\x76"
                 b"\x65\x72\x20\x75\x73\x21") == {
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
                               "tp_udhi": False,
                               "tp_srr": tp_srr.STATUS_REPORT_REQUESTED,
                               "tp_mti": tp_mti.SMS_STATUS_OR_COMMAND,
                               "tp_mr": 0xcd,
                               "tp_pid": tp_pid.DEFAULT,
                               "tp_ct": tp_ct.DELETE_PREVIOUSLY_SUBMITTED_SM,
                               "tp_mn": 0xcc,
                               "tp_da": {
                                   "ext": None,
                                   "number": "123456",
                                   "number_plan": plan.UNKNOWN,
                                   "type_of_number": number_type.INTERNATIONAL_NUMBER
                               },
                               "tp_cd": {
                                   "user_data_header": None,
                                   "user_data": b"Deliver us!"
                               }
                           }}
                       }
                   }
               }
           }
