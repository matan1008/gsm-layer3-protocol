from construct import BitStruct, Nibble, Bytewise, this, Switch, Container, Enum
from gsm_layer3_protocol.sms import sms_struct, CpData, CpError, cp_cause

protocol_discriminator = Enum(
    Nibble,
    GROUP_CALL_CONTROL=0,
    BROADCAST_CALL_CONTROL=1,
    PDSS1=2,
    CALL_CONTROL=3,
    PDSS2=4,
    MOBILITY_MANAGEMENT=5,
    RADIO_RESOURCES=6,
    SMS=9,
    NON_CALL_RELATED_SS=0xb,
    EXTENSION_OF_PD=0xe,
    TEST_PROCEDURES=0xf
)


class L3Message(Container):
    def __init__(self, transaction_identifier, protocol_discriminator, l3_protocol):
        super().__init__(
            transaction_identifier=transaction_identifier,
            protocol_discriminator=protocol_discriminator,
            l3_protocol=l3_protocol
        )


l3_struct = BitStruct(
    "transaction_identifier" / Nibble,
    "protocol_discriminator" / protocol_discriminator,
    "l3_protocol" / Bytewise(Switch(
        this.protocol_discriminator,
        {
            protocol_discriminator.SMS: sms_struct
        }
    ))
)
