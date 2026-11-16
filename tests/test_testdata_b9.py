"""Rules for the files of metacrafter-testdata from 2024 snapshots of open data portals of Scotland and Greece
(Dateno sources cdi00000828, Marine Scotland Data; cdi00000831, Stirling Council; cdi00000833, Angus Council;
cdi00000862, Thessaloniki; cdi00000875, CUHK Research Data Repository): ICES code lists and statistical
rectangles, AphiaIDs, FAO species codes, Scottish GSS codes, UPRN and USRN, SEED codes, the Scottish urban rural
classification, Scottish Marine Regions, parking contravention codes and Greek month abbreviations.

Matched as tests/test_testdata_baseline.py matches them.
"""
import re

import pytest

from metacrafterext.rules.common import marine
from metacrafterext.rules.common.generic import validate_category_value
from metacrafterext.rules.gb import codes
from metacrafterext.rules.gr.periods import validate_el_month_abbreviation
from metacrafterext.rules.tz.geo import validate_tz_region, validate_tz_region_by_value
from tests.test_testdata_baseline import field_matches, guarded_by, load

VALIDATORS = [
    (marine.validate_ices_parameter_code, ["CD", "HG", "PB", "CB118", "CB153", "ANT", "BAA", "SKIN ULC"], ["cadmium", "cd", "Metals", ""]),
    (marine.validate_ices_matrix_code, ["LI", "MU", "SED63", "SB", "BI"], ["Liver", "SEDTOT", "li", ""]),
    (marine.validate_ices_method_of_analysis_code, ["GC-MS", "GC-ECD", "ICP-MS", "AAS"], ["gas chromatography", "GCMS", ""]),
    (marine.validate_ices_station_type, ["B", "RH", "IH", "IH-A"], ["Coast", "X", ""]),
    (marine.validate_ices_gear_code, ["GOV", "ROT", "BT4A", "BT8", "NCT"], ["Otter trawl", "Drop", "OT", "BT184_21", ""]),
    (marine.validate_ices_qualifier_flag, ["<", ">", "D", "Q"], ["N", "<=", "d", ""]),
    (marine.validate_ices_basis_code, ["W", "D", "L"], ["F", "LCA 2006-08", "w", ""]),
    (marine.validate_ices_statistical_rectangle, ["34E5", "43D6", "37F3", "46F2", "36e4"], ["37I2", "39-40 E5", "00E5", "37A4", "E534", ""]),
    (marine.validate_worms_aphia_id, ["126436", "156533", "105865", "126436.0"], ["Pres/Abs", "12", "0126436", "Gadus morhua", ""]),
    (marine.validate_fao_asfis_code, ["COD", "HAD", "WHB", "MAC"], ["cod", "CODS", "DRB*", "Atlantic cod", ""]),
    (marine.validate_scottish_marine_region,
     ["Outer Hebrides", "Shetland Isles", "Forth and Tay", "Argyll & Clyde", "West Highlands & North Coast", "All Scotland", "SOLWAY"],
     ["Irish Sea", "Northern North Sea", "Highland", "Argyll & Bute", ""]),
    (codes.validate_uprn, ["122046218", "117097853", "100023336956", "122046218.0"], ["12345", "0122046218", "1000233369567", "FK8 1SD", ""]),
    (codes.validate_usrn, ["38002160", "47901305", "38009090.0"], ["122046218", "3800216", "08002160", "Main Street", ""]),
    (codes.validate_scottish_seed_code, ["5720826", "8212627", "5745829"], ["572082", "57208260", "0720826", "Dunblane Primary School", ""]),
    (codes.validate_scotland_urban_rural,
     ["1", "2", "6", "8", "Other Urban Areas", "Accessible Small Towns", "Remote Rural", "accessible rural", "Large Urban Areas"],
     ["0", "9", "Urban", "Rural", ""]),
    (codes.validate_parking_contravention_code,
     ["01", "16", "40j", "16 - Parked without displaying a valid permit", "06 - No ticket", "23-Parked in bay not designated for vehicle"],
     ["Parked without displaying a valid permit", "1", "16/09/2022", "2022", ""]),
    (validate_el_month_abbreviation, ["ΙΑΝ", "ΦΕΒ", "ΜΑΡ", "ΑΠΡ", "ΜΑΙ", "ΙΟΝ", "ΙΟΛ", "ΙΟΥΛ", "Αυγ", "Σεπτ.", "ΔΕΚ", "Ιανουάριος"],
     ["jan", "june", "ΔΕΥ", "ΙΟΝΙΟ", ""]),
    (validate_tz_region_by_value, ["Dodoma", "Dar es Salaam", "Pwani", "Coast Region"], ["Coast", "coast", "Open Sea", "Estuary", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value
    assert not func(None)


def test_coast_is_a_region_under_a_region_name():
    # the field-name rule keeps Coast, the English name of Pwani
    assert validate_tz_region("Coast")


def test_a_long_decimal_is_no_category():
    # status_BAC and se_status of the CSEMP assessments hold the distance to a threshold
    for value in ["-0.108360984950716", "2.44627267233258", "0.158856488805864", "4,98661545757929"]:
        assert not validate_category_value(value), value
    for value in ["Current", "1", "1.5", "A1", "Allocated Site", "2.25"]:
        assert validate_category_value(value), value


FIELDS = [
    ("common/marine.yaml", "icesparametercodebyname", ["determinand", "PARAM", "parameter_code", "param_code"],
     ["determinand_group", "parameter", "Parameter", "VariableName"]),
    ("common/marine.yaml", "icesmatrixcodebyname", ["matrix", "MATRX", "matrix_code"], ["Matrix_Sample_Material", "material"]),
    ("common/marine.yaml", "icesmethodofanalysiscodebyname", ["metoa", "METOA"], ["method", "Method"]),
    ("common/marine.yaml", "icesqualifierflagbyname", ["qflag", "normConc.qflag", "CORG.qflag", "qflag_norm", "LIPIDWT_qflag", "DRYWT%.qflag"],
     ["flag", "quality_flag", "qflags_all_values"]),
    ("common/marine.yaml", "icesbasiscodebyname", ["basis", "basis_profile", "BASIS"], ["FMSYBasis", "basis_of_record", "basisOfRecord"]),
    ("common/marine.yaml", "icesstationtypebyname", ["MSTAT", "mstat"], ["WLTYP", "station", "status"]),
    ("common/marine.yaml", "icesgearcodebyname", ["Gear", "gear", "gear_code", "GearCode"], ["GearType", "Gear Type", "Gear_Category", "gearName", "all_gear"]),
    ("common/marine.yaml", "icesstatisticalrectanglebyname",
     ["ICES Rectangle", "ICES_Rectangle", "ICESStSq", "ices_rectangle", "StatRec", "statistical_rectangle", "Statistical Rectangles", "ICES StatSq"],
     ["rectangle", "ICES_area", "Scottish Marine Region", "ICESname"]),
    ("common/marine.yaml", "wormsaphiaidbyname", ["AphiaID", "Aphia_Code", "species_aphia_id", "SpeciesAphiaID", "valid_AphiaID", "aphia_id"],
     ["aphia", "ScientificName", "LifeForm"]),
    ("common/marine.yaml", "faoasfiscodebyname", ["Species(FAOCodes)", "3-alpha", "fao_code", "FAO species code", "asfis_code", "species_fao"],
     ["SpeciesCode", "alpha3", "fao_area", "gearAbbr"]),
    ("gb/gb_geo.yaml", "gbuprnbynamewithvalues", ["uprn", "UPRN", "cag_uprn_nearest", "Unique_Property_Reference_Number", "property_uprn", "uprn_number"],
     ["Site_UPRN", "Block_UPRN", "usrn", "urn"]),
    ("gb/gb_geo.yaml", "gbusrnbyname", ["usrn", "USRN", "cag_usrn_nearest", "unique_street_reference_number"], ["uprn", "urn", "street"]),
    ("gb/gb_geo.yaml", "gbscotlandurbanruralclassificationbyname",
     ["RURAL_CLASSIFICATION", "RURAL_CLASSIFICATION_DESCRIPTION", "urban_rural_classification", "UR6FOLD", "UR8_FOLD", "UrbanRural6fold"],
     ["Rural_or_Urban_Road", "classification", "rural"]),
    ("gb/gb_geo.yaml", "gbscottishmarineregionbyname", ["Scottish Marine Region", "scottish_marine_region", "marine_region", "SMR"],
     ["Region", "region", "CSEMP_region", "Total Production for all Scottish Marine Regions (Tonnes)"]),
    ("gb/gb_geo.yaml", "gbeastingbyprefixedname", ["X_easting", "X_Easting", "cag_easting", "site_easting"], ["Y_northing", "x", "east"]),
    ("gb/gb_geo.yaml", "gbnorthingbyprefixedname", ["Y_northing", "Y_Northing", "cag_northing"], ["X_easting", "y", "north"]),
    ("gb/gb_education.yaml", "gbscottishseedcodebyname", ["Seed_Code", "seedno", "SEED code", "seed_number", "school_seed", "SeedCode"],
     ["seed", "random_seed", "School_Name", "seeds"]),
    ("gb/gb_transport.yaml", "gbparkingcontraventioncodebyname", ["Contravention", "contravention_code", "Contravention Code", "PCN_contravention"],
     ["Contravention_Date", "Fixed_Penalty_Notice", "contraventions"]),
    ("gr/gr_datetime.yaml", "elmonthabbreviationbyname", ["month_name", "month", "Μήνας", "ΜΗΝΑΣ", "MonthName"], ["monthly", "DayDate", "έτος"]),
    ("common/science.yaml", "speciesbylatinfieldname",
     ["Species_Latin_name", "Species Latin name", "SpeciesSciName", "Latin species name", "ScientificSpeciesName", "Latin Name", "Scientific Name",
      "Species_scientific_name"],
     ["Species_alternative_name", "Species_name", "CommonSpeciesName", "name"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    spec = load(path, rule_id)
    assert spec["key"]
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("gb/gb_geo.yaml", "gbscotlandintermediatezonecodevalue", ["S02002436", "S02002445"], ["S01013001", "S0200243", "E02002436"]),
    ("gb/gb_geo.yaml", "gbscotlandhealthboardcodevalue", ["S08000019"], ["S12000030", "S080000190"]),
    ("gb/gb_geo.yaml", "gbscotlandcouncilareacodevalue", ["S12000030", "S12000036"], ["S92000003", "E12000030"]),
    ("gb/gb_geo.yaml", "gbscotlandelectoralwardcodevalue", ["S13003118", "S13003121"], ["S16000144", "E05003118"]),
    ("gb/gb_geo.yaml", "gbscottishparliamentconstituencycodevalue", ["S16000144", "S16000088"], ["S14000057", "S13003118"]),
    ("gb/gb_geo.yaml", "gbscotlandlocalitycodevalue", ["S19001277", "S19001315"], ["S20001477"]),
    ("gb/gb_geo.yaml", "gbscotlandsettlementcodevalue", ["S20001477", "S20001992"], ["S19001277"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    spec = load(path, rule_id)
    pattern = re.compile(spec["rule"])
    for value in good:
        assert pattern.fullmatch(value), value
        assert spec["minlen"] <= len(value) <= spec["maxlen"]
    for value in bad:
        assert not pattern.fullmatch(value), value


@pytest.mark.parametrize("path,rule_id", [("common/objects.yaml", "oidvalue"), ("ext/ext_internet.yaml", "ipv4")])
def test_a_version_field_holds_no_oid_or_address(path, rule_id):
    # runtime_version 3.0.3.80 of an E-Prime log
    guard = re.compile(load(path, rule_id)["fieldregex"])
    for name in ["runtime_version", "studio_version", "experiment_version", "Version", "firmware"]:
        assert not guard.search(name), name
    for name in ["oid", "object_identifier", "sysObjectID", "code", "ip", "ip_address", "host"]:
        assert guard.search(name), name
