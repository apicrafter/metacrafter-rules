"""Codes of European statistics and registers and small vocabularies found in the Cypriot files of
metacrafter-testdata (an April 2024 snapshot of the National Open Data Portal of Cyprus, data.gov.cy, Dateno
source cdi00000396): the age classes and the country and aggregate codes of Eurostat tables, codes of the
European List of Waste, EASA approval references, EU marketing authorisation numbers of medicines, IMO port
facility numbers, the technologies and bands of mobile base stations, routes of administration of medicines,
polling stations and ISO weeks written without the W.
"""
import re

_SPACE = re.compile(r"\s+")


def _text(value):
    if value is None or isinstance(value, bool):
        return ""
    return _SPACE.sub(" ", str(value).strip())


# ------------------------------------------------------------------ Eurostat
_AGE_CLASS = re.compile(r"^(?:TOTAL|UNK|Y_(?:LT|GE)\d{1,3}|Y\d{1,3}(?:-\d{1,3})?)$")
_AGE_CLASS_Y = re.compile(r"^Y(?:_(?:LT|GE))?\d")


def validate_eurostat_age_class(value):
    """A code of the Eurostat AGE code list: Y18-34, Y_LT14, Y_GE65, Y15, TOTAL, UNK (not 18-34, 41 or
    Total)."""
    return bool(_AGE_CLASS.match(_text(value)))


def validate_eurostat_age_class_y(value):
    """An age class written with the Y of the code list (Y18-34, Y_LT14): TOTAL and UNK alone do not tell an
    AGE column from the other dimensions of a Eurostat table."""
    text = _text(value)
    return bool(_AGE_CLASS.match(text) and _AGE_CLASS_Y.match(text))


_GEO_CODE = re.compile(r"^(?:[A-Z]{2}|E[UA]\d{2}(?:_\d{4})?|EXT_EU\d{2}(?:_\d{4})?|EFTA|UK_OCT|TOTAL|STLS|RNC|UNK)$")


def validate_eurostat_geo_code(value):
    """A country or aggregate code of the Eurostat GEO and CITIZEN code lists: CY, EL, UK, EU27_2020,
    EXT_EU27_2020, EFTA, STLS, RNC, TOTAL, UNK (not GRC, Cyprus or cy)."""
    return bool(_GEO_CODE.match(_text(value)))


# ------------------------------------------------------------------ European List of Waste
_EWC = re.compile(r"^(?:0?[1-9]|1\d|20) ?(?:0[1-9]|1[0-4]) ?(?:0[1-9]|[1-9]\d)\*?$")


def validate_eu_waste_code(value):
    """A code of the European List of Waste: 20 03 01, 200301, 15 01 10*, 170201, and 30105 where a sheet
    dropped the zero of chapter 03 (not 210101, 2003 or a year)."""
    text = _text(value)
    if text.endswith(".0"):
        text = text[:-2]
    return bool(_EWC.match(text))


# ------------------------------------------------------------------ registers
_EASA_APPROVAL = re.compile(r"^(?:[A-Z]{2}|EASA)\.(?:ATO|CCTO|FSTD|AeMC|145|147|21[GJ]|CAMO|CAO|MG|MF)\.\d{3,5}$")


def validate_easa_approval_number(value):
    """The reference of an EASA organisation approval: CY.ATO.002, CY.147.001, UK.145.01234, EASA.21J.031
    (not CY-ATO-002 or CY.WL.001V)."""
    return bool(_EASA_APPROVAL.match(_text(value)))


_EU_MA_NUMBER = re.compile(r"^EU/[12]/\d{2}/\d{3,4}/\d{3}(?:[-–]\d{3})?$")


def validate_eu_marketing_authorisation_number(value):
    """The number of a centrally authorised medicine in the Union Register: EU/2/10/118/011, EU/1/96/007/001
    (not EU/2/10/118 or CY.ML.0002V)."""
    return bool(_EU_MA_NUMBER.match(_text(value)))


_IMO_PORT_FACILITY = re.compile(r"^[A-Z]{2}[A-Z2-9]{3}-\d{4}$")


def validate_imo_port_facility_number(value):
    """A port facility number of the IMO GISIS maritime security module: CYLMS-0001, NLRTM-0352 (not CYLMS
    or CY-0001)."""
    return bool(_IMO_PORT_FACILITY.match(_text(value)))


# ------------------------------------------------------------------ mobile networks
_BAND = r"(?:GSM|DCS|UMTS|LTE|(?:5G-)?NR) ?-?\d{3,4}(?: DSS)?"
_MOBILE_BANDS = re.compile(rf"^{_BAND}(?:(?:, ?|-| ){_BAND})*$")


def validate_mobile_network_band(value):
    """The technologies and bands of a mobile base station: GSM900, LTE1800, GSM900, UMTS2100, LTE1800,
    GSM 900-UMTS 900-LTE 800, 5G-NR 700 (not 900 MHz, UHF-TV or GSM)."""
    return bool(_MOBILE_BANDS.match(_text(value)))


