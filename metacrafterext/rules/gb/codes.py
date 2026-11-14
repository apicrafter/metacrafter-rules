"""Validators of United Kingdom codes found in the data.gov.uk files of metacrafter-testdata.

Each function takes one value and returns True when it has the form of the code. Field-name
rules use them to check the values of a field; value rules use them after a pattern match.
"""
import re

# 100 km squares of the Ordnance Survey National Grid that cover land of Great Britain. The
# grid letters A-Z without I name 25 squares in each 500 km square (H, N, O, S, T); only these
# hold land, so a reference in another square (OC, TI) is no grid reference.
_OS_SQUARES = frozenset("""
HL HM HN HO HP HQ HR HS HT HU HV HW HX HY HZ
NA NB NC ND NE NF NG NH NJ NK NL NM NN NO NP NQ NR NS NT NU NV NW NX NY NZ
OA OB OF OG OL OM OQ OR OV OW
SA SB SC SD SE SF SG SH SJ SK SL SM SN SO SP SQ SR SS ST SU SV SW SX SY SZ
TA TB TF TG TL TM TQ TR TV TW
""".split())
_OS_GRID = re.compile(r"^([A-Z]{2}) ?(\d+)(?: (\d+))?$")


def validate_os_grid_reference(value):
    """An Ordnance Survey National Grid reference: a 100 km square of Great Britain and an
    even number of digits, 2 to 10, half eastings and half northings (SD 97624 17311,
    TQ 873 846, TL97441340). With a space between the halves both must be equally long."""
    m = _OS_GRID.match(str(value).strip().upper())
    if not m or m.group(1) not in _OS_SQUARES:
        return False
    if m.group(3) is not None:
        return 1 <= len(m.group(2)) <= 5 and len(m.group(2)) == len(m.group(3))
    return len(m.group(2)) in (2, 4, 6, 8, 10)


def validate_os_grid_reference_spaced(value):
    """A grid reference written with spaces (SD 97624 17311, TQ 873 846): the form that is not
    mistaken for a Scottish company number (SC086146) or an Ofsted URN (SC068179)."""
    text = str(value).strip()
    return " " in text and validate_os_grid_reference(text)


_OUTWARD = re.compile(r"^[A-Z]{1,2}\d[A-Z\d]?$")
_SECTOR = re.compile(r"^[A-Z]{1,2}\d[A-Z\d]? \d$")


def validate_gb_postcode_district(value):
    """The outward code of a UK postcode: LS13, NW1, WC1H, N6. A trailing space is allowed."""
    return bool(_OUTWARD.match(str(value).strip().upper()))


def validate_gb_postcode_sector(value):
    """A UK postcode sector: the outward code, a space and one digit (LS27 9, WF3 1)."""
    return bool(_SECTOR.match(" ".join(str(value).split()).upper()))


_CCG_ODS = re.compile(r"^\d{2}[A-Z]$")
_ODS = re.compile(r"^(?=.*\d)[A-Z0-9]{3,6}$|^[A-Z]{3}$")


def validate_ccg_ods_code(value):
    """The ODS code of a clinical commissioning group: two digits and a letter (02T, 99A)."""
    return bool(_CCG_ODS.match(str(value).strip()))


def validate_nhs_ods_code(value):
    """An NHS Organisation Data Service code: three to six capital letters and digits with a
    digit (RXF, 02T, QF7, Y55, A81001) or three letters (QWO, QHM)."""
    return bool(_ODS.match(str(value).strip()))


_NPTG = re.compile(r"^[EN][0S]\d{6}$")
_NAPTAN_CODE = re.compile(r"^(?=.*[A-Za-z])[A-Za-z0-9]{7,8}$")


def validate_nptg_locality_code(value):
    """An NPTG locality code: E or N, 0 or S, six digits (E0029368, N0075002)."""
    return bool(_NPTG.match(str(value).strip()))


def validate_naptan_code(value):
    """A NaPTAN SMS code of a stop: seven or eight letters and digits with a letter (MANJMGMW)."""
    return bool(_NAPTAN_CODE.match(str(value).strip()))


_EPC_RATING = re.compile(r"^(?:A\+?|[B-G])$")


def validate_epc_rating(value):
    """An energy performance certificate band: A (A+ on a DEC) to G."""
    return bool(_EPC_RATING.match(str(value).strip().upper()))


_GRADE = re.compile(r"^(?:AA|AO|EO|HEO|SEO|G[67]|UG[67]|GRADE [67]|SCS ?[1-4]A?|SCS PAY BAND [1-4]|PB[1-4]|AA/AO|PS)(?:\b.*)?$")


def validate_civil_service_grade(value):
    """A UK civil service grade as organograms give it: AA, AO, EO, HEO, SEO, G7, G6, SCS1 to
    SCS4 (SCS1A), Grade 7, SCS Pay Band 2; a department suffix may follow (G7 National,
    HEO (UKHO B2))."""
    return bool(_GRADE.match(" ".join(str(value).split()).upper()))


_BREED = re.compile(r"^[A-Z]{2,4}(?: ?X)?$")


def validate_cattle_breed_code(value):
    """A BCMS cattle breed code: two to four letters, an X for a cross (AA, AAX, BAZ X)."""
    return bool(_BREED.match(str(value).strip()))


_VOA = re.compile(r"^[A-Z]{2}\d{0,2}$")


def validate_voa_description_code(value):
    """A VOA primary description code: two letters and up to two digits (CO, CS, CP1, CS10)."""
    return bool(_VOA.match(str(value).strip()))


_PLANNING = re.compile(r"^(?:\d{2}|\d{4})/\d{3,6}/[A-Z]{1,8}$")


def validate_planning_application_ref(value):
    """A planning application reference of the YY/NNNNN/TYPE form (14/01103/FUL, 2019/1602/P)."""
    return bool(_PLANNING.match(str(value).strip()))


_GB_VAT = re.compile(r"^(?:(?:GB|XI) ?)?(?:\d{3} ?\d{4} ?\d{2}(?: ?\d{3})?|GD\d{3}|HA\d{3})$")


def validate_gb_vat(value):
    """A UK VAT registration number: nine digits (or twelve for a branch), spaces allowed, an
    optional GB or XI prefix (673598875, GB 446 0099 53, 744 3643 29)."""
    return bool(_GB_VAT.match(" ".join(str(value).split()).upper()))


_CH_NUMBER = re.compile(r"^(?:(?:AC|FC|GE|GN|GS|IC|IP|LP|NA|NF|NI|NL|NO|NP|NR|NZ|OC|RC|SA|SC|SF|SI|SL|SO|SP|SR|SZ|ZC)\d{6}|R\d{7}|\d{7,8})$")


def validate_companies_house_number(value):
    """A Companies House company number: eight digits or two letters and six digits (OC387148,
    SC086146); spreadsheets drop the leading zero of a numeric one (4832101 for 04832101).
    Six digits and fewer are other registers (Irish CRO numbers 123456)."""
    return bool(_CH_NUMBER.match(str(value).strip().upper()))
