"""
Validation functions for Mexican-specific identifiers.
"""


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

