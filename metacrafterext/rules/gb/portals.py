"""Validators for the United Kingdom files of metacrafter-testdata that come from 2024 snapshots of
UK open data portals (data.gov.uk, Cambridgeshire Insight, Calderdale Data Works, Open Leicester,
London Datastore, Open Data Glasgow and others).

Each function takes one value and returns True when it has the form of the code or name. Field-name
rules use them to check the values of a field; value rules use them after a pattern match.
"""
import re


def _text(value):
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return " ".join(str(value).split()) if value is not None else ""


# --- Statistical geography --------------------------------------------------------------------

# The name part of an LSOA or MSOA name is the name of a local authority district: words in
# Latin letters with apostrophes, commas, full stops and hyphens (Kingston upon Hull, City of;
# St. Helens; King's Lynn and West Norfolk; Rhondda Cynon Taf).
_AREA = r"[A-Z][A-Za-z'’.,-]*(?: [A-Za-z'’.,&-]+){0,6}"
_LSOA_NAME = re.compile(r"^" + _AREA + r" \d{3}[A-Z]$")
_MSOA_NAME = re.compile(r"^" + _AREA + r" \d{3}$")


def validate_gb_lsoa_name(value):
    """A name of a lower layer super output area of England and Wales: the name of the local
    authority district, the three digits of the middle layer area and a letter (Cambridge 001A,
    City of London 001C)."""
    return bool(_LSOA_NAME.match(_text(value)))


def validate_gb_msoa_name(value):
    """A name of a middle layer super output area of England and Wales: the name of the local
    authority district and three digits (Leicester 003, Barking and Dagenham 001)."""
    return bool(_MSOA_NAME.match(_text(value)))


_HAS_DIGIT = re.compile(r"\d")
_NAME_CHARS = re.compile(r"^[A-Za-zÀ-ÿŵŷŴŶ][A-Za-zÀ-ÿŵŷŴŶ '’.,&()/-]*$")
# Rows of totals and of other geographies that a column of local authorities also holds.
_NOT_AN_AREA = frozenset(
    "total totals all england wales scotland northern ireland great britain united kingdom uk "
    "england and wales n/a na none unknown other various".split()
) | {"england and wales", "great britain", "united kingdom", "northern ireland", "not known"}


def validate_gb_area_name(value):
    """A name of an area of the United Kingdom (a local authority, a constituency, a parish):
    words in letters, 3 to 60 characters, no digits (Calderdale, Barking and Dagenham, Hampshire
    County Council, Holborn and St Pancras). A code (E14000614, CMK, 37) is no name."""
    text = _text(value)
    if not 3 <= len(text) <= 60 or _HAS_DIGIT.search(text) or not _NAME_CHARS.match(text):
        return False
    if text.isupper() and len(text) <= 4:
        return False
    return text.lower() not in _NOT_AN_AREA


# A ward name of Glasgow has its number before it (10 Anderston/City/Yorkhill, 1 - Linn).
_WARD = re.compile(r"^(?:\d{1,2} ?-? ?)?[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ '’.,&()/-]*$")


def validate_gb_ward_name(value):
    """A ward name under a bare ward column: a name in letters, with the ward number of a
    Scottish council before it (Castle, Hayes & Coney Hall, 10 Anderston/City/Yorkhill). A ward
    number alone (3, 8) is no name."""
    text = _text(value)
    return 3 <= len(text) <= 60 and bool(_WARD.match(text)) and not (text.isupper() and len(text) <= 3)


_USRN = re.compile(r"^[1-9]\d{7}$")


def validate_gb_usrn(value):
    """A Unique Street Reference Number: eight digits (44100754, 20001350)."""
    return bool(_USRN.match(_text(value)))


# --- Schools ----------------------------------------------------------------------------------

def validate_school_name(value):
    """A name of a school: a text with a letter and no more than a few digits, at least four
    characters (Abbey Park Academy, St Malachy's Catholic Primary School). A number (5406), a
    code or a yes/no flag is no name."""
    text = _text(value)
    if not 4 <= len(text) <= 120:
        return False
    letters = sum(ch.isalpha() for ch in text)
    digits = sum(ch.isdigit() for ch in text)
    if letters < 4 or digits > letters // 3:
        return False
    return text.lower() not in {"true", "false", "school", "total", "none", "unknown"}


# --- Brownfield land registers ----------------------------------------------------------------

def _phrase(value):
    return _text(value).lower().rstrip(". ")


_PLANNING_STATUS = frozenset(["permissioned", "not permissioned", "pending decision"])
_OWNERSHIP_STATUS = frozenset([
    "owned by a public authority", "not owned by a public authority", "mixed ownership", "unknown ownership",
])
_PERMISSION_TYPE = frozenset([
    "full planning permission", "outline planning permission", "reserved matters approval",
    "permission in principle", "technical details consent", "planning permission granted under an order",
    "other",
])


