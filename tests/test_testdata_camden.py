"""Rules for the Camden Council files of metacrafter-testdata (a 2024 snapshot of data.camden.nsw.gov.au, the
Opendatasoft open data portal of Camden Council, New South Wales): council wards, NSW environmental planning
instruments and development control plans, heritage item numbers and significance levels, blue-green algae
alert levels; the water quality readings of the South Creek stormwater sensors (dissolved oxygen, turbidity,
conductivity, salinity, TDS, pH and temperature under The Things Network payload names), solar energy,
Opendatasoft geolocation points, directions in words, MGA coordinates named xcord / ycord, common names of
species and long GeoJSON boundaries.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.au.codes import validate_au_lga_name_plain
from metacrafterext.rules.au.planning import (
    validate_au_algae_alert_colour,
    validate_au_algae_alert_level,
    validate_au_council_ward,
    validate_au_heritage_significance,
    validate_au_nsw_dcp,
    validate_au_nsw_epi,
    validate_au_nsw_epi_or_abbreviation,
    validate_au_nsw_heritage_item_number,
    validate_not_au_council_ward,
)
from metacrafterext.rules.common.fieldwork import validate_cardinal_direction, validate_compass_point
from metacrafterext.rules.common.taxa import validate_vernacular_name, validate_vernacular_with_scientific
from metacrafterext.rules.common.waterquality import (
    validate_conductivity,
    validate_dissolved_oxygen,
    validate_energy_amount,
    validate_salinity,
    validate_total_dissolved_solids,
    validate_turbidity,
)
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (validate_au_council_ward, ["North Ward", "Central Ward", "SOUTH WARD", "Bass Hill Ward", "Ward 1", "A Ward", "Division 3",
                                "Unsubdivided", "Macquarie Ward"],
     ["Camden", "North", "Ward End", "Ward 123", "CAMDEN", "Abbey", ""]),
    (validate_not_au_council_ward, ["Abbey", "Castle", "Ward End", "St Helier", "Hornsey Central"],
     ["North Ward", "Ward 2", "SOUTH WARD", "1234", ""]),
    (validate_au_nsw_epi, ["Camden LEP 2010", "Camden Local Environmental Plan 2010",
                           "SEPP (Precincts—Western Parkland City) 2021 – Camden Growth Centres (Appendix 5)",
                           "State Environmental Planning Policy (Biodiversity and Conservation) 2021",
                           "State Environmental Planning Policy No 19—Bushland in Urban Areas", "Albury Local Environmental Plan 2010",
                           "Sydney Regional Environmental Plan No 20—Hawkesbury-Nepean River (No 2—1997)", "Interim Development Order No 1"],
     ["Camden DCP 2019", "LEP", "Camden", "Local Environmental Plan", "Leptospirosis 2010", "Help 2010", "CLEP2010"]),
    (validate_au_nsw_epi_or_abbreviation, ["CLEP2010", "SEPP2021", "LEP 2013", "SREP20", "Camden LEP 2010"],
     ["CLEP", "SEPP", "2010", "Camden DCP 2019"]),
    (validate_au_nsw_dcp, ["Camden DCP 2019", "Camden Growth Centre Precincts DCP", "Turner Road DCP", "Oran Park DCP",
                           "Camden Growth Centre Precincts DCP Appendices", "Oran Park DCP Appendices and Attachments",
                           "Camden Growth Centre Precincts DCP – Schedule 7 –  Pondicherry", "Hornsby Development Control Plan 2013",
                           "DCP No 5"],
     ["DCP", "Camden LEP 2010", "data center provider", "dcp", "1234"]),
    (validate_au_nsw_heritage_item_number, ["I38", "I122", "I90A", "A12", "C3", "i5"], ["38", "I12345", "IA", "B12", ""]),
    (validate_au_heritage_significance, ["Local", "State", "National", "World", "LOCAL", "Commonwealth"], ["High", "3", "Regional", ""]),
    (validate_au_algae_alert_level, ["Green alert", "Amber alert", "Red alert", "No alert", "Green level surveillance", "RED ALERT",
                                     "Amber Alert Level"],
     ["Red", "Green", "Yellow warning", "High", "Amber Alert 2023-01", ""]),
    (validate_au_algae_alert_colour, ["Green", "Amber", "Red", "Green alert", "No alert"], ["Yellow", "High", "Blue", ""]),
    (validate_cardinal_direction, ["East", "Northeast", "North-East", "south west", "North-northeast", "Northbound", "Westward",
                                   "SOUTHEAST"],
     ["N", "NE", "North-South", "Northern", "Up", "Inbound", ""]),
    (validate_vernacular_name, ["European Carp", "Australian Bass", "noisy miner", "masked lapwing - plover (vanellus miles)",
                                "London plane", "Colourful Koi Carp", "Bird/small arboreal mammal"],
     ["1234", "Animalia", "a b c d e f g", "", "x" * 120]),
    (validate_vernacular_with_scientific, ["australian magpie (cracticus tibicen)", "Noisy Miner (Manorina melanocephala)",
                                           "masked lapwing - plover (vanellus miles)"],
     ["Manorina melanocephala", "noisy miner", "clear incident", "Camden (NSW)"]),
    (validate_dissolved_oxygen, ["4.9", "0.0", "55.49", "8.2 mg/L", "95 %", "112"], ["-1", "2022-03-16", "12 NTU", "600", "abc"]),
    (validate_turbidity, ["41.56", "18.7", "0.8 FNU", "120 NTU", "79.47"], ["-3.2", "638 uS/cm", "20000", "abc"]),
    (validate_conductivity, ["638.0", "637.28", "1.2 dS/m", "638 uS/cm", "52000"], ["-5", "7.2 pH", "300000", "abc"]),
    (validate_salinity, ["0.34", "35.1 PSU", "34‰", "280 ppm"], ["-1", "12 NTU", "abc"]),
    (validate_total_dissolved_solids, ["322.0", "480 mg/L", "321.63"], ["-2", "638 uS/cm", "abc"]),
    (validate_energy_amount, ["2.325", "0.0", "-0.05056", "9.059 kWh", "1200 MWh", "35 GJ"], ["5 kW", "2023-04-12", "A+++", "abc", ""]),
    (validate_au_lga_name_plain, ["CAMDEN", "WARRUMBUNGLE", "UPPER HUNTER", "Camden", "Albury (C)"],
     ["NSW", "QLD", "10050", "NORTH WARD", "Division 3", "BIRNIN GWARI"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


def test_directions_in_words_are_not_compass_points():
    # The 16-wind abbreviations are compass_point, the words cardinal_direction: one field gets one.
    for value in ("N", "NNE", "SW"):
        assert validate_compass_point(value) and not validate_cardinal_direction(value), value
    for value in ("East", "Northeast"):
        assert validate_cardinal_direction(value) and not validate_compass_point(value), value


FIELDS = [
    ("au/au_geo.yaml", "aucouncilwardbyname", ["ward", "ward_name", "WARD_NAME", "wardname", "tag", "council_ward", "ward_label"],
     ["wards", "award", "ward_code", "tags"]),
    ("au/au_legal.yaml", "ausnwepibyname", ["epi", "EPI_NAME", "epi_title", "iteminst", "item_inst", "planning_instrument",
                                           "environmental_planning_instrument", "lep_name"],
     ["episode", "epic", "dcp_epi", "instrument"]),
    ("au/au_legal.yaml", "ausnwdcpbyname", ["dcp", "dcp1", "dcp4", "DCP_NAME", "development_control_plan"], ["dcp_epi", "dcp12", "dcps"]),
    ("au/au_legal.yaml", "ausnwheritageitemnumberbyname", ["item_no", "H_ID", "heritage_item_no", "item_number", "heritage_id", "itemno"],
     ["item", "item_name", "hid", "items_no"]),
    ("au/au_legal.yaml", "auheritagesignificancebyname", ["itemsig", "SIG", "significance", "heritage_significance",
                                                          "significance_level"],
     ["signature", "sig_value", "significant"]),
    ("au/au_environment.yaml", "aualgaealertlevelbyname", ["current_new_alert_status", "previous_alert_status", "alert_level", "alert",
                                                           "alert_status", "bga alert level"],
     ["alerts", "alert_details", "alerted_by"]),
    ("au/au_environment.yaml", "aualgaealertcolourbyname", ["bga_alert", "algae_status", "algal_alert_level", "cyanobacteria_level",
                                                            "blue_green_algae_alert", "algae"],
     ["algaecide", "algae_species", "cyanide"]),
    ("common/environment.yaml", "phbysensorname", ["payload_fields_ph", "uplink_message_decoded_payload_ph", "object_ph",
                                                   "payload_fields_pheht_ph"],
     ["payload_fields_ph_mv", "ph_mv", "payload_fields_phone"]),
    ("common/environment.yaml", "dissolvedoxygenbyname", ["payload_fields_optod_oxygen_mg", "payload_fields_optod_oxygen_percent",
                                                          "payload_fields_optod_oxygen_ppm", "dissolved_oxygen", "DO_mg_L", "DO (%)",
                                                          "do_sat", "Dissolved Oxygen (mg/L)", "oxygen_ppm", "mean_dissolved_oxygen"],
     ["oxygen", "o2", "do", "oxygen_saturation", "spo2", "door"]),
    ("common/environment.yaml", "turbiditybyname", ["payload_fields_ntu_turbidityntu", "payload_fields_ntu_turbidityfnu",
                                                    "payload_fields_ntu_turbidity_mg_l", "turbidity", "Turbidity_NTU", "NTU",
                                                    "turbidity (ntu)"],
     ["turbine", "turb", "turbidity_flag"]),
    ("common/environment.yaml", "conductivitybyname", ["payload_fields_c4e_conductivity_us_cm", "conductivity", "EC_uS_cm",
                                                       "specific_conductance", "SpC", "electrical_conductivity", "cond_us_cm"],
     ["thermal_conductivity", "hydraulic_conductivity", "ec", "cond", "conductor"]),
    ("common/environment.yaml", "salinitybyname", ["payload_fields_c4e_salinity_ppm", "salinity", "salinity_psu", "sal_ppt",
                                                   "surface_salinity"],
     ["sal", "salary", "salinity_flag"]),
    ("common/environment.yaml", "totaldissolvedsolidsbyname", ["payload_fields_c4e_tdskcl_ppm", "total_dissolved_solids", "TDS_mg_L",
                                                               "tds_ppm", "tds (mg/l)", "tdskcl"],
     ["tds", "tds_amount", "tds_deducted"]),
    ("common/values.yaml", "temperaturebysensorname", ["payload_fields_optod_temperature", "payload_fields_pheht_temperature",
                                                       "payload_fields_c4e_temperature", "uplink_message_decoded_payload_temp",
                                                       "object_temperature"],
     ["temperature", "payload_fields_temperature_flag", "payload_fields_template"]),
    ("common/values.yaml", "energyamountbyname", ["energy_generated", "energy_kwh", "kwh_consumed", "electricity_consumption_kwh",
                                                  "energy", "Energy (kJ)", "total_energy_consumption", "kwh", "power_consumption"],
     ["energy_rating", "energy_class", "energy_source", "renewable_energy_share", "kw"]),
    ("common/geo.yaml", "geopointgeolocationbyname", ["geolocation", "geo_location", "geoloc", "geolocalisation", "geo_position"],
     ["location", "geolocation_accuracy", "geo"]),
    ("common/geo.yaml", "cardinaldirectionbyname", ["aspect_of_installation", "aspect", "direction", "wind_direction",
                                                    "travel_direction", "orientation", "facing"],
     ["directions", "director", "aspects_count"]),
    ("common/geo.yaml", "eastingbyxcoordname", ["xcord", "x_coord", "xcoordinate", "x_coordinate", "XCOORD", "x_coord_mga"],
     ["x", "xcord2x", "y_coord"]),
    ("common/geo.yaml", "northingbyycoordname", ["ycord", "y_coord", "ycoordinate", "y_coordinate"], ["y", "x_coord"]),
    ("common/science.yaml", "vernacularnamebyname", ["vernacularName", "dwc:vernacularName", "fish_species", "other_fish_species",
                                                     "bird_species", "tree_common_name", "species_common_name", "common_species_name"],
     ["common_name", "species", "fish_size"]),
    ("common/science.yaml", "vernacularnamewithscientificbyspecies", ["species", "species_name", "bird species"], ["subspecies_x", "specie"]),
    ("common/telecom.yaml", "imeideviceidfield", ["device_id", "mobile_device_id", "equipment_id"], ["imei", "dev_id"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("au/au_legal.yaml", "ausnwepivalue", ["Camden Local Environmental Plan 2010", "SEPP (Precincts—Western Parkland City) 2021"],
     ["Camden DCP 2019", "LEP"]),
    ("au/au_legal.yaml", "ausnwdcpvalue", ["Camden DCP 2019", "Hornsby Development Control Plan 2013"], ["DCP", "Camden LEP 2010"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def test_new_field_rules_need_values():
    for path, rule_id, _, _ in FIELDS:
        spec = load(path, rule_id)
        assert spec.get("validator") and spec.get("needs_values") is True, rule_id


def test_device_id_is_no_imei_by_its_name_alone():
    # The LoRaWAN sensors of Camden Council have device ids such as snla1k512.
    assert not field_matches("common/telecom.yaml", "imeifield", "device_id")
    assert field_matches("common/telecom.yaml", "imeifield", "imei")
    assert load("common/telecom.yaml", "imeideviceidfield")["validator"].endswith("validate_imei")


def test_uk_ward_name_refuses_australian_council_wards():
    spec = load("gb/gb_geo.yaml", "ukwardnamebyknown")
    assert spec["rule"].endswith("validate_not_au_council_ward")
    assert value_matches("gb/gb_geo.yaml", "ukwardnamebyknown", "Abbey")
    assert not value_matches("gb/gb_geo.yaml", "ukwardnamebyknown", "North Ward")


def test_long_geojson_geometries():
    # The geo_shape of the Camden LGA boundary is one polygon of 200 202 characters.
    short = load("common/geo_text.yaml", "geojsongeometrytext")
    long_ = load("common/geo_text.yaml", "geojsongeometrylongtext")
    assert short["maxlen"] == 100000 and long_["minlen"] == 100001 and long_["maxlen"] >= 1000000
    ring = ", ".join(f"[150.{i:06d}, -34.{i:06d}]" for i in range(8000))
    value = '{"coordinates": [[[' + ring + ']]], "type": "Polygon"}'
    assert len(value) > 200000
    assert value_matches("common/geo_text.yaml", "geojsongeometrylongtext", value)
    assert not value_matches("common/geo_text.yaml", "geojsongeometrytext", value)
