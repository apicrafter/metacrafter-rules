"""
Validation functions for US-specific identifiers.
"""


def validate_us_driver_license(value):
    """
    Validates US driver license number format.
    
    US driver licenses vary by state, but common patterns include:
    - Alphanumeric strings of 6-18 characters
    - Some states use specific formats (e.g., all digits, specific prefixes)
    - Many states have check digits or validation algorithms
    
    This validator performs basic format validation and checks for common
    invalid patterns. State-specific validation would require additional
    context (state field) which is not always available.
    
    Args:
        value: Driver license string
        
    Returns:
        bool: True if valid format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    dl = value.strip()
    
    # Basic length check (6-18 characters as per rule pattern)
    if len(dl) < 6 or len(dl) > 18:
        return False
    
    # Must be alphanumeric
    if not dl.replace(' ', '').replace('-', '').isalnum():
        return False
    
    # Remove spaces and dashes for validation
    dl_clean = dl.replace(' ', '').replace('-', '')
    
    # Check for common invalid patterns
    # All zeros or all same character
    if len(set(dl_clean)) == 1:
        return False
    
    # Common test/invalid patterns
    invalid_patterns = [
        '000000', '111111', '123456', '1234567', '12345678',
        'abcdef', 'test', 'sample', 'example', 'invalid'
    ]
    dl_lower = dl_clean.lower()
    if dl_lower in invalid_patterns:
        return False
    
    # Check for sequential patterns (common in test data)
    if len(dl_clean) >= 6:
        # Check if all digits are sequential
        if dl_clean.isdigit():
            digits = [int(d) for d in dl_clean]
            # Check if strictly increasing or decreasing
            if all(digits[i] == digits[i-1] + 1 for i in range(1, len(digits))):
                return False
            if all(digits[i] == digits[i-1] - 1 for i in range(1, len(digits))):
                return False
    
    # Basic validation passed
    return True


def validate_aba_routing(value):
    """
    Validates US ABA routing number using MOD-10 checksum.
    
    ABA routing number format:
    - 9 digits
    - MOD-10 checksum algorithm
    
    Algorithm:
    1. Multiply digits by weights: 3, 7, 1, 3, 7, 1, 3, 7, 1
    2. Sum all products
    3. Check digit = (10 - (sum mod 10)) mod 10
    4. Last digit must match calculated check digit
    
    Args:
        value: ABA routing number string (9 digits, may include dashes)
        
    Returns:
        bool: True if valid ABA routing number, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    routing = value.replace(' ', '').replace('-', '').replace('.', '')
    
    # Must be exactly 9 digits
    if len(routing) != 9:
        return False
    
    if not routing.isdigit():
        return False
    
    # Check for obviously invalid patterns
    if routing == '000000000' or len(set(routing)) == 1:
        return False
    
    # MOD-10 checksum validation
    weights = [3, 7, 1, 3, 7, 1, 3, 7, 1]
    digits = [int(d) for d in routing]
    
    # Calculate weighted sum
    total = sum(digit * weight for digit, weight in zip(digits, weights))
    
    # Check digit validation: sum must be divisible by 10
    return total % 10 == 0


