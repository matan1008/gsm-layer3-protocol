from datetime import timedelta
import pytest
from construct import Byte
from gsm_layer3_protocol.sms_protocol.tpdu_parameters import \
    RelativeTpVpAdapter, tp_vp_enhanced, TpVpEnhancedSemiOctet, \
    TpVpEnhanced


@pytest.mark.parametrize("time_in_seconds,expected", [
    (timedelta(minutes=10).total_seconds(), b"\x01"),
    (timedelta(hours=15).total_seconds(), b"\x95"),
    (timedelta(days=3).total_seconds(), b"\xa9"),
    (timedelta(weeks=6).total_seconds(), b"\xc6")
])
def test_building_relative_validity_period(time_in_seconds, expected):
    assert RelativeTpVpAdapter(Byte).build(time_in_seconds) == expected


@pytest.mark.parametrize("data, time_in_seconds", [
    (b"\x01", timedelta(minutes=10).total_seconds()),
    (b"\x95", timedelta(hours=15).total_seconds()),
    (b"\xa9", timedelta(days=3).total_seconds()),
    (b"\xc6", timedelta(weeks=6).total_seconds())
])
def test_parsing_relative_validity_period(data, time_in_seconds):
    assert RelativeTpVpAdapter(Byte).parse(data) == time_in_seconds


def test_building_enhanced_semi_octet():
    assert tp_vp_enhanced.build(
        TpVpEnhanced(
            False,
            False,
            TpVpEnhancedSemiOctet(5, 3, 30)
        )
    ) == b"\x03\x50\x30\x03\x00\x00\x00"


def test_parsing_enhanced_semi_octet():
    assert tp_vp_enhanced.parse(
        b"\x03\x50\x30\x03\x00\x00\x00"
    ) == TpVpEnhanced(False, False, TpVpEnhancedSemiOctet(5, 3, 30))
