"""Australian codes found in the AIMS data of metacrafter-testdata (the AIMS GeoNetwork snapshot):
Great Barrier Reef feature identifiers of GBRMPA and the sectors of the AIMS Long-Term Monitoring
Program."""
import re

# GBR_ID: whole degrees of south latitude (9 in the Torres Strait to 24 at the southern end of the
# Marine Park), a hyphen and three digits; LABEL_ID adds a lowercase letter for a part of a feature.
_GBR_REEF_ID = re.compile(r"^(?:09|1\d|2[0-4])-\d{3}[a-z]?$")

AIMS_LTMP_SECTORS = frozenset("CG PC CL CA IN TO CU WH PO SW CB".split())


def validate_au_gbr_reef_id(value):
    """A GBRMPA feature identifier: 11-049, 19-051a, 09-246 (not 30-123 or 11-49)."""
    return bool(_GBR_REEF_ID.match(str(value).strip()))


def validate_au_aims_ltmp_sector(value):
    """A sector code of the AIMS Long-Term Monitoring Program: CA (Cairns), SW (Swains), CB
    (Capricorn-Bunker). Six of them are also country codes, so rules need a sector field."""
    return str(value).strip() in AIMS_LTMP_SECTORS
