import pytest
from gsm_layer3_protocol.enums import bcd_number_plan as plan, \
    bcd_type_of_number as number_type
from gsm_layer3_protocol.sms_protocol.called_party_bcd_address import \
    AddressField, bcd_address, service_center_address


@pytest.mark.parametrize("type_of_number,number_plan,number,expected", [
    (number_type.UNKNOWN, plan.UNKNOWN, "00", b"\x02\x80\x00"),
    (number_type.ALPHANUMERIC, plan.UNKNOWN, "005", b"\x03\xd0\x00\xf5"),
    (number_type.INTERNATIONAL_NUMBER, plan.NATIONAL_NUMBERING_PLAN,
     "#4155552671", b"\x0b\x98\x4b\x51\x55\x25\x76\xf1")
])
def test_building_bcd_address(type_of_number, number_plan, number, expected):
    assert bcd_address.build(
        AddressField(type_of_number, number_plan, number)) == expected


@pytest.mark.parametrize("data, type_of_number,number_plan,number", [
    (b"\x02\x80\x00", number_type.UNKNOWN, plan.UNKNOWN, "00"),
    (b"\x03\xd0\x00\xf5", number_type.ALPHANUMERIC, plan.UNKNOWN, "005"),
    (b"\x0b\x98\x4b\x51\x55\x25\x76\xf1", number_type.INTERNATIONAL_NUMBER,
     plan.NATIONAL_NUMBERING_PLAN, "#4155552671")
])
def test_parsing_bcd_address(data, type_of_number, number_plan, number):
    assert bcd_address.parse(data) == AddressField(type_of_number, number_plan,
                                                   number)


@pytest.mark.parametrize("type_of_number,number_plan,number,expected", [
    (number_type.UNKNOWN, plan.UNKNOWN, "00", b"\x02\x80\x00"),
    (number_type.ALPHANUMERIC, plan.UNKNOWN, "005", b"\x03\xd0\x00\xf5"),
    (number_type.INTERNATIONAL_NUMBER, plan.NATIONAL_NUMBERING_PLAN,
     "#4155552671", b"\x07\x98\x4b\x51\x55\x25\x76\xf1")
])
def test_building_service_center_address(type_of_number, number_plan, number,
                                         expected):
    assert service_center_address.build(
        AddressField(type_of_number, number_plan, number)) == expected


@pytest.mark.parametrize("data, type_of_number,number_plan,number", [
    (b"\x02\x80\x00", number_type.UNKNOWN, plan.UNKNOWN, "00"),
    (b"\x03\xd0\x00\xf5", number_type.ALPHANUMERIC, plan.UNKNOWN, "005"),
    (b"\x07\x98\x4b\x51\x55\x25\x76\xf1", number_type.INTERNATIONAL_NUMBER,
     plan.NATIONAL_NUMBERING_PLAN, "#4155552671")
])
def test_parsing_service_center_address(data, type_of_number, number_plan,
                                        number):
    assert service_center_address.parse(data) == AddressField(type_of_number,
                                                              number_plan,
                                                              number)
