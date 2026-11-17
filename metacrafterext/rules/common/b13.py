"""Helpers and validators of country-neutral codes found in 2024 snapshots of 43 data catalogues (Dateno
sources cdi00001606 to cdi00004515; Harvard Dataverse, the ASARECA data hub, HealthData.gov): Gleditsch-Ward
country codes, Correlates of War abbreviations, Polity scores, FAOSTAT codes and epidemiological weeks.

Each function takes one value and returns True when it has the form of the code.
"""
import re

_FLOAT_TAIL = re.compile(r"\.0+$")
_GW = re.compile(r"[1-9]\d{0,2}")
_COW_ABB = re.compile(r"[A-Z]{3}")
_POLITY = re.compile(r"-?(?:10|\d)|-66|-77|-88")
_FAO_AREA = re.compile(r"[1-9]\d{0,3}")
_FAO_ITEM = re.compile(r"[1-9]\d{0,4}")
_FAO_ELEMENT = re.compile(r"[1-9]\d{2,4}")
_WEEK = re.compile(r"0?[1-9]|[1-4]\d|5[0-3]")


def text(value):
    """The value as a string with single spaces; empty for None and booleans."""
    if value is None or isinstance(value, bool):
        return ""
    return " ".join(str(value).split())


def number(value):
    """The value as a string, with the .0 that a float column adds removed: 111.0 is 111."""
    return _FLOAT_TAIL.sub("", text(value))


def fold(value):
    """Lower case without accents, punctuation and spaces: Béjaïa and BEJAIA are bejaia."""
    import unicodedata

    decomposed = unicodedata.normalize("NFKD", text(value).lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in decomposed if not unicodedata.combining(c)))


def validate_gw_country_code(value):
    """A Gleditsch-Ward country number: 2, 200, 710, 540.0 (not 0, not USA)."""
    return bool(_GW.fullmatch(number(value)))


def validate_cow_country_abbreviation(value):
    """A Correlates of War country abbreviation: USA, UKG, GMY (not US, not usa)."""
    return bool(_COW_ABB.fullmatch(text(value)))


def validate_polity_score(value):
    """A Polity score: -10 to 10, or -66, -77, -88; 10.0 of a float column (not 11, not 0.5)."""
    return bool(_POLITY.fullmatch(number(value)))


def validate_faostat_area_code(value):
    """A FAOSTAT area code: 114, 231, 5000."""
    return bool(_FAO_AREA.fullmatch(number(value)))


def validate_faostat_item_code(value):
    """A FAOSTAT item code: 15, 56, 3010."""
    return bool(_FAO_ITEM.fullmatch(number(value)))


def validate_faostat_element_code(value):
    """A FAOSTAT element code: 5510, 5312, 551."""
    return bool(_FAO_ELEMENT.fullmatch(number(value)))


def validate_epi_week(value):
    """An epidemiological (MMWR) week: 1 to 53, 01 (not 0, not 54)."""
    return bool(_WEEK.fullmatch(number(value)))
