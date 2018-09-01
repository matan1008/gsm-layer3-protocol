from construct import *
from gsm_layer3_protocol.enums import tp_mti as tp_mti_enum, tp_fcs as tp_fcs_enum, tp_pid as tp_pid_enum


class TpScts(Container):
    def __init__(self, year, month, day, hour, minute, second, gmt):
        super().__init__(year=year, month=month, day=day, hour=hour, minute=minute, second=second, gmt=gmt)


class DigitNibblesAdapter(Adapter):
    def _decode(self, obj, context, path):
        return (obj & 0x0f) * 10 + ((obj & 0xf0) >> 4)

    def _encode(self, obj, context, path):
        return (int(obj / 10) & 0x0f) + ((obj % 10) << 4)


class GmtAdapter(Adapter):
    def _decode(self, obj, context, path):
        sign = -1 if obj & 0x08 else 1
        tz = ((obj & 0x07) * 10 + ((obj & 0xf0) >> 4)) / 4.0
        return sign * tz

    def _encode(self, obj, context, path):
        sign = 0 if obj >= 0 else 0x08
        tz_min = int(abs(obj) * 4.0)
        return ((int(tz_min / 10) & 0x07) + ((tz_min % 10) << 4)) | sign


tp_udhi = Flag
tp_mti = tp_mti_enum
tp_fcs = tp_fcs_enum
tp_pi = Struct(
    Padding(5),
    "tp_udl" / Flag,
    "tp_dcs" / Flag,
    "tp_pid" / Flag
)
tp_scts = Bytewise(Struct(
    "year" / DigitNibblesAdapter(Byte),
    "month" / DigitNibblesAdapter(Byte),
    "day" / DigitNibblesAdapter(Byte),
    "hour" / DigitNibblesAdapter(Byte),
    "minute" / DigitNibblesAdapter(Byte),
    "second" / DigitNibblesAdapter(Byte),
    "gmt" / GmtAdapter(Byte)
))
tp_pid = tp_pid_enum
tp_dcs = Octet # TODO: Make it a nice structure or enum
