from construct import *
from gsm_layer3_protocol.enums import message_type as cp_type_enum
from gsm_layer3_protocol.sms_protocol.cp_error import cp_error_struct
from gsm_layer3_protocol.sms_protocol.cp_data import cp_data_struct

sms_struct = Struct(
    "message_type" / cp_type_enum,
    StopIf(this.message_type == cp_type_enum.CP_ACK),
    "cp_layer_protocol" / Switch(
        this.message_type,
        {
            cp_type_enum.CP_ERROR: cp_error_struct,
            cp_type_enum.CP_DATA: cp_data_struct
        }
    )
)
