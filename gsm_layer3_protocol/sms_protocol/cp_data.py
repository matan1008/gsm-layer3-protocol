from construct import *
from gsm_layer3_protocol.enums import message_type as cp_type_enum, rp_mti
from gsm_layer3_protocol.sms_protocol.rp_ack import rp_ack_struct


class CpData(Container):
    def __init__(self, mti, rp):
        super().__init__(message_type=cp_type_enum.CP_DATA, cp_layer_protocol={"mti": mti, "rp": rp})


cp_data_struct = Prefixed(
    "length_indicator" / Byte,
    BitStruct(
        "spare" / Padding(5),
        "mti" / rp_mti,
        "rp" / Bytewise(Switch(
            this.mti,
            {
                rp_mti.RP_ACK_MS_TO_N: rp_ack_struct,
                rp_mti.RP_ACK_N_TO_MS: rp_ack_struct
            }
        ))
    )
)
