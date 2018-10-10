import pytest
from construct import GreedyBytes, Bitwise
from gsm_layer3_protocol.sms_protocol.tp_user_data import Gsm7Adapter


@pytest.mark.parametrize("message,expected", [
    ("diafaan.com", b"\xe4\x74\xd8\x1c\x0e\xbb\x5d\xe3\x77\x1b"),
])
def test_building_gsm7(message, expected):
    assert Bitwise(Gsm7Adapter(GreedyBytes)).build(message) == expected


@pytest.mark.parametrize("data, message", [
    (b"\xe4\x74\xd8\x1c\x0e\xbb\x5d\xe3\x77\x1b", "diafaan.com"),
])
def test_parsing_gsm7(data, message):
    assert Bitwise(Gsm7Adapter(GreedyBytes)).parse(data) == message
