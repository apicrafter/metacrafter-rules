"""Slovenian codes found in a 2024 snapshot of the open data portal of Slovenia (podatki.gov.si, Dateno
source cdi00001493): activity codes (SKD), budget user codes, heritage register numbers (EŠD), cadastral
municipality codes, parcel numbers, statistical regions, salary subgroups, registration numbers, tax numbers
and postal codes.
"""
import re

_SKD = re.compile(r"(?:[A-U] ?)?\d{2}\.\d{3}")
_PU = re.compile(r"\d{5}")
_ESD = re.compile(r"\d{1,5}")
_KO = re.compile(r"\d{1,4}(?:\s*-\s*\S.*)?")
_PARCEL = r"\*?\d{1,5}(?:/\d{1,4})?"
# 637/4; 632/4, 632/5; 637/4 in 637/5; 1526/42, k.o. Sevnica
_PARCELS = re.compile(_PARCEL + r"(?:(?:\s*[,;]\s*|\s+in\s+|\s+)" + _PARCEL + r")*(?:,?\s*k\.\s?o\.\s*\S.*)?", re.I)
_SALARY_SUBGROUP = re.compile(r"[A-K]0?[1-7]")
_MATICNA = re.compile(r"\d{7}(?:\d{3})?")
_TAX = re.compile(r"(?:SI ?)?[1-9]\d{7}")
_POSTCODE = re.compile(r"(?:SI-)?[1-9]\d{3}(?: \S.*)?")

REGIONS = (
    "Pomurska", "Podravska", "Koroška", "Savinjska", "Zasavska", "Posavska", "Jugovzhodna Slovenija",
    "Osrednjeslovenska", "Gorenjska", "Primorsko-notranjska", "Goriška", "Obalno-kraška",
)
_REGIONS = frozenset(name.lower() for name in REGIONS) | frozenset((
    "osrednje slovenska", "osrednje-slovenska", "primorsko notranjska", "obalno kraška", "notranjsko-kraška",
    "spodnjeposavska",
))


def _text(value):
    if value is None or isinstance(value, bool):
        return ""
    text = " ".join(str(value).split())
    # Exports of Python bytes: b'46116'.
    if len(text) > 3 and text.startswith("b'") and text.endswith("'"):
        text = text[2:-1]
    return text


def validate_si_skd_code(value):
    """A code of the Slovenian classification of activities: I56.300, R93.190, 56.101 (not I56.30)."""
    return bool(_SKD.fullmatch(_text(value)))


def validate_si_proracunski_uporabnik(value):
    """A code of a Slovenian budget user: five digits, 12130, 00078."""
    return bool(_PU.fullmatch(_text(value)))


def validate_si_esd(value):
    """A record number of the Slovenian heritage register: one to five digits, 828."""
    return bool(_ESD.fullmatch(_text(value)))


def validate_si_ko_code(value):
    """A code of a Slovenian cadastral municipality: 1961, 2304, 1961 - Trzin (not a name alone)."""
    return bool(_KO.fullmatch(_text(value)))


def validate_si_parcel_number(value):
    """Slovenian parcel numbers: 637/4, 2455, *137/3, 632/4, 632/5, 1526/42, k.o. Sevnica."""
    text = _text(value)
    return "/" in text and bool(_PARCELS.fullmatch(text)) or bool(re.fullmatch(_PARCEL, text))


def validate_si_statistical_region(value):
    """A statistical region of Slovenia: Savinjska, OBALNO-KRAŠKA, Jugovzhodna Slovenija, Osrednje
    slovenska, Gorenjska regija (not Štajerska, not Vzhodna Slovenija)."""
    text = _text(value).lower()
    for suffix in (" statistična regija", " regija"):
        if text.endswith(suffix):
            text = text[: -len(suffix)]
    return text in _REGIONS


def validate_si_placna_podskupina(value):
    """A code of a salary subgroup of the Slovenian public sector: A01, C3, J03 (not L01)."""
    return bool(_SALARY_SUBGROUP.fullmatch(_text(value)))


def validate_si_maticna_stevilka(value):
    """A Slovenian registration number: seven digits, or ten with the unit number (5154715000)."""
    return bool(_MATICNA.fullmatch(_text(value)))


def validate_si_tax_number(value):
    """A Slovenian tax number: eight digits, 77003535, also SI77003535."""
    return bool(_TAX.fullmatch(_text(value)))


def validate_si_postcode(value):
    """A Slovenian postal code, with the post office that tables write after it: 1360, 8270 Krško."""
    return bool(_POSTCODE.fullmatch(_text(value)))
