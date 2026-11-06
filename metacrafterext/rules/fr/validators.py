"""
Validation functions for French-specific identifiers.
"""

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
