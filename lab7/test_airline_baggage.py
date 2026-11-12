import math
import pytest
from hypothesis import given, strategies as st
from airline_baggage import parse_booking, total_weight, tag_label


# =====================================================================
# FUNCTION 1: parse_booking()
# =====================================================================

@given(st.one_of(st.text(), st.none(), st.integers(), st.floats()))
def test_parse_booking_no_crash(s):
    """
    Fuzz test parse_booking with arbitrary text, None, and numeric inputs.
    The function must never crash with unhandled exceptions.
    Any successfully parsed booking must satisfy structural invariants.
    """
    try:
        result = parse_booking(s)
        if result is not None:
            assert isinstance(result, tuple) and len(result) == 3, (
                f"Expected 3-tuple, got {type(result)}: {result}"
            )
            airline, flight, seat = result
            assert isinstance(airline, str) and len(airline) > 0, "Airline must be a non-empty string"
            assert isinstance(flight, int) and flight > 0, "Flight number must be a positive integer"
            assert isinstance(seat, str) and len(seat) == 1 and seat.isalpha(), "Seat letter must be a single alphabetic char"
    except Exception as e:
        pytest.fail(f"parse_booking crashed on input {repr(s)} with {type(e).__name__}: {e}")


@given(st.one_of(
    st.just(""),
    st.just("AI20312A"),           # Missing separators
    st.just("AI-203-12-A"),        # Extra separators
    st.just("-203-12A"),           # Missing airline
    st.just("AI--12A"),            # Missing flight number
    st.just("AI-XYZ-12A"),         # Non-integer flight number
    st.just("AI-203-"),            # Missing seat info
    st.just("AI-0-12A"),           # Zero/invalid flight number
    st.just("AI--203-12A"),        # Negative flight number
    st.just("123-203-12A"),        # Numeric airline code
    st.just("AI-203-12"),          # Missing seat letter
))
def test_parse_booking_malformed_rejection(malformed):
    """
    Property test verifying that malformed booking codes are safely rejected (returns None)
    without raising uncaught exceptions.
    """
    try:
        result = parse_booking(malformed)
        assert result is None, f"Expected None for malformed input {repr(malformed)}, got {result}"
    except Exception as e:
        pytest.fail(f"parse_booking crashed on malformed input {repr(malformed)} with {type(e).__name__}: {e}")


@given(
    airline=st.from_regex(r'^[A-Za-z]{2,3}$', fullmatch=True),
    flight=st.integers(min_value=1, max_value=9999),
    row=st.integers(min_value=1, max_value=99),
    seat_letter=st.from_regex(r'^[A-Za-z]$', fullmatch=True)
)
def test_parse_booking_valid_inputs(airline, flight, row, seat_letter):
    """
    Property test verifying that valid booking codes are parsed correctly
    into (AIRLINE, flight_number, SEAT_LETTER).
    """
    code = f"{airline}-{flight}-{row}{seat_letter}"
    result = parse_booking(code)
    assert result == (airline.upper(), flight, seat_letter.upper()), (
        f"Incorrect parse for valid code {code}: got {result}"
    )


# =====================================================================
# FUNCTION 2: total_weight()
# =====================================================================

@given(st.one_of(st.text(), st.none(), st.integers(), st.floats()))
def test_total_weight_no_crash(s):
    """
    Fuzz test total_weight with arbitrary text, None, and numeric inputs.
    The function must never crash with unhandled exceptions.
    Valid total weight must be a finite, non-negative number.
    """
    try:
        result = total_weight(s)
        if result is not None:
            assert isinstance(result, (int, float)), f"Expected numeric result, got {type(result)}"
            assert not math.isnan(result), "Total weight cannot be NaN"
            assert not math.isinf(result), "Total weight cannot be infinite"
            assert result >= 0.0, f"Total weight cannot be negative: {result}"
    except Exception as e:
        pytest.fail(f"total_weight crashed on input {repr(s)} with {type(e).__name__}: {e}")


