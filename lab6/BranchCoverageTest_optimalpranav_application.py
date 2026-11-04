
import pytest
from airline_baggage import baggage_fee, carry_on_ok, check_in_status


def test_invalid_cabin():
    with pytest.raises(ValueError):
        baggage_fee("first", 20, "domestic", False)


def test_negative_weight():
    with pytest.raises(ValueError):
        baggage_fee("economy", -1, "domestic", False)


def test_member_non_business():
    assert baggage_fee("economy", 20, "domestic", True) == 0


def test_non_member():
    assert baggage_fee("economy", 20, "domestic", False) == 100


def test_business_member():
    assert baggage_fee("business", 45, "domestic", True) == 100


def test_within_allowance():
    assert baggage_fee("business", 40, "domestic", False) == 0


def test_domestic_route():
    assert baggage_fee("economy", 20, "domestic", False) == 100


def test_international_route():
    assert baggage_fee("economy", 20, "international", False) == 225


def test_excess_exactly_twenty():
    assert baggage_fee("economy", 35, "domestic", False) == 400


def test_excess_above_twenty_domestic():
    assert baggage_fee("economy", 36, "domestic", False) == 420


def test_excess_above_twenty_international():
    assert baggage_fee("economy", 36, "international", False) == 2100


def test_infant_two_items():
    assert carry_on_ok(10, 2, True) is True


def test_infant_more_items():
    assert carry_on_ok(10, 3, True) is False


def test_non_infant_overweight():
    assert carry_on_ok(8, 1, False) is False


def test_non_infant_allowed_weight_one_item():
    assert carry_on_ok(7, 1, False) is True


def test_non_infant_multiple_items():
    assert carry_on_ok(5, 2, False) is False


def test_checkin_open_with_baggage():
    assert check_in_status(60, True, False) == "open"


def test_checkin_late_with_baggage():
    assert check_in_status(50, True, False) == "late"


def test_checkin_closed_with_baggage():
    assert check_in_status(44, True, False) == "closed"


def test_checkin_without_baggage():
    assert check_in_status(45, False, False) == "open"


def test_checkin_international():
    assert check_in_status(105, False, True) == "open"


def test_checkin_international_late():
    assert check_in_status(100, False, True) == "late"


def test_checkin_international_closed():
    assert check_in_status(89, False, True) == "closed"
