"""
Validation functions for German-specific identifiers.
"""


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


def validate_de_hrb(value):
    """
    Validates German HRB (Handelsregisternummer) format.
    
    German HRB format:
    - Single uppercase letter (A-Z) representing the registry court
    - Followed by 1-6 digits
    - Total length: 2-7 characters
    - Common prefixes: B (Berlin), H (Hamburg), M (Munich), etc.
    
    Args:
        value: HRB number string (may include spaces or dashes)
        
    Returns:
        bool: True if valid HRB format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    hrb = value.replace(' ', '').replace('-', '').replace('.', '').upper()
    
    # Length check: 2-7 characters total
    # But number part must be 1-6 digits, so min is 2 (1 letter + 1 digit), max is 7 (1 letter + 6 digits)
    if len(hrb) < 2 or len(hrb) > 7:
        return False
    
    # Format: Single letter + 1-6 digits
    if not hrb[0].isalpha() or not hrb[0].isupper():
        return False
    
    letter = hrb[0]
    number_part = hrb[1:]
    
    # Number part must be 1-6 digits
    if len(number_part) < 1 or len(number_part) > 6:
        return False
    
    if not number_part.isdigit():
        return False
    
    # Check for obviously invalid patterns
    # All zeros
    if number_part == '0' * len(number_part):
        return False
    
    # Common valid registry court letters (not exhaustive, but helps filter)
    # All uppercase letters A-Z are technically valid for different courts
    # We accept any uppercase letter as valid
    
    # Basic format validation passed
    return True


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

