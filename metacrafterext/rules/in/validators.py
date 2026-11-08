"""
Validation functions for Indian-specific identifiers.
"""

from metacrafterext.rules.common.identifiers import _verhoeff_is_valid
from metacrafterext.rules.common.placeholders import rejects_repeated_digits

# Fourth character of a PAN: the holder type (P person, C company, H Hindu undivided
# family, F firm, A association of persons, T trust, B body of individuals, L local
# authority, J artificial juridical person, G government).
_PAN_HOLDER_TYPES = frozenset("PCHFATBLJG")


@rejects_repeated_digits
def validate_in_aadhaar(value):
    """
    Validates an Indian Aadhaar number.

    An Aadhaar number has 12 digits, does not start with 0 or 1 and ends with a
    Verhoeff check digit. Spaces and hyphens between digit groups are allowed
    (``2345 6789 0124``).

    Args:
        value: Aadhaar number string

    Returns:
        bool: True if the value is a valid Aadhaar number, False otherwise
    """
    if not isinstance(value, str):
        return False

    number = value.replace(' ', '').replace('-', '')
    if len(number) != 12 or not number.isdigit():
        return False

    if number[0] in '01':
        return False

    return _verhoeff_is_valid(number)


def validate_in_pan(value):
    """
    Validates the format of an Indian PAN (Permanent Account Number).

    A PAN has 10 characters: 5 uppercase letters, 4 digits and 1 uppercase letter.
    The fourth letter is the holder type (P, C, H, F, A, T, B, L, J or G). The last
    letter is a check character; its algorithm is not published, so it is not checked.

    Format: AAAPA9999A
    Example: ABCPE1234F

    Args:
        value: PAN string

    Returns:
        bool: True if the value has the PAN format, False otherwise
    """
    if not isinstance(value, str):
        return False

    pan = value.strip()
    if len(pan) != 10 or not pan.isascii():
        return False

    if not (pan[:5].isalpha() and pan[:5].isupper()):
        return False

    if not pan[5:9].isdigit():
        return False

    if not (pan[9].isalpha() and pan[9].isupper()):
        return False

    return pan[3] in _PAN_HOLDER_TYPES


def validate_ifsc(value):
    """
    Validates Indian IFSC (Indian Financial System Code) format.
    
    IFSC format:
    - 4 uppercase letters (bank code)
    - 0 (zero, always present)
    - 6 alphanumeric characters (branch code)
    - Total: 11 characters
    
    Format: XXXX0XXXXXX
    Example: HDFC0001234, SBIN0005678
    
    Args:
        value: IFSC string (11 characters)
        
    Returns:
        bool: True if valid IFSC format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    ifsc = value.replace(' ', '').replace('-', '').upper()
    
    # Must be exactly 11 characters
    if len(ifsc) != 11:
        return False
    
    # Format: 4 letters + 0 + 6 alphanumeric
    if not ifsc[:4].isalpha() or not ifsc[:4].isupper():
        return False
    
    if ifsc[4] != '0':
        return False
    
    if not ifsc[5:].isalnum():
        return False
    
    if len(ifsc[5:]) != 6:
        return False
    
    # Check for obviously invalid patterns
    if ifsc[5:] == '000000':
        return False
    
    return True

