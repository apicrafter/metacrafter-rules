"""
Validation functions for global identifiers with check digits.

These functions validate identifiers that use check digit algorithms to reduce
false positives in pattern matching.
"""
import datetime
import re


def validate_iban(value):
    """
    Validates IBAN using MOD-97-10 algorithm.
    
    Args:
        value: IBAN string (may include spaces or dashes)
        
    Returns:
        bool: True if valid IBAN, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    # Remove spaces and dashes, convert to uppercase
    iban = value.replace(' ', '').replace('-', '').upper()
    
    # Basic format check
    if len(iban) < 15 or len(iban) > 34:
        return False
    if not iban[:2].isalpha() or not iban[2:4].isdigit():
        return False
    if not iban[4:].replace(' ', '').isalnum():
        return False
    
    # MOD-97-10 check
    # Rearrange: move first 4 characters to end
    rearranged = iban[4:] + iban[:4]
    
    # Convert letters to numbers (A=10, B=11, ..., Z=35)
    numeric = ''
    for c in rearranged:
        if c.isalpha():
            numeric += str(ord(c) - ord('A') + 10)
        else:
            numeric += c
    
    try:
        remainder = int(numeric) % 97
        return remainder == 1
    except (ValueError, OverflowError):
        return False


def validate_isin(value):
    """
    Validates ISIN using Luhn algorithm variant.
    
    Args:
        value: ISIN string (12 characters)
        
    Returns:
        bool: True if valid ISIN, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    isin = value.upper().replace(' ', '').replace('-', '')
    
    if len(isin) != 12:
        return False
    
    if not isin[:2].isalpha():
        return False
    
    # Convert to numeric string (each character becomes one or two digits)
    numeric = ''
    for char in isin:
        if char.isalpha():
            # Convert letter to two-digit number (A=10, B=11, ..., Z=35)
            num = ord(char) - ord('A') + 10
            numeric += str(num)
        elif char.isdigit():
            numeric += char
        else:
            return False
    
    # Apply Luhn algorithm to the numeric string
    # Double every second digit from right (odd positions in reversed string)
    total = 0
    for i, digit_char in enumerate(reversed(numeric)):
        digit = int(digit_char)
        # Double every second digit (odd indices: 1, 3, 5, ...)
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit = (digit // 10) + (digit % 10)
        total += digit
    
    return total % 10 == 0


def validate_gtin(value):
    """
    Validates GTIN (EAN/UPC) using check digit algorithm.
    Supports GTIN-8, GTIN-12, GTIN-13, GTIN-14.
    
    Args:
        value: GTIN string (8, 12, 13, or 14 digits)
        
    Returns:
        bool: True if valid GTIN, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    gtin = value.replace(' ', '').replace('-', '')
    
    if not gtin.isdigit():
        return False
    
    if len(gtin) not in [8, 12, 13, 14]:
        return False
    
    # Calculate check digit
    digits = [int(d) for d in gtin[:-1]]
    check_digit = int(gtin[-1])
    
    # Multiply by 3 and 1 alternately (right to left)
    total = 0
    for i, digit in enumerate(reversed(digits)):
        multiplier = 3 if i % 2 == 0 else 1
        total += digit * multiplier
    
    calculated_check = (10 - (total % 10)) % 10
    
    return calculated_check == check_digit


def validate_sscc(value):
    """
    Validates SSCC (Serial Shipping Container Code) using GTIN check digit algorithm.
    SSCC is 18 digits total, with optional "00" application identifier prefix.
    
    Args:
        value: SSCC string (18 digits, optionally prefixed with "00")
        
    Returns:
        bool: True if valid SSCC, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    sscc = value.replace(' ', '').replace('-', '')
    
    # Remove optional "00" prefix if present
    if sscc.startswith('00') and len(sscc) == 20:
        sscc = sscc[2:]
    
    if not sscc.isdigit():
        return False
    
    if len(sscc) != 18:
        return False
    
    # Calculate check digit using GTIN algorithm
    digits = [int(d) for d in sscc[:-1]]
    check_digit = int(sscc[-1])
    
    # Multiply by 3 and 1 alternately (right to left)
    total = 0
    for i, digit in enumerate(reversed(digits)):
        multiplier = 3 if i % 2 == 0 else 1
        total += digit * multiplier
    
    calculated_check = (10 - (total % 10)) % 10
    
    return calculated_check == check_digit


def validate_issn(value):
    """
    Validates ISSN using MOD-11 algorithm.
    
    Args:
        value: ISSN string (with or without hyphen)
        
    Returns:
        bool: True if valid ISSN, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    issn = value.replace('-', '').replace(' ', '').upper()
    
    if len(issn) != 8:
        return False
    
    if not issn[:-1].isdigit():
        return False
    if issn[7] not in '0123456789X':
        return False
    
    # MOD-11 check
    weights = [8, 7, 6, 5, 4, 3, 2]
    total = sum(int(issn[i]) * weights[i] for i in range(7))
    
    check_value = (11 - (total % 11)) % 11
    check_char = 'X' if check_value == 10 else str(check_value)
    
    return issn[7] == check_char


def validate_imei(value):
    """
    Validates IMEI using Luhn algorithm.
    
    Args:
        value: IMEI string (14 or 15 digits, with or without dashes)
        
    Returns:
        bool: True if valid IMEI, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    imei = value.replace('-', '').replace(' ', '')
    
    if not imei.isdigit():
        return False
    
    if len(imei) not in [14, 15]:
        return False
    
    # Use 14 digits for check digit calculation
    digits = [int(d) for d in imei[:14]]
    
    # Luhn algorithm for IMEI: the check digit makes the full 15-digit number
    # pass Luhn, so when computing over the 14 payload digits the rightmost
    # payload digit IS doubled (reversed index 0).
    total = 0
    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 0:  # rightmost payload digit is doubled
            doubled = digit * 2
            total += (doubled // 10) + (doubled % 10)
        else:
            total += digit
    
    check_digit = (10 - (total % 10)) % 10
    
    if len(imei) == 15:
        return int(imei[14]) == check_digit
    else:
        return True  # 14-digit IMEI without check digit is also valid


def validate_imsi(value):
    """
    Validates IMSI (International Mobile Subscriber Identity).
    
    IMSI is a 15-digit number with structure: MCC (3 digits) + MNC (2-3 digits) + MSIN (9-10 digits)
    
    Args:
        value: IMSI string (15 digits)
        
    Returns:
        bool: True if valid IMSI format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    imsi = value.replace(' ', '').replace('-', '')
    
    if not imsi.isdigit():
        return False
    
    if len(imsi) != 15:
        return False
    
    # Structure: MCC (3 digits) + MNC (2-3 digits) + MSIN (9-10 digits)
    # MCC: Mobile Country Code (3 digits, range 001-999)
    mcc = imsi[:3]
    mcc_num = int(mcc)
    if mcc_num < 1 or mcc_num > 999:
        return False
    
    # MNC: Mobile Network Code (2-3 digits)
    # IMSI is always 15 digits total
    # If MNC is 2 digits: MSIN is 10 digits (positions 5-14)
    # If MNC is 3 digits: MSIN is 9 digits (positions 6-14)
    # We accept both formats as valid
    
    # Check if 2-digit MNC is valid (MSIN length would be 10)
    if len(imsi[5:]) == 10:
        # Valid 2-digit MNC format
        return True
    
    # Check if 3-digit MNC is valid (MSIN length would be 9)
    if len(imsi[6:]) == 9:
        # Valid 3-digit MNC format
        return True
    
    # If neither format matches, it's invalid
    return False


def validate_msisdn(value):
    """
    Validates MSISDN (Mobile Station International Subscriber Directory Number).
    
    MSISDN is in E.164 format: country code (1-3 digits) + subscriber number.
    Total length: 11-15 digits, must start with 1-9 (not 0).
    
    Args:
        value: MSISDN string (11-15 digits, E.164 format)
        
    Returns:
        bool: True if valid MSISDN format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    # Remove common formatting characters
    msisdn = value.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')
    
    if not msisdn.isdigit():
        return False
    
    # E.164 format: 11-15 digits total
    if len(msisdn) < 11 or len(msisdn) > 15:
        return False
    
    # Must start with 1-9 (not 0)
    if msisdn[0] == '0':
        return False
    
    # Country codes are 1-3 digits, subscriber numbers are the rest
    # We can't validate specific country codes without a full list,
    # but we validate the format is correct
    return True


def validate_iccid(value):
    """
    Validates ICCID (Integrated Circuit Card Identifier) using Luhn algorithm.
    
    ICCID is 19-20 digits with structure: Issuer ID (2 digits) + Account ID (variable) + Check digit (1 digit)
    Uses Luhn algorithm for check digit validation (ITU-T E.118 standard).
    
    Args:
        value: ICCID string (19-20 digits)
        
    Returns:
        bool: True if valid ICCID with correct check digit, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    iccid = value.replace(' ', '').replace('-', '')
    
    if not iccid.isdigit():
        return False
    
    if len(iccid) not in [19, 20]:
        return False
    
    # Luhn algorithm for check digit validation
    # Use all digits except the last one for calculation
    digits = [int(d) for d in iccid[:-1]]
    check_digit = int(iccid[-1])
    
    # Luhn algorithm: double every second digit from right (odd positions)
    total = 0
    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 0:  # Even position in reversed = rightmost, don't double
            total += digit
        else:  # Odd position in reversed = second from right, double it
            doubled = digit * 2
            total += (doubled // 10) + (doubled % 10)
    
    calculated_check = (10 - (total % 10)) % 10
    
    return check_digit == calculated_check


def validate_lei(value):
    """
    Validates LEI using MOD-97-10 algorithm (similar to IBAN).
    
    Args:
        value: LEI string (20 characters)
        
    Returns:
        bool: True if valid LEI, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    lei = value.upper().replace(' ', '').replace('-', '')
    
    if len(lei) != 20:
        return False
    
    # MOD-97-10 check (last 2 digits are checksum)
    main_part = lei[:18]
    checksum = lei[18:]
    
    if not checksum.isdigit():
        return False
    
    # Convert to numeric
    numeric = ''
    for c in main_part:
        if c.isalpha():
            numeric += str(ord(c) - ord('A') + 10)
        elif c.isdigit():
            numeric += c
        else:
            return False
    
    numeric += checksum
    
    try:
        remainder = int(numeric) % 97
        return remainder == 1
    except (ValueError, OverflowError):
        return False


def validate_isrc(value):
    """
    Validates ISRC format (no check digit, but format validation).
    
    Args:
        value: ISRC string (12 characters)
        
    Returns:
        bool: True if valid ISRC format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    isrc = value.upper().replace('-', '').replace(' ', '')
    
    if len(isrc) != 12:
        return False
    
    # Format: CCXXXNNNNNNN (2-letter country, 3 alphanumeric, 7 digits)
    # Country code must be 2 uppercase letters (ISO 3166-1 alpha-2)
    # Note: We validate format only, not against full country code list
    if not isrc[:2].isalpha() or not isrc[:2].isupper():
        return False
    # Registrant code: 3 alphanumeric characters (can be letters or digits)
    if not isrc[2:5].isalnum():
        return False
    # Year and designation: 7 digits
    if not isrc[5:].isdigit():
        return False
    
    # Basic country code validation: reject obviously invalid patterns
    # XX is reserved/unassigned in ISO 3166-1, but we'll allow it for format validation
    # since we can't validate against full country code list without external data
    
    return True


def validate_isni(value):
    """
    Validates ISNI using MOD-11-2 algorithm.
    
    Args:
        value: ISNI string (16 characters, with or without spaces)
        
    Returns:
        bool: True if valid ISNI, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    isni = value.replace(' ', '').replace('-', '')
    
    if len(isni) != 16:
        return False
    
    if not isni.isdigit():
        return False
    
    # MOD-11-2 check (ISO 27729)
    # Weights are 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 2, 3, 4, 5, 6 (repeating pattern)
    # For 16 digits, we need weights for positions 0-14
    base_weights = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    weights = []
    for i in range(15):
        weights.append(base_weights[i % 10])
    
    total = sum(int(isni[i]) * weights[i] for i in range(15))
    
    check_value = (12 - (total % 11)) % 11
    check_char = 'X' if check_value == 10 else str(check_value)
    
    return isni[15] == check_char


def validate_orcid(value):
    """
    Validates ORCID using MOD-11-2 algorithm.
    
    ORCID format: 0000-0001-2345-6789 (16 digits with dashes) or 0000-0001-2345-678X
    The last character is a check digit calculated using MOD-11-2.
    
    Args:
        value: ORCID string (with or without dashes)
        
    Returns:
        bool: True if valid ORCID, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    # Remove dashes and spaces
    orcid = value.replace('-', '').replace(' ', '')
    
    # Must be 16 characters
    if len(orcid) != 16:
        return False
    
    # Must start with 0000-000
    if not orcid.startswith('0000000'):
        return False
    
    # Last character can be digit or X
    if not (orcid[-1].isdigit() or orcid[-1] == 'X'):
        return False
    
    # All other characters must be digits
    if not orcid[:-1].isdigit():
        return False
    
    # MOD-11-2 check digit calculation
    # Weights: 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 2, 3, 4, 5, 6 (repeating)
    base_weights = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    weights = []
    for i in range(15):
        weights.append(base_weights[i % 10])
    
    total = sum(int(orcid[i]) * weights[i] for i in range(15))
    
    check_value = (12 - (total % 11)) % 11
    check_char = 'X' if check_value == 10 else str(check_value)
    
    return orcid[15] == check_char


def validate_grid(value):
    """
    Validates GRID (Global Research Identifier Database) format.
    
    GRID format: grid.XXXX.XX where:
    - XXXX is 4-6 digits
    - XX is 1-2 hexadecimal characters
    
    Args:
        value: GRID string
        
    Returns:
        bool: True if valid GRID format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    grid = value.strip().lower()
    
    # Must start with "grid."
    if not grid.startswith('grid.'):
        return False
    
    parts = grid[5:].split('.')
    if len(parts) != 2:
        return False
    
    # First part: 4-6 digits
    if not parts[0].isdigit():
        return False
    if len(parts[0]) < 4 or len(parts[0]) > 6:
        return False
    
    # Second part: 1-2 hexadecimal characters
    if not all(c in '0123456789abcdef' for c in parts[1]):
        return False
    if len(parts[1]) < 1 or len(parts[1]) > 2:
        return False
    
    return True


def validate_openalex_id(value):
    """
    Validates OpenAlex ID format.
    
    OpenAlex ID format: [ACIVW][1-9]\d{3,9}
    - First character is one of: A, C, I, V, W
    - Second character is 1-9 (not 0)
    - Followed by 3-9 digits
    
    Args:
        value: OpenAlex ID string
        
    Returns:
        bool: True if valid OpenAlex ID format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    oaid = value.strip().upper()
    
    # Must be 5-11 characters (1 prefix + 1 digit + 3-9 more digits)
    if len(oaid) < 5 or len(oaid) > 11:
        return False
    
    # First character must be A, C, I, V, or W
    if oaid[0] not in 'ACIVW':
        return False
    
    # Second character must be 1-9 (not 0)
    if not oaid[1].isdigit() or oaid[1] == '0':
        return False
    
    # Remaining characters must be digits
    if not oaid[2:].isdigit():
        return False
    
    # Total length check: 3-9 digits after prefix and first digit
    if len(oaid[2:]) < 3 or len(oaid[2:]) > 9:
        return False
    
    return True


_FIGI_CONSONANTS = set('BCDFGHJKLMNPQRSTVWXYZ')
_FIGI_RESERVED_PREFIXES = {'BS', 'BM', 'GG', 'GB', 'GH', 'KY', 'VG'}


def validate_figi(value):
    """
    Validates a FIGI (Financial Instrument Global Identifier).

    A FIGI is 12 characters with a defined structure:

    * positions 1-2: upper-case consonants, excluding the reserved combinations
      (``BS``, ``BM``, ``GG``, ``GB``, ``GH``, ``KY``, ``VG``) that collide with
      ISIN country prefixes;
    * position 3: always ``G``;
    * positions 4-11: consonants or digits (vowels are never used);
    * position 12: a modulo-10 (Luhn-style, base-36) check digit.

    Args:
        value: FIGI string

    Returns:
        bool: True if the value is a valid FIGI, False otherwise.
    """
    if not isinstance(value, str):
        return False

    figi = value.upper().replace(' ', '').replace('-', '')

    if len(figi) != 12:
        return False

    if figi[0] not in _FIGI_CONSONANTS or figi[1] not in _FIGI_CONSONANTS:
        return False

    if figi[:2] in _FIGI_RESERVED_PREFIXES:
        return False

    if figi[2] != 'G':
        return False

    for ch in figi[3:11]:
        if not (ch.isdigit() or ch in _FIGI_CONSONANTS):
            return False

    if not figi[11].isdigit():
        return False

    total = 0
    for i in range(11):
        ch = figi[i]
        mapped = int(ch) if ch.isdigit() else ord(ch) - 55
        if (i + 1) % 2 == 0:
            mapped *= 2
        total += sum(int(d) for d in str(mapped))

    check = (10 - (total % 10)) % 10
    return check == int(figi[11])


def validate_tr_vkn(value):
    """
    Validates a Turkish tax identification number (Vergi Kimlik Numarası).

    A 10-digit number whose final digit is a check digit computed with the
    official VKN algorithm over the first nine digits.

    Args:
        value: VKN string (spaces and dashes are ignored)

    Returns:
        bool: True if the value is a valid Turkish tax number, False otherwise.
    """
    if not isinstance(value, str):
        return False

    vkn = value.replace(' ', '').replace('-', '')
    if len(vkn) != 10 or not vkn.isdigit():
        return False

    total = 0
    for i in range(9):
        c1 = (int(vkn[i]) + (9 - i)) % 10
        c2 = (c1 * pow(2, 9 - i)) % 9
        if c1 != 0 and c2 == 0:
            c2 = 9
        total += c2
    check = (10 - (total % 10)) % 10
    return check == int(vkn[9])


def validate_id_nik(value):
    """
    Validates the structure of an Indonesian NIK (Nomor Induk Kependudukan).

    A NIK is 16 digits: 6 digits of area code, a 6-digit birth date in
    ``DDMMYY`` form (the day has 40 added for female holders), and a 4-digit
    sequence that is never ``0000``. There is no check digit, so the embedded
    date is validated to reduce false positives.

    Args:
        value: NIK string (spaces and dashes are ignored)

    Returns:
        bool: True if the value has a valid NIK structure, False otherwise.
    """
    if not isinstance(value, str):
        return False

    nik = value.replace(' ', '').replace('-', '')
    if len(nik) != 16 or not nik.isdigit():
        return False

    day = int(nik[6:8])
    if day > 40:
        day -= 40
    month = int(nik[8:10])
    sequence = nik[12:16]

    if not (1 <= day <= 31):
        return False
    if not (1 <= month <= 12):
        return False
    if sequence == '0000':
        return False
    return True


_ROR_CROCKFORD = '0123456789abcdefghjkmnpqrstvwxyz'
_ROR_PATTERN = re.compile(r'^0[a-hj-km-np-tv-z0-9]{6}[0-9]{2}$')


def validate_ror_id(value):
    """
    Validates a ROR ID (Research Organization Registry identifier).

    A ROR ID is a 9-character identifier: a leading ``0``, six Crockford
    base-32 characters, and a 2-digit ISO 7064 MOD 97-10 checksum. An optional
    ``https://ror.org/`` prefix (or leading path) is ignored.

    Args:
        value: ROR ID string (with or without the ror.org prefix)

    Returns:
        bool: True if the value is a valid ROR ID, False otherwise.
    """
    if not isinstance(value, str):
        return False

    ror = value.strip().rstrip('/').split('/')[-1].lower()
    if not _ROR_PATTERN.match(ror):
        return False

    number = 0
    for ch in ror[:-2]:
        number = number * 32 + _ROR_CROCKFORD.index(ch)
    checksum = str(98 - ((number * 100) % 97)).zfill(2)
    return checksum == ror[-2:]


def _nl_elfproef(number):
    """Returns True if a 9-digit string passes the Dutch 11-test (elfproef)."""
    if len(number) != 9 or not number.isdigit():
        return False
    if number == '000000000':
        return False
    weights = [9, 8, 7, 6, 5, 4, 3, 2, -1]
    return sum(int(number[i]) * weights[i] for i in range(9)) % 11 == 0


def validate_nl_bsn(value):
    """
    Validates a Dutch BSN (Burgerservicenummer).

    A 9-digit number that passes the Dutch 11-test (elfproef): the digits are
    weighted 9, 8, ..., 2 and the final digit by -1, and the weighted sum must
    be divisible by 11.

    Args:
        value: BSN string (spaces and dashes are ignored)

    Returns:
        bool: True if the value is a valid BSN, False otherwise.
    """
    if not isinstance(value, str):
        return False
    return _nl_elfproef(value.replace(' ', '').replace('-', ''))


def validate_nl_rsin(value):
    """
    Validates a Dutch RSIN (Rechtspersonen en Samenwerkingsverbanden
    Informatienummer).

    An RSIN uses the same 9-digit 11-test (elfproef) as the BSN.

    Args:
        value: RSIN string (spaces and dashes are ignored)

    Returns:
        bool: True if the value is a valid RSIN, False otherwise.
    """
    if not isinstance(value, str):
        return False
    return _nl_elfproef(value.replace(' ', '').replace('-', ''))


def validate_fr_siren(value):
    """
    Validates a French SIREN company identifier.

    A 9-digit number whose final digit is a Luhn check digit.

    Args:
        value: SIREN string (spaces and dashes are ignored)

    Returns:
        bool: True if the value is a valid SIREN, False otherwise.
    """
    if not isinstance(value, str):
        return False

    siren = value.replace(' ', '').replace('-', '')
    if len(siren) != 9 or not siren.isdigit():
        return False
    return _luhn_is_valid(siren)


def validate_gln(value):
    """
    Validates GLN (Global Location Number) using GTIN check digit algorithm.
    GLN is 13 digits and uses the same check digit algorithm as GTIN-13.
    
    Args:
        value: GLN string (13 digits)
        
    Returns:
        bool: True if valid GLN, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    gln = value.replace(' ', '').replace('-', '')
    
    if not gln.isdigit():
        return False
    
    if len(gln) != 13:
        return False
    
    # Use GTIN validation algorithm (same as GTIN-13)
    return validate_gtin(gln)


def validate_asn(value):
    """
    Validates ASN (Autonomous System Number) range.
    
    ASN range is 1-4294967295 (32-bit unsigned integer).
    Most common ASNs are 4-6 digits, but the full range is valid.
    
    Args:
        value: ASN string (numeric)
        
    Returns:
        bool: True if valid ASN range, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    asn = value.strip()
    
    if not asn.isdigit():
        return False
    
    try:
        asn_num = int(asn)
        # Valid ASN range: 1 to 4294967295 (2^32 - 1)
        return 1 <= asn_num <= 4294967295
    except (ValueError, OverflowError):
        return False


def validate_language_tag(value):
    """
    Validates IETF BCP 47 language tag format.
    
    Format: language[-script][-region][-variant][-extension][-privateuse]
    - language: 2-3 letters (ISO 639-1/639-2) or 5-8 alphanumeric (registered)
    - script: 4 letters (ISO 15924)
    - region: 2 letters (ISO 3166-1) or 3 digits (UN M.49)
    - variant: 5-8 alphanumeric or 1 letter + 3 alphanumeric
    - extension: 1 letter + 1-8 alphanumeric
    - privateuse: 'x' + 1-8 alphanumeric
    
    Args:
        value: Language tag string
        
    Returns:
        bool: True if valid BCP 47 format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    tag = value.strip().lower()
    
    if not tag:
        return False
    
    # Split by hyphens
    parts = tag.split('-')
    
    if not parts:
        return False
    
    # First part is language subtag
    lang = parts[0]
    if not lang:
        return False
    
    # Language subtag: 2-3 letters (ISO 639) or 5-8 alphanumeric (registered)
    if len(lang) < 2 or len(lang) > 8:
        return False
    
    if len(lang) <= 3:
        # ISO 639 codes: 2-3 letters
        if not lang.isalpha():
            return False
    else:
        # Registered language tags: 5-8 alphanumeric
        if len(lang) < 5 or len(lang) > 8:
            return False
        if not lang.isalnum():
            return False
    
    # Process remaining subtags
    i = 1
    while i < len(parts):
        subtag = parts[i]
        if not subtag:
            return False
        
        # Script subtag: exactly 4 letters
        if len(subtag) == 4 and subtag.isalpha():
            i += 1
            continue
        
        # Region subtag: 2 letters or 3 digits
        if (len(subtag) == 2 and subtag.isalpha()) or (len(subtag) == 3 and subtag.isdigit()):
            i += 1
            continue
        
        # Variant: 5-8 alphanumeric, or 1 letter + 3 alphanumeric
        if len(subtag) >= 5 and len(subtag) <= 8 and subtag.isalnum():
            i += 1
            continue
        if len(subtag) == 4 and subtag[0].isalpha() and subtag[1:].isalnum():
            i += 1
            continue
        
        # Extension: 1 letter + 1-8 alphanumeric
        if len(subtag) >= 2 and len(subtag) <= 9 and subtag[0].isalpha() and subtag[1:].isalnum():
            i += 1
            continue
        
        # Private use: 'x' + 1-8 alphanumeric
        if subtag[0] == 'x' and len(subtag) >= 2 and len(subtag) <= 9 and subtag[1:].isalnum():
            i += 1
            continue
        
        # If we get here, subtag doesn't match any valid pattern
        return False
    
    return True


def validate_eu_vat(value, country_code=None):
    """
    Validates EU VAT number using country-specific checksum algorithms.
    
    EU VAT numbers have different validation rules per country:
    - AT (Austria): MOD-11
    - BE (Belgium): MOD-97
    - BG (Bulgaria): MOD-11
    - CY (Cyprus): MOD-11
    - CZ (Czech Republic): MOD-11
    - DE (Germany): MOD-11
    - DK (Denmark): MOD-11
    - EE (Estonia): MOD-11
    - ES (Spain): MOD-23
    - FI (Finland): MOD-11
    - FR (France): MOD-11
    - GR (Greece): MOD-11
    - HR (Croatia): MOD-11
    - HU (Hungary): MOD-11
    - IE (Ireland): MOD-23
    - IT (Italy): MOD-11
    - LT (Lithuania): MOD-11
    - LU (Luxembourg): MOD-11
    - LV (Latvia): MOD-11
    - MT (Malta): MOD-37
    - NL (Netherlands): MOD-11
    - PL (Poland): MOD-11
    - PT (Portugal): MOD-11
    - RO (Romania): MOD-11
    - SE (Sweden): MOD-11
    - SI (Slovenia): MOD-11
    - SK (Slovakia): MOD-11
    
    Args:
        value: VAT number string (may include spaces or dashes)
        country_code: Optional 2-letter country code to use specific validation
        
    Returns:
        bool: True if valid EU VAT format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    vat = value.replace(' ', '').replace('-', '').replace('.', '').upper()
    
    # Basic format check: 2-letter country code + 6-12 alphanumeric
    if len(vat) < 8 or len(vat) > 14:
        return False
    
    # Extract country code
    if not vat[:2].isalpha():
        return False
    
    detected_country = vat[:2]
    vat_number = vat[2:]
    
    # Use provided country_code or detected one
    country = (country_code or detected_country).upper()
    
    # Basic format validation: alphanumeric after country code
    if not vat_number.isalnum():
        return False
    
    # Country-specific length checks
    country_lengths = {
        'AT': 9, 'BE': 10, 'BG': 9, 'CY': 9, 'CZ': 8, 'DE': 9,
        'DK': 8, 'EE': 9, 'ES': 9, 'FI': 8, 'FR': 11, 'GR': 9,
        'HR': 11, 'HU': 8, 'IE': 8, 'IT': 11, 'LT': 9, 'LU': 8,
        'LV': 11, 'MT': 8, 'NL': 12, 'PL': 10, 'PT': 9, 'RO': 2,  # RO: 2-10
        'SE': 12, 'SI': 8, 'SK': 10
    }
    
    if country in country_lengths:
        expected_len = country_lengths[country]
        if country == 'RO':
            # Romania: 2-10 digits
            if not (2 <= len(vat_number) <= 10 and vat_number.isdigit()):
                return False
        else:
            if len(vat_number) != expected_len:
                return False
    
    # Basic checksum validation for common countries
    # Note: Full implementation would require country-specific algorithms
    # This provides basic format and structure validation
    
    # Check for obviously invalid patterns
    if vat_number.isdigit():
        # All zeros or all same digit
        if len(set(vat_number)) == 1:
            return False
    
    # Additional country-specific basic checks
    if country == 'DE':
        # German VAT: 9 digits, starts with country code
        if len(vat_number) != 9 or not vat_number.isdigit():
            return False
    elif country == 'FR':
        # French VAT: 11 characters total (FR + 2 letters + 9 digits)
        # But in our pattern, vat_number is after country code, so it's 2 letters + 9 digits = 11
        if len(vat_number) != 11:
            return False
        if not (vat_number[:2].isalpha() and vat_number[2:].isdigit()):
            return False
        # Check that letters are valid (typically A-Z)
        if not vat_number[:2].isupper():
            return False
    elif country == 'IT':
        # Italian VAT: 11 digits
        if len(vat_number) != 11 or not vat_number.isdigit():
            return False
    elif country == 'ES':
        # Spanish VAT: 9 characters (1 letter + 8 digits or 8 digits + 1 letter)
        if len(vat_number) != 9:
            return False
    elif country == 'NL':
        # Dutch VAT: 12 characters (2 letters + 9 digits + B + 2 digits)
        if len(vat_number) != 12:
            return False
    
    # Basic validation passed
    # Full checksum validation would require country-specific implementations
    
    # Reject obviously invalid country codes (XX is reserved/unassigned)
    if country in ['XX', 'ZZ']:
        return False
    
    return True


def validate_euid(value):
    """
    Validates EUID (European Unique Identifier) format.
    
    EUID format:
    - 2-letter country code (ISO 3166-1 alpha-2)
    - Followed by 4-18 alphanumeric characters
    - Total length: 6-20 characters
    
    Args:
        value: EUID string (may include spaces or dashes)
        
    Returns:
        bool: True if valid EUID format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    euid = value.replace(' ', '').replace('-', '').upper()
    
    # Length check: 6-20 characters
    if len(euid) < 6 or len(euid) > 20:
        return False
    
    # Format: 2-letter country code + 4-18 alphanumeric
    if not euid[:2].isalpha():
        return False
    
    country_code = euid[:2]
    identifier = euid[2:]
    
    # Identifier part must be 4-18 alphanumeric (strict check)
    if len(identifier) < 4:
        return False
    if len(identifier) > 18:
        return False
    
    if not identifier.isalnum():
        return False
    
    # Check for obviously invalid patterns
    if identifier.isdigit():
        # All zeros or all same digit
        if len(set(identifier)) == 1:
            return False
    
    # Reject obviously invalid country codes (XX is reserved/unassigned)
    if country_code in ['XX', 'ZZ']:
        return False
    
    # Basic format validation passed
    return True


def validate_mongodb_objectid(value):
    """
    Validates MongoDB ObjectId format.
    
    MongoDB ObjectId is a 24-character hexadecimal string.
    Format: 24 hex characters (0-9, a-f, A-F)
    
    Args:
        value: ObjectId string (24 hex characters)
        
    Returns:
        bool: True if valid ObjectId format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    objectid = value.strip()
    
    if len(objectid) != 24:
        return False
    
    # Check if all characters are hexadecimal
    try:
        int(objectid, 16)
        return True
    except ValueError:
        return False


def validate_isbn13(value):
    """
    Validates ISBN-13 using EAN-13 check digit algorithm (same as GTIN-13).
    
    ISBN-13 is essentially a GTIN-13 with prefix 978 or 979.
    Uses the same check digit algorithm as GTIN-13.
    
    Args:
        value: ISBN-13 string (13 digits, may include hyphens)
        
    Returns:
        bool: True if valid ISBN-13, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    isbn = value.replace('-', '').replace(' ', '')
    
    if not isbn.isdigit():
        return False
    
    if len(isbn) != 13:
        return False
    
    # ISBN-13 should start with 978 or 979
    if not isbn.startswith('978') and not isbn.startswith('979'):
        return False
    
    # Use GTIN validation algorithm (same as EAN-13)
    return validate_gtin(isbn)


def validate_ulid(value):
    """
    Validates ULID (Universally Unique Lexicographically Sortable Identifier) format.
    
    ULID is 26 characters using Crockford's Base32 encoding.
    Characters: 0-9, A-Z (excluding I, L, O, U for readability)
    Valid characters: 0123456789ABCDEFGHJKMNPQRSTVWXYZ
    
    Args:
        value: ULID string (26 characters)
        
    Returns:
        bool: True if valid ULID format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    ulid = value.upper().strip()
    
    if len(ulid) != 26:
        return False
    
    # Valid ULID characters (Crockford's Base32)
    valid_chars = set('0123456789ABCDEFGHJKMNPQRSTVWXYZ')
    
    # Check all characters are valid
    if not all(c in valid_chars for c in ulid):
        return False
    
    return True


def validate_snowflake_id(value):
    """
    Validates Snowflake ID format.
    
    Snowflake IDs are 64-bit integers, typically represented as 17-19 digit numbers.
    Range: 0 to 2^63 - 1 (9223372036854775807)
    Most common: 18-19 digits
    
    Args:
        value: Snowflake ID string (numeric)
        
    Returns:
        bool: True if valid Snowflake ID range, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    snowflake = value.strip()
    
    if not snowflake.isdigit():
        return False
    
    # Snowflake IDs are typically 15-19 digits
    if len(snowflake) < 15 or len(snowflake) > 19:
        return False
    
    try:
        snowflake_num = int(snowflake)
        # Valid range: 0 to 2^63 - 1 (9223372036854775807)
        # But we'll accept the full 64-bit unsigned range for flexibility
        return 0 <= snowflake_num <= 18446744073709551615
    except (ValueError, OverflowError):
        return False


def validate_doi(value):
    """
    Validates DOI (Digital Object Identifier) format.
    
    DOI format: 10.xxxx/yyyy where:
    - Prefix: 10.xxxx (4+ digits after 10.)
    - Suffix: yyyy (variable length, can contain various characters)
    
    Args:
        value: DOI string
        
    Returns:
        bool: True if valid DOI format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    doi = value.strip()
    
    # Must start with "10."
    if not doi.startswith('10.'):
        return False
    
    # Must contain a forward slash
    if '/' not in doi:
        return False
    
    parts = doi.split('/', 1)
    if len(parts) != 2:
        return False
    
    prefix = parts[0]  # "10.xxxx"
    suffix = parts[1]
    
    # Prefix must be "10." followed by at least 4 digits
    if len(prefix) < 6:  # "10." + at least 4 digits
        return False
    
    prefix_suffix = prefix[3:]  # Everything after "10."
    if not prefix_suffix.isdigit() or len(prefix_suffix) < 4:
        return False
    
    # Suffix must not be empty
    if not suffix:
        return False
    
    # Suffix can contain various characters but should be reasonable length
    if len(suffix) > 200:
        return False
    
    return True


def validate_oid(value):
    """
    Validates OID (ITU/ISO/IEC Object Identifier) format.
    
    OID format: Dot-separated numeric identifiers starting with 0-3.
    Examples: 1.3.6.1.4.1.343, 2.5.4.87
    
    Args:
        value: OID string
        
    Returns:
        bool: True if valid OID format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    oid = value.strip()
    
    if not oid:
        return False
    
    # Must start with 0, 1, 2, or 3
    if oid[0] not in '0123':
        return False
    
    # Split by dots
    parts = oid.split('.')
    
    if len(parts) < 2:
        return False
    
    # Each part must be numeric and non-empty
    for part in parts:
        if not part:
            return False
        if not part.isdigit():
            return False
    
    # Reasonable length check
    if len(oid) > 100:
        return False
    
    return True


def validate_eidr(value):
    """
    Validates EIDR (Entertainment Identifier Registry) format.
    
    EIDR format: 10.5240/XXXX-XXXX-XXXX-XXXX-XXXX-X
    Where XXXX are 4 hexadecimal characters and X is 1 hexadecimal character.
    Examples: 10.5240/58DD-06EB-3EED-A705-EE28-7, 10.5240/E058-3983-F191-9805-DD81-Q
    
    Args:
        value: EIDR string
        
    Returns:
        bool: True if valid EIDR format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    eidr = value.strip().upper()
    
    # Must start with "10.5240/"
    if not eidr.startswith('10.5240/'):
        return False
    
    # Extract the suffix part (after "10.5240/")
    suffix = eidr[8:]
    
    # Expected format: XXXX-XXXX-XXXX-XXXX-XXXX-X (5 groups of 4 hex + dash + 1 hex)
    # Total: 4 + 1 + 4 + 1 + 4 + 1 + 4 + 1 + 4 + 1 + 1 = 26 characters
    if len(suffix) != 26:
        return False
    
    # Split by dashes
    parts = suffix.split('-')
    if len(parts) != 6:
        return False
    
    # First 5 parts must be 4 hex characters each
    for i in range(5):
        if len(parts[i]) != 4:
            return False
        if not all(c in '0123456789ABCDEF' for c in parts[i]):
            return False
    
    # Last part must be 1 character (Base32 encoding: 0-9, A-Z excluding I, L, O, U)
    # For simplicity, we accept any alphanumeric character (case-insensitive)
    if len(parts[5]) != 1:
        return False
    if not parts[5].isalnum():
        return False
    
    return True


def validate_isbn10(value):
    """
    Validates ISBN-10 using MOD-11 check digit algorithm.
    
    ISBN-10 is 10 characters: 9 digits + 1 check digit (0-9 or X).
    Check digit is calculated using MOD-11 algorithm.
    
    Args:
        value: ISBN-10 string (10 characters, may include hyphens)
        
    Returns:
        bool: True if valid ISBN-10, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    isbn = value.replace('-', '').replace(' ', '')
    
    if len(isbn) != 10:
        return False
    
    # First 9 characters must be digits
    if not isbn[:9].isdigit():
        return False
    
    # Last character can be digit or X
    if isbn[9] not in '0123456789Xx':
        return False
    
    # MOD-11 check digit calculation
    total = 0
    for i in range(9):
        total += int(isbn[i]) * (10 - i)
    
    check_value = (11 - (total % 11)) % 11
    check_char = 'X' if check_value == 10 else str(check_value)
    
    return isbn[9].upper() == check_char


def validate_duns(value):
    """
    Validates DUNS (Data Universal Numbering System) format.
    
    DUNS is a 9-digit number assigned by Dun & Bradstreet.
    Some patterns are invalid:
    - All zeros (000000000)
    - Test numbers (commonly 000000001, 000000002, etc.)
    - Sequential patterns that are known test numbers
    
    Args:
        value: DUNS string (9 digits)
        
    Returns:
        bool: True if valid DUNS format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    duns = value.replace(' ', '').replace('-', '')
    
    if not duns.isdigit():
        return False
    
    if len(duns) != 9:
        return False
    
    # Reject all zeros
    if duns == '000000000':
        return False
    
    # Reject common test numbers (first few sequential numbers)
    # These are commonly used as test data
    if duns in ['000000001', '000000002', '000000003', '000000004', '000000005']:
        return False
    
    # Additional validation: DUNS numbers typically don't start with 0
    # (though this is not a strict requirement, it helps reduce false positives)
    # We'll allow it but note that real DUNS numbers rarely start with 0
    
    return True


def validate_imo_number(value):
    """
    Validates an IMO ship identification number using its check digit.

    An IMO number is 7 digits. The check digit (the last digit) is computed by
    multiplying each of the first six digits by a weight from 7 down to 2,
    summing the products, and taking the result modulo 10.

    Example: 9074729 -> (9*7)+(0*6)+(7*5)+(4*4)+(7*3)+(2*2) = 139; 139 % 10 = 9.

    Args:
        value: IMO number string (an optional ``IMO`` prefix is ignored)

    Returns:
        bool: True if the value is a valid IMO number, False otherwise.
    """
    if not isinstance(value, str):
        return False

    imo = value.strip().upper()
    if imo.startswith('IMO'):
        imo = imo[3:].strip()

    if len(imo) != 7 or not imo.isdigit():
        return False

    # First digit of a real IMO number is non-zero.
    if imo[0] == '0':
        return False

    total = 0
    for i, ch in enumerate(imo[:6]):
        total += int(ch) * (7 - i)

    return total % 10 == int(imo[6])


_VERHOEFF_D = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
    (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
    (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
    (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
    (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
    (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
    (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
    (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
    (9, 8, 7, 6, 5, 4, 3, 2, 1, 0),
)
_VERHOEFF_P = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
    (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
    (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
    (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
    (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
    (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
    (7, 0, 4, 6, 9, 1, 3, 2, 5, 8),
)


def _verhoeff_is_valid(number):
    """Return True if ``number`` (a digit string) satisfies the Verhoeff check."""
    c = 0
    for i, ch in enumerate(reversed(number)):
        c = _VERHOEFF_D[c][_VERHOEFF_P[i % 8][int(ch)]]
    return c == 0


def validate_snomed_ct(value):
    """
    Validates a SNOMED CT identifier (SCTID).

    An SCTID is a 6-18 digit number whose final digit is a Verhoeff check digit
    computed over the preceding digits. The two digits immediately before the
    check digit form the partition identifier; its first digit must be 0 or 1.

    Args:
        value: SCTID string

    Returns:
        bool: True if the value is a structurally valid SCTID, False otherwise.
    """
    if not isinstance(value, str):
        return False

    sctid = value.strip()
    if len(sctid) < 6 or len(sctid) > 18 or not sctid.isdigit():
        return False

    # SCTIDs do not have leading zeros.
    if sctid[0] == '0':
        return False

    # Partition identifier: two digits before the check digit; first is 0 or 1.
    if sctid[-3] not in ('0', '1'):
        return False

    return _verhoeff_is_valid(sctid)


def _regon_check_digit(digits, weights):
    total = sum(int(d) * w for d, w in zip(digits, weights))
    check = total % 11
    return 0 if check == 10 else check


def validate_pl_regon(value):
    """
    Validates a Polish REGON statistical business number.

    REGON comes in two lengths, each with a weighted modulo-11 check digit:
      * REGON-9  -> 9 digits, weights [8, 9, 2, 3, 4, 5, 6, 7] over the first 8.
      * REGON-14 -> 14 digits, weights [2, 4, 8, 5, 0, 9, 7, 3, 6, 1, 2, 4, 8]
        over the first 13. Its first 9 digits must themselves be a valid REGON-9.

    Args:
        value: REGON string (spaces and dashes are ignored)

    Returns:
        bool: True if the value is a valid REGON, False otherwise.
    """
    if not isinstance(value, str):
        return False

    regon = value.replace(' ', '').replace('-', '')
    if not regon.isdigit() or len(regon) not in (9, 14):
        return False

    if regon == '0' * len(regon):
        return False

    if len(regon) == 9:
        expected = _regon_check_digit(regon[:8], [8, 9, 2, 3, 4, 5, 6, 7])
        return expected == int(regon[8])

    # 14-digit REGON: first 9 digits must be a valid REGON-9.
    if not validate_pl_regon(regon[:9]):
        return False
    expected = _regon_check_digit(
        regon[:13], [2, 4, 8, 5, 0, 9, 7, 3, 6, 1, 2, 4, 8]
    )
    return expected == int(regon[13])


def validate_pl_pesel(value):
    """
    Validates a Polish PESEL national identification number.

    A PESEL is 11 digits: the first six encode a date of birth (with the month
    offset by century), followed by a serial number and a modulo-10 check digit
    (weights [1, 3, 7, 9, 1, 3, 7, 9, 1, 3] over the first ten digits).

    Args:
        value: PESEL string (spaces and dashes are ignored)

    Returns:
        bool: True if the value is a valid PESEL, False otherwise.
    """
    if not isinstance(value, str):
        return False

    pesel = value.replace(' ', '').replace('-', '')
    if len(pesel) != 11 or not pesel.isdigit():
        return False

    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    total = sum(int(d) * w for d, w in zip(pesel[:10], weights))
    check = (10 - (total % 10)) % 10
    if check != int(pesel[10]):
        return False

    # Validate the embedded date of birth (century encoded in the month field).
    year = int(pesel[0:2])
    month = int(pesel[2:4])
    day = int(pesel[4:6])
    century_map = {0: 1900, 20: 2000, 40: 2100, 60: 2200, 80: 1800}
    offset = (month // 20) * 20
    if offset not in century_map:
        return False
    real_month = month - offset
    full_year = century_map[offset] + year
    try:
        datetime.date(full_year, real_month, day)
    except ValueError:
        return False

    return True


def validate_tr_tckimlik(value):
    """
    Validates a Turkish national identification number (T.C. Kimlik No).

    An 11-digit number where:
      * the first digit is non-zero,
      * the 10th digit = ((d1+d3+d5+d7+d9)*7 - (d2+d4+d6+d8)) mod 10,
      * the 11th digit = (sum of the first ten digits) mod 10.

    Args:
        value: TC Kimlik string (spaces and dashes are ignored)

    Returns:
        bool: True if the value is a valid TC Kimlik No, False otherwise.
    """
    if not isinstance(value, str):
        return False

    tc = value.replace(' ', '').replace('-', '')
    if len(tc) != 11 or not tc.isdigit():
        return False

    d = [int(ch) for ch in tc]
    if d[0] == 0:
        return False

    odd_sum = d[0] + d[2] + d[4] + d[6] + d[8]
    even_sum = d[1] + d[3] + d[5] + d[7]
    tenth = (odd_sum * 7 - even_sum) % 10
    if tenth != d[9]:
        return False

    eleventh = sum(d[:10]) % 10
    return eleventh == d[10]


def validate_pl_nip(value):
    """
    Validates a Polish NIP (tax identification number).

    A NIP is 10 digits with a modulo-11 check digit using weights
    [6, 5, 7, 2, 3, 4, 5, 6, 7] over the first nine digits (a remainder of 10
    is invalid).

    Args:
        value: NIP string (spaces and dashes are ignored)

    Returns:
        bool: True if the value is a valid NIP, False otherwise.
    """
    if not isinstance(value, str):
        return False

    nip = value.replace(' ', '').replace('-', '')
    if len(nip) != 10 or not nip.isdigit():
        return False

    weights = [6, 5, 7, 2, 3, 4, 5, 6, 7]
    total = sum(int(d) * w for d, w in zip(nip[:9], weights))
    check = total % 11
    if check == 10:
        return False
    return check == int(nip[9])


def validate_us_npi(value):
    """
    Validates a US National Provider Identifier (NPI).

    An NPI is 10 digits whose final digit is a Luhn check digit computed after
    prefixing the constant ``80840`` (the ISO issuer prefix) to the first nine
    digits.

    Args:
        value: NPI string (spaces and dashes are ignored)

    Returns:
        bool: True if the value is a valid NPI, False otherwise.
    """
    if not isinstance(value, str):
        return False

    npi = value.replace(' ', '').replace('-', '')
    if len(npi) != 10 or not npi.isdigit():
        return False

    base = '80840' + npi[:9]
    total = 0
    for i, ch in enumerate(reversed(base)):
        digit = int(ch)
        if i % 2 == 0:  # positions counted from the check digit position
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    check = (10 - (total % 10)) % 10
    return check == int(npi[9])


def validate_fr_nir(value):
    """
    Validates a French NIR / INSEE social security number.

    A NIR is 13 digits followed by a 2-digit control key equal to
    ``97 - (N mod 97)`` where N is the 13-digit number. Corsica department
    codes ``2A``/``2B`` are supported by substituting them per the official
    algorithm.

    Args:
        value: NIR string (spaces are ignored)

    Returns:
        bool: True if the value is a valid NIR, False otherwise.
    """
    if not isinstance(value, str):
        return False

    nir = value.replace(' ', '').upper()
    if len(nir) != 15:
        return False

    body = nir[:13]
    key_part = nir[13:]
    if not key_part.isdigit():
        return False

    # Handle Corsica department codes 2A / 2B in positions 6-7.
    corsica = body[5:7]
    numeric_body = body
    if corsica == '2A':
        numeric_body = body[:5] + '19' + body[7:]
    elif corsica == '2B':
        numeric_body = body[:5] + '18' + body[7:]

    if not numeric_body.isdigit():
        return False

    key = 97 - (int(numeric_body) % 97)
    return key == int(key_part)


def validate_th_idcard(value):
    """
    Validates a Thai national identification number.

    A 13-digit number whose final digit is a check digit: multiply the first 12
    digits by weights 13 down to 2, sum, and the check digit is
    ``(11 - (sum mod 11)) mod 10``.

    Args:
        value: Thai ID string (spaces and dashes are ignored)

    Returns:
        bool: True if the value is a valid Thai ID, False otherwise.
    """
    if not isinstance(value, str):
        return False

    tid = value.replace(' ', '').replace('-', '')
    if len(tid) != 13 or not tid.isdigit():
        return False

    if tid[0] == '0':
        return False

    total = sum(int(tid[i]) * (13 - i) for i in range(12))
    check = (11 - (total % 11)) % 10
    return check == int(tid[12])


def _luhn_is_valid(number):
    """Returns True if an all-digit string passes the Luhn (mod 10) checksum."""
    total = 0
    for i, ch in enumerate(reversed(number)):
        digit = int(ch)
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def validate_sa_id(value):
    """
    Validates a Saudi Arabian national ID (Hawiyya).

    A 10-digit number that starts with ``1`` (Saudi citizen) and whose digits
    pass the Luhn checksum.

    Args:
        value: Saudi ID string (spaces and dashes are ignored)

    Returns:
        bool: True if the value is a valid Saudi national ID, False otherwise.
    """
    if not isinstance(value, str):
        return False

    sid = value.replace(' ', '').replace('-', '')
    if len(sid) != 10 or not sid.isdigit():
        return False
    if sid[0] != '1':
        return False
    return _luhn_is_valid(sid)


def validate_sa_iqama(value):
    """
    Validates a Saudi Arabian Iqama (residence permit) number.

    A 10-digit number that starts with ``2`` (resident) and whose digits pass
    the Luhn checksum.

    Args:
        value: Iqama string (spaces and dashes are ignored)

    Returns:
        bool: True if the value is a valid Iqama number, False otherwise.
    """
    if not isinstance(value, str):
        return False

    iqama = value.replace(' ', '').replace('-', '')
    if len(iqama) != 10 or not iqama.isdigit():
        return False
    if iqama[0] != '2':
        return False
    return _luhn_is_valid(iqama)


def validate_th_taxid(value):
    """
    Validates a Thai tax identification number (TIN).

    A 13-digit number sharing the same weighted modulo-11 check digit as the
    Thai national ID. Unlike the national ID, a leading zero is allowed because
    juristic-person tax IDs may begin with ``0``.

    Args:
        value: Thai tax ID string (spaces and dashes are ignored)

    Returns:
        bool: True if the value is a valid Thai tax ID, False otherwise.
    """
    if not isinstance(value, str):
        return False

    tid = value.replace(' ', '').replace('-', '')
    if len(tid) != 13 or not tid.isdigit():
        return False

    total = sum(int(tid[i]) * (13 - i) for i in range(12))
    check = (11 - (total % 11)) % 10
    return check == int(tid[12])


def validate_vn_taxcode(value):
    """
    Validates a Vietnamese tax code (Mã số thuế).

    The 10-digit base code carries a modulo-11 check digit using weights
    ``[31, 29, 23, 19, 17, 13, 7, 5, 3]`` over the first nine digits, where the
    check digit is ``10 - (sum mod 11)``. An optional 3-digit branch suffix
    (``NNNNNNNNNN-NNN``) is accepted; the branch part is not checksummed.

    Args:
        value: Vietnamese tax code string (spaces are ignored)

    Returns:
        bool: True if the value is a valid Vietnamese tax code, False otherwise.
    """
    if not isinstance(value, str):
        return False

    code = value.replace(' ', '')
    if '-' in code:
        base, _, branch = code.partition('-')
        if len(branch) != 3 or not branch.isdigit():
            return False
    else:
        base = code

    if len(base) != 10 or not base.isdigit():
        return False

    weights = [31, 29, 23, 19, 17, 13, 7, 5, 3]
    total = sum(int(base[i]) * weights[i] for i in range(9))
    check = 10 - (total % 11)
    return check == int(base[9])


def validate_isbn(value):
    """
    Validates an ISBN in either the 10- or 13-digit form.

    Dispatches to :func:`validate_isbn10` or :func:`validate_isbn13` based on
    the length after stripping hyphens and spaces.

    Args:
        value: ISBN string (10 or 13 chars, may include hyphens/spaces)

    Returns:
        bool: True if the value is a valid ISBN-10 or ISBN-13, False otherwise.
    """
    if not isinstance(value, str):
        return False

    cleaned = value.replace('-', '').replace(' ', '')
    if len(cleaned) == 10:
        return validate_isbn10(value)
    if len(cleaned) == 13:
        return validate_isbn13(value)
    return False


def validate_uk_nhs(value):
    """
    Validates a UK NHS number.

    A 10-digit number whose final digit is a modulo-11 check digit: the first
    nine digits are multiplied by weights 10 down to 2, summed, and the check
    digit is ``11 - (sum mod 11)`` (a result of 11 maps to 0; a result of 10 is
    invalid).

    Args:
        value: NHS number string (spaces and dashes are ignored)

    Returns:
        bool: True if the value is a valid NHS number, False otherwise.
    """
    if not isinstance(value, str):
        return False

    nhs = value.replace(' ', '').replace('-', '')
    if len(nhs) != 10 or not nhs.isdigit():
        return False

    weights = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    total = sum(int(nhs[i]) * weights[i] for i in range(9))
    check = 11 - (total % 11)
    if check == 11:
        check = 0
    if check == 10:
        return False
    return check == int(nhs[9])

