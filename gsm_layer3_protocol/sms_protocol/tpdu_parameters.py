from construct import *
import gsm_layer3_protocol.enums as enums
from gsm_layer3_protocol.sms_protocol.called_party_bcd_address import bcd_address


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


tp_mti = enums.tp_mti
tp_mms = Flag
tp_srr = enums.tp_srr
tp_mr = Octet
tp_da = bcd_address
tp_pid = enums.tp_pid
tp_dcs = Octet  # TODO: Make it a nice structure or enum
tp_scts = Bytewise(Struct(
    "year" / DigitNibblesAdapter(Byte),
    "month" / DigitNibblesAdapter(Byte),
    "day" / DigitNibblesAdapter(Byte),
    "hour" / DigitNibblesAdapter(Byte),
    "minute" / DigitNibblesAdapter(Byte),
    "second" / DigitNibblesAdapter(Byte),
    "gmt" / GmtAdapter(Byte)
))
tp_dt = Bytewise(Struct(
    "year" / DigitNibblesAdapter(Byte),
    "month" / DigitNibblesAdapter(Byte),
    "day" / DigitNibblesAdapter(Byte),
    "hour" / DigitNibblesAdapter(Byte),
    "minute" / DigitNibblesAdapter(Byte),
    "second" / DigitNibblesAdapter(Byte),
    "gmt" / GmtAdapter(Byte)
))
tp_ra = bcd_address
tp_st = enums.tp_st
tp_mn = Octet
tp_ct = enums.tp_ct
tp_fcs = enums.tp_fcs
tp_udhi = Flag
tp_srq = enums.tp_srq
tp_pi = Struct(
    Padding(5),
    "tp_udl" / Flag,
    "tp_dcs" / Flag,
    "tp_pid" / Flag
)
tp_lp = enums.tp_lp
