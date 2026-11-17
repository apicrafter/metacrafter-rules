"""UK codes found in 2024 snapshots of the Open Data NI portal (admin.opendatani.gov.uk, Dateno source
temp00004663) and of the GeoServers of Pembrokeshire, Cumbria, Cheshire East and the Brecon Beacons
(temp00003701, temp00001527, temp00001530, temp00001526): Healthcare Resource Groups, Northern Ireland
wards, Super Output Areas and district councils of 1992, road numbers and AddressBase classes.
"""
import re

from metacrafterext.rules.common.b13 import number, text

_HRG = re.compile(r"[A-Z]{2}\d{2}[A-Z]")
_NI_WARD = re.compile(r"95([A-Z])\1\d{2}")
_NI_SOA = re.compile(r"95([A-Z])\1\d{2}[SW]\d")
_NI_LGD = re.compile(r"95([A-Z])\1")
_ROAD = re.compile(r"[ABM]\d{1,4}(?:\(M\))?")
_ABC = re.compile(r"[CLMOPRUXZ](?:[A-Z](?:\d{2}(?:[A-Z0-9]{2})?)?)?")


def validate_gb_hrg_code(value):
    """An HRG4 code: AA22G, AA26H, WA14Z (not AA2G)."""
    return bool(_HRG.fullmatch(text(value)))


def validate_gb_ni_ward_1992_code(value):
    """A Northern Ireland ward of 1992: 95AA01 (Aldergrove); the district letters are doubled."""
    return bool(_NI_WARD.fullmatch(text(value)))


def validate_gb_ni_soa_code(value):
    """A Northern Ireland Super Output Area: 95AA01S1, 95AA02W1."""
    return bool(_NI_SOA.fullmatch(text(value)))


def validate_gb_ni_lgd_1992_code(value):
    """A Northern Ireland district council of 1973 to 2015: 95AA (Antrim) to 95ZZ (Strabane)."""
    return bool(_NI_LGD.fullmatch(text(value)))


def validate_gb_road_number(value):
    """A UK road number: A2, M1, B101, A1(M) (not D121)."""
    return bool(_ROAD.fullmatch(number(value).upper().replace(" ", "")))


def validate_gb_addressbase_classification(value):
    """An AddressBase classification code: RD02, RI01, PP, CR08, R."""
    return bool(_ABC.fullmatch(text(value)))
