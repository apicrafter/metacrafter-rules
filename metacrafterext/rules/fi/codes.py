"""Validators of Finnish area codes found in 2024 snapshots of Finnish open data portals (Dateno sources
cdi00000621 to cdi00000633: the GeoServer of Statistics Finland, Avoindata.fi, Tampere, Helsinki Region
Infoshare): municipality numbers, region, sub-region and electoral district codes of the classifications
of Statistics Finland, postal codes, and the cell codes of statistical grids.

Each function takes one value and returns True when it has the form of the code.
"""
import re


def _text(value):
    """The value as stripped text; a float of a whole number (91.0) as its integer text."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    text = str(value).strip()
    if re.fullmatch(r"\d+\.0", text):
        return text[:-2]
    return text


_KUNTA = re.compile(r"^\d{1,3}$")


def validate_fi_kuntanumero(value):
    """A Finnish municipality number: three digits (091 Helsinki); a file that stores it as a
    number loses the leading zeros (91, 5)."""
    return bool(_KUNTA.match(_text(value)))


_MAAKUNTA = frozenset("01 02 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21".split())


def validate_fi_maakunta_code(value):
    """A Finnish region code: 01 to 21 without 03 (20 was Itä-Uusimaa until 2011); the leading
    zero may be lost."""
    text = _text(value)
    return text.zfill(2) in _MAAKUNTA and len(text) <= 2


_SEUTUKUNTA = re.compile(r"^\d{3}$")


def validate_fi_seutukunta_code(value):
    """A Finnish sub-region code: three digits (011 Helsinki)."""
    return bool(_SEUTUKUNTA.match(_text(value)))


_VAALIPIIRI = re.compile(r"^(?:0?[1-9]|1[0-5])(?: \D.*vaalipiiri)?$", re.I)


def validate_fi_vaalipiiri_code(value):
    """A Finnish electoral district number: 01 to 13 (to 15 before 2015), also before its name
    (12 Oulun vaalipiiri)."""
    return bool(_VAALIPIIRI.match(_text(value)))


_POSTCODE = re.compile(r"^\d{3,5}$")


def validate_fi_postcode(value):
    """A Finnish postal code: five digits (00100); a file that stores it as a number loses the
    leading zeros (100, 920)."""
    return bool(_POSTCODE.match(_text(value)))


_GRID_CELL = re.compile(r"^(?:CRS\d{4,5}RES)?\d{1,5}k?mN\d{2,8}E\d{2,8}$")


def validate_inspire_grid_cell_code(value):
    """A cell code of a statistical grid in the INSPIRE form: cell size, N and northing, E and
    easting (1kmN2599E4695, 250mN66380E02720)."""
    return bool(_GRID_CELL.match(_text(value)))
