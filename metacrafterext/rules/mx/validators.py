"""
Validation functions for Mexican-specific identifiers.
"""
import re

from metacrafterext.rules.common.placeholders import rejects_repeated_digits


@rejects_repeated_digits
def validate_clabe(value):
    """
    Validates Mexican CLABE (Clave Bancaria Estandarizada) using MOD-10 checksum.
    
    CLABE format:
    - 18 digits total
    - First 3 digits: Bank code
    - Next 3 digits: Branch code (plaza)
    - Next 11 digits: Account number
    - Last digit: Check digit (MOD-10)
    
    MOD-10 algorithm:
    1. Multiply digits by weights: 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7
    2. Sum all products
    3. Check digit = (10 - (sum mod 10)) mod 10
    
    Args:
        value: CLABE string (18 digits)
        
    Returns:
        bool: True if valid CLABE, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    clabe = value.replace(' ', '').replace('-', '').replace('.', '')
    
    # Must be exactly 18 digits
    if len(clabe) != 18:
        return False
    
    if not clabe.isdigit():
        return False
    
    # MOD-10 checksum validation
    weights = [3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7]
    digits = [int(d) for d in clabe[:17]]  # First 17 digits
    check_digit = int(clabe[17])  # Last digit
    
    # Calculate weighted sum
    total = sum(digit * weight for digit, weight in zip(digits, weights))
    
    # Calculate check digit
    calculated_check = (10 - (total % 10)) % 10
    
    return calculated_check == check_digit



_MX_RFC = re.compile(r"^([A-ZÑ&]{3,4})[ -]?(\d{2})(\d{2})(\d{2})[ -]?([A-Z0-9]{2}[0-9A])$")


def validate_mx_rfc(value):
    """
    Validates the shape of a Mexican RFC (Registro Federal de Contribuyentes).

    Four letters for persons (three for companies), the date of birth or incorporation
    (YYMMDD) and a three-character homoclave: GODE561231GR8, ABC010203XY1. An IETF RFC
    reference ([RFC 1918]) in a column named RFC is not one (metacrafter-rules #69).

    Args:
        value: RFC string, optionally with a space or dash before the date and the homoclave

    Returns:
        bool: True if the value has the shape of an RFC with a real month and day
    """
    if not isinstance(value, str):
        return False
    match = _MX_RFC.match(value.strip().upper())
    if not match:
        return False
    month, day = int(match.group(3)), int(match.group(4))
    return 1 <= month <= 12 and 1 <= day <= 31


_MX_POSTCODE = re.compile(r"^\d{5}$")


def validate_mx_postcode(value):
    """A Mexican código postal: five digits, 01000 to 99999 (a float of a whole number, 6500.0,
    lost its leading zero). A ratio (0.0024) is not one."""
    text = str(value).strip()
    if re.fullmatch(r"\d{4}\.0", text):
        text = "0" + text[:-2]
    return bool(_MX_POSTCODE.match(text)) and text != "00000"
