from construct import *
from gsm_layer3_protocol.enums import rp_mti
from gsm_layer3_protocol.sms_protocol.sms_submit_report_rp_ack import sms_submit_report_tpdu_struct
from gsm_layer3_protocol.sms_protocol.sms_deliver_report_rp_ack import sms_deliver_report_tpdu_struct


class RpAck(Container):
    def __init__(self, message_reference, tpdu=None):
        super().__init__(message_reference=message_reference, rp_user_data={"tpdu": tpdu})


rp_ack_struct = Struct(
    "message_reference" / Byte,
    "rp_user_data" / Optional(Struct(
        "rp_user_data_iei" / Const(0x41, Byte),
        "tpdu" / IfThenElse(
            this._._.mti == rp_mti.RP_ACK_MS_TO_N,
            sms_deliver_report_tpdu_struct,
            sms_submit_report_tpdu_struct
        )
    ))
)