# ------------------------------------------------------------------ medicines
_ROUTES = frozenset((
    "oral", "parenteral", "topical", "ocular", "ophthalmic", "rectal", "vaginal", "nasal", "inhalation",
    "transdermal", "intravenous", "intramuscular", "subcutaneous", "sublingual", "buccal", "cutaneous",
    "intradermal", "intrathecal", "intramammary", "intrauterine", "intravitreal", "intravesical", "otic",
    "auricular", "dental", "epidural", "oromucosal", "intraarticular", "intra-articular", "intraperitoneal",
    "in ovo", "spot-on", "pour-on", "in-feed", "in drinking water", "deep im",
    "po", "or", "iv", "im", "sc", "id", "sl", "pr", "pv", "top", "inh", "eu", "imam",
))
_ROUTE_SPLIT = re.compile(r"\s*(?:,|;|/|\n| and | or |&)\s*")
_ROUTE_WORDS = re.compile(r"\s+(?:use|route|administration)$")


def validate_medication_route(value):
    """A route of administration of a medicine or several of them: Oral, Parenteral, Topical, Intravenous use,
    IM, SC, IM / IV, DEEP IM (not Tablet, 5 mg or National)."""
    text = str(value).strip().lower() if value is not None and not isinstance(value, bool) else ""
    parts = [_ROUTE_WORDS.sub("", _SPACE.sub(" ", p)) for p in _ROUTE_SPLIT.split(text) if p.strip()]
    return 1 <= len(parts) <= 5 and all(p in _ROUTES for p in parts)


_SUBSTANCE = re.compile(r"^[^\W\d_][\w .,'’()/+&%:;\n-]{2,200}$")


def validate_active_substance(value):
    """The active substance of a medicine as a register names it: RABEPRAZOLE, Montelukast sodium, Coagulation
    factor VIII, TOLTRAZURIL 50 MG/ML, Imidacloprid and Moxidectin on two lines (not a number, N/A or a
    code)."""
    text = str(value).strip() if value is not None and not isinstance(value, bool) else ""
    return bool(_SUBSTANCE.match(text)) and sum(ch.isalpha() for ch in text) >= max(4, len(text) // 2)


# ------------------------------------------------------------------ elections
_STATION = re.compile(r"^[^\W_][\w .,'’\"()/&-]{3,120}$")


def validate_polling_station(value):
    """The name of a polling station, most often the building that hosts it: Γ ΔΗΜ. ΣΧΟΛΕΙΟ ΚΑΙΜΑΚΛΙΟΥ, ΔΗΜΟΤΙΚΟ
    ΣΧΟΛΕΙΟ ΑΓΙΟΥ ΑΝΔΡΕΟΥ, St Mary's Church Hall (not ΚΕΝΤΡΟ Α, 157 or a code)."""
    text = _text(value)
    letters = sum(ch.isalpha() for ch in text)
    return bool(_STATION.match(text)) and letters >= 8 and letters >= len(text) * 0.6 and " " in text


# ------------------------------------------------------------------ weeks
_ISO_WEEK = re.compile(r"^(?:19|20)\d{2} ?- ?W?(?:0?[1-9]|[1-4]\d|5[0-3])$")


def validate_iso_week_loose(value):
    """A year and an ISO week as epidemiological tables write them: 2021-W32, 2021-1, 2020-53, 2022 - 16 (not
    2021-54, 2021 or 01/2020)."""
    return bool(_ISO_WEEK.match(_text(value)))


# ------------------------------------------------------------------ air quality
_AIR_POLLUTANT = re.compile(r"^(?:PM(?:10|2[.,]?5|1)|NO[2Xx]?|SO2|O3|CO|C6H6|NH3|BaP|Pb|As|Cd|Ni|Hg)$")


def validate_air_pollutant(value):
    """The notation of an air pollutant of air quality reporting: PM10, PM2.5, NO, NO2, NOX, SO2, O3, CO, C6H6
    (not Nitrogen Dioxide, a station code or a number)."""
    return bool(_AIR_POLLUTANT.match(_text(value)))


# Countries with NUTS regions or statistical regions coded the same way: the EU, EFTA, the United Kingdom
# and the candidate countries. Greece is EL in NUTS.
_NUTS_COUNTRIES = frozenset(
    "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK "
    "CH IS LI NO UK AL ME MK RS TR BA XK MD UA GE".split()
)
_NUTS_CODE = re.compile(r"([A-Z]{2})[0-9A-Z]{0,3}")


def validate_nuts_code(value):
    """A NUTS code: a country (IT, EL) and up to three more characters for the levels 1 to 3 (ITC, ITC1,
    ITC11, DE21H), not a name or the code of a country outside the classification."""
    text = str(value).strip().upper()
    match = _NUTS_CODE.fullmatch(text)
    if not match or match.group(1) not in _NUTS_COUNTRIES:
        return False
    # ITC and UKI are level 1; a longer code has a digit (ITC11, DE21H), a word has none (ROMA, ESTE).
    return len(text) <= 3 or any(ch.isdigit() for ch in text)
