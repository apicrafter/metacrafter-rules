"""Codes of Australian councils, land titles and planning found in the Opendatasoft portals of the City
of Melbourne, the City of Greater Geelong, Liverpool City Council and Peclet (metacrafter-testdata, 2024
snapshots, Dateno sources cdi00000100, cdi00000102, cdi00000104 and cdi00000117): CLUE small areas of the
City of Melbourne, NSW lot identifiers and survey plan numbers, NSW and Victorian planning zones, planning
and building application numbers, parking restrictions, Geoscape persistent identifiers, ANZSIC division
titles, Victorian Biodiversity Atlas taxon ids, DCA road crash codes and Australian state names."""
import re


def _text(value):
    return " ".join(str(value).strip().split())


# ------------------------------------------------------------------ CLUE small areas (City of Melbourne)
# The 13 small areas of the Census of Land Use and Employment and the total of the municipality.
CLUE_SMALL_AREAS = frozenset(
    a.lower()
    for a in (
        "Carlton", "Docklands", "East Melbourne", "Kensington", "Melbourne (CBD)", "Melbourne (Remainder)",
        "North Melbourne", "Parkville", "Port Melbourne", "South Yarra", "Southbank",
        "West Melbourne (Industrial)", "West Melbourne (Residential)", "City of Melbourne",
        "City of Melbourne (total)", "City of Melbourne (Total)",
    )
)


def validate_au_clue_small_area(value):
    """A CLUE small area of the City of Melbourne: Melbourne (CBD), West Melbourne (Residential),
    Docklands, City of Melbourne (total) (not Fitzroy, Richmond or Melbourne CBD)."""
    return _text(value).lower() in CLUE_SMALL_AREAS


# ------------------------------------------------------------------ land titles
_NSW_LOT_ID = re.compile(r"^[A-Z0-9]{0,6}/[A-Z0-9]{0,4}/(?:DP|SP|CP|PP)\d{1,7}$")
_SURVEY_PLAN = re.compile(r"^(?:DP|SP|CP|PP|LP|PS|TP|PC|RP|FP|CS|AP|BUP|GTP|SSP) ?\d{1,7}[A-Z]?$")


def validate_au_nsw_lot_id(value):
    """An NSW lot identifier of the Spatial Services cadastre, lot/section/plan: 23/O/DP1417,
    1//DP225807, //SP37549 (not DP1417, 1/2/3 or 23/O/1417)."""
    text = _text(value).upper()
    return bool(_NSW_LOT_ID.match(text)) and text != "//"


def validate_au_survey_plan_number(value):
    """An Australian survey plan number with the plan type: DP1417, SP37549, PS612345R, RP123456,
    LP 1234 (not 1417, DP, ABC1234 or DP12345678)."""
    return bool(_SURVEY_PLAN.match(_text(value).upper()))


# ------------------------------------------------------------------ planning zones
_NSW_ZONE = re.compile(r"^(?:RU[1-6]|R[1-5]|B[1-8]|E[1-5]|MU1|IN[1-4]|SP[1-5]|RE[12]|C[1-4]|W[1-4]|UL|DM)$")
_VIC_ZONE = re.compile(
    r"^(?:GRZ|NRZ|RGZ|LDRZ|MUZ|TZ|RLZ|RAZ|RCZ|GWZ|GWAZ|FZ|PPRZ|PCRZ|PUZ|SUZ|CDZ|UGZ|UFZ|PDZ|DZ|ACZ|CCZ"
    r"|C1Z|C2Z|C3Z|IN1Z|IN2Z|IN3Z|RDZ|PZ|CA|R1Z|R2Z|R3Z|B1Z|B2Z|B3Z|B4Z|B5Z|ERZ|MAZ)\d{0,2}$")


def validate_au_nsw_land_zone(value):
    """A zone code of an NSW Standard Instrument LEP: R2, RU1, SP2, B4, E1, MU1, C3, W1, UL (not R6,
    GRZ1 or B9)."""
    return bool(_NSW_ZONE.match(_text(value).upper()))


def validate_au_vic_planning_zone(value):
    """A Victorian planning scheme zone, with the number of its schedule: GRZ1, UGZ3, IN1Z, C1Z, FZ,
    PCRZ, RCZ13 (not R2, GRZ123 or ZONE1)."""
    return bool(_VIC_ZONE.match(_text(value).upper()))


# ------------------------------------------------------------------ applications to councils
_PLANNING_APPLICATION = re.compile(
    r"^(?:\d{4}_)?(?:DA|D|TP|TPM|BP|CDC|PA|PP|MOD|DEV|SUB|PLN|PLP|CC|OC)[-/ ]?"
    r"(?:\d{1,6}[-/]\d{2,4}|\d{4}[-/]\d{1,6})(?:[-/][A-Z0-9]{1,3})?$")


def validate_au_planning_application_number(value):
    """A council planning or building application number: DA-404/2015, D/2008/940, 2015_D/2008/940/C,
    TP-2014-43/A, TPM-2010-31, BP-2014-1813/1 (not 1501/2014/005613/2, DA or 2015)."""
    return bool(_PLANNING_APPLICATION.match(_text(value).upper()))


# ------------------------------------------------------------------ parking restrictions
_PARKING_TIME = r"(?:\d{1,2}(?:/\d)?P|[MFD]P\d{1,2}P?|[HQ]P|P ?/? ?\d{1,2} ?MINS?|P ?\d{1,2}|P|\d{1,2} ?MIN(?:UTES?|S)?)"
_PARKING_KIND = (r"(?:METER|MTR|TICKET|TKT(?: A)?|TICKET A|DISABLED(?: ONLY)?|DIS|AREA|RPA(?: \w+)?|FREE|PERMIT"
                 r"|M-\w+|SAT-SUN|SUN|SAT|MON-\w+|M-F)")
