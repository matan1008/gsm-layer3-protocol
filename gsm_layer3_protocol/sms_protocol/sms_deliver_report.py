from construct import *
from gsm_layer3_protocol.enums import tp_mti, tp_fcs as tp_fcs_enum, tp_pid as tp_pid_enum
from gsm_layer3_protocol.sms_protocol.tp_user_data import tp_ud_struct, TpUserData


class RpErrorSmsDeliverReport(Container):
    def __init__(self, tp_fcs, tp_pid=None, tp_dcs=None, tp_ud=None):
        tp_pi = {
            "tp_udl": tp_ud is not None,
            "tp_dcs": tp_dcs is not None,
            "tp_pid": tp_pid is not None,
        }
        if isinstance(tp_ud, bytes):
            tp_ud = TpUserData(tp_ud)
        tp_udhi = tp_ud is not None and tp_ud.user_data_header is not None
        super().__init__(tp_mti=tp_mti.SMS_DELIVER_OR_REPORT, tp_udhi=tp_udhi, tp_fcs=tp_fcs, tp_pi=tp_pi,
                         tp_pid=tp_pid, tp_scts=None, tp_dcs=tp_dcs, tp_ud=tp_ud)


rp_error_tpdu_struct = Prefixed(
    "tpdu_length" / Byte,
    BitStruct(
        Padding(1),
        "tp_udhi" / Flag,
        Padding(4),
        "tp_mti" / tp_mti,
        "tp_fcs" / tp_fcs_enum,
        "tp_pi" / Struct(
            Padding(5),
            "tp_udl" / Flag,
            "tp_dcs" / Flag,
            "tp_pid" / Flag
        ),
        "tp_scts" / If(
            this.tp_mti is tp_mti.SMS_SUBMIT_OR_REPORT,
            Struct(
                "year" / BitsSwapped(Hex(Byte)),
                "month" / BitsSwapped(Hex(Byte)),
                "day" / BitsSwapped(Hex(Byte)),
                "hour" / BitsSwapped(Hex(Byte)),
                "minute" / BitsSwapped(Hex(Byte)),
                "gmt" / Byte
            )
        ),
        "tp_pid" / If(this.tp_pi.tp_pid, tp_pid_enum),
        "tp_dcs" / If(this.tp_pi.tp_dcs, Octet),  # TODO: Make it a nice structure or enum
        "tp_ud" / If(this.tp_pi.tp_udl, Bytewise(tp_ud_struct))
    )
)
