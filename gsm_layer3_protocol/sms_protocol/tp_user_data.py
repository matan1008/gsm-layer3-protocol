from construct import *
from gsm_layer3_protocol.enums import tp_udh_elements


class TpUserDataHeaderElement(Container):
    def __init__(self, element_type, element_data):
        super().__init__(element_type=element_type, element_data=element_data)


class TpUserDataHeader(ListContainer):
    def __init__(self, *elements):
        super().__init__(elements)


class TpUserData(Container):
    def __init__(self, user_data, user_data_header=None):
        super().__init__(user_data_header=user_data_header, user_data=user_data)


tp_udh_struct = Prefixed(
    "user_data_header_length" / Byte,
    GreedyRange(
        Struct(
            "element_type" / tp_udh_elements,
            "element_data" / Prefixed(Byte, GreedyBytes)  # TODO: Replace with header elements parsing.
        )
    )
)

tp_ud_struct = Prefixed(
    "user_data_length" / Byte,
    Struct(
        "user_data_header" / If(this._.tp_udhi, tp_udh_struct),
        "user_data" / GreedyBytes
    )
)
