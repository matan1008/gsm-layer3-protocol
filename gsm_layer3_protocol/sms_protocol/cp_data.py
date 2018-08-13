from construct import *
from gsm_layer3_protocol.enums import message_type as cp_type_enum


class CpData(Container):
    def __init__(self, mti):
        super().__init__(message_type=cp_type_enum.CP_DATA, cp_layer_protocol={"mti": mti})


cp_data_struct = Prefixed(
    "length_indicator" / Byte,
    BitStruct(
        "spare" / Padding(5),
        "mti" / BitsInteger(3)
    )
)
