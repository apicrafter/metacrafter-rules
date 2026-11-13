"""
Validation functions for global identifiers with check digits.

These functions validate identifiers that use check digit algorithms to reduce
false positives in pattern matching.
"""
import datetime
import re
from metacrafterext.rules.common.placeholders import rejects_repeated_digits


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
    
    # Remove spaces (also no-break spaces of office exports) and dashes, convert to uppercase
    iban = value.replace(' ', '').replace('\u00a0', '').replace('\u202f', '').replace('-', '').upper()
    
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


@rejects_repeated_digits
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


@rejects_repeated_digits
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


@rejects_repeated_digits
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


@rejects_repeated_digits
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


# Mobile country codes (MCC) assigned in ITU-T E.212, with the codes in use that
# ITU does not list (289 Abkhazia, 995 British Indian Ocean Territory).
# 001 is the test network code, 901/902 are international operators, 991 is for
# trials of international services and 999 is for internal use (private networks).
IMSI_MCC_CODES = frozenset("""
001
202 204 206 208 212 213 214 216 218 219 220 221 222 225 226 228 230 231 232 234
235 238 240 242 244 246 247 248 250 255 257 259 260 262 266 268 270 272 274 276
278 280 282 283 284 286 288 289 290 292 293 294 295 297
302 308 310 311 312 313 314 315 316 330 332 334 338 340 342 344 346 348 350 352
354 356 358 360 362 363 364 365 366 368 370 372 374 376
400 401 402 404 405 406 410 412 413 414 415 416 417 418 419 420 421 422 424 425
426 427 428 429 430 431 432 434 436 437 438 440 441 450 452 454 455 456 457 460
461 466 467 470 472
502 505 510 514 515 520 525 528 530 536 537 539 540 541 542 543 544 545 546 547
548 549 550 551 552 553 554 555
602 603 604 605 606 607 608 609 610 611 612 613 614 615 616 617 618 619 620 621
622 623 624 625 626 627 628 629 630 631 632 633 634 635 636 637 638 639 640 641
642 643 645 646 647 648 649 650 651 652 653 654 655 657 658 659
702 704 706 708 710 712 714 716 722 724 730 732 734 736 738 740 742 744 746 748
750
901 902 991 995 999
""".split())


@rejects_repeated_digits
def validate_imsi(value):
    """
    Validates IMSI (International Mobile Subscriber Identity).

    IMSI is a 15-digit number with structure: MCC (3 digits) + MNC (2-3 digits) + MSIN (9-10 digits)
    The MCC must be an assigned mobile country code (IMSI_MCC_CODES): about a
    quarter of random 15-digit numbers start with one.

    Args:
        value: IMSI string (15 digits)

    Returns:
        bool: True if valid IMSI format, False otherwise
    """
    if not isinstance(value, str):
        return False

    imsi = value.replace(' ', '').replace('-', '')

    if not (imsi.isascii() and imsi.isdigit()):
        return False

    if len(imsi) != 15:
        return False

    # Structure: MCC (3 digits) + MNC (2-3 digits) + MSIN (9-10 digits)
    # MCC: Mobile Country Code, one of the assigned codes
    if imsi[:3] not in IMSI_MCC_CODES:
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


@rejects_repeated_digits
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


# ISO 3166-1 alpha-2 codes assigned to countries and territories.
ISO_3166_1_ALPHA2 = frozenset("""
AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BL BM BN BO BQ
BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CW CX CY CZ DE DJ DK DM
DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS
GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN
KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ
MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM
PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV
SX SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI
VN VU WF WS YE YT ZA ZM ZW
""".split())

# Country code elements of ISRC beyond ISO 3166-1 alpha-2. The International ISRC Agency
# allocates extra codes to national agencies (QM, QT, QZ for the US, UK and GX for PPL UK,
# BC, BK, BP, BX for Brazil, CB for Canada, FX for France, KS for South Korea, ZB for South
# Africa), keeps CP, DG and ZZ for itself, and uses QN, XK and YU. ISRCs are permanent, so
# codes withdrawn from ISO 3166-1 after the ISRC began in 1986 stay valid in old codes.
ISRC_EXTRA_COUNTRY_CODES = frozenset("""
BC BK BP BX CB CP DG FX GX KS QM QN QT QZ UK XK YU ZB ZZ
AN BU CS DD NT SU TP YD ZR
""".split())

