from construct import *
from gsm_layer3_protocol.enums import message_type as cp_type_enum


class CpAck(Container):
    def __init__(self):
        """
        Container for cp-ack messages.
        """
        super().__init__(message_type=cp_type_enum.CP_ACK)
