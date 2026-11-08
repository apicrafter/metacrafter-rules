"""
Validation functions for French-specific identifiers.
"""

from metacrafterext.rules.common.placeholders import rejects_repeated_digits

# Characters of the check key; I and O are not used.
_FR_VAT_KEY_ALPHABET = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'


def _luhn_is_valid(digits):
    total = 0
    for i, ch in enumerate(reversed(digits)):
        digit = int(ch)
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def validate_fr_vat(value):
    """
    Validates a French VAT number (numéro de TVA intracommunautaire).

    The number is ``FR``, a 2-character check key and the 9-digit SIREN of
    the business:

    - The SIREN has a Luhn check digit (numbers of Monaco, whose SIREN part
      starts with 000, are not SIREN numbers and skip this check).
    - A numeric key equals ``(12 + 3 * (SIREN mod 97)) mod 97``.
    - Newer keys contain a letter (the alphabet has no I and O) and are
      checked against the SIREN by the algorithm python-stdnum uses.

    Args:
        value: French VAT string (spaces, dots and dashes are ignored)

    Returns:
        bool: True if valid French VAT number, False otherwise
    """
    if not isinstance(value, str):
        return False

    vat = value.replace(' ', '').replace('-', '').replace('.', '').upper()
    if len(vat) != 13 or not vat.startswith('FR'):
        return False

    key, siren = vat[2:4], vat[4:]
    if not siren.isdigit() or not siren.isascii():
        return False
    if any(ch not in _FR_VAT_KEY_ALPHABET for ch in key):
        return False
    if not siren.startswith('000') and not _luhn_is_valid(siren):
        return False

    if key.isdigit():
        return int(key) == int(siren + '12') % 97
    if key[0].isdigit():
        check = _FR_VAT_KEY_ALPHABET.index(key[0]) * 24 + _FR_VAT_KEY_ALPHABET.index(key[1]) - 10
    else:
        check = _FR_VAT_KEY_ALPHABET.index(key[0]) * 34 + _FR_VAT_KEY_ALPHABET.index(key[1]) - 100
    return (int(siren) + 1 + check // 11) % 11 == check % 11


# The card with a 12-digit number was issued from 1988 (pilot in Hauts-de-Seine) until the
# card with a 9-character number replaced it in 2021.
FR_CNI_FIRST_YEAR = 1988
FR_CNI_LAST_YEAR = 2021


@rejects_repeated_digits
def validate_fr_cni(value):
    """
    Validates the number of a French national identity card (CNI) issued from 1988 to 2021.

    The number has 12 digits:

    - digits 1-2: year of issue, digits 3-4: month of issue;
    - digits 5-7: issuing department and office (before 2017 a 2-digit department
      and the sub-prefecture, since 2017 a 3-digit department);
    - digits 8-12: sequence number assigned in chronological order.

    The year must be from 1988 to 2021 and the month from 01 to 12. The number has no
    check digit: the check digit is character 13 of the second MRZ line, computed over
    the 12 digits. Digits 5-7 are not checked: their encoding changed in 2017 and few
    3-digit values are invalid in both forms. The card issued since 2021 has a
    9-character alphanumeric number and is not matched.

    Args:
        value: CNI number string (spaces are ignored)

    Returns:
        bool: True if the value has the structure of a CNI number, False otherwise.
    """
    if not isinstance(value, str):
        return False

    cni = value.replace(' ', '')
    if len(cni) != 12 or not (cni.isascii() and cni.isdigit()):
        return False

    year = int(cni[0:2])
    year += 1900 if year >= FR_CNI_FIRST_YEAR % 100 else 2000
    month = int(cni[2:4])
    return FR_CNI_FIRST_YEAR <= year <= FR_CNI_LAST_YEAR and 1 <= month <= 12


def validate_fr_siret(value):
    """SIRET (14 digits): Luhn check, or for La Poste (SIREN 356000000) a digit sum divisible by 5."""
    if not isinstance(value, str):
        return False
    digits = value.replace(" ", "")
    if len(digits) != 14 or not digits.isdigit():
        return False
    if digits.startswith("356000000"):
        return sum(int(d) for d in digits) % 5 == 0
    return _luhn_is_valid(digits)
