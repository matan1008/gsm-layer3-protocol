from enum import Enum
from itertools import count
from construct import Adapter, Const, Byte, Prefixed, BitStruct, Padding, Bytewise, GreedyBytes, Container
from gsm_layer3_protocol.enums import bcd_type_of_number, bcd_number_plan

NumbersEncoding = Enum("NumbersEncoding",
                       zip(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "#", "a", "b", "c"], count()))


class BcdAddresAdapter(Adapter):
    def _decode(self, obj, context, path):
        number = ""
        for octet in obj:
            if octet & 0xf0 == 0xf0:
                number += NumbersEncoding(octet & 0x0f).name
                break
            else:
                number += NumbersEncoding(octet & 0x0f).name + NumbersEncoding((octet >> 4) & 0x0f).name
        return number

    def _encode(self, obj, context, path):
        data = b""
        for i in range(0, len(obj), 2):
            if i == len(obj) - 1:
                data += (0xf0 + NumbersEncoding[obj[i]].value).to_bytes(1, "big")
            else:
                data += ((NumbersEncoding[obj[i + 1]].value << 4) + NumbersEncoding[obj[i]].value).to_bytes(1, "big")
        return data


class BcdAddress(Container):
    def __init__(self, type_of_number, number_plan, number):
        super().__init__(type_of_number=type_of_number, number_plan=number_plan, number=number)


zero_lengthed_bcd_address = Const(0x00, Byte)
bcd_address = Prefixed(
    "address_length" / Byte,
    BitStruct(
        "ext" / Padding(1, b"\x01"),
        "type_of_number" / bcd_type_of_number,
        "number_plan" / bcd_number_plan,
        "number" / Bytewise(BcdAddresAdapter(GreedyBytes))
    )
)
