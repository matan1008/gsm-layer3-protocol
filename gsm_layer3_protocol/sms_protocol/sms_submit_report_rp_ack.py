from construct import *
import gsm_layer3_protocol.sms_protocol.tpdu_parameters as tpdu_parameters
from gsm_layer3_protocol.enums import tp_mti as tp_mti_enum
from gsm_layer3_protocol.sms_protocol.tp_user_data import tp_ud_struct, TpUserData


class RpAckSmsSubmitReport(Container):
    def __init__(self, tp_scts, tp_pid=None, tp_dcs=None, tp_ud=None):
        tp_pi = {
            "tp_udl": tp_ud is not None,
            "tp_dcs": tp_dcs is not None,
            "tp_pid": tp_pid is not None,
        }
        if isinstance(tp_ud, bytes):
            tp_ud = TpUserData(tp_ud)
        tp_udhi = tp_ud is not None and tp_ud.user_data_header is not None
        super().__init__(tp_mti=tp_mti_enum.SMS_SUBMIT_OR_REPORT, tp_udhi=tp_udhi, tp_pi=tp_pi,
                         tp_scts=tp_scts, tp_pid=tp_pid, tp_dcs=tp_dcs, tp_ud=tp_ud)


sms_submit_report_tpdu_struct = BitStruct(
    Padding(1),
    "tp_udhi" / tpdu_parameters.tp_udhi,
    Padding(4),
    "tp_mti" / Const(tp_mti_enum.SMS_SUBMIT_OR_REPORT, tpdu_parameters.tp_mti),
    "tp_pi" / tpdu_parameters.tp_pi,
    "tp_scts" / tpdu_parameters.tp_scts,
    "tp_pid" / If(this.tp_pi.tp_pid, tpdu_parameters.tp_pid),
    "tp_dcs" / If(this.tp_pi.tp_dcs, tpdu_parameters.tp_dcs),
    "tp_ud" / If(this.tp_pi.tp_udl, Bytewise(tp_ud_struct))
)
