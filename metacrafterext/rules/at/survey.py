"""Validators for Austrian cadastre and national survey codes of the BEV (Bundesamt für Eich- und
Vermessungswesen): cadastral municipality numbers, parcel numbers, land register entry numbers,
ÖK 50 map sheets, Gauss-Krüger meridian zones and control point designations.

Sources: the BEV interface descriptions of the control point files (BEV_S_GV_TP-EP-PP-MP-HP-CSV
V1.8.1, BEV_S_GV_TP-EP-ETRS89_CSV V1.1) and of the cadastre parcel data (BEV_S_KA_Grundstuecksdaten
-csv V1.2).
"""
import re

# KG-Nummer 01002 to 92129 (BEV); read as an integer, a number of Vienna loses its zero (1204).
_KG = re.compile(r"^(?:0[1-9]|[1-8]\d|9[0-2])\d{3}$")


def _whole(value):
    """The text of a whole number, without the .0 of a value read as a float."""
    text = str(value).strip()
    return text[:-2] if text.endswith(".0") else text


def validate_at_kg_number(value):
    """An Austrian cadastral municipality number, 01002 to 92129: five digits, or four when the
    leading zero of a Vienna number was lost (1204)."""
    text = _whole(value)
    if len(text) == 4 and text.isdigit():
        text = "0" + text
    return bool(_KG.match(text)) and 1002 <= int(text) <= 92129


def validate_at_kg_number_text(value):
    """An Austrian cadastral municipality number written with five digits (01204): the check of a
    field named only KG, which may also be a weight in kilograms."""
    text = str(value).strip()
    return len(text) == 5 and validate_at_kg_number(text)


_GST = re.compile(r"^\.?[1-9]\d{0,4}(?:/[1-9]\d{0,3})?$")


def validate_at_grundstuecksnummer(value):
    """An Austrian parcel number: main number, optionally a slash and the subdivision number, with
    a leading dot for building plots (2799, 551/1, .129/3)."""
    return bool(_GST.match(str(value).strip()))


def validate_at_einlagezahl(value):
    """An Austrian land register entry number (Einlagezahl), 1 to 99999."""
    text = _whole(value)
    return text.isdigit() and not text.startswith("0") and len(text) <= 5


def validate_at_oek50_sheet(value):
    """A sheet number of the Austrian map 1:50,000 in the BMN layout, 1 to 213."""
    text = _whole(value)
    return text.isdigit() and not text.startswith("0") and 1 <= int(text) <= 213


def validate_at_gk_meridian(value):
    """A meridian zone of the Austrian MGI Gauss-Krüger grid: M28, M31 or M34."""
    return str(value).strip().upper() in ("M28", "M31", "M34")


# TP + number + hyphen + ÖK 50 sheet, or EP + KG number + hyphen + number; then the
# monumentation mark (letter and digit). Connected points add a semicolon and the point name.
_FESTPUNKT = re.compile(r"^(?:TP\d{1,4}-(?P<sheet>\d{1,3})|EP(?P<kg>\d{5})-\d{1,4})[A-Z]\d$")


def validate_at_festpunkt_id(value):
    """A BEV control point designation (TP47-38T1, EP01404-3545E1), alone or followed by a
    semicolon and the point name as in the ANSCHLUSS fields (TP4-84T1; GRÄN, KIRCHE)."""
    head = str(value).strip().split(";", 1)[0].strip()
    m = _FESTPUNKT.match(head)
    if not m:
        return False
    if m.group("sheet"):
        return validate_at_oek50_sheet(m.group("sheet"))
    return validate_at_kg_number(m.group("kg"))