def validate_gb_brownfield_planning_status(value):
    """A PlanningStatus of the brownfield land register standard: permissioned, not permissioned
    or pending decision, in any case."""
    return _phrase(value) in _PLANNING_STATUS


def validate_gb_brownfield_ownership_status(value):
    """An OwnershipStatus of the brownfield land register standard (owned by a public authority,
    not owned by a public authority, mixed ownership, unknown ownership), in any case."""
    return _phrase(value) in _OWNERSHIP_STATUS


def validate_gb_brownfield_permission_type(value):
    """A PermissionType of the brownfield land register standard (full planning permission,
    outline planning permission, reserved matters approval, permission in principle, technical
    details consent, planning permission granted under an order, other), in any case."""
    return _phrase(value) in _PERMISSION_TYPE


_CT_BAND = re.compile(r"^(?:band )?[A-I]$", re.I)


def validate_gb_council_tax_band(value):
    """A council tax band: a letter A to H, or I in Wales, also written Band D."""
    return bool(_CT_BAND.match(_text(value)))


# --- Procurement, companies, grants -----------------------------------------------------------

# A code with its label after it: 271501-Information Communication Technology, 321000  Social
# Community Care Supplies & Services, 62020 - Information technology consultancy activities.
_PROCLASS = re.compile(r"^[1-9]\d{5}(?:(?:\s*[-:–]\s*|\s+)[A-Za-z].*)?$", re.S)


def validate_gb_proclass_code(value):
    """A ProClass procurement classification code: six digits (271501, 321000), also with the
    label after it (271501-Information Communication Technology : Services)."""
    return bool(_PROCLASS.match(_text(value).replace("\xa0", " ").replace("ÿ", " ")))


_SIC_ONE = r"(?:\d{4,5}|\d{2}\.\d{1,2}(?:/\d)?)"
_SIC = re.compile(r"^" + _SIC_ONE + r"(?:\s*[,;]\s*" + _SIC_ONE + r")*(?:\s+-\s+\D.*)?$", re.S)


def validate_gb_sic_code(value):
    """A UK SIC 2007 code: the five digits of Companies House (62020), a class or subclass in the
    ONS notation (25.62, 74.90/9), four digits of a class or of the 2003 list (4525), several
    codes in one cell, or a code with its label (74990 - Non-trading company)."""
    return bool(_SIC.match(_text(value)))


_CRS = re.compile(r"^[A-Z]{3}$")


def validate_gb_crs_code(value):
    """A CRS code of a National Rail station: three capital letters (HFX, BHM)."""
    return bool(_CRS.match(_text(value)))


_ESD_SERVICE = re.compile(r"^https?://id\.esd\.org\.uk/service/\d{1,5}$")


def validate_gb_esd_service_uri(value):
    """A URI of a service of the Local Government Service List: http://id.esd.org.uk/service/646."""
    return bool(_ESD_SERVICE.match(_text(value)))


_360G = re.compile(r"^360G-[A-Za-z0-9][A-Za-z0-9_.:-]*$")


def validate_gb_360giving_id(value):
    """An identifier with a 360Giving publisher prefix: 360G-, the publisher's name and an
    identifier of its own (360G-indigotrust:IND296, 360G-BarnetCouncil-ORG:137)."""
    return bool(_360G.match(_text(value)))


_ORG_ID = re.compile(r"^(?:[A-Z]{2}-[A-Z0-9]{2,8}-[A-Za-z0-9_./-]+|360G-[A-Za-z0-9][A-Za-z0-9_.:-]*)$")


def validate_org_id_or_360g(value):
    """An organisation identifier of a 360Giving file: a list code of org-id.guide and the
    identifier in that list (GB-CHC-1131948, GB-LAE-BNE), or the publisher's own identifier
    (360G-indigotrust:org-32368)."""
    return bool(_ORG_ID.match(_text(value)))


# --- Spending and amounts ---------------------------------------------------------------------

_ORG_TEXT = re.compile(r"^[A-Za-z][A-Za-z0-9 '’.,&()/:-]*$")


def validate_gb_spend_body(value):
    """A department or body of a UK spend file (Department Family, Entity): a name or an acronym
    in letters (Department for Transport, DFID, MoJ HQ, HMRC). A site reference (T1, T10) is no
    body."""
    text = _text(value)
    if not 2 <= len(text) <= 100 or not _ORG_TEXT.match(text):
        return False
    return sum(ch.isalpha() for ch in text) >= 2 and not re.fullmatch(r"[A-Z]\d{1,3}", text)


_SYMBOL_AMOUNT = re.compile(
    r"^(?:-\s?)?\(?(?:-\s?)?[£€$]\s?(?:-\s?)?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d{1,2})?\)?(?:\s?[kmKM]|bn)?$"
)


def validate_symbol_amount(value):
    """An amount of money written with its currency sign before the digits: £37,350.00, -£1,917.95,
    £0, (£250.00), € 1,200, $15.5m. A bare number or a range (£145,000 - £149,999) is not one."""
    return bool(_SYMBOL_AMOUNT.match(_text(value)))
