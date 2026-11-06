"""
Validation functions for German-specific identifiers.
"""
import re


def validate_de_steuer_id(value):
    """
    Validates a German tax identification number (Steuerliche Identifikationsnummer / IdNr).

    Rules:
    - Exactly 11 digits (separators and spaces are ignored).
    - The first digit must not be 0.
    - Among the first 10 digits exactly one digit must repeat (appear two or
      three times) while at least one digit is absent -- the official
      structural constraint.
    - The 11th digit is a check digit computed with the ISO 7064 MOD 11,10
      algorithm over the first 10 digits.

    Args:
        value: tax id string (may include spaces, dots or dashes)

    Returns:
        bool: True if the value is a structurally valid Steuer-IdNr.
    """
    if not isinstance(value, str):
        return False

    idnr = value.replace(' ', '').replace('.', '').replace('-', '').replace('/', '')

    if len(idnr) != 11 or not idnr.isdigit():
        return False

    if idnr[0] == '0':
        return False

    first_ten = idnr[:10]

    # Structural rule: exactly one digit repeats among the first ten digits.
    counts = {}
    for ch in first_ten:
        counts[ch] = counts.get(ch, 0) + 1
    repeated = [c for c, n in counts.items() if n > 1]
    if len(repeated) != 1:
        return False
    if counts[repeated[0]] > 3:
        return False

    # ISO 7064 MOD 11,10 check digit.
    product = 10
    for ch in first_ten:
        digit = int(ch)
        s = (digit + product) % 10
        if s == 0:
            s = 10
        product = (s * 2) % 11
    check = (11 - product) % 10

    return check == int(idnr[10])


def _iso7064_mod11_10_check(digits):
    """Check digit of a digit string by ISO 7064 MOD 11,10."""
    product = 10
    for ch in digits:
        total = (int(ch) + product) % 10
        if total == 0:
            total = 10
        product = (total * 2) % 11
    return (11 - product) % 10


_DE_HRB_RE = re.compile(r'^(?:HRA|HRB|GnR|PR|VR) ?[1-9][0-9]{0,5}(?: ?[A-Z]{1,3})?$')


def validate_de_hrb(value):
    """
    Validates a German commercial register number (Handelsregisternummer).

    The number is the register section and the entry number of up to six
    digits, optionally followed by a suffix of the court, such as B for
    Berlin-Charlottenburg:

    - Section: HRA (sole traders and partnerships), HRB (corporations),
      GnR (cooperatives), PR (partnerships of liberal professions) or VR
      (associations).
    - An optional space, then 1-6 digits that do not start with 0.
    - An optional suffix of 1-3 capital letters, optionally after a space.

    Examples: ``HRA 11223``, ``HRB 12345 B``, ``GnR 11223``.

    Args:
        value: register number string

    Returns:
        bool: True if the value has the format of a register number.
    """
    if not isinstance(value, str):
        return False
    return _DE_HRB_RE.match(value.strip()) is not None


def validate_de_ust(value):
    """
    Validates a German VAT identification number (USt-IdNr.).

    The number is ``DE`` and 9 digits; the first digit is not 0 and the last
    one is a check digit of the first eight by ISO 7064 MOD 11,10.

    Args:
        value: USt-IdNr. string such as ``DE136695976``

    Returns:
        bool: True if the value is a valid USt-IdNr.
    """
    if not isinstance(value, str):
        return False
    number = value.strip()
    if len(number) != 11 or not number.startswith('DE'):
        return False
    digits = number[2:]
    if not digits.isdigit() or not digits.isascii() or digits[0] == '0':
        return False
    return _iso7064_mod11_10_check(digits[:8]) == int(digits[8])


def validate_de_ops(value):
    """
    Validates German OPS (Operationen- und Prozedurenschlüssel) code format.
    
    German OPS code format:
    - 1-5 digits (main code)
    - Optional: dot followed by 1-2 digits (subcode)
    - Total: 3-7 characters
    
    Format examples:
    - 1-12 (without dot)
    - 1-12.1 (with dot and 1 digit subcode)
    - 1-12.12 (with dot and 2 digit subcode)
    
    Common structure:
    - First digit: category (1-9)
    - Next 1-2 digits: subcategory
    - Optional dot and subcode
    
    Args:
        value: OPS code string (may include dot separator)
        
    Returns:
        bool: True if valid OPS format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    ops = value.replace(' ', '').replace('-', '').strip()
    
    # Length check: 3-7 characters
    if len(ops) < 3 or len(ops) > 7:
        return False
    
    # Split by dot if present
    if '.' in ops:
        parts = ops.split('.')
        if len(parts) != 2:
            return False
        
        main_part = parts[0]
        sub_part = parts[1]
        
        # Main part: 1-5 digits
        if not main_part.isdigit() or len(main_part) < 1 or len(main_part) > 5:
            return False
        
        # Sub part: 1-2 digits
        if not sub_part.isdigit() or len(sub_part) < 1 or len(sub_part) > 2:
            return False
    else:
        # No dot: must be 1-5 digits
        if not ops.isdigit() or len(ops) < 1 or len(ops) > 5:
            return False
    
    # Additional validation: first digit should be 1-9 (not 0)
    # This helps filter out years and other common 4-digit numbers
    first_char = ops[0] if '.' not in ops else ops.split('.')[0][0]
    if first_char == '0':
        return False
    
    # Check for obviously invalid patterns
    # Reject common year patterns (20XX, 19XX) when they appear as main code
    if '.' not in ops and len(ops) == 4:
        if ops.startswith('19') or ops.startswith('20'):
            # Could be a year, but OPS codes can also start with 1 or 2
            # Only reject if it's clearly a year range (1900-2099)
            try:
                year_num = int(ops)
                if 1900 <= year_num <= 2099:
                    return False
            except ValueError:
                pass
    
    return True

