from construct import *


class RpSmma(Container):
    def __init__(self, message_reference):
        super().__init__(message_reference=message_reference)


rp_smma_struct = Struct(
    "message_reference" / Byte
)
