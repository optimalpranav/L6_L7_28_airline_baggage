import pytest
from airline_baggage import baggage_fee, carry_on_ok, check_in_status


def test_invalid_cabin():
    with pytest.raises(ValueError):
        baggage_fee("first", 20, "domestic", False)


def test_negative_weight():
    with pytest.raises(ValueError):
        baggage_fee("economy", -5, "domestic", False)


def test_member_discount():
    assert baggage_fee("economy", 20, "domestic", True) == 0


def test_business_member():
    assert baggage_fee("business", 45, "domestic", True) == 100


def test_domestic_excess():
    assert baggage_fee("economy", 20, "domestic", False) == 100


def test_international_excess():
    assert baggage_fee("economy", 20, "international", False) == 225


def test_high_excess_domestic():
    assert baggage_fee("economy", 40, "domestic", False) == 1000


def test_high_excess_international():
    assert baggage_fee("economy", 40, "international", False) == 2500


def test_infant_two_items():
    assert carry_on_ok(10, 2, True) is True


def test_infant_more_than_two_items():
    assert carry_on_ok(5, 3, True) is False


def test_carry_on_overweight():
    assert carry_on_ok(8, 1, False) is False


def test_carry_on_multiple_items():
    assert carry_on_ok(5, 2, False) is False


def test_checkin_open():
    assert check_in_status(100, True, False) == "open"


def test_checkin_late():
    assert check_in_status(50, True, False) == "late"


def test_checkin_closed():
    assert check_in_status(40, True, False) == "closed"


def test_international_checkin():
    assert check_in_status(120, False, True) == "open"