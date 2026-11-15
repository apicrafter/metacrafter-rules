"""Earthquake catalogues, found in the Chilean files of metacrafter-testdata (the seismicity catalogues of the
Integrated Plate boundary Observatory Chile and of the 2015 Illapel aftershocks, datos.uchile.cl, a 2024
snapshot): the magnitude of an event."""
import re

_NUMBER = re.compile(r"[+-]?\d{1,2}(?:[.,]\d{1,4})?")
_MISSING = frozenset(("na", "nan", "n/a", "-", "--", "-9.9", "-9.99", "-999", "-999.0", "9.99", "0", "0.0", "0.00"))
# magType of a catalogue, sometimes in the magnitude column of merged tables: Mw, ML, mb, Ms, Md, Mwc
_TYPED = re.compile(r"^(?:m[wlbsdcjnh][a-z]{0,2}\s*=?\s*)?([+-]?\d{1,2}(?:[.,]\d{1,4})?)(?:\s*m[wlbsdcjnh][a-z]{0,2})?$", re.I)


def validate_earthquake_magnitude(value):
    """An earthquake magnitude: a number from -3 to 10 (4.46, 1.864, 8.8, -0.3, Mw 6.1, 5.2 ML), or a
    marker of no magnitude (NaN, -9.9). Not 25, 1200 or a word."""
    text = str(value).strip()
    if text.lower() in _MISSING:
        return True
    match = _TYPED.match(text)
    if not match:
        return False
    number = float(match.group(1).replace(",", "."))
    return -3.0 <= number <= 10.0


def validate_earthquake_magnitude_decimal(value):
    """A magnitude written with its decimals (4.46, 1.9), which whole numbers from 1 to 10 (a rating, a
    rank) are not."""
    text = str(value).strip()
    return validate_earthquake_magnitude(text) and bool(re.search(r"[.,]\d", text))
