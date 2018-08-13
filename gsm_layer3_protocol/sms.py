from construct import *

cp_cause = Enum(
    Byte,
    NETWORK_FAILURE=17, CONGESTION=22, INVALID_TID=81, SEMANTICALLY_INCORRECT=95, INVALID_MANDATORY_INFORMATION=96,
    MESSAGE_TYPE_NOT_IMPLEMENTED=97, NOT_COMPATIBLE_WITH_PROTOCOL_STATE=98, INFORMATION_ELEMENT_NOT_IMPLEMENTED=99,
    PROTOCOL_ERROR=111
)

message_type = Enum(Byte, CP_DATA=1, CP_ACK=4, CP_ERROR=0x10)


class CpAck(Container):
    def __init__(self):
        super().__init__(
            message_type=message_type.CP_ACK
        )


class CpError(Container):
    def __init__(self, cp_cause):
        super().__init__(
            message_type=message_type.CP_ERROR,
            cp_layer_protocol={"cp_cause": cp_cause}
        )


class CpData(Container):
    def __init__(self, mti):
        super().__init__(
            message_type=message_type.CP_DATA,
            cp_layer_protocol={"mti": mti}
        )


cp_error_struct = Struct(
    "cp_cause" / cp_cause
)

cp_data_struct = Prefixed(
    "length_indicator" / Byte,
    BitStruct(
        "spare" / Padding(5),
        "mti" / BitsInteger(3)
    )
)

sms_struct = Struct(
    "message_type" / message_type,
    StopIf(this.message_type == message_type.CP_ACK),
    "cp_layer_protocol" / Switch(
        this.message_type,
        {
            message_type.CP_ERROR: cp_error_struct,
            message_type.CP_DATA: cp_data_struct
        }
    )
)
