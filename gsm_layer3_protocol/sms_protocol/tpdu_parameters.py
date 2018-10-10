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


class TpDcsGeneralDataCodingIndicationNoMessageClass(Container):
    def __init__(self):
        super().__init__(coding_group=enums.dcs_coding_groups.GENERAL_DATA_CODING_INDICATION,
                         character_set=enums.dcs_character_set.GSM_7)


class TpDcsGeneralDataCodingIndication(Container):
    def __init__(self, compressed, character_set, message_class=None):
        super().__init__(coding_group=enums.dcs_coding_groups.GENERAL_DATA_CODING_INDICATION, compressed=compressed,
                         character_set=character_set, message_class=message_class)


class TpDcsMessageMarkedForAutomaticDeletionGroup(Container):
    def __init__(self, compressed, character_set, message_class=None):
        super().__init__(coding_group=enums.dcs_coding_groups.MESSAGE_MARKED_FOR_AUTOMATIC_DELETION_GROUP,
                         compressed=compressed, character_set=character_set, message_class=message_class)


class TpDcsDiscardMessage(Container):
    def __init__(self, indication_sense, indication_type):
        super().__init__(coding_group=enums.dcs_coding_groups.DISCARD_MESSAGE, indication_sense=indication_sense,
                         indication_type=indication_type)


class TpDcsStoreMessageGsm7(Container):
    def __init__(self, indication_sense, indication_type):
        super().__init__(coding_group=enums.dcs_coding_groups.STORE_MESSAGE_GSM7, indication_sense=indication_sense,
                         indication_type=indication_type)


class TpDcsStoreMessageUcs2(Container):
    def __init__(self, indication_sense, indication_type):
        super().__init__(coding_group=enums.dcs_coding_groups.STORE_MESSAGE_UCS2, indication_sense=indication_sense,
                         indication_type=indication_type)


class TpDcsDataCodingMessageClass(Container):
    def __init__(self, character_set, message_class):
        super().__init__(coding_group=enums.dcs_coding_groups.DATA_CODING_MESSAGE_CLASS, character_set=character_set,
                         message_class=message_class)


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


class TpDcsAdapter(Adapter):
    def _decode(self, obj, context, path):
        c = Container()
        if obj == 0:
            c.character_set = enums.dcs_character_set.GSM_7
            c.coding_group = enums.dcs_coding_groups.GENERAL_DATA_CODING_INDICATION
        elif (obj & 0xc0) >> 6 in (0, 1):
            c.compressed = bool(obj & 0b00100000)
            c.character_set = enums.dcs_character_set.decmapping[(obj & 0b00001100) >> 2]
            if obj & 0b00010000:
                c.message_class = obj & 0b00000011
            c.coding_group = enums.dcs_coding_groups.decmapping[(obj & 0b11000000) >> 6]
        elif (obj & 0xf0) >> 4 in (0xc, 0xd, 0xe):
            c.indication_sense = bool(obj & 0b00001000)
            c.indication_type = enums.dcs_indication_type.decmapping[obj & 0x3]
            c.character_set = (enums.dcs_character_set.UCS2
                               if (obj & 0xf0) >> 4 == 0xe
                               else enums.dcs_character_set.GSM_7)
            c.coding_group = enums.dcs_coding_groups.decmapping[(obj & 0xf0) >> 4]
        elif (obj & 0xf0) >> 4 == 0xf:
            c.character_set = enums.dcs_character_set.DATA_8BIT if (obj & 0b00000100) else enums.dcs_character_set.GSM_7
            c.message_class = obj & 0b00000011
            c.coding_group = enums.dcs_coding_groups.DATA_CODING_MESSAGE_CLASS
        return c

    def _encode(self, obj, context, path):
        if obj.coding_group == enums.dcs_coding_groups.GENERAL_DATA_CODING_INDICATION and obj.get("compressed") is None:
            return 0
        elif obj.coding_group in (enums.dcs_coding_groups.GENERAL_DATA_CODING_INDICATION,
                                  enums.dcs_coding_groups.MESSAGE_MARKED_FOR_AUTOMATIC_DELETION_GROUP):
            return (
                (int(obj.coding_group) << 6) | (int(obj.compressed) << 5) |
                (int(obj.get("message_class") is not None) << 4) | (int(obj.character_set) << 2) |
                (0 if obj.get("message_class") is None else int(obj.message_class))
            )
        elif obj.coding_group in (enums.dcs_coding_groups.DISCARD_MESSAGE,
                                  enums.dcs_coding_groups.STORE_MESSAGE_GSM7,
                                  enums.dcs_coding_groups.STORE_MESSAGE_UCS2):
            return (int(obj.coding_group) << 4) | (int(obj.indication_sense) << 3) | (int(obj.indication_type) << 3)
        elif obj.coding_group == enums.dcs_coding_groups.DATA_CODING_MESSAGE_CLASS:
            return (
                (int(obj.coding_group) << 4) | (int(obj.character_set == enums.dcs_character_set.DATA_8BIT) << 4) |
                obj.message_class
            )


tp_mti = enums.tp_mti
tp_mms = enums.tp_mms
tp_vpf = enums.tp_vpf
tp_sri = enums.tp_sri
tp_srr = enums.tp_srr
tp_mr = Octet
tp_oa = Bytewise(bcd_address)
tp_da = bcd_address
tp_pid = enums.tp_pid
tp_dcs = TpDcsAdapter(Octet)
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
