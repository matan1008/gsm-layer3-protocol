from construct import *
from gsm_layer3_protocol.enums import message_type as rp_cause_value


class RpCause(Container):
    def __init__(self, cause_value, diagnostic_field):
        super().__init__(cause_value=cause_value, diagnostic_field=diagnostic_field)


rp_cause_struct = Prefixed(
    "length_indicator" / Byte,
    BitStruct(
        "ext" / Padding(1),
        "cause_value" / rp_cause_value,
        "diagnostic_field" / Octet
    )
)
