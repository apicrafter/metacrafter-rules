"""Rules for the TERN files of metacrafter-testdata (geonetwork.tern.org.au, 2024): AusPlots site
names, IBRA bioregions, Australian Soil Classification orders, NVIS growth forms, strata and cover
classes, Australian Faunal Directory and TERN vocabulary IRIs; scientific names without
authorship, their authorship, soil horizons, durations in words, times with a one-digit hour,
compass points, UTM zones and geodetic datums; and the guards that keep power plants off plant
individuals, Mexican postcodes off C:P ratios and bylines off taxon authorships.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.au import ecology
from metacrafterext.rules.common import fieldwork
from metacrafterext.rules.mx.validators import validate_mx_postcode
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (ecology.validate_au_ausplots_site_id,
     ["SAASTP0001", "NSFNNC0001", "QDAEIU0008", "WAACOO0021", "NSFNNC001", "QDWET0001", "TCFBEL0001", "SAA-STP-0001"],
     ["SAAXYZ0001", "NSABHC0001-53596", "SASB001", "WA0005", "XXANNC0001"]),
    (ecology.validate_au_ibra_region_code, ["NNC", "SEH", "WET", "KIN", "YAL"], ["NSW", "AVW01", "nnc", "XYZ"]),
    (ecology.validate_au_ibra_region, ["NSW North Coast", "Wet Tropics", "south eastern highlands", "Ben Lomond"],
     ["Riverland", "NNC", "Victoria"]),
    (ecology.validate_au_soil_order,
     ["Tenosols", "Chromosol", "Brown, Kurosol ", "Acidic-mottled, Dystrophic, Yellow Dermosol", "Calcarosols", "VERTOSOL"],
     ["Podzol", "Vertisol", "sand", "Sodosolic"]),
    (ecology.validate_au_nvis_growth_form_code, ["tree", "Tussock grass", "Chenopod", "shrub; fern", "T", "mallee shrub", "Forb"],
     ["sapling", "ground layer", "NA", "shrub; seedling", "phanerophyte", "TT"]),
    (ecology.validate_au_nvis_stratum, ["U", "M1", "G3", "E", "Mid-storey"], ["G4", "NA", "canopy", "U12"]),
    (ecology.validate_au_nvis_cover_class, ["d", "c", "i", "r", "bi", "bc"], ["NA", "x", "D", "cc"]),
    (ecology.validate_au_afd_taxon_url, ["https://biodiversity.org.au/afd/taxa/a14348d8-1a5d-47d1-9f66-dc82b7714a81"],
     ["https://biodiversity.org.au/afd/taxa/Formicidae", "a14348d8-1a5d-47d1-9f66-dc82b7714a81"]),
    (ecology.validate_au_tern_cv_concept, ["http://linked.data.gov.au/def/tern-cv/889dfc31-5b1c-48c0-8bc7-e12f13d63891"],
     ["http://www.w3.org/ns/sosa/phenomenonTime", "https://w3id.org/tern/ontologies/tern/SamplingPoint"]),
    (fieldwork.validate_scientific_name,
     ["Pardalotus striatus", "Casuarius casuarius johnsonii", "Solenopsis sp. B", "Iridomyrmex sp. anc1 (anceps complex)",
      "Rhytidoponera nr victoriae", "Megapodius (Megapodius) reinwardt castanonotus", "Eremophila latrobei subsp. glabra ",
      "Trachymene pilosa (Native Parsnip)", "Iridomyrmex anceps (Roger, 1863)", "Acacia x grayana"],
     ["Calomyrmex", "rotundata", "NA", "Formicidae", "Bird and bat", "Daintree Rainforest, Cape Tribulation"]),
    (fieldwork.validate_scientific_name_authorship,
     ["Latreille, 1809", "(Forel, 1901)", "F. Müller, 1866", "Giachino & Peck 2003", "Butler (1877)", "L.", "Gould",
      "(Lea 1924)", "J.E. Gray, 1831", "(E. André, 1896)", "R.Br.", "Benth. ex F.Muell."],
     ["1809", "NA", "FORMICIDAE", "check id", "FORMICIDAE Latreille, 1809", "some words in a sentence"]),
    (fieldwork.validate_author_byline, ["Jane Smith", "Pascoe", "Иванов И. И."], ["(Lea 1924)", "Pascoe 1869", "Mayr, 1870"]),
    (fieldwork.validate_soil_horizon, ["A", "A1", "A12", "B21", "Bt", "Bk2", "2C", "AB", "E"], ["NA", "A11 sandy", "Horizon", "Z"]),
    (fieldwork.validate_duration_text, ["20 minutes", "3 hours", "3 hours, 20 minutes", "2  days", "1 hour", "1.5 hrs"],
     ["20", "NA", "3 days later", "hours"]),
    (fieldwork.validate_clock_time, ["7:02", "7:02:00", "16:44", "9:50:00 AM", "10:10:00 AM", "6:15"], ["25:00", "13:00 PM", "7:2", "NA"]),
    (fieldwork.validate_clock_time_with_seconds, ["7:02:00", "9:50 AM", "16:44:10"], ["3:16", "16:44", "7:02:61"]),
    (fieldwork.validate_compass_point, ["N", "SSW", "ne", "WSW"], ["Nil", "NA flat", "NEN", "North"]),
    (fieldwork.validate_utm_zone, ["50 J", "55H", "56", "Zone 55"], ["61", "0", "50 O"]),
    (fieldwork.validate_utm_zone_with_band, ["50 J", "55H", "33U"], ["56", "3", "A"]),
    (fieldwork.validate_geodetic_datum, ["WGS 84", "WGS84", "GDA94", "GDA2020", "NAD83", "AGD66", "ETRS89"],
     ["EPSG:4326", "WGS", "4326", "GDA"]),
    (fieldwork.validate_elevation_value, ["535", "402.5", "1205 m", "-28", "3.5", "12"], ["9000", "abc", "12345", "3", "8"]),
    (fieldwork.validate_week_of_year, ["35", "53", "35.0", "1"], ["54", "0", "x"]),
    (validate_mx_postcode, ["06500", "6500.0", "99999"], ["0.0024", "00000", "1234", "123456"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("au/au_environment.yaml", "auausplotssiteidbyname", ["site_location_name", "Ausplot_ID", "ausplots_site_id"], ["site", "plot", "siteId_old"]),
    ("au/au_environment.yaml", "auibraregioncodebyname", ["Bioregion_Name", "bioregion", "ibra_code", "IBRA7_REG_CODE", "reg_code_7"],
     ["region", "bioregional_plan"]),
    ("au/au_environment.yaml", "auibraregionbyname", ["Bioregion_Full_Name", "bioregion_name", "ibra_reg_name", "reg_name_7"],
     ["region_name", "bioregion_code"]),
    ("au/au_environment.yaml", "ausoilorderbyname", ["soilClassification", "soilClassification ", "asc_order", "soil_order", "ASC"],
     ["soil_texture", "classification"]),
    ("au/au_environment.yaml", "aunvisgrowthformbyname", ["growth_form", "dominantGrowthForm", "growthForm", "plant_growth_form"],
     ["life_form", "growth_stage"]),
    ("au/au_environment.yaml", "aunvisstratumbyname", ["stratumType", "substratumType", "stratum", "nvis_stratum"], ["strata_count", "stratification"]),
    ("au/au_environment.yaml", "aunviscoverclassbyname", ["coverclass", "cover_class", "nvis_cover_code", "crown_cover_class"],
     ["coverType", "cover_percentage"]),
    ("common/science.yaml", "speciesbyfieldname",
     ["scientificName", "verbatimIdentification", "species", "Species", "mostDominantSpecies", "fifthMostDomainant Species",
      "herbarium_determination", "fieldSpeciesNames", "originalscientificname", "speciesOriginal", "Target_Species"],
     ["subspeciesOriginal", "species_count", "speciesArea", "scientificNameAuthorship"]),
    ("common/science.yaml", "dwcscientificnameauthorshipbyfield", ["authorship", "scientificNameAuthorship", "Author/Date", "dwc:scientificNameAuthorship"],
     ["author", "authorName", "authorshipDate"]),
    ("common/environment.yaml", "soilhorizonbyname", ["soilHorizon", "horizon", "horizon_designation"], ["horizonBoundary", "time_horizon"]),
    ("common/dateandtime.yaml", "clocktimebyname", ["startTime", "endTime", "finishTime", "time start", "time_finish", "phenomenonTime"],
     ["time", "datetime", "starttimestamp"]),
    ("common/dateandtime.yaml", "durationtextbyname", ["samplingDuration", "duration", "survey_duration"], ["samplingDuration_minutes", "durationType"]),
    ("common/geo.yaml", "compasspointbyname", ["aspect", "slopeAspect_direction", "aspect_orientation", "wind_direction", "winddir"],
     ["aspect_degree", "slopeAspect_degrees", "aspect_ratio"]),
    ("common/geo.yaml", "utmzonebyname", ["utm_zone", "mga_zone", "UTMZone", "zone_utm"], ["zone", "time_zone"]),
    ("common/geo.yaml", "geodeticdatumbyname", ["datum", "geodeticDatum", "dwc:geodeticDatum", "horizontal_datum"], ["date", "data"]),
    ("common/geo.yaml", "elevationbyname", ["elevation", "Elevation", "elevation_metres", "elevation [Metre]", "altitude", "elev_m"],
     ["elevation_source", "alt", "relevation"]),
    ("common/dateandtime.yaml", "weekofyearbyname", ["week_number", "week_of_year", "weekNo", "calendar_week"], ["week", "kw", "weekday"]),
    ("common/geo.yaml", "latitudebyshortname", ["featureLatitude", "transectLatitude", "decimalLatitude", "latdecimal", "lat"], ["latest", "plate"]),
    ("common/geo.yaml", "longitudebyshortname", ["featureLongitude", "transectLongitude", "decimalLongitude", "longdecimal", "lon"], ["long", "salon"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name.strip()), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("au/au_environment.yaml", "auausplotssiteidvalue", ["SAASTP0001", "NSFNNC0001", "NSFNNC001"], ["SAAXYZ0001", "NSABHC0001-53596"]),
    ("au/au_environment.yaml", "ausoilordervalue", ["Tenosols", "Brown, Kurosol"], ["Podzol", "Sodosolic soil"]),
    ("au/au_environment.yaml", "auafdtaxonvalue", ["https://biodiversity.org.au/afd/taxa/45862761-9b24-4d48-af4d-616134d71964"],
     ["https://biodiversity.org.au/afd/taxa/Formicidae"]),
    ("au/au_environment.yaml", "auterncvconceptvalue", ["http://linked.data.gov.au/def/tern-cv/7431d40e-0bf8-403f-bda5-8f9cd0e76a4f"],
     ["http://linked.data.gov.au/def/tern-cv/"]),
    ("common/dateandtime.yaml", "clocktimewithsecondsvalue", ["7:02:00", "9:50:00 AM"], ["3:16", "16:44"]),
    ("common/dateandtime.yaml", "durationtextvalue", ["3 hours, 20 minutes", "20 minutes", "2  days"], ["20", "minutes"]),
    ("common/geo.yaml", "geodeticdatumvalue", ["WGS 84", "GDA94", "GDA2020"], ["EPSG:4326", "WGS"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def test_zone_alone_needs_a_latitude_band():
    spec = load("common/geo.yaml", "utmzonewithbandbyname")
    assert spec["validator"].endswith("validate_utm_zone_with_band")
    assert field_matches("common/geo.yaml", "utmzonewithbandbyname", "zone")


def test_plant_id_is_not_a_power_plant_by_name():
    assert not field_matches("en/en_environment.yaml", "enenergypointfield", "plantId")
    assert field_matches("en/en_environment.yaml", "enenergypointfield", "power_plant_id")


def test_cp_is_a_postcode_only_with_five_digits():
    assert load("mx/mx_geo.yaml", "mxpostcodeknown")["validator"].endswith("validate_mx_postcode")


def test_bylines_leave_taxon_authorships():
    assert load("common/dublincore.yaml", "authorfield")["validator"].endswith("validate_author_byline")
