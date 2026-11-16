"""Attributes of protected areas, species assessments and cyclone tracks found in 2024 snapshots of the
environment data portals of the Pacific (SPREP, Dateno sources cdi00001247 to cdi00001264) and of the New
Zealand open data portal (cdi00001241): the governance, ownership, designation, no-take and verification
fields of the World Database on Protected Areas, the population trend of the IUCN Red List, the basin and
nature columns of IBTrACS and c-squares codes.
"""
import re


def _text(value):
    if value is None or isinstance(value, bool):
        return ""
    return " ".join(str(value).split())


_WDPA_GOVERNANCE = frozenset((
    "federal or national ministry or agency", "sub-national ministry or agency", "government-delegated management",
    "transboundary governance", "collaborative governance", "joint governance", "individual landowners",
    "non-profit organisations", "non-profit organizations", "for-profit organisations", "for-profit organizations",
    "indigenous peoples", "local communities", "not reported",
))
_WDPA_OWNERSHIP = frozenset((
    "state", "communal", "individual landowners", "for-profit organisations", "for-profit organizations",
    "non-profit organisations", "non-profit organizations", "joint ownership", "multiple ownership", "contested",
    "not reported",
))
_WDPA_DESIGNATION = frozenset(("national", "regional", "international", "not applicable"))
_WDPA_NO_TAKE = frozenset(("all", "part", "none", "not reported", "not applicable"))
_WDPA_VERIFICATION = frozenset(("state verified", "expert verified", "not reported"))
_POPULATION_TREND = frozenset(("increasing", "decreasing", "stable", "unknown"))
_IBTRACS_BASIN = frozenset(("NA", "EP", "WP", "NI", "SI", "SP", "SA", "MM"))
_IBTRACS_NATURE = frozenset(("DS", "TS", "ET", "SS", "NR", "MX"))
_CSQUARES = re.compile(r"[1357][0-8](?:0\d|1[0-7])(?::[1-4]\d{2})*(?::[1-4])?")


def validate_wdpa_governance_type(value):
    """A governance type of the WDPA (GOV_TYPE): Federal or national ministry or agency, Indigenous
    peoples, Collaborative governance, Not Reported."""
    return _text(value).lower() in _WDPA_GOVERNANCE


def validate_wdpa_ownership_type(value):
    """An ownership type of the WDPA (OWN_TYPE): State, Communal, Joint ownership, Not Reported."""
    return _text(value).lower() in _WDPA_OWNERSHIP


def validate_wdpa_designation_type(value):
    """A designation type of the WDPA (DESIG_TYPE): National, Regional, International, Not Applicable."""
    return _text(value).lower() in _WDPA_DESIGNATION


def validate_wdpa_no_take(value):
    """A no-take status of the WDPA (NO_TAKE): All, Part, None, Not Reported, Not Applicable."""
    return _text(value).lower() in _WDPA_NO_TAKE


def validate_wdpa_verification(value):
    """A verification status of the WDPA (VERIF): State Verified, Expert Verified, Not Reported."""
    return _text(value).lower() in _WDPA_VERIFICATION


def validate_iucn_population_trend(value):
    """A population trend of a Red List assessment: Increasing, Decreasing, Stable, Unknown."""
    return _text(value).lower() in _POPULATION_TREND


def validate_ibtracs_basin(value):
    """A basin code of IBTrACS: NA, EP, WP, NI, SI, SP, SA (MM for a missing one)."""
    return _text(value) in _IBTRACS_BASIN


def validate_ibtracs_nature(value):
    """A storm nature of IBTrACS: DS, TS, ET, SS, NR, MX."""
    return _text(value) in _IBTRACS_NATURE


def validate_csquares_code(value):
    """A c-squares code of any resolution: 3112, 3112:3, 3112:360, 1212:121:2."""
    return bool(_CSQUARES.fullmatch(_text(value)))


def validate_csquares_code_fine(value):
    """A c-squares code finer than a ten-degree square, which its colons show: 3112:360, 1212:121:2
    (not 3112, which is any number)."""
    text = _text(value)
    return ":" in text and bool(_CSQUARES.fullmatch(text))


_WDPA_ID = re.compile(r"[1-9]\d{0,9}(?:\.0)?")


def validate_wdpa_id(value):
    """A site ID of the WDPA: a number without leading zeros (902678, 555555577), also read as a float."""
    return bool(_WDPA_ID.fullmatch(_text(value)))
