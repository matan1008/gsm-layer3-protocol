from construct import *
from gsm_layer3_protocol.enums import rp_cause as rp_cause_value
from gsm_layer3_protocol.sms_protocol.rp_cause import rp_cause_struct, RpCause
from gsm_layer3_protocol.sms_protocol.rp_error_tpdu import rp_error_tpdu_struct


class RpError(Container):
    def __init__(self, message_reference, rp_cause, tpdu=None):
        if isinstance(rp_cause, EnumIntegerString) and rp_cause in rp_cause_value.encmapping:
            cause = RpCause(rp_cause)
        else:
            cause = rp_cause
        super().__init__(message_reference=message_reference, rp_cause=cause,
                         rp_user_data={"tpdu": tpdu})


rp_error_struct = Struct(
    "message_reference" / Byte,
    "rp_cause" / rp_cause_struct,
    "rp_user_data" / Optional(Struct(
        "rp_user_data_iei" / Const(0x41, Byte),
        "tpdu" / rp_error_tpdu_struct
    ))
)
