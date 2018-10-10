from gsm_layer3_protocol import parse, build
from gsm_layer3_protocol.enums import *
from gsm_layer3_protocol.l3_message import L3Message
from gsm_layer3_protocol.sms_protocol.cp_data import CpData
from gsm_layer3_protocol.sms_protocol.rp_data import RpDataNToMs
from gsm_layer3_protocol.sms_protocol.sms_deliver import SmsDeliver
from gsm_layer3_protocol.enums import bcd_number_plan as plan, \
    bcd_type_of_number as number_type
from gsm_layer3_protocol.sms_protocol.called_party_bcd_address import \
    AddressField
from gsm_layer3_protocol.sms_protocol.tp_user_data import TpUserData, \
    TpUserDataHeader, TpUserDataHeaderElement
from gsm_layer3_protocol.sms_protocol.tpdu_parameters import TpScts, \
    TpDcsGeneralDataCodingIndicationNoMessageClass


def test_building_sms_deliver_with_data_header():
    originator_address = AddressField(
        number_type.INTERNATIONAL_NUMBER,
        plan.UNKNOWN,
        "123456"
    )
    sms_deliver = SmsDeliver(
        False,
        tp_sri.STATUS_REPORT_SHALL_BE_RETURNED,
        tp_lp.NOT_FORWARDED_OR_SPAWNED,
        tp_mms.NO_MORE_MESSAGES_ARE_WAITING,
        originator_address,
        tp_pid.DEFAULT,
        TpDcsGeneralDataCodingIndicationNoMessageClass(),
        TpScts(18, 9, 1, 23, 6, 0, 2),
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
            originator_address,
            sms_deliver
        ))
    )) == (b"\x39\x01\x29\x01\x01\x04\x90\x21\x43\x65\x00\x20\x64\x06\x90\x21"
           b"\x43\x65\x00\x00\x81\x90\x10\x32\x60\x00\x80\x12\x05\x00\x03\x03"
           b"\x02\x01\x88\x65\x76\xda\x5e\x96\x83\xea\xf3\x10")


def test_parsing_sms_deliver_with_data_header():
    assert parse(b"\x39\x01\x29\x01\x01\x04\x90\x21\x43\x65\x00\x20\x64\x06"
                 b"\x90\x21\x43\x65\x00\x00\x81\x90\x10\x32\x60\x00\x80\x12"
                 b"\x05\x00\x03\x03\x02\x01\x88\x65\x76\xda\x5e\x96\x83\xea"
                 b"\xf3\x10") == {
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
                               "tp_rp": False,
                               "tp_udhi": True,
                               "tp_sri": tp_sri.STATUS_REPORT_SHALL_BE_RETURNED,
                               "tp_lp": tp_lp.NOT_FORWARDED_OR_SPAWNED,
                               "tp_mms": tp_mms.NO_MORE_MESSAGES_ARE_WAITING,
                               "tp_mti": tp_mti.SMS_DELIVER_OR_REPORT,
                               "tp_oa": {
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
                               "tp_scts": {
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
