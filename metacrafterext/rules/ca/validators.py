"""
Validation functions for Canadian-specific identifiers.
"""


def validate_ca_sin(value):
    """
    Validates a Canadian Social Insurance Number (SIN).

    Rules:
    - Exactly 9 digits (spaces and dashes are ignored).
    - Must not be all identical digits.
    - Passes the Luhn checksum.

    Args:
        value: SIN string (may include spaces or dashes)

    Returns:
        bool: True if the value is a valid SIN, False otherwise.
    """
    if not isinstance(value, str):
        return False

    sin = value.replace(' ', '').replace('-', '')

    if len(sin) != 9 or not sin.isdigit():
        return False

    if len(set(sin)) == 1:
        return False

    # Luhn checksum.
    total = 0
    for i, ch in enumerate(sin):
        digit = int(ch)
        if i % 2 == 1:  # every second digit (0-indexed) is doubled
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return total % 10 == 0
