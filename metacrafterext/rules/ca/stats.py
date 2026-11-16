"""Statistics Canada codes and other Canadian classifications found in a 2024 snapshot of Borealis, the
Canadian Dataverse Repository (borealisdata.ca, Dateno source cdi00000328): vectors of the data tables,
federal electoral districts, census metropolitan areas, census tracts, economic regions, province codes of
the SGC and province names, National Occupational Classification codes, terrestrial ecozones and the census
unit identifiers of the Canadian Historical GIS."""
import re

from metacrafterext.rules.ca.geo import PROVINCE_CODES


def _text(value):
    return " ".join(str(value).strip().split())


def _digits(value):
    """The text of a code a spreadsheet may have read as a number: 35076.0 is 35076."""
    text = _text(value)
    return text[:-2] if text.endswith(".0") else text


# ------------------------------------------------------------------ data tables
_VECTOR = re.compile(r"^[Vv]\d{1,10}$")
_VECTOR_LONG = re.compile(r"^[Vv]\d{6,10}$")


def validate_ca_statcan_vector(value):
    """A vector of a Statistics Canada data table: v65201210, V1212389364, v1 (not 65201210, v2.1 or
    v12345678901)."""
    return bool(_VECTOR.match(_text(value)))


def validate_ca_statcan_vector_long(value):
    """A vector of six to ten digits, which is read without the field name: v65201210, v1212389364
    (not v1, v2021 or version labels)."""
    return bool(_VECTOR_LONG.match(_text(value)))


# ------------------------------------------------------------------ census geography
def validate_ca_feduid(value):
    """A federal electoral district code, the province code and three digits: 35076, 59034, 10002,
    35076.0 (not 99001, 3507, 350760 or Orléans)."""
    text = _digits(value)
    return text.isdigit() and len(text) == 5 and text[:2] in PROVINCE_CODES


def validate_ca_cmauid(value):
    """A census metropolitan area or census agglomeration code of three digits: 535, 462, 825, 205,
    999, 535.0 (not 5, 35, 5350 or Toronto)."""
    text = _digits(value)
    return text.isdigit() and len(text) == 3


_CTUID = re.compile(r"^\d{7}\.\d{2}$")


def validate_ca_ctuid(value):
    """A census tract identifier, the code of the metropolitan area and the tract name: 5350001.00,
    0010003.01 (not 0001.00, 5350001 or 535000100)."""
    return bool(_CTUID.match(_text(value)))


def validate_ca_eruid(value):
    """An economic region code, the province code and two digits: 3530, 1210, 5930, 3530.0 (not 9930,
    353, 35300 or 1069)."""
    text = _digits(value)
    return text.isdigit() and len(text) == 4 and text[:2] in PROVINCE_CODES


def validate_ca_sgc_province_code(value):
    """The SGC code of a province or territory: 10, 24, 35, 59, 62, 35.0 (not 1, 6, 99 or ON)."""
    return _digits(value) in PROVINCE_CODES


# The provinces and territories by English and French name, and the earlier name of Newfoundland.
PROVINCE_NAMES = frozenset((
    "alberta", "british columbia", "manitoba", "new brunswick", "newfoundland and labrador", "newfoundland",
    "nova scotia", "northwest territories", "nunavut", "ontario", "prince edward island", "quebec", "québec",
    "saskatchewan", "yukon", "yukon territory", "colombie-britannique", "nouveau-brunswick",
    "terre-neuve-et-labrador", "terre-neuve", "nouvelle-écosse", "nouvelle-ecosse", "territoires du nord-ouest",
    "île-du-prince-édouard", "ile-du-prince-edouard"))


def validate_ca_province_name(value):
    """A province or territory of Canada by name: Alberta, Nova Scotia, Quebec, Québec, Colombie-Britannique
    (not ON, Canada, Toronto or Washington)."""
    return _text(value).lower() in PROVINCE_NAMES


# ------------------------------------------------------------------ classifications
def validate_ca_noc_code(value):
    """A unit group of the National Occupational Classification: four digits before NOC 2021 (3112,
    0111), five in NOC 2021 (21100, 00010), 3112.0 (not 311, 9999, 99999 or 211000)."""
    text = _digits(value)
    return text.isdigit() and len(text) in (4, 5) and set(text) != {"9"}


ECOZONES = frozenset((
    "arctic cordillera", "northern arctic", "southern arctic", "taiga plains", "taiga shield", "boreal shield",
    "atlantic maritime", "mixedwood plains", "boreal plains", "prairies", "taiga cordillera", "boreal cordillera",
    "pacific maritime", "montane cordillera", "hudson plains"))


def validate_ca_ecozone(value):
    """A terrestrial ecozone of Canada: Boreal Shield, Mixedwood Plains, atlantic maritime, Boreal Shield
    Ecozone (not Literature, shield, Great Lakes or Travaillant Upland HS)."""
    text = _text(value).lower()
    if text.endswith(" ecozone"):
        text = text[:-8]
    return text in ECOZONES


# ------------------------------------------------------------------ Canadian Historical GIS
_TCPUID = re.compile(r"^(?:AB|BC|MB|NB|NL|NF|NS|NT|NU|ON|PE|QC|SK|YT)\d{3}(?:\d{3})?$")


def validate_ca_tcp_uid(value):
    """A census division or subdivision of a historical census in the Canadian Historical GIS: ON001,
    BC004, PE001003, BC001004 (not ON0010, XX001, 3501005 or ON)."""
    return bool(_TCPUID.match(_text(value).upper()))
