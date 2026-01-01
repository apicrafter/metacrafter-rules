"""
Validation functions for Spanish-specific identifiers.
"""


def validate_es_passport(value):
    """
    Validates Spanish passport number format.
    
    Spanish passport format:
    - 2-3 letter prefix (typically PAA, PAB, PAC, etc. for regular passports)
    - Followed by 6 digits
    - Total length: 8-9 characters
    
    Common prefixes:
    - PAA, PAB, PAC, PAD, PAE, PAF, PAG, PAH, PAI, PAJ, PAK, PAL, PAM, PAN, PAO, PAP, PAQ, PAR, PAS, PAT, PAU, PAV, PAW, PAX, PAY, PAZ
    - Other prefixes may exist for special passport types
    
    Args:
        value: Passport number string
        
    Returns:
        bool: True if valid format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    passport = value.strip().upper()
    
    # Remove spaces and dashes
    passport_clean = passport.replace(' ', '').replace('-', '').replace('.', '')
    
    # Length check: 8-9 characters (2-3 letters + 6 digits)
    if len(passport_clean) < 8 or len(passport_clean) > 9:
        return False
    
    # Check format: letters followed by digits
    if len(passport_clean) == 8:
        # 2 letters + 6 digits
        if not passport_clean[:2].isalpha():
            return False
        if not passport_clean[2:].isdigit():
            return False
    elif len(passport_clean) == 9:
        # 3 letters + 6 digits
        if not passport_clean[:3].isalpha():
            return False
        if not passport_clean[3:].isdigit():
            return False
    
    # Validate prefix (common Spanish passport prefixes start with 'PA')
    prefix = passport_clean[:2] if len(passport_clean) == 8 else passport_clean[:3]
    
    # Most common Spanish passport prefixes start with 'PA'
    # But we allow any 2-3 letter prefix to be flexible
    if len(prefix) == 2:
        # 2-letter prefix: should be alphabetic
        if not prefix.isalpha():
            return False
    elif len(prefix) == 3:
        # 3-letter prefix: should be alphabetic
        if not prefix.isalpha():
            return False
    
    # Check that digits are not all zeros or all same digit
    digits = passport_clean[-6:]
    if digits == '000000' or len(set(digits)) == 1:
        return False
    
    return True


def validate_es_nie(value):
    """
    Validates Spanish NIE (Número de Identidad de Extranjero) using MOD-23 checksum.
    
    Spanish NIE format:
    - Format 1: X-0000000-A (or X0000000A, X.0000000.A)
    - Format 2: Y-0000000-A (or Y0000000A, Y.0000000.A)
    - Format 3: Z-0000000-A (or Z0000000A, Z.0000000.A)
    - Format 4: 00000000-A (8 digits + letter)
    - Letter prefix: X, Y, or Z (or single letter)
    - 7-8 digits
    - Check letter: A-Z (MOD-23 checksum)
    
    Args:
        value: NIE string (may include spaces, dashes, or dots)
        
    Returns:
        bool: True if valid NIE, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    nie = value.replace(' ', '').replace('-', '').replace('.', '').upper()
    
    # Length check: 9-12 characters (with separators removed)
    if len(nie) < 9 or len(nie) > 12:
        return False
    
    # Check letter mapping for MOD-23
    check_letters = 'TRWAGMYFPDXBNJZSQVHLCKE'
    
    # Format 1-3: Letter prefix (X, Y, Z, or any letter) + 7 digits + check letter
    if nie[0].isalpha() and len(nie) >= 9:
        prefix = nie[0]
        # Check if we have 7 digits followed by a letter
        if len(nie) == 9:
            digits_part = nie[1:8]
            check_letter = nie[8]
            
            if digits_part.isdigit() and check_letter.isalpha():
                # MOD-23 checksum calculation
                try:
                    remainder = int(digits_part) % 23
                    expected_letter = check_letters[remainder]
                    return check_letter == expected_letter
                except (ValueError, IndexError):
                    return False
    
    # Format 4: 8 digits + check letter (this format is less common, validate carefully)
    # Note: This format might be for specific NIE types
    if len(nie) == 9 and nie[:8].isdigit() and nie[8].isalpha():
        digits_part = nie[:8]
        check_letter = nie[8]
        
        # MOD-23 checksum calculation
        try:
            remainder = int(digits_part) % 23
            expected_letter = check_letters[remainder]
            return check_letter == expected_letter
        except (ValueError, IndexError):
            return False
    
    # Format with leading zero: X0 + 6 digits + letter
    if len(nie) == 9 and nie[0].isalpha() and nie[1] == '0' and nie[2:8].isdigit() and nie[8].isalpha():
        digits_part = nie[1:8]  # 0 + 6 digits
        check_letter = nie[8]
        
        # MOD-23 checksum calculation
        try:
            remainder = int(digits_part) % 23
            expected_letter = check_letters[remainder]
            return check_letter == expected_letter
        except (ValueError, IndexError):
            return False
    
    return False


def validate_es_vat(value):
    """
    Validates Spanish VAT (IVA) number using MOD-23 checksum.
    
    Spanish VAT format:
    - ES prefix
    - 9 characters: 1 letter + 8 digits OR 8 digits + 1 letter
    - MOD-23 checksum validation
    
    Common formats:
    - ESA12345678 (letter + 8 digits)
    - ES12345678A (8 digits + letter)
    
    Args:
        value: Spanish VAT string (may include spaces or dashes)
        
    Returns:
        bool: True if valid Spanish VAT, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    vat = value.replace(' ', '').replace('-', '').replace('.', '').upper()
    
    # Must start with ES
    if not vat.startswith('ES'):
        return False
    
    vat_number = vat[2:]
    
    # Must be 9 characters
    if len(vat_number) != 9:
        return False
    
    # Check letter mapping for MOD-23
    check_letters = 'TRWAGMYFPDXBNJZSQVHLCKE'
    
    # Format 1: Letter + 8 digits
    if vat_number[0].isalpha() and vat_number[1:].isdigit():
        digits_part = vat_number[1:]
        check_letter = vat_number[0]
        
        try:
            remainder = int(digits_part) % 23
            expected_letter = check_letters[remainder]
            return check_letter == expected_letter
        except (ValueError, IndexError):
            return False
    
    # Format 2: 8 digits + letter
    if vat_number[:8].isdigit() and vat_number[8].isalpha():
        digits_part = vat_number[:8]
        check_letter = vat_number[8]
        
        try:
            remainder = int(digits_part) % 23
            expected_letter = check_letters[remainder]
            return check_letter == expected_letter
        except (ValueError, IndexError):
            return False
    
    return False

