from construct import *
import gsm_layer3_protocol.sms_protocol.tpdu_parameters as tpdu_parameters
from gsm_layer3_protocol.enums import tp_mti as tp_mti_enum
from gsm_layer3_protocol.sms_protocol.tp_user_data import tp_udh_struct, TpUserData


class SmsCommand(Container):
    def __init__(self, tp_srr, tp_mr, tp_pid, tp_ct, tp_mn, tp_da, tp_cd=None):
        if isinstance(tp_cd, bytes):
            tp_cd = TpUserData(tp_cd)
        tp_udhi = tp_cd is not None and tp_cd.user_data_header is not None
        super().__init__(tp_mti=tp_mti_enum.SMS_STATUS_OR_COMMAND, tp_udhi=tp_udhi, tp_srr=tp_srr, tp_mr=tp_mr,
                         tp_pid=tp_pid, tp_ct=tp_ct, tp_mn=tp_mn, tp_da=tp_da, tp_cd=tp_cd)


sms_command_tpdu_struct = BitStruct(
    Padding(1),
    "tp_udhi" / tpdu_parameters.tp_udhi,
    "tp_srr" / tpdu_parameters.tp_srr,
    Padding(3),
    "tp_mti" / Const(tp_mti_enum.SMS_STATUS_OR_COMMAND, tpdu_parameters.tp_mti),
    "tp_mr" / tpdu_parameters.tp_mr,
    "tp_pid" / tpdu_parameters.tp_pid,
    "tp_ct" / tpdu_parameters.tp_ct,
    "tp_mn" / tpdu_parameters.tp_mn,
    "tp_da" / tpdu_parameters.tp_da,
    "tp_cd" / Bytewise(Prefixed(
        "tp_cdl" / Byte,
        Struct(
            "user_data_header" / If(this._.tp_udhi, tp_udh_struct),
            "user_data" / GreedyBytes
        )
    ))
)