_ISRC_PATTERN = re.compile(r'^([A-Z]{2})[A-Z0-9]{3}[0-9]{7}$')


def validate_isrc(value):
    """
    Validates ISRC format and its country code (ISRC has no check digit).

    Format: CC XXX YY NNNNN (country code, 3 alphanumeric registrant characters,
    2-digit year, 5-digit designation). The country code must be an ISO 3166-1
    alpha-2 code or a code the International ISRC Agency allocated
    (ISRC_EXTRA_COUNTRY_CODES); unassigned codes such as XX are rejected.

    Args:
        value: ISRC string (12 characters, dashes and spaces are ignored)

    A value with an ISO 3166 country code that passes the ISIN check digit is rejected:
    ISINs have the same shape when their positions 6-12 are digits.

    Returns:
        bool: True if valid ISRC, False otherwise
    """
    if not isinstance(value, str):
        return False

    isrc = value.upper().replace('-', '').replace(' ', '')

    match = _ISRC_PATTERN.match(isrc)
    if match is None:
        return False

    country = match.group(1)
    if country not in ISO_3166_1_ALPHA2 and country not in ISRC_EXTRA_COUNTRY_CODES:
        return False
    # An ISIN has the same length and starts with a country code too; one with an ISO 3166
    # country code that passes the ISIN check digit is an ISIN (DE0006201106), not an ISRC
    # (metacrafter-rules #61). Codes of the ISRC Agency (UK, QM, ZZ) are not ISIN prefixes.
    return not (country in ISO_3166_1_ALPHA2 and validate_isin(isrc))


_MOD11_2_PATTERN = re.compile(r'^[0-9]{15}[0-9X]$')


def _iso7064_mod11_2_is_valid(number):
    """
    Checks a 16-character number whose last character is an ISO 7064 MOD 11-2 check
    character (a digit or X), as used by ISNI (ISO 27729) and ORCID.
    """
    if not _MOD11_2_PATTERN.match(number):
        return False
    total = 0
    for digit in number[:-1]:
        total = (total + int(digit)) * 2
    check_value = (12 - total % 11) % 11
    check_char = 'X' if check_value == 10 else str(check_value)
    return number[-1] == check_char


@rejects_repeated_digits
def validate_isni(value):
    """
    Validates ISNI (ISO 27729) using the ISO 7064 MOD 11-2 check character.

    Args:
        value: ISNI string (16 characters, with or without spaces or dashes;
            the check character can be X)

    Returns:
        bool: True if valid ISNI, False otherwise
    """
    if not isinstance(value, str):
        return False

    isni = value.upper().replace(' ', '').replace('-', '')
    return _iso7064_mod11_2_is_valid(isni)


