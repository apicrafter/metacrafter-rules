"""Canadian geographic and hydrometric codes found in the 2024 snapshots of the Canadian Watershed
Information Network (canwinmap.ad.umanitoba.ca, Dateno source cdi00000267) and of the open data portals of
the City of Calgary (data.calgary.ca, cdi00000286) and the City of Edmonton (data.edmonton.ca, cdi00000289):
Water Survey of Canada station numbers and drainage area codes, DGUIDs and SGC codes of Statistics Canada,
Dominion Land Survey land descriptions and postal codes."""
import re


def _text(value):
    return " ".join(str(value).strip().split())


# ------------------------------------------------------------------ Water Survey of Canada
# 05BH004: major drainage area (01 to 11), sub-drainage and sub-sub-drainage letters, station.
_WSC_STATION = re.compile(r"^(?:0[1-9]|1[01])[A-Z]{2}\d{3}$")
_WSC_AREA = re.compile(r"^(?:0?[1-9]|1[01])(?:[A-Z]{1,2})?$")


def validate_ca_wsc_station_number(value):
    """A hydrometric station number of the Water Survey of Canada: 05BH004, 08MF005, 05LJ021 (not
    12AB001, 5BH004, MB05LDS002 or 05BH04)."""
    return bool(_WSC_STATION.match(_text(value).upper()))


def validate_ca_wsc_drainage_area_code(value):
    """A drainage area code of the Water Survey of Canada: a major drainage area (05, 5, 10), a
    sub-drainage area (05L) or a sub-sub-drainage area (05LJ) (not 12, 501, 05L1 or Nelson River)."""
    return bool(_WSC_AREA.match(_text(value).upper()))


# ------------------------------------------------------------------ Statistics Canada
# The SGC codes of the provinces and territories: 10 Newfoundland and Labrador to 62 Nunavut.
PROVINCE_CODES = frozenset(("10", "11", "12", "13", "24", "35", "46", "47", "48", "59", "60", "61", "62"))
# Vintage, type (A administrative, S statistical), schema and the id of the area in that geography.
_DGUID = re.compile(r"^(?:19|20)\d{2}[AS]\d{4}[0-9A-Z.]{1,12}$")
_FLOAT_ZERO = re.compile(r"^(\d+)\.0$")


def validate_ca_dguid(value):
    """A Dissemination Geography Unique Identifier of Statistics Canada: 2021A000011124 (Canada),
    2021A000248 (Alberta), 2021S051248112107 (a dissemination area), 2021A0011T3A (a forward sortation
    area) (not 4811, 2021X000248 or 2021A0002)."""
    return bool(_DGUID.match(_text(value).upper()))


def validate_ca_sgc_code(value):
    """A Standard Geographical Classification code: a province or territory (48, 59), a census division
    (4806) or a census subdivision (4806016), which begin with the code of the province (not 73, 99,
    480 or 9906016)."""
    text = _text(value)
    m = _FLOAT_ZERO.match(text)
    if m:
        text = m.group(1)
    return text.isdigit() and len(text) in (2, 4, 7) and text[:2] in PROVINCE_CODES


# ------------------------------------------------------------------ Dominion Land Survey
# NE-20-52-25-W4, SE28 21 30 W1: quarter, section (1 to 36), township, range, meridian.
_DLS = re.compile(
    r"^(?:(NE|NW|SE|SW)[ -]?)?(0?[1-9]|[12]\d|3[0-6])[ -](0?[1-9]|[1-9]\d|1[0-2]\d)[ -](0?[1-9]|[1-3]\d)"
    r"[ -]?([WE])[ -]?([1-7])$")


def validate_ca_dls_land_description(value):
    """A legal land description of the Dominion Land Survey: NE-20-52-25-W4, SE28 21 30 W1,
    SE03 37 12 W2, 20-52-25-W4 (not NE-40-52-25-W4, 20-52-25, SE28 or Plan 6042KS Blk 2 Lot 5)."""
    return bool(_DLS.match(_text(value).upper()))


# ------------------------------------------------------------------ postal codes
_CA_POSTCODE = re.compile(r"^[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ -]?\d[ABCEGHJ-NPRSTV-Z]\d$")


def validate_ca_postcode(value):
    """A Canadian postal code, with or without the space: T2G 2M2, T5H1E8, t6a3j6, K1A 0B1 (not T5H,
    D1A 1A1, T2G 2M or SW1A 1AA)."""
    return bool(_CA_POSTCODE.match(_text(value).upper()))
