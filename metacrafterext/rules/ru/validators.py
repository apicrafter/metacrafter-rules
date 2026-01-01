"""
Validation functions for Russian-specific identifiers.
"""


def validate_ru_medicine_reg(value):
    """
    Validates Russian medicine registration number format.
    
    Russian medicine registration format:
    - Format 1: ЛС-XXXXXX (6 digits)
    - Format 2: ЛП-XXXXXX (6 digits)
    - Format 3: ЛСР-XXXXXX/XX (6 digits + / + 2 digits)
    
    Where:
    - ЛС = Лекарственное средство (Medicine)
    - ЛП = Лекарственный препарат (Drug)
    - ЛСР = Лекарственное средство регистрационный (Registered medicine)
    
    Args:
        value: Medicine registration number string
        
    Returns:
        bool: True if valid format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    reg = value.strip()
    
    # Format 1 & 2: ЛС-XXXXXX or ЛП-XXXXXX (9 characters: 2 letters + dash + 6 digits)
    if len(reg) == 9:
        if reg.startswith('ЛС-') or reg.startswith('ЛП-'):
            digits = reg[3:]
            if digits.isdigit() and len(digits) == 6:
                # Check for obviously invalid patterns
                if digits == '000000':
                    return False
                return True
    
    # Format 3: ЛСР-XXXXXX/XX (13 characters: 3 letters + dash + 6 digits + / + 2 digits)
    if len(reg) == 13:
        if reg.startswith('ЛСР-'):
            parts = reg[4:].split('/')
            if len(parts) == 2:
                main_part = parts[0]
                sub_part = parts[1]
                if (main_part.isdigit() and len(main_part) == 6 and
                    sub_part.isdigit() and len(sub_part) == 2):
                    # Check for obviously invalid patterns
                    if main_part == '000000':
                        return False
                    return True
    
    return False


def validate_ru_equity_securities_reg(value):
    """
    Validates Russian equity securities registration number format.
    
    Russian equity securities registration format:
    - 7 characters: 1 digit + 5 digits + 1 letter
    - Format: X-XXXXX-X
    
    The format represents:
    - First digit: Registration type/category
    - Next 5 digits: Sequential number
    - Last letter: Check character or category
    
    Args:
        value: Registration number string (may include separators)
        
    Returns:
        bool: True if valid format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    reg = value.replace(' ', '').replace('-', '').replace('.', '').upper()
    
    # Must be exactly 7 characters
    if len(reg) != 7:
        return False
    
    # Format: 1 digit + 5 digits + 1 letter
    if not (reg[0].isdigit() and 
            reg[1:6].isdigit() and 
            reg[6].isalpha()):
        return False
    
    # Check for obviously invalid patterns
    if reg[:6] == '000000':
        return False
    
    # Additional validation: first digit should be 1-9 (not 0)
    if reg[0] == '0':
        return False
    
    return True


def validate_ru_snils(value):
    """
    Validates Russian SNILS (СНИЛС) number with checksum validation.
    
    SNILS format: XXX-XXX-XXX XX (11 digits total: 9 digits + 2 check digits)
    
    Checksum algorithm:
    1. Take first 9 digits
    2. Multiply each digit by its position (1-9)
    3. Sum all products
    4. If sum < 100, checksum is the sum (formatted as 2 digits)
    5. If sum == 100 or 101, checksum is 00
    6. If sum > 101, checksum is sum % 101
    7. If checksum == 100, it becomes 00
    
    Args:
        value: SNILS number string (may include dashes and spaces)
        
    Returns:
        bool: True if valid format and checksum, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    # Remove separators
    snils = value.replace('-', '').replace(' ', '')
    
    # Must be exactly 11 digits
    if len(snils) != 11 or not snils.isdigit():
        return False
    
    # Extract first 9 digits and checksum (last 2 digits)
    digits = snils[:9]
    checksum = int(snils[9:11])
    
    # Calculate checksum
    total = sum(int(digit) * (i + 1) for i, digit in enumerate(digits))
    
    # Apply checksum rules
    if total < 100:
        calculated_checksum = total
    elif total == 100 or total == 101:
        calculated_checksum = 0
    else:
        calculated_checksum = total % 101
        if calculated_checksum == 100:
            calculated_checksum = 0
    
    return calculated_checksum == checksum


def validate_ru_kadastr(value):
    """
    Validates Russian kadastr number format.
    
    Format: XX:XX:XXXXXXX:XXXXX
    - First segment: 1-2 digits (region/district)
    - Second segment: 1-2 digits (area)
    - Third segment: 6-7 digits (parcel)
    - Fourth segment: 1-6 digits (sub-parcel)
    
    Args:
        value: Kadastr string (may include colons)
        
    Returns:
        bool: True if valid kadastr format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    # Remove spaces
    kadastr = value.replace(' ', '')
    
    # Split by colon
    parts = kadastr.split(':')
    if len(parts) != 4:
        return False
    
    # Validate each segment
    if not (1 <= len(parts[0]) <= 2 and parts[0].isdigit()):
        return False
    if not (1 <= len(parts[1]) <= 2 and parts[1].isdigit()):
        return False
    if not (6 <= len(parts[2]) <= 7 and parts[2].isdigit()):
        return False
    if not (1 <= len(parts[3]) <= 6 and parts[3].isdigit()):
        return False
    
    # Check for invalid patterns (all zeros in any segment)
    for part in parts:
        if part == '0' * len(part):
            return False
    
    return True


def validate_ru_bik(value):
    """
    Validates Russian BIK (Bank Identification Code) format.
    
    BIK format:
    - 9 digits (standard format)
    - Some systems may use 6 digits (abbreviated)
    - First 2 digits: region code (01-99, but not all valid)
    - Cannot be all zeros or all same digit
    
    Note: Current rule pattern matches 6 digits, but standard BIK is 9 digits.
    This validator accepts both formats for compatibility.
    
    Args:
        value: BIK string (may include spaces or dashes)
        
    Returns:
        bool: True if valid BIK format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    bik = value.replace(' ', '').replace('-', '').replace('.', '')
    
    # Accept both 6-digit (abbreviated) and 9-digit (standard) formats
    if len(bik) != 6 and len(bik) != 9:
        return False
    
    if not bik.isdigit():
        return False
    
    # Cannot be all zeros or all same digit
    if len(set(bik)) == 1:
        return False
    
    # Basic format validation
    # Full validation would require BIK registry lookup
    # For now, we validate format and reject obviously invalid patterns
    
    return True