def validate_orcid(value):
    """
    Validates ORCID using the ISO 7064 MOD 11-2 check character.

    ORCID format: 0000-0001-2345-6789 (16 digits with dashes) or 0000-0001-2345-678X
    The last character is a check character calculated using ISO 7064 MOD 11-2.
    ORCID iDs start with 0000-000 or, since 2023, with 0009-00.

    Args:
        value: ORCID string (with or without dashes)

    Returns:
        bool: True if valid ORCID, False otherwise
    """
    if not isinstance(value, str):
        return False

    orcid = value.upper().replace('-', '').replace(' ', '')

    # Must start with 0000-000 or 0009-00
    if not orcid.startswith(('0000000', '000900')):
        return False

    return _iso7064_mod11_2_is_valid(orcid)


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
    r"""
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


@rejects_repeated_digits
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


@rejects_repeated_digits
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


@rejects_repeated_digits
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


@rejects_repeated_digits
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
    The number may have the prefix AS, as in AS64496.
    
    Args:
        value: ASN string (digits, optionally prefixed with AS)
        
    Returns:
        bool: True if valid ASN range, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    asn = value[2:] if value[:2].upper() == 'AS' else value
    
    if not asn.isdigit() or not asn.isascii():
        return False
    
    try:
        asn_num = int(asn)
        # Valid ASN range: 1 to 4294967295 (2^32 - 1)
        return 1 <= asn_num <= 4294967295
    except (ValueError, OverflowError):
        return False


# Language tag syntax of RFC 5646 (section 2.1), subtags in their fixed order.
_LANGUAGE_TAG_PATTERN = re.compile(
    r'[a-z]{2,3}(?:-[a-z]{3}){0,3}'           # language, up to 3 extlang subtags
    r'(?:-[a-z]{4})?'                          # script
    r'(?:-(?:[a-z]{2}|[0-9]{3}))?'             # region
    r'(?:-(?:[a-z0-9]{5,8}|[0-9][a-z0-9]{3}))*'  # variants
    r'(?:-[a-wyz0-9](?:-[a-z0-9]{2,8})+)*'     # extensions: singleton other than x
    r'(?:-x(?:-[a-z0-9]{1,8})+)?'              # private use
)


def validate_language_tag(value):
    """
    Validates IETF BCP 47 language tag syntax (RFC 5646), case-insensitive.

    Format: language[-extlang][-script][-region][-variant]*[-extension]*[-privateuse]
    - language: 2-3 letters (ISO 639), optionally followed by up to 3 extlang
      subtags of 3 letters (zh-yue)
    - script: 4 letters (ISO 15924)
    - region: 2 letters (ISO 3166-1) or 3 digits (UN M.49)
    - variant: 5-8 alphanumeric, or a digit + 3 alphanumeric (de-CH-1901)
    - extension: a singleton (one letter or digit other than x) followed by
      subtags of 2-8 alphanumeric (en-u-ca-gregory)
    - privateuse: 'x' followed by subtags of 1-8 alphanumeric (en-US-x-private)

    The check is syntactic: a region such as XX is accepted (XA..XZ are private-use
    regions in the IANA registry). 4-letter (reserved) and 5-8 letter (registered)
    language subtags are well-formed in RFC 5646, but the IANA registry has none,
    so they are rejected: values such as "english" are words, not language tags.
    Private-use-only tags (x-...) and grandfathered tags (i-klingon) are rejected too.

    Args:
        value: Language tag string

    Returns:
        bool: True if valid BCP 47 format, False otherwise
    """
    if not isinstance(value, str):
        return False

    # Non-ASCII letters can lower-case to ASCII ones (the Kelvin sign to k).
    if not value.isascii():
        return False

    tag = value.strip().lower()

    return _LANGUAGE_TAG_PATTERN.fullmatch(tag) is not None


# VAT number formats of the VIES system (country prefix, then the number).
# Greece uses the prefix EL, Northern Ireland XI.
_EU_VAT_FORMATS = {
    'AT': r'U\d{8}',
    'BE': r'[01]\d{9}',
    'BG': r'\d{9,10}',
    'CY': r'\d{8}[A-Z]',
    'CZ': r'\d{8,10}',
    'DE': r'\d{9}',
    'DK': r'\d{8}',
    'EE': r'\d{9}',
    'EL': r'\d{9}',
    'ES': r'[A-Z]\d{7}[A-Z0-9]|\d{8}[A-Z]',
    'FI': r'\d{8}',
    'FR': r'[0-9A-HJ-NP-Z]{2}\d{9}',
    'HR': r'\d{11}',
    'HU': r'\d{8}',
    'IE': r'\d{7}[A-W][A-IW]?|\d[A-Z+*]\d{5}[A-W]',
    'IT': r'\d{11}',
    'LT': r'\d{9}|\d{12}',
    'LU': r'\d{8}',
    'LV': r'\d{11}',
    'MT': r'\d{8}',
    'NL': r'\d{9}B\d{2}',
    'PL': r'\d{10}',
    'PT': r'\d{9}',
    'RO': r'[1-9]\d{1,9}',
    'SE': r'\d{10}01',
    'SI': r'\d{8}',
    'SK': r'\d{10}',
    'XI': r'\d{9}|\d{12}|GD\d{3}|HA\d{3}',
}
_EU_VAT_RES = {
    country: re.compile(r'(?:%s)' % pattern, re.ASCII)
    for country, pattern in _EU_VAT_FORMATS.items()
}


def validate_eu_vat(value, country_code=None):
    """
    Validates an EU VAT number in the compact form that the VIES system checks.

    The number is the 2-letter code of the member state (EL for Greece, XI
    for Northern Ireland) followed by the national number, with no spaces or
    other separators: ``DE136695976``, ``FR40303265045``, ``NL004495445B01``.

    - The national number must have the format of its country.
    - German and French numbers must also pass their check digits
      (:func:`metacrafterext.rules.de.validators.validate_de_ust`,
      :func:`metacrafterext.rules.fr.validators.validate_fr_vat`).
    - Numbers of one repeated digit are rejected.

    Args:
        value: VAT number string
        country_code: Optional 2-letter country code the number must belong to
            (GR is read as EL)

    Returns:
        bool: True if valid EU VAT number, False otherwise
    """
    if not isinstance(value, str):
        return False

    vat = value.strip()
    country, number = vat[:2], vat[2:]
    if country_code is not None:
        expected = country_code.upper()
        if country != ('EL' if expected == 'GR' else expected):
            return False

    pattern = _EU_VAT_RES.get(country)
    if pattern is None or not pattern.fullmatch(number):
        return False

    digits = ''.join(ch for ch in number if ch.isdigit())
    if len(digits) == len(number) and len(set(digits)) == 1:
        return False

    if country == 'DE':
        from metacrafterext.rules.de.validators import validate_de_ust
        return validate_de_ust(vat)
    if country == 'FR':
        from metacrafterext.rules.fr.validators import validate_fr_vat
        return validate_fr_vat(vat)
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

    # 26 Base32 characters carry 130 bits; a ULID has 128, so the first
    # character is at most 7 (the largest ULID is 7ZZZZZZZZZZZZZZZZZZZZZZZZZ).
    if ulid[0] not in '01234567':
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
        # Dot notation writes arcs without leading zeros (0.0391 is a decimal fraction)
        if len(part) > 1 and part[0] == '0':
            return False

    # Under the root arcs 0 (itu-t) and 1 (iso) the second arc is 0..39 (ITU-T X.660), so
    # 0.39106583072100315 is a fraction, not an OID.
    if parts[0] in ('0', '1') and int(parts[1]) > 39:
        return False

    # Reasonable length check
    if len(oid) > 100:
        return False
    
    return True


def validate_oid_value(value):
    """
    Validates an OID found by value alone: validate_oid() and at least three arcs.

    Two arcs (0.1, 1.5) are far more often decimal numbers than OIDs, such as crop offsets
    or ratios, so a value-only match needs three arcs (2.5.4, 1.3.6.1.4.1.343). Fields
    named as OIDs are matched by the field-name rule.
    """
    return validate_oid(value) and value.strip().count('.') >= 2


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


@rejects_repeated_digits
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


@rejects_repeated_digits
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


@rejects_repeated_digits
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


@rejects_repeated_digits
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


@rejects_repeated_digits
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


@rejects_repeated_digits
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


AE_EMIRATES_ID_FIRST_YEAR = 1900


def validate_ae_emirates_id(value):
    """
    Validates a UAE Emirates ID number.

    15 digits: ``784`` (ISO 3166 numeric code of the UAE), a four-digit year
    (usually the year of birth), a seven-digit number and a check digit. The
    year must be from 1900 to the current year. The check digit is not checked:
    no official source confirms the algorithm.

    Args:
        value: Emirates ID string (spaces and dashes are ignored)

    Returns:
        bool: True if the value has the Emirates ID structure, False otherwise.
    """
    if not isinstance(value, str):
        return False

    eid = value.replace(' ', '').replace('-', '')
    if len(eid) != 15 or not (eid.isascii() and eid.isdigit()):
        return False
    if not eid.startswith('784'):
        return False
    year = int(eid[3:7])
    return AE_EMIRATES_ID_FIRST_YEAR <= year <= datetime.date.today().year


@rejects_repeated_digits
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


@rejects_repeated_digits
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


@rejects_repeated_digits
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


@rejects_repeated_digits
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



@rejects_repeated_digits
def validate_fi_ytunnus(value):
    """Validates a Finnish business ID (Y-tunnus), such as 0112038-9.

    Seven digits, a hyphen and a check digit: the digits are weighted 7, 9, 10, 5, 8, 4, 2;
    the remainder of the sum modulo 11 gives check digit 0 (remainder 0) or 11 - remainder.
    A remainder of 1 is never issued.

    Args:
        value: Business ID string

    Returns:
        bool: True if the check digit is valid, False otherwise
    """
    if not isinstance(value, str):
        return False
    match = re.fullmatch(r"(\d{7})-?(\d)", value.strip())
    if not match:
        return False
    remainder = sum(int(d) * w for d, w in zip(match.group(1), (7, 9, 10, 5, 8, 4, 2))) % 11
    if remainder == 1:
        return False
    return int(match.group(2)) == (0 if remainder == 0 else 11 - remainder)


@rejects_repeated_digits
def validate_cl_rut(value):
    """Validates a Chilean RUT/RUN, such as 76.123.456-K or 78325576-6.

    The body digits are weighted 2, 3, 4, 5, 6, 7 from the right (repeating); 11 minus the
    sum modulo 11 is the check character, with 11 written 0 and 10 written K.

    Args:
        value: RUT string, with or without dots

    Returns:
        bool: True if the check character is valid, False otherwise
    """
    if not isinstance(value, str):
        return False
    match = re.fullmatch(r"(\d{1,2}(?:\.?\d{3}){2})-?([\dkK])", value.strip())
    if not match:
        return False
    body = match.group(1).replace(".", "")
    total = sum(int(d) * (2 + i % 6) for i, d in enumerate(reversed(body)))
    check = 11 - total % 11
    expected = "0" if check == 11 else "K" if check == 10 else str(check)
    return match.group(2).upper() == expected


def _luhn_ok(digits):
    """True when a string of digits passes the Luhn (mod 10) check."""
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


_SE_ORGNR = re.compile(r'^(\d{6})-?(\d{4})$')


def validate_se_orgnr(value):
    """
    Validates a Swedish organisation number (organisationsnummer): ten digits, written
    NNNNNN-NNNN, whose third digit is 2 or more (personal identity numbers have a month
    there) and whose last digit is the Luhn check digit.

    Estonian procurement ids such as 315341-0000 have the same shape (metacrafter-rules #61).
    """
    if not isinstance(value, str):
        return False
    match = _SE_ORGNR.match(value.strip())
    if match is None:
        return False
    digits = match.group(1) + match.group(2)
    return int(digits[2]) >= 2 and _luhn_ok(digits)


_US_DEA = re.compile(r'^([A-Z])([A-Z9])(\d{7})$')


def validate_us_dea(value):
    """
    Validates a US DEA registration number: a registrant type letter, the first letter of
    the registrant's last name (or 9), six digits and a check digit. The check digit is the
    last digit of the sum of digits 1, 3 and 5 plus twice the sum of digits 2, 4 and 6.

    A contract number such as EC2017481 has the shape but not the check digit
    (metacrafter-rules #61).
    """
    if not isinstance(value, str):
        return False
    match = _US_DEA.match(value.strip().upper())
    if match is None:
        return False
    d = [int(ch) for ch in match.group(3)]
    return (d[0] + d[2] + d[4] + 2 * (d[1] + d[3] + d[5])) % 10 == d[6]


def validate_hu_giro(value):
    """
    Validates a Hungarian bank branch routing code (pénzforgalmi jelzőszám): eight digits,
    the first eight of an account number, whose digits weighted 9, 7, 3, 1, 9, 7, 3, 1 sum
    to a multiple of 10 (the last digit is the check digit).
    """
    if not isinstance(value, str):
        return False
    digits = value.strip()
    if len(digits) != 8 or not digits.isdigit():
        return False
    weights = (9, 7, 3, 1, 9, 7, 3, 1)
    return sum(int(ch) * w for ch, w in zip(digits, weights)) % 10 == 0


def validate_gr_gemi(value):
    """
    Validates the shape of a Greek General Commercial Registry number (ΓΕΜΗ): twelve
    digits, or nine to eleven when a sheet stored it as a number and dropped the leading
    zeros (51772519000). A float cell (51772519000.0) is read as its integer.
    """
    if not isinstance(value, str):
        return False
    text = value.strip()
    if text.endswith(".0"):
        text = text[:-2]
    return 9 <= len(text) <= 12 and text.isdigit()


def _code_text(value):
    text = str(value).strip()
    return text[:-2] if text.endswith(".0") else text


def validate_it_istat_province(value):
    """An Italian ISTAT province code: three digits, 001 to 299 (historical and statistical
    codes included). The two-letter sigla (TO) is another type."""
    text = _code_text(value)
    return len(text) == 3 and text.isdigit() and 1 <= int(text) <= 299


def validate_hu_county_code(value):
    """A Hungarian county number of two digits, 01 to 20."""
    text = _code_text(value)
    return len(text) == 2 and text.isdigit() and 1 <= int(text) <= 20


def validate_ro_county_code(value):
    """A Romanian SIRUTA county number: 1 to 40, 51 or 52."""
    text = _code_text(value)
    if not text.isdigit() or len(text) > 2:
        return False
    number = int(text)
    return 1 <= number <= 40 or number in (51, 52)


def validate_cz_cast_obce(value):
    """A Czech RÚIAN code of a part of a municipality: five or six digits."""
    text = _code_text(value)
    return text.isdigit() and 5 <= len(text) <= 6


_NEAK_SPECIALTY = re.compile(r"^\d{3}[0-9A-Z]$")


def validate_hu_neak_specialty(value):
    """A Hungarian NEAK specialty code: three digits and a digit or a letter (2200, 010C)."""
    return bool(_NEAK_SPECIALTY.match(str(value).strip()))


_BUDGET_LINE = re.compile(r"^(?:19|20)\d{2} \d{3,6} -\s*(?:\d{5})?\s*-\s*(?:\d{5})?(?:\s.*)?$")


def validate_es_aplicacion_presupuestaria(value):
    """Spanish budget lines (aplicación presupuestaria), one per line: the year, the organic, the
    programme and the economic code (2026 001130 - 33210 - 62999), maybe followed by an amount;
    the programme and economic codes may be empty."""
    lines = [line.strip() for line in str(value).splitlines() if line.strip()]
    return bool(lines) and all(_BUDGET_LINE.match(line) for line in lines)


_NO_ORGNR_WEIGHTS = (3, 2, 7, 6, 5, 4, 3, 2)


@rejects_repeated_digits
def validate_no_orgnr(value):
    """Validates a Norwegian organisation number (organisasjonsnummer) of the Brønnøysund
    Register Centre: nine digits starting with 8 or 9 (922727457, 974 760 673, NO 974760673 MVA).

    The first eight digits are weighted 3, 2, 7, 6, 5, 4, 3, 2; 11 minus the sum modulo 11 is
    the check digit, 11 written 0; a remainder of 1 (check digit 10) is not issued. Chilean
    RUTs without dots and dash use the same weights, so a plain nine-digit number is not
    told apart by its value: the field name decides (metacrafter-rules #69).
    """
    if not isinstance(value, str):
        return False
    text = re.sub(r"[\s.]", "", value.strip().upper())
    text = re.sub(r"^NO", "", text)
    text = re.sub(r"MVA$", "", text)
    if not re.fullmatch(r"[89]\d{8}", text):
        return False
    total = sum(int(d) * w for d, w in zip(text[:8], _NO_ORGNR_WEIGHTS))
    check = 11 - total % 11
    if check == 10:
        return False
    return int(text[8]) == (0 if check == 11 else check)