def validate_cusip(value):
    """
    Validates CUSIP (Committee on Uniform Securities Identification Procedures) using check digit algorithm.
    
    CUSIP format:
    - 9 characters total
    - First 6 characters: alphanumeric (issuer and issue)
    - Next 2 characters: alphanumeric or special characters (*@#)
    - Last character: check digit (digit)
    
    Check digit algorithm:
    1. Convert characters to numeric values (A=10, B=11, ..., Z=35, *=36, @=37, #=38)
    2. Multiply by 1 or 2 alternately (starting with 1)
    3. Sum all digits of products
    4. Check digit = (10 - (sum mod 10)) mod 10
    
    Args:
        value: CUSIP string (9 characters)
        
    Returns:
        bool: True if valid CUSIP, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    cusip = value.upper().replace(' ', '').replace('-', '')
    
    # Must be exactly 9 characters
    if len(cusip) != 9:
        return False
    
    # First 8 characters: alphanumeric or special (*@#)
    # Last character: must be a digit
    if not cusip[8].isdigit():
        return False
    
    # Convert characters to numeric values
    def char_to_value(c):
        if c.isdigit():
            return int(c)
        elif c.isalpha():
            return ord(c) - ord('A') + 10
        elif c == '*':
            return 36
        elif c == '@':
            return 37
        elif c == '#':
            return 38
        else:
            return None
    
    # Calculate check digit
    total = 0
    for i, char in enumerate(cusip[:8]):
        value = char_to_value(char)
        if value is None:
            return False
        
        # Multiply by 1 or 2 alternately (positions 0,2,4,6 use 1; 1,3,5,7 use 2)
        multiplier = 2 if i % 2 == 1 else 1
        product = value * multiplier
        
        # Sum all digits of product
        while product > 0:
            total += product % 10
            product //= 10
    
    # Calculate check digit
    check_digit = (10 - (total % 10)) % 10
    
    return int(cusip[8]) == check_digit


def validate_us_ssn(value):
    """
    Validates US Social Security Number format.
    
    SSN rules:
    - Cannot be 000-00-0000
    - Area code (first 3 digits) cannot be 000, 666, or 900-999
    - Group number (middle 2 digits) cannot be 00
    - Serial number (last 4 digits) cannot be 0000
    
    Args:
        value: SSN string (may include dashes, spaces, or dots)
        
    Returns:
        bool: True if valid SSN format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    ssn = value.replace('-', '').replace(' ', '').replace('.', '')
    
    if len(ssn) != 9 or not ssn.isdigit():
        return False
    
    area = ssn[:3]
    group = ssn[3:5]
    serial = ssn[5:]
    
    # Cannot be all zeros
    if ssn == '000000000':
        return False
    
    # Area code restrictions
    if area == '000' or area == '666':
        return False
    try:
        area_num = int(area)
        if 900 <= area_num <= 999:
            return False
    except ValueError:
        return False
    
    # Group number cannot be 00
    if group == '00':
        return False
    
    # Serial number cannot be 0000
    if serial == '0000':
        return False
    
    return True


def validate_us_ein(value):
    """
    Validates US Employer Identification Number format.
    
    EIN format:
    - 9 digits total
    - First 2 digits have restrictions (cannot be 00, 07, 08, 09, 17, 18, 19, 28, 29, 49, 69, 70, 78, 79, 80, 90, 96)
    - Cannot be all zeros or all same digit
    
    Args:
        value: EIN string (may include dashes, spaces, or dots)
        
    Returns:
        bool: True if valid EIN format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    ein = value.replace('-', '').replace(' ', '').replace('.', '')
    
    if len(ein) != 9 or not ein.isdigit():
        return False
    
    # Cannot be all zeros or all same digit
    if len(set(ein)) == 1:
        return False
    
    # First 2 digits restrictions
    prefix = ein[:2]
    invalid_prefixes = ['00', '07', '08', '09', '17', '18', '19', 
                        '28', '29', '49', '69', '70', '78', '79', 
                        '80', '90', '96']
    if prefix in invalid_prefixes:
        return False
    
    return True


def validate_us_itin(value):
    """
    Validates US ITIN format.
    
    ITIN format:
    - Always starts with 9
    - Format: 9XX-XX-XXXX or 9XX-7X-XXXX
    - Second segment (positions 3-4): 70-88, 90-92, 94-99
    - Cannot be all zeros or all same digit
    
    Args:
        value: ITIN string (may include dashes or spaces)
        
    Returns:
        bool: True if valid ITIN format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    itin = value.replace('-', '').replace(' ', '').replace('.', '')
    
    if len(itin) != 9 or not itin.isdigit():
        return False
    
    # Must start with 9
    if itin[0] != '9':
        return False
    
    # Second segment (positions 3-4) must be in valid range
    try:
        second_seg = int(itin[3:5])
        valid_ranges = [
            (70, 88),  # 70-88
            (90, 92),  # 90-92
            (94, 99)   # 94-99
        ]
        
        if not any(start <= second_seg <= end for start, end in valid_ranges):
            return False
    except (ValueError, IndexError):
        return False
    
    # Cannot be all zeros or all same digit
    if len(set(itin)) == 1:
        return False
    
    return True


def validate_us_passport(value):
    """
    Validates US passport number format.
    
    US passport format:
    - 9 digits
    - Cannot be all zeros or all same digit
    - Cannot start with 0
    - Common test patterns should be rejected
    
    Args:
        value: Passport number string (may include dashes, spaces, or dots)
        
    Returns:
        bool: True if valid passport format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    passport = value.replace('-', '').replace(' ', '').replace('.', '')
    
    if len(passport) != 9 or not passport.isdigit():
        return False
    
    # Cannot be all zeros or all same digit
    if len(set(passport)) == 1:
        return False
    
    # Cannot start with 0
    if passport[0] == '0':
        return False
    
    # Reject common test patterns
    test_patterns = ['123456789', '000000001', '111111111', '987654321']
    if passport in test_patterns:
        return False
    
    return True

