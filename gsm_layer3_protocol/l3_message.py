from construct import BitStruct, Nibble, Bytewise, this, Switch, Container
from gsm_layer3_protocol.enums import protocol_discriminator as pd
from gsm_layer3_protocol.sms_protocol.sms import sms_struct


class L3Message(Container):
    def __init__(self, transaction_identifier, protocol_discriminator, l3_protocol):
        super().__init__(
            transaction_identifier=transaction_identifier,
            protocol_discriminator=protocol_discriminator,
            l3_protocol=l3_protocol
        )


l3_struct = BitStruct(
    "transaction_identifier" / Nibble,
    "protocol_discriminator" / pd,
    "l3_protocol" / Bytewise(Switch(
        this.protocol_discriminator,
        {
            pd.SMS: sms_struct
        }
    ))
)
