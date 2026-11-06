"""
Validation functions for German transport identifiers.
"""
import re

_DE_PLATE_RE = re.compile(r'^[A-ZÄÖÜ]{1,3}[- ]?[A-Z]{1,2} ?[1-9][0-9]{0,3}[EH]?$')


def validate_de_vehicle_plate(value):
    """
    Validates German vehicle license plate format (Kfz-Kennzeichen).

    German plate format:
    - Distinguishing sign of the district: 1-3 capital letters, umlauts
      possible (B, M, HH, LÖ)
    - A hyphen or a space (optional)
    - Identification letters: 1-2 capital letters without umlauts
    - An optional space and a number of 1-4 digits that does not start with 0
    - An optional suffix: E (electric vehicle) or H (historic vehicle)

    Examples:
    - B-AB 1234 (Berlin)
    - M-XY 123 (Munich)
    - AB CD 123H (historic vehicle)

    Args:
        value: German vehicle plate string

    Returns:
        bool: True if valid format, False otherwise
    """
    if not isinstance(value, str):
        return False
    return _DE_PLATE_RE.match(value.strip()) is not None
