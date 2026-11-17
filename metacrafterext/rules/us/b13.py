"""US codes found in 2024 snapshots of NYC Open Data (Dateno source cdi00001862) and Harvard Dataverse
(cdi00001690): school codes (DBN), boroughs, borough codes, community districts and parks property numbers
of New York City; congressional districts, Congress numbers and party identification of survey respondents.
"""
import re

from metacrafterext.rules.common.b13 import number, text

_DBN = re.compile(r"\d{2}[KMQRX]\d{3}")
BOROUGHS = ("Manhattan", "Bronx", "Brooklyn", "Queens", "Staten Island")
_BOROUGHS = frozenset(name.lower() for name in BOROUGHS) | frozenset(("the bronx", "m", "x", "k", "q", "r", "b", "mn", "bx", "bk", "qn", "si"))
_BOROUGH_CODE = re.compile(r"[1-5]")
_CD3 = re.compile(
    r"1(?:0[1-9]|1[0-2]|64)|2(?:0[1-9]|1[0-2]|2[6-8])|3(?:0[1-9]|1[0-8]|5[56])|4(?:0[1-9]|1[0-4]|8[0-4])|5(?:0[1-3]|95)"
)
_BOARD = re.compile(r"0?[1-9]|1[0-8]")
_PARKS = re.compile(r"[BMQRX][A-Z]?\d{2,3}[A-Z]{0,2}(?:\d{2})?(?:-(?:ZN)?\d{2,3}[A-Z]?)?")
_STATES = (
    "A[KLRSZ]|C[AOT]|D[CE]|FL|G[AU]|HI|I[ADLN]|K[SY]|LA|M[ADEINOPST]|N[CDEHJMVY]|O[HKR]|P[AR]|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY]"
)
_DISTRICT = re.compile(r"(?:" + _STATES + r")-?(?:0?\d|[1-4]\d|5[0-3]|AL)")
_CONGRESS = re.compile(r"(?:[1-9]\d?|1[0-2]\d)(?:st|nd|rd|th)?")
_PARTY_ID = frozenset((
    "democrat", "republican", "independent", "other", "not sure", "strong democrat", "not very strong democrat",
    "weak democrat", "lean democrat", "lean republican", "not very strong republican", "weak republican",
    "strong republican", "don't know", "skipped", "not asked",
))
_PARTY_CODE = re.compile(r"[1-9]")


def validate_us_nyc_dbn(value):
    """A school code of New York City: 01M015, 24Q600 (not 01A015)."""
    return bool(_DBN.fullmatch(text(value).upper()))


def validate_us_nyc_borough(value):
    """A borough of New York City or its abbreviation: Manhattan, BROOKLYN, Staten Island, M, X, K, Q, R."""
    return text(value).lower() in _BOROUGHS


def validate_us_nyc_borough_code(value):
    """A borough code of New York City: 1 to 5."""
    return bool(_BOROUGH_CODE.fullmatch(number(value)))


def validate_us_nyc_community_district(value):
    """A community district of New York City: 310, 101, 164, or the board number in the borough, 1 to 18."""
    candidate = number(value)
    return bool(_CD3.fullmatch(candidate) or _BOARD.fullmatch(candidate))


def validate_us_nyc_parks_property_id(value):
    """A property number of NYC Parks: B028, X010A, M042-ZN01 (not A028)."""
    return bool(_PARKS.fullmatch(text(value)))


def validate_us_congressional_district(value):
    """A congressional district: NY10, CA-12, WY-AL (not XX10, not NY99)."""
    return bool(_DISTRICT.fullmatch(text(value).upper()))


def validate_us_congress_number(value):
    """A number of a US Congress: 96, 111, 111.0, 117th (not 0, not a year)."""
    return bool(_CONGRESS.fullmatch(number(value)))


def validate_us_party_identification(value):
    """A party identification answer: codes 1 to 9 of pid3 and pid7, or Democrat, Strong Republican, Not sure."""
    candidate = number(value)
    return bool(_PARTY_CODE.fullmatch(candidate)) or candidate.lower() in _PARTY_ID
