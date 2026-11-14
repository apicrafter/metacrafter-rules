"""Rules for the AIMS files of metacrafter-testdata (Australian Institute of Marine Science, AIMS
GeoNetwork snapshot of 2024): Great Barrier Reef feature identifiers and AIMS Long-Term
Monitoring Program sectors, decimal years, life stages, vessel names, plastic polymers, species
colour names, and times with seconds (the pattern lacked the second colon); the TERN rule
for species names takes the AIMS species fields.

Matched as tests/test_testdata_baseline.py matches them.
"""
import re

import pytest

from metacrafterext.rules.au.codes import validate_au_aims_ltmp_sector, validate_au_gbr_reef_id
from metacrafterext.rules.common.chemistry import validate_polymer_name, validate_polymer_name_or_code
from metacrafterext.rules.common.dateandtime import is_valid_time, validate_decimal_year
from metacrafterext.rules.common.generic import validate_colour_name, validate_vessel_name
from metacrafterext.rules.common.fieldwork import validate_scientific_name
from metacrafterext.rules.common.taxa import validate_life_stage
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (validate_au_gbr_reef_id, ["11-049", "21-550", "19-051a", "09-246", "24-001"], ["30-123", "11-49", "11-0490", "MCSWEENEY REEF", "11-049A", "08-001"]),
    (validate_au_aims_ltmp_sector, ["CA", "SW", "CB", "WH", "PO"], ["NO", "ca", "North", "XX", ""]),
    (validate_decimal_year, ["1994.83", "2019.0417", "2004", 1998.58], ["19.94", "3000.1", "1994,83", "1994.8312345", "abc"]),
    (is_valid_time, ["16:41:59", "00:32:43", "10:00", "23:59"], ["7:45", "25:00:00", "10:60:00", "1994.83"]),
    (validate_life_stage, ["AD", "JUV", "adult", "Juvenile", "larvae", "Sub-adult", "young of year"], ["I", "II", "Final", "Completed", "child"]),
    (validate_vessel_name, ["Solander", "Ferguson", "Cape Ferguson", "RV Investigator", "Queen Mary 2"], ["9224752", "2019-01-01", "12.5", "https://x.org/a"]),
    (validate_polymer_name, ["polypropylene", "Polyethylene terephthalate", "Polybutyleneterephthalate", "Cellulose based", "NFC:rayon",
                             "rayon:polyester", "Styrene-ethylene-butylene-styrene", "polyvinyl chloride", "nylon"],
     ["Polymer", "PET", "Polygon", "Poland", "Transparent", "politics"]),
    (validate_polymer_name_or_code, ["PET", "PP", "HDPE", "polypropylene"], ["PX", "Polygon", "Pennsylvania"]),
    (validate_scientific_name, ["Lethrinus laticaudis", "Sillago sp", "Choerodon cf. cyanodus", "Sargassum spp.",
                               "Plectropomus maculatus", "Scomberomorus queenslandicus"],
     ["Lethrinidae", "sand", "Grass Emperor", "12388"]),
    (validate_colour_name, ["Transparent", "black", "light blue", "Blue-green", "Black/White", "#1E90FF", "Pink"],
     ["colour", "Red Hat", "Fibre", "12", "cellulose"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("au/au_geo.yaml", "augbrreefidbyname", ["GBR_ID", "LABEL_ID", "gbrmpa_reef_id", "REEF_ID", "reef_label"], ["REEF_NAME", "reef", "gbr_sector"]),
    ("au/au_geo.yaml", "auaimsltmpsectorbyname", ["sector", "A_SECTOR", "ltmp_sector", "GBR_SECTOR", "sector_code"], ["sectors", "subsector", "sector_name"]),
    ("common/dateandtime.yaml", "decimalyearbyfield", ["Deci_Year", "decimal_year", "dec_year", "decyear", "decimal_date", "year_frac", "fractional_year"],
     ["year", "Year", "decade", "date"]),
    ("common/science.yaml", "dwclifestagebyfield", ["stage", "lifeStage", "life_stage", "dwc:lifeStage", "development_stage", "age_class"],
     ["stage_name", "backstage", "stages"]),
    ("common/science.yaml", "speciesbyfieldname", ["species", "scientificName", "latin_name"], ["family", "common_name"]),
    ("common/transport.yaml", "vesselnamebyfield", ["RV", "vessel", "vessel_name", "ship_name", "shipname", "Research vessel", "boat_name"],
     ["vessels", "ship_date", "ship_mode", "rvalue"]),
    ("common/environment.yaml", "polymertypebyfield", ["Polymer", "polymer_type", "plastic_type", "FTIR_polymer", "resin_type"],
     ["polymerase", "plastic", "material"]),
    ("common/common.yaml", "colourbyfield", ["colour", "Color", "colours", "vehicle_colour", "colour_name", "hair color"],
     ["colourful", "discolouration", "color_temperature"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("au/au_geo.yaml", "augbrreefidvalue", ["11-049", "19-051a"], ["30-123", "11-49", "MCSWEENEY REEF"]),
    ("common/environment.yaml", "polymertypevalue", ["polypropylene", "polyethylene terephthalate", "rayon:polyester"], ["PET", "Polymer", "Polygon"]),
    ("ext/ext_datetime.yaml", "timebypatmin", ["16:41:59", "00:32:43"], ["164159", "16:4159", "10:3000", "7:45"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def test_reef_id_value_rule_needs_a_reef_field():
    guard = load("au/au_geo.yaml", "augbrreefidvalue")["fieldregex"]
    for name in ("REEF_NAME", "gbr_label", "reef"):
        assert re.search(guard, name), name
    for name in ("case_number", "file_no", "code"):
        assert not re.search(guard, name), name


def test_new_field_rules_need_values():
    for path, rule_id, _, _ in FIELDS:
        if rule_id == "speciesbyfieldname":  # the TERN rule, checked for the AIMS field names
            continue
        assert load(path, rule_id).get("needs_values") is True, rule_id
