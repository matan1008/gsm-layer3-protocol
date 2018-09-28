from construct import *
import gsm_layer3_protocol.sms_protocol.tpdu_parameters as tpdu_parameters
from gsm_layer3_protocol.enums import tp_mti as tp_mti_enum
from gsm_layer3_protocol.sms_protocol.tp_user_data import tp_ud_struct, TpUserData


class SmsSubmit(Container):
    def __init__(self, tp_rp, tp_srr, tp_rd, tp_mr, tp_da, tp_pid, tp_dcs, tp_vp=None, tp_ud=None):
        tp_vpf = tpdu_parameters.tp_vpf.NOT_PRESENT if tp_vp is None else tp_vp._tp_vpf
        if isinstance(tp_ud, bytes):
            tp_ud = TpUserData(tp_ud)
        elif tp_ud is None:
            tp_ud = TpUserData(b"")
        tp_udhi = tp_ud.user_data_header is not None
        super().__init__(tp_mti=tp_mti_enum.SMS_SUBMIT_OR_REPORT, tp_rp=tp_rp, tp_udhi=tp_udhi, tp_srr=tp_srr,
                         tp_vpf=tp_vpf, tp_rd=tp_rd, tp_mr=tp_mr, tp_da=tp_da, tp_pid=tp_pid, tp_dcs=tp_dcs,
                         tp_vp=tp_vp, tp_ud=tp_ud)


sms_submit_tpdu_struct = BitStruct(
    "tp_rp" / tpdu_parameters.tp_rp,
    "tp_udhi" / tpdu_parameters.tp_udhi,
    "tp_srr" / tpdu_parameters.tp_srr,
    "tp_vpf" / tpdu_parameters.tp_vpf,
    "tp_rd" / tpdu_parameters.tp_rd,
    "tp_mti" / Const(tp_mti_enum.SMS_SUBMIT_OR_REPORT, tpdu_parameters.tp_mti),
    "tp_mr" / tpdu_parameters.tp_mr,
    "tp_da" / tpdu_parameters.tp_da,
    "tp_pid" / tpdu_parameters.tp_pid,
    "tp_dcs" / tpdu_parameters.tp_dcs,
    "tp_vp" / Switch(
        this.tp_vpf,
        {
            tpdu_parameters.tp_vpf.ENHANCED_FORMAT: Bytewise(tpdu_parameters.tp_vp_enhanced),
            tpdu_parameters.tp_vpf.RELATIVE_FORMAT: tpdu_parameters.tp_vp_relative,
            tpdu_parameters.tp_vpf.ABSOLUTE_FORMAT: tpdu_parameters.tp_vp_absolute
        }
    ),
    "tp_ud" / Bytewise(tp_ud_struct)
)
