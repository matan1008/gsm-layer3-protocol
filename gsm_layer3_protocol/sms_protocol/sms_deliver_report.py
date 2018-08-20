from construct import *
from gsm_layer3_protocol.enums import tp_mti, tp_fcs


class RpErrorSmsDeliverReport(Container):
    def __init__(self, tp_udhi, failure_cause, parameter_indicator):
        super().__init__(tp_mti=tp_mti.SMS_DELIVER_OR_REPORT, tp_udhi=tp_udhi)

tp_pid = Struct(

)

rp_smma_struct = Struct(
    Padding(1),
    "tp_udhi" / Flag,
    Padding(4),
    "tp_mti" / tp_mti,
    "tp_fcs" / tp_fcs,

)
