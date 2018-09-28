from construct import *
import gsm_layer3_protocol.sms_protocol.tpdu_parameters as tpdu_parameters
from gsm_layer3_protocol.enums import tp_mti as tp_mti_enum
from gsm_layer3_protocol.sms_protocol.tp_user_data import tp_ud_struct, TpUserData


class SmsDeliver(Container):
    def __init__(self, tp_rp, tp_sri, tp_lp, tp_mms, tp_oa, tp_pid, tp_dcs, tp_ud=None):
        if isinstance(tp_ud, bytes):
            tp_ud = TpUserData(tp_ud)
        elif tp_ud is None:
            tp_ud = TpUserData(b"")
        tp_udhi = tp_ud.user_data_header is not None
        super().__init__(tp_mti=tp_mti_enum.SMS_DELIVER_OR_REPORT, tp_rp=tp_rp, tp_udhi=tp_udhi, tp_sri=tp_sri,
                         tp_lp=tp_lp, tp_mms=tp_mms, tp_oa=tp_oa, tp_pid=tp_pid, tp_dcs=tp_dcs, tp_ud=tp_ud)


sms_deliver_tpdu_struct = BitStruct(
    "tp_rp" / tpdu_parameters.tp_rp,
    "tp_udhi" / tpdu_parameters.tp_udhi,
    "tp_sri" / tpdu_parameters.tp_sri,
    Padding(1),
    "tp_lp" / tpdu_parameters.tp_lp,
    "tp_mms" / tpdu_parameters.tp_mms,
    "tp_mti" / Const(tp_mti_enum.SMS_SUBMIT_OR_REPORT, tpdu_parameters.tp_mti),
    "tp_oa" / tpdu_parameters.tp_oa,
    "tp_pid" / tpdu_parameters.tp_pid,
    "tp_dcs" / tpdu_parameters.tp_dcs,
    "tp_ud" / Bytewise(tp_ud_struct)
)
