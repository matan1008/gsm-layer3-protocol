from datetime import timedelta
from construct import *
import gsm_layer3_protocol.enums as enums
from gsm_layer3_protocol.sms_protocol.called_party_bcd_address import bcd_address


class TpScts(Container):
    def __init__(self, year, month, day, hour, minute, second, gmt):
        super().__init__(year=year, month=month, day=day, hour=hour, minute=minute, second=second, gmt=gmt)


class TpVpAbsolute(Container):
    def __init__(self, year, month, day, hour, minute, second, gmt):
        super().__init__(year=year, month=month, day=day, hour=hour, minute=minute, second=second, gmt=gmt,
                         _tp_vpf=enums.tp_vpf.ABSOLUTE_FORMAT)


class TpVpRelative(Container):
    def __init__(self, second):
        super().__init__(second=second, _tp_vpf=enums.tp_vpf.RELATIVE_FORMAT)


class TpVpEnhancedRelative(Container):
    def __init__(self, second):
        super().__init__(second=second, _validity_period_format=enums.tp_vp_enhanced_format.RELATIVE_FORMAT)


class TpVpEnhancedInteger(Container):
    def __init__(self, second):
        super().__init__(second=second, _validity_period_format=enums.tp_vp_enhanced_format.RELATIVE_INTEGER)


class TpVpEnhancedSemiOctet(Container):
    def __init__(self, hour, minute, second):
        super().__init__(hour=hour, minute=minute, second=second,
                         _validity_period_format=enums.tp_vp_enhanced_format.SEMI_OCTET)


class TpVpEnhanced(Container):
    def __init__(self, extension_bit, single_shot_sm, validity_period):
        super().__init__(extension_bit=extension_bit, single_shot_sm=single_shot_sm,
                         validity_period_format=validity_period._validity_period_format,
                         validity_period=validity_period,
                         _tp_vpf=enums.tp_vpf.ENHANCED_FORMAT)


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


class RelativeTpVpAdapter(Adapter):
    def _decode(self, obj, context, path):
        if obj <= 143:
            period = timedelta(minutes=((obj + 1) * 5))
        elif obj <= 167:
            period = timedelta(hours=12, minutes=((obj - 143) * 30))
        elif obj <= 196:
            period = timedelta(days=(obj - 166))
        else:
            # Better checking <= 255 and raising an exception
            period = timedelta(weeks=(obj - 192))
        return period.total_seconds()

    def _encode(self, obj, context, path):
        if timedelta(seconds=obj) <= timedelta(hours=12):
            return int(((obj / 60) / 5) - 1)
        elif timedelta(seconds=obj) <= timedelta(days=1):
            return int(((obj - (12 * 60 * 60)) / (30 * 60)) + 143)
        elif timedelta(seconds=obj) <= timedelta(days=30):
            return int((obj / timedelta(days=1).total_seconds()) + 166)
        else:
            # Better checking <= 63 weeks and raising an exception
            return int((obj / timedelta(days=7).total_seconds()) + 192)


tp_mti = enums.tp_mti
tp_mms = enums.tp_mms
tp_vpf = enums.tp_vpf
tp_sri = enums.tp_sri
tp_srr = enums.tp_srr
tp_mr = Octet
tp_oa = bcd_address
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
tp_vp_relative = Struct("second" / RelativeTpVpAdapter(Octet))
tp_vp_absolute = Bytewise(Struct(
    "year" / DigitNibblesAdapter(Byte),
    "month" / DigitNibblesAdapter(Byte),
    "day" / DigitNibblesAdapter(Byte),
    "hour" / DigitNibblesAdapter(Byte),
    "minute" / DigitNibblesAdapter(Byte),
    "second" / DigitNibblesAdapter(Byte),
    "gmt" / GmtAdapter(Byte)
))
tp_vp_enhanced = FixedSized(7, BitStruct(
    "extension_bit" / Flag,
    "single_shot_sm" / Flag,
    Padding(3),
    "validity_period_format" / enums.tp_vp_enhanced_format,
    "validity_period" / Bytewise(Switch(
        this.validity_period_format,
        {
            enums.tp_vp_enhanced_format.RELATIVE_FORMAT: Struct("second" / RelativeTpVpAdapter(Byte)),
            enums.tp_vp_enhanced_format.RELATIVE_INTEGER: Struct("second" / Byte),
            enums.tp_vp_enhanced_format.SEMI_OCTET: Struct(
                "hour" / DigitNibblesAdapter(Byte),
                "minute" / DigitNibblesAdapter(Byte),
                "second" / DigitNibblesAdapter(Byte)
            )
        }
    ))
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
tp_rp = Flag
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
tp_rd = enums.tp_rd
tp_lp = enums.tp_lp