@given(st.one_of(
    st.just("abc"),
    st.just("12.5,abc,20"),
    st.just("-5"),
    st.just("10,-2,5"),
    st.just("12.5,,23"),
    st.just(",,"),
    st.just("nan"),
    st.just("inf"),
    st.just("-inf"),
    st.just("12.5, nan, 20"),
    st.just("12.5, inf, 20"),
))
def test_total_weight_malformed_rejection(malformed):
    """
    Property test verifying that negative weights, NaN, inf, alphabetic,
    and missing CSV values are safely rejected (returns None) without crashing.
    """
    try:
        result = total_weight(malformed)
        assert result is None, f"Expected None for invalid input {repr(malformed)}, got {result}"
    except Exception as e:
        pytest.fail(f"total_weight crashed on malformed input {repr(malformed)} with {type(e).__name__}: {e}")


@given(st.lists(
    st.floats(min_value=0.0, max_value=500.0, allow_nan=False, allow_infinity=False),
    min_size=1,
    max_size=10
))
def test_total_weight_valid_inputs(weights):
    """
    Property test verifying that valid CSV lists of positive baggage weights
    are summed accurately.
    """
    csv_str = ",".join(f"{w:.2f}" for w in weights)
    expected_sum = sum(round(w, 2) for w in weights)
    result = total_weight(csv_str)
    assert result is not None, f"Expected numeric sum for valid CSV {csv_str}"
    assert math.isclose(result, expected_sum, rel_tol=1e-4, abs_tol=1e-4), (
        f"Sum mismatch: expected ~{expected_sum}, got {result}"
    )


# =====================================================================
# FUNCTION 3: tag_label()
# =====================================================================

@given(st.one_of(st.text(), st.none(), st.integers(), st.floats()))
def test_tag_label_no_crash(s):
    """
    Fuzz test tag_label with arbitrary text, unicode, None, and numeric inputs.
    The function must never crash with IndexError or AttributeError.
    Any non-empty tag label must be an uppercase string.
    """
    try:
        result = tag_label(s)
        if result is not None:
            assert isinstance(result, str), f"Expected str result, got {type(result)}"
            assert result == result.upper(), f"Tag label must be uppercase: {result}"
    except Exception as e:
        pytest.fail(f"tag_label crashed on input {repr(s)} with {type(e).__name__}: {e}")


@given(
    st.one_of(
        st.just(""),
        st.just("   "),
        st.just("\t\n"),
        st.just("Pranav"),                       # Single-word name
        st.just("  Pranav  "),                   # Single-word with spaces
        st.just("Pranav Shamnur"),               # Standard two-word name
        st.just("  Pranav   Shamnur  "),         # Two-word with irregular spacing
        st.just("Pranav Kumar Shamnur"),         # Three-word name
        st.just("José García"),                  # Unicode name
        st.just("Émile Zola"),                   # Unicode accented initial
    )
)
def test_tag_label_names_variety(name):
    """
    Property test verifying tag_label formatting across single-word, multi-word,
    Unicode, and whitespace-only name inputs.
    """
    try:
        result = tag_label(name)
        assert isinstance(result, str), f"Expected string for {repr(name)}, got {type(result)}"
        words = name.split()
        if not words:
            assert result == "", f"Expected empty string for whitespace/empty name, got {repr(result)}"
        elif len(words) == 1:
            assert result == words[0].upper(), (
                f"Expected single name {words[0].upper()}, got {repr(result)}"
            )
        else:
            first_initial = words[0][0].upper()
            last_name = words[-1].upper()
            assert result == f"{first_initial}. {last_name}", (
                f"Expected '{first_initial}. {last_name}', got {repr(result)}"
            )
    except Exception as e:
        pytest.fail(f"tag_label crashed on name {repr(name)} with {type(e).__name__}: {e}")
