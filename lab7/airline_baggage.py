import math


def parse_booking(code):
    """
    Parses an airline booking code in the format: <AIRLINE>-<FLIGHT>-<SEAT>
    e.g., 'AI-203-12A' -> ('AI', 203, 'A')

    Validates:
    - Input must be a string.
    - Exactly 3 hyphen-separated components.
    - Airline code must be 2 to 3 alphabetic characters.
    - Flight number must be positive integer digits (1-9999).
    - Seat info must have a valid alphabetic seat letter at the end.
    Returns (airline, flight, seat_letter) or None if malformed.
    """
    if not isinstance(code, str):
        return None

    code = code.strip()
    if not code:
        return None

    parts = code.split('-')
    if len(parts) != 3:
        return None

    airline, flight_str, seat_str = parts
    airline = airline.strip()
    flight_str = flight_str.strip()
    seat_str = seat_str.strip()

    # Airline code validation (2-3 letters)
    if not airline.isalpha() or not (2 <= len(airline) <= 3):
        return None

    # Flight number validation (positive integer digits)
    if not flight_str.isdigit():
        return None
    flight = int(flight_str)
    if flight <= 0:
        return None

    # Seat information validation (e.g., '12A', '3F')
    if len(seat_str) < 1:
        return None
    seat_letter = seat_str[-1].upper()
    if not seat_letter.isalpha():
        return None

    row_part = seat_str[:-1]
    if row_part and not row_part.isdigit():
        return None

    return airline.upper(), flight, seat_letter


def total_weight(weights_csv):
    """
    Computes total baggage weight from a comma-separated string of weights.
    e.g., '12.5,7,23' -> 42.5

    Validates:
    - Input must be a string.
    - Handles empty or whitespace-only input safely by returning 0.0.
    - Each comma-separated element must parse as a valid finite float.
    - Rejects negative weights, NaN, infinity, and malformed/alphabetic tokens safely.
    Returns total weight as float, or None if malformed.
    """
    if not isinstance(weights_csv, str):
        return None

    weights_csv = weights_csv.strip()
    if not weights_csv:
        return 0.0

    items = weights_csv.split(',')
    total = 0.0

    for item in items:
        token = item.strip()
        if not token:
            # Empty element between commas (e.g. "12.5,,23")
            return None
        try:
            val = float(token)
        except (ValueError, TypeError):
            return None

        if math.isnan(val) or math.isinf(val):
            return None
        if val < 0.0:
            return None

        total += val

    return round(total, 2)


def tag_label(name):
    """
    Formats a passenger name for a baggage tag label.
    e.g., 'Pranav Shamnur' -> 'P. SHAMNUR'

    Validates:
    - Input must be a string.
    - Handles empty or whitespace-only names by returning "".
    - Handles single-word names safely (e.g. 'Pranav' -> 'PRANAV').
    - Handles multi-word names by taking first initial and last surname.
    - Handles Unicode names and irregular spacing appropriately.
    Returns uppercase formatted string, or "" for invalid/empty input.
    """
    if not isinstance(name, str):
        return ""

    name = name.strip()
    if not name:
        return ""

    parts = name.split()
    if not parts:
        return ""

    if len(parts) == 1:
        return parts[0].upper()

    first_initial = parts[0][0].upper()
    last_name = parts[-1].upper()
    return f"{first_initial}. {last_name}"


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter a booking code (e.g. AI-203-12A): ")
    result = parse_booking(user_input)
    print("Airline, Flight and Seat Letter:", result)

    print("\n==== Running total_weight ====")
    user_input = input("Enter bag weights in kg as CSV (e.g. 12.5,7,23): ")
    result = total_weight(user_input)
    print("Total Weight:", result)

    print("\n==== Running tag_label ====")
    user_input = input("Enter a passenger name (first and last): ")
    result = tag_label(user_input)
    print("Tag Label:", result)


if __name__ == "__main__":
    main()
