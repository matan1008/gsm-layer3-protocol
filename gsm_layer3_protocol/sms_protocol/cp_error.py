from construct import *
from gsm_layer3_protocol.enums import message_type as cp_type_enum, cp_cause as cp_cause_enum


class CpError(Container):
    def __init__(self, cp_cause):
        super().__init__(message_type=cp_type_enum.CP_ERROR, cp_layer_protocol={"cp_cause": cp_cause})


cp_error_struct = Struct(
    "cp_cause" / cp_cause_enum
)
