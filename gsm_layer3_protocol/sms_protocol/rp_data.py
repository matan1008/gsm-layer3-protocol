from construct import *
from gsm_layer3_protocol.enums import rp_mti
from gsm_layer3_protocol.sms_protocol.called_party_bcd_address import zero_lengthed_bcd_address, service_center_address
from gsm_layer3_protocol.sms_protocol.sms_submit import sms_submit_tpdu_struct
from gsm_layer3_protocol.sms_protocol.sms_command import sms_command_tpdu_struct
from gsm_layer3_protocol.sms_protocol.sms_deliver import sms_deliver_tpdu_struct
from gsm_layer3_protocol.sms_protocol.sms_status_report import sms_status_report_tpdu_struct
from gsm_layer3_protocol.sms_protocol.sms_submit_report_rp_ack import sms_submit_report_tpdu_struct
from gsm_layer3_protocol.sms_protocol.sms_deliver_report_rp_ack import sms_deliver_report_tpdu_struct


class RpDataMsToN(Container):
    def __init__(self, message_reference, rp_destination_address, tpdu=None):
        super().__init__(message_reference=message_reference, rp_originator_address=None,
                         rp_destination_address=rp_destination_address, rp_user_data={"tpdu": tpdu})


class RpDataNToMs(Container):
    def __init__(self, message_reference, rp_originator_address, tpdu=None):
        super().__init__(message_reference=message_reference, rp_originator_address=rp_originator_address,
                         rp_destination_address=None, rp_user_data={"tpdu": tpdu})


rp_data_struct = Struct(
    "message_reference" / Byte,
    "rp_originator_address" / IfThenElse(this._.mti == rp_mti.RP_DATA_MS_TO_N, zero_lengthed_bcd_address,
                                         service_center_address),
    "rp_destination_address" / IfThenElse(this._.mti == rp_mti.RP_DATA_MS_TO_N, service_center_address,
                                          zero_lengthed_bcd_address),
    "rp_user_data" / Struct("tpdu" / Prefixed(
        "tpdu_length" / Byte,
        IfThenElse(
            this._._.mti == rp_mti.RP_DATA_MS_TO_N,
            Select(sms_deliver_report_tpdu_struct, sms_command_tpdu_struct, sms_submit_tpdu_struct),
            Select(sms_deliver_tpdu_struct, sms_status_report_tpdu_struct, sms_submit_report_tpdu_struct)
        )
    ))
)