_PARKING_SIGN = re.compile(
    rf"^(?:{_PARKING_TIME}(?: ?{_PARKING_KIND})*(?: [-0-9.:APM ]+)?(?: .*)?"
    r"|(?:LOADING ZONE|LZ) ?\d{0,3} ?(?:M|MIN|MINS|HR)?(?: .*)?|CLEARWAY.*|CW TOW.*|S/ ?\(?NO STOPPING\)?.*"
    r"|NO (?:STOPPING|STANDING|PARKING).*|P/ ?\(NO PARKING\).*|DISABLED(?: ONLY)?|PP|SP|LZ\d{1,3}"
    r"|(?:BUS|TAXI|PERMIT|MAIL|POLICE) ZONE.*)$")


def validate_au_parking_restriction(value):
    """An Australian parking restriction: 2P, 1/2P Meter, 2P MTR M-SAT 7:30-18:30, P 10 Mins, QP, MP2P,
    Loading Zone 15M, LZ30, 3P Ticket, Clearway (Tow away), 1p (not 2 Hours, Parking, Free or 15)."""
    text = _text(value).upper()
    if not text or text.isdigit():
        return False
    return bool(_PARKING_SIGN.match(text))


# ------------------------------------------------------------------ Geoscape persistent identifiers
_GNAF_PID = re.compile(r"^GA(?:NSW|VIC|QLD|SA|WA|TAS|NT|ACT|OT)\d{9,10}$")
# Administrative Boundaries: a lower case prefix of the theme and twelve characters, hexadecimal in the
# older releases (lga94484cf6e0e2), URL-safe base64 in the newer ones (lgp9wJk6uBtcEPS).
_GEOSCAPE_PID = re.compile(r"^(?:lga|lgp|loc|lcp|sal|ssc|sa[1-4]|mb[0-9a-z]|ste|stp|wad|wdp|wrd|sed|sep|ced|cep"
                           r"|gcc|poa|ucl|sos|tr[0-9a-z]|ra[0-9a-z]|tgn|ast)[0-9A-Za-z_-]{12}$")


def validate_au_geoscape_pid(value):
    """A Geoscape (PSMA) persistent identifier: lga94484cf6e0e2, lgpa9f1f9d86a5e, lgp9wJk6uBtcEPS,
    GANSW704411427 (not lga94484cf6, 94484cf6e0e2, GANSW12)."""
    text = _text(value)
    return bool(_GNAF_PID.match(text) or _GEOSCAPE_PID.match(text))


# ------------------------------------------------------------------ ANZSIC division titles
ANZSIC_DIVISIONS = (
    "Agriculture, Forestry and Fishing", "Mining", "Manufacturing", "Electricity, Gas, Water and Waste Services",
    "Construction", "Wholesale Trade", "Retail Trade", "Accommodation and Food Services",
    "Transport, Postal and Warehousing", "Information Media and Telecommunications",
    "Financial and Insurance Services", "Rental, Hiring and Real Estate Services",
    "Professional, Scientific and Technical Services", "Administrative and Support Services",
    "Public Administration and Safety", "Education and Training", "Health Care and Social Assistance",
    "Arts and Recreation Services", "Other Services",
)


def _division_key(text):
    text = re.sub(r"\s*&\s*", " and ", text.lower())
    text = re.sub(r"\s*\(no\.\)$", "", text)
    return re.sub(r"[^a-z]+", " ", text).strip()


_ANZSIC_DIVISION_KEYS = frozenset(_division_key(d) for d in ANZSIC_DIVISIONS)


def validate_au_anzsic_division_name(value):
    """An ANZSIC 2006 division title in any case, with & for and: Agriculture, Forestry and Fishing,
    ELECTRICITY, GAS, WATER AND WASTE SERVICES, Transport, Postal & Warehousing (not A, Agriculture,
    Business Services or Admin and Support Services)."""
    return _division_key(_text(value)) in _ANZSIC_DIVISION_KEYS


# ------------------------------------------------------------------ Victorian Biodiversity Atlas
def validate_au_vba_taxon_id(value):
    """A Victorian Biodiversity Atlas taxon id: 10705, 501234, 10705.0 (not 0, A10705 or 1234567)."""
    text = _text(value)
    if text.endswith(".0"):
        text = text[:-2]
    return text.isdigit() and 1 <= len(text) <= 6 and int(text) > 0


# ------------------------------------------------------------------ road crashes
_DCA = re.compile(r"^1\d{2}(?:\s+[A-Za-z].*)?$")


def validate_au_dca_code(value):
    """A DCA code of a road crash, alone or with its description: 132 Vehicles in same lane/ right rear,
    110, 171 Left off carriageway into object (not 250, 13 or Cross traffic)."""
    return bool(_DCA.match(_text(value)))


# ------------------------------------------------------------------ state names
AU_STATE_NAMES = frozenset(
    s.lower()
    for s in (
        "New South Wales", "Victoria", "Queensland", "South Australia", "Western Australia", "Tasmania",
        "Northern Territory", "Australian Capital Territory", "Other Territories", "Other Territory",
    )
)


def validate_au_state_name(value):
    """The name of an Australian state or territory: New South Wales, Victoria, Other Territories,
    TASMANIA (not NSW, Australia or Sydney)."""
    return _text(value).lower() in AU_STATE_NAMES
