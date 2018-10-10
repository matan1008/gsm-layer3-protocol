from construct import *
from construct.lib import bits2bytes, bytes2bits, bytestringtype
from construct.core import stream_read, stream_write
from gsm_layer3_protocol.enums import tp_udh_elements, dcs_character_set


class TpUserDataHeaderElement(Container):
    def __init__(self, element_type, element_data):
        super().__init__(element_type=element_type, element_data=element_data)


class TpUserDataHeader(ListContainer):
    def __init__(self, *elements):
        super().__init__(elements)


class TpUserData(Container):
    def __init__(self, user_data, user_data_header=None):
        super().__init__(user_data_header=user_data_header, user_data=user_data)


class SeptetsLengthAdapter(Adapter):
    def _decode(self, obj, context, path):
        return ((obj * 7) // 8) + (obj % 8 > 0)

    def _encode(self, obj, context, path):
        return (obj * 8) // 7


class Gsm7Adapter(Adapter):
    GSM_CHR = ("@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ\x1bÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>?"
               "¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ`¿abcdefghijklmnopqrstuvwxyzäöñüà")
    EXT_CHR = ("````````````````````^```````````````````{}`````\\````````````[~]`"
               "|````````````````````````````````````€``````````````````````````")

    def _decode(self, obj, context, path):
        decoded_data = ""
        obj = obj[:len(obj) - (len(obj) % 8)]
        padded_bits = "".join([format(c, "08b") for c in bits2bytes(obj)[::-1]])
        padded_bits = padded_bits[:len(padded_bits)-((7 - (context.get("_offset", 0) % 7)) % 7)]
        unpadded_bits = padded_bits[len(padded_bits) % 7:]
        bytes_to_decode = [int(unpadded_bits[i:i + 7], 2) for i in range(0, len(unpadded_bits), 7)]
        bytes_to_decode_iter = iter(bytes_to_decode)
        for c in bytes_to_decode_iter:
            if c == 0x1b:
                decoded_data += self.EXT_CHR[next(bytes_to_decode_iter)]
            else:
                decoded_data += self.GSM_CHR[c]
        return decoded_data[::-1]

    def _encode(self, obj, context, path):
        bits = ""
        for c in obj[::-1]:
            if c in self.GSM_CHR:
                bits += format(self.GSM_CHR.find(c), "07b")
            elif c in self.EXT_CHR:
                bits += format(0x1b, "07b") + format(self.EXT_CHR.find(c), "07b")
        bits += "0" * ((7 - (context.get("_offset", 0) % 7)) % 7)
        bits = "0" * (8 - (len(bits) % 8)) + bits
        return bytes2bits(b"".join([(int(bits[i:i + 8], 2)).to_bytes(1, "big") for i in range(0, len(bits), 8)])[::-1])


class AutoAlignment(Construct):
    r"""
    Appends additional null bytes to achieve a length that is shortest multiple of a modulus.

    Note that subcon can actually be variable size, it is the eventual amount of bytes that is read or written during parsing or building that determines actual padding.

    Parsing first parses subcon, then consumes an amount of bytes to sum up to specified length, and discards it. Building first builds subcon, then writes specified pattern byte to sum up to specified length. Size is subcon size plus modulo remainder, unless SizeofError was raised.

    :param modulus: integer or context lambda, modulus to final length
    :param pattern: optional, b-character, padding pattern, default is \\x00

    :raises StreamError: requested reading negative amount, could not read enough bytes, requested writing different amount than actual data, or could not write all bytes
    :raises PaddingError: modulus was less than 2
    :raises PaddingError: pattern was not bytes (b-character)

    Can propagate any exception from the lambda, possibly non-ConstructError.

    Example::

        >>> d = Aligned(4, Int16ub)
        >>> d.parse(b'\x00\x01\x00\x00')
        1
        >>> d.sizeof()
        4
    """

    def __init__(self, modulus, pattern=b"\x00"):
        if not isinstance(pattern, bytestringtype) or len(pattern) != 1:
            raise PaddingError("pattern expected to be bytes character")
        super(AutoAlignment, self).__init__()
        self.flagbuildnone = True
        self.modulus = modulus
        self.pattern = pattern

    def _parse(self, stream, context, path):
        modulus = self.modulus(context) if callable(self.modulus) else self.modulus
        stream_read(stream, (modulus - len(stream.rbuffer)) % modulus)

    def _build(self, obj, stream, context, path):
        modulus = self.modulus(context) if callable(self.modulus) else self.modulus
        bits_to_add = (modulus - len(stream.wbuffer)) % modulus
        stream_write(stream, self.pattern * bits_to_add, bits_to_add)

    def _sizeof(self, context, path):
        raise SizeofError("cannot calculate size")


tp_udh_struct = Prefixed(
    "user_data_header_length" / Byte,
    GreedyRange(
        Struct(
            "element_type" / tp_udh_elements,
            "element_data" / Prefixed(Byte, GreedyBytes)  # TODO: Replace with header elements parsing.
        )
    )
)


def is_gsm7(ctx):
    if ctx == Container():
        return False
    return ("character_set" not in ctx.tp_dcs) or (ctx.tp_dcs.character_set == dcs_character_set.GSM_7)


tp_ud_struct = IfThenElse(
    is_gsm7,
    Prefixed(
        "user_data_length" / SeptetsLengthAdapter(Byte),
        BitStruct(
            "user_data_header" / If(this._.tp_udhi, Bytewise(tp_udh_struct)),
            "_offset" / Tell,
            "user_data" / Gsm7Adapter(GreedyBytes),
            AutoAlignment(8),
        )
    ),
    Prefixed(
        "user_data_length" / Byte,
        Struct(
            "user_data_header" / If(this._.tp_udhi, tp_udh_struct),
            "user_data" / GreedyBytes
        )
    )
)
