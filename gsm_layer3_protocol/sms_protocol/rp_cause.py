from construct import *
from gsm_layer3_protocol.enums import rp_cause


class RpCause(Container):
    def __init__(self, cause_value, diagnostic_field=None):
        super().__init__(cause_value=cause_value, diagnostic_field=diagnostic_field)


rp_cause_struct = Prefixed(
    "length_indicator" / Byte,
    "rp_cause" / BitStruct(
        "ext" / Padding(1),
        "cause_value" / rp_cause,
        "diagnostic_field" / Optional(Octet)
    )
)
