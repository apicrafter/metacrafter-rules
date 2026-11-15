"""Rules for the files of four Australian Opendatasoft portals in metacrafter-testdata (2024 snapshots of
data.melbourne.vic.gov.au, www.geelongdataexchange.com.au, data.liverpool.nsw.gov.au and data.peclet.com.au):
CLUE small areas of the City of Melbourne, NSW lot identifiers and survey plan numbers, NSW and Victorian
planning zones, planning application numbers, parking restrictions, Geoscape PIDs, ANZSIC division titles,
Victorian Biodiversity Atlas ids, DCA crash codes, state names; pipe materials, the useful life expectancy
and age class of trees, electric power, ISO 8601 repeating intervals, crash severity; and the fixes of names
and false labels found there.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.au.council import (
    validate_au_anzsic_division_name,
    validate_au_clue_small_area,
    validate_au_dca_code,
    validate_au_geoscape_pid,
    validate_au_nsw_land_zone,
    validate_au_nsw_lot_id,
    validate_au_parking_restriction,
    validate_au_planning_application_number,
    validate_au_state_name,
    validate_au_survey_plan_number,
    validate_au_vba_taxon_id,
    validate_au_vic_planning_zone,
)
from metacrafterext.rules.common.assets import (
    validate_crash_severity,
    validate_electric_power,
    validate_iso8601_repeating_interval,
    validate_pipe_material,
    validate_tree_age_class,
    validate_tree_useful_life_expectancy,
)
from metacrafterext.rules.common.generic import validate_class_or_order_name, validate_taxon_name
from metacrafterext.rules.common.identifiers import validate_card_number_text, validate_twitter_at_handle
from metacrafterext.rules.ng.geo import validate_ng_lga_code
from metacrafterext.rules.za.finances import validate_za_economic_classification_value
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (validate_au_clue_small_area, ["Melbourne (CBD)", "West Melbourne (Residential)", "Docklands", "City of Melbourne (total)",
                                   "melbourne (remainder)"],
     ["Fitzroy", "Melbourne CBD", "Richmond", "Melbourne", ""]),
    (validate_au_nsw_lot_id, ["23/O/DP1417", "1//DP225807", "//SP37549", "9/16/DP758477", "B//DP943176"],
     ["DP1417", "1/2/3", "23/O/1417", "//", "23//PS1234"]),
    (validate_au_survey_plan_number, ["DP1417", "SP37549", "PS612345R", "RP123456", "LP 1234"],
     ["1417", "DP", "ABC1234", "DP12345678", ""]),
    (validate_au_nsw_land_zone, ["R2", "RU1", "SP2", "B4", "E1", "MU1", "C3", "W1", "UL"], ["R6", "GRZ1", "B9", "RU7", ""]),
    (validate_au_vic_planning_zone, ["GRZ1", "UGZ3", "IN1Z", "C1Z", "FZ", "PCRZ", "RCZ13", "LDRZ2"], ["R2", "GRZ123", "ZONE1", "RU1"]),
    (validate_au_planning_application_number, ["DA-404/2015", "D/2008/940", "2015_D/2008/940/C", "TP-2014-43/A", "TPM-2010-31",
                                               "BP-2014-1813/1", "CDC-123/2019"],
     ["1501/2014/005613/2", "DA", "2015", "0", "DA-404"]),
    (validate_au_parking_restriction, ["2P", "1/2P Meter", "2P MTR M-SAT 7:30-18:30", "P 10 Mins", "QP", "MP2P", "Loading Zone 15M",
                                       "LZ30", "3P Ticket", "Clearway (Tow away)", "1p", "2P Voucher", "15 MINUTE"],
     ["2 Hours", "Parking", "Free", "15", "Paid", "HORSE DRAWN VEHICLE", ""]),
    (validate_au_geoscape_pid, ["lga94484cf6e0e2", "lgpa9f1f9d86a5e", "lgp9wJk6uBtcEPS", "lgp-_ZwGx_nQhtR", "GANSW704411427"],
     ["lga94484cf6", "94484cf6e0e2", "GANSW12", "abc94484cf6e0e2x"]),
    (validate_au_anzsic_division_name, ["Agriculture, Forestry and Fishing", "ELECTRICITY, GAS, WATER AND WASTE SERVICES",
                                        "Transport, Postal & Warehousing", "Agriculture, Forestry And Fishing", "Other Services"],
     ["A", "Agriculture", "Business Services", "Admin and Support Services", "Vacant Space"]),
    (validate_au_vba_taxon_id, ["10705", "501234", "10705.0"], ["0", "A10705", "1234567", ""]),
    (validate_au_dca_code, ["132 Vehicles in same lane/ right rear", "110", "171 Left off carriageway into object"],
     ["250", "13", "Cross traffic", ""]),
    (validate_au_state_name, ["New South Wales", "Victoria", "Other Territories", "TASMANIA"], ["NSW", "Australia", "Sydney", ""]),
    (validate_pipe_material, ["Ductile Iron Concrete Lined", "Vitreous Clay", "Poly Vinyl Chloride (PVC)", "Asbestos or Fibro Cement",
                              "Copper Pipe", "RCP", "DICL", "uPVC", "Brick"],
     ["Unknown", "Fair", "375", "Stormwater", "UNK", "Permeable"]),
    (validate_tree_useful_life_expectancy, ["31-60 years", "61+ years", "6-10 years (>50% canopy)", "<1 year", "20+ years",
                                            "10 - 20 years", "< 5 years"],
     ["35", "Mature", "2019", ""]),
    (validate_tree_age_class, ["Semi-Mature", "Mature", "Over-mature", "Juvenile", "New", "Young", "Senescent"],
     ["35", "Good", "Developer Maintained", "Adult", ""]),
    (validate_electric_power, ["80W", "150 W", "350 kW", "50 - 350 kW", "6.6 kW", "1.5 MW"], ["350 kWh", "80", "kW", "50 kVA"]),
    (validate_iso8601_repeating_interval, ["R/2015-01-02/P2W", "R5/2008-03-01T13:00:00Z/P1Y2M10DT2H30M", "R/P1Y", "R12/P1M/2024-12-31"],
     ["P2W", "R/2015-01-02", "R/P", "R"]),
    (validate_crash_severity, ["Fatal", "Serious", "Minor", "First Aid", "Property Damage Only", "Serious Injury", "Not known"],
     ["Daylight", "Sealed", "3", ""]),
    (validate_taxon_name, ["ANIMALIA", "CHORDATA", "MOLOSSIDAE", "Myrtaceae"], ["SMITH", "MAMMAL", "BIRD", "Sm1th"]),
    (validate_class_or_order_name, ["CHIROPTERA", "MAMMALIA", "Passeriformes"], ["SMITH", "ECONOMY"]),
    (validate_card_number_text, ["4111 1111 1111 1111", "4111-XXXX-XXXX-1111", "************1111", "4111111111111111"],
     ["Yes", "No", "1234", ""]),
    (validate_twitter_at_handle, ["@LifelineAust", "@TheRMH"], ["LifelineAust", "https://twitter.com/ASSMStrata", "a@b.au"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


def test_fixed_false_labels():
    # ABS LGA codes (10500, 11250) of the NSW EPA bin survey are no GRID3 LGA codes of Nigeria.
    for value in ("10500", "11250", "13660"):
        assert not validate_ng_lga_code(value), value
    assert validate_ng_lga_code("19001")
    # Households alone (Total Population | Households of the Greater Geelong forecasts).
    assert not validate_za_economic_classification_value("Households")
    assert validate_za_economic_classification_value("Compensation of employees")


FIELDS = [
    ("au/au_council.yaml", "aucluesmallareabyname", ["clue_small_area", "CLUE small area", "clue_area", "small_area", "geography",
                                                     "featurenam"],
     ["clue_block", "area", "small_area_code"]),
    ("au/au_council.yaml", "aunswlotidbyname", ["lotidstring", "lot_id_string", "lot_dp", "lot/sec/dp"], ["lotnumber", "lot", "lot_size"]),
    ("au/au_council.yaml", "ausurveyplannumberbyname", ["planlabel", "plan_label", "Plan No", "DP Number", "deposited_plan"],
     ["plan", "planoid", "plannumber_text", "planning"]),
    ("au/au_council.yaml", "aunswlandzonebyname", ["sym_code", "zone_code", "Land Zone", "zoning", "LZN_CODE"],
     ["zone_number", "timezone", "zones"]),
    ("au/au_council.yaml", "auvicplanningzonebyname", ["zone_code", "ZONE_CODE", "planning_zone", "zone"], ["zone_number", "ozone"]),
    ("au/au_council.yaml", "auplanningapplicationnumberbyname", ["formatted_application_number", "DA Number", "permit_num",
                                                                 "council_ref", "town_planning_application", "dat_id", "application"],
     ["application_date", "permit_type", "description"]),
    ("au/au_council.yaml", "auparkingrestrictionbyname", ["restriction_display", "TypeDesc1", "Description1", "parking_limit",
                                                          "baytype", "BayType", "restriction_and_payment_display", "limitation"],
     ["description", "restriction_days_count", "parking_zone"]),
    ("au/au_council.yaml", "augeoscapepidbyname", ["LGA_PID", "lg_ply_pid", "ADDRESS_DETAIL_PID", "loc_pid", "pid"], ["pids", "rapid"]),
    ("au/au_council.yaml", "auanzsicdivisionnamebyname", ["industry_label", "a1_description", "anzsic_indusrty",
                                                          "industry_division_title", "ANZSIC Division Name"],
     ["clue_industry", "industry_description", "industry"]),
    ("au/au_council.yaml", "auvbataxonidbyname", ["victorian_biodiversity_atlas_code", "VBA_TAXON_ID", "vba_code", "vba"], ["taxon_id", "vbar"]),
    ("au/au_council.yaml", "audcacodebyname", ["dca", "DCA_CODE", "dca_description"], ["dcac", "academy"]),
    ("au/au_council.yaml", "austatenamebyname", ["state_name_2021", "STATE_NAME_2021", "official_name_state", "STE_NAME21",
                                                 "State/Territory"],
     ["state", "state_code_2021", "statement"]),
    ("au/au_geo.yaml", "aulganamecouncilbyname", ["lga_label", "council_name", "councilnam", "NSW_LGA__3", "nsw_lga_2",
                                                  "official_name_local_government_area", "long_official_name_local_government_area",
                                                  "local_government_area", "abb_name"],
     ["council", "lga", "councillors"]),
    ("au/au_geo.yaml", "aulgacodebarebyname", ["lga", "LGA", "lga_2021"], ["lga_name", "lga_code"]),
    ("au/au_geo.yaml", "aupostalareabyname", ["poa_code21", "POA_NAME21", "poa"], ["poac", "poa_area"]),
    ("au/au_geo.yaml", "aulocalitybyname", ["loc_name", "locality_name", "SAL_NAME21", "suburb_2"], ["location", "loc", "suburbs"]),
    ("au/au_transport.yaml", "auroadsigncodeshortbyname", ["scode", "svalue", "a_code"], ["code", "s_desc", "scode_desc"]),
    ("au/au_industry.yaml", "auanzsicbyname", ["anzsic4_code", "industry_anzsic4_code", "ANZSIC1_CODE", "industry_class_code",
                                               "industry_group_code"],
     ["industry_code", "industry"]),
    ("au/au_act.yaml", "auactsectionbyname", ["Section_Notified", "Section No.", "section_number"], ["sectionnumber"]),
    ("au/au_act.yaml", "auactblockbyname", ["Block_Current", "Block No.", "block_number"], ["blockno", "BLOCKNO"]),
    ("pii/au/au_pii.yaml", "auphonebyname", ["business_phone_number", "contact_ph", "Phone 2", "free_call", "telephone"],
     ["ph", "soil_ph", "phone_type"]),
    ("common/assets.yaml", "pipematerialbyname", ["pipe_material", "material", "mat_desc", "rehab_material"],
     ["bus_shelter_material", "art_material", "materials"]),
    ("common/assets.yaml", "treeusefullifeexpectancybyname", ["useful_life_expectency", "ule", "ULE", "life_expectancy", "sule"],
     ["useful", "rule", "schedule"]),
    ("common/assets.yaml", "treeageclassbyname", ["age_description", "age", "Age", "age_class", "maturity"], ["agency", "average", "page"]),
    ("common/assets.yaml", "electricpowerbyname", ["nominal_rating_watts", "wattage", "charger_capacities", "rated_power", "power_kw"],
     ["powerlines", "capacity", "power_dom"]),
    ("common/assets.yaml", "crashseveritybyname", ["severity", "CRASH_SEVERITY", "accident_severity"], ["severity_count", "crash_date"]),
    ("common/geo.yaml", "geopointcoordinatesbyname", ["co_ordinates", "coordinatelocation", "latlong_text", "geo", "centroid"],
     ["geography", "geom_type", "coordinate_system"]),
    ("common/geo.yaml", "streetbyname", ["str_name", "street_nam", "StreetFrom", "between_street_1", "onstreet", "road_name", "fromstreet"],
     ["street_no", "streets", "roadname_count"]),
    ("common/geo.yaml", "addressbyplacename", ["building_address", "venue_address", "development_address", "address_point", "address_pnt"],
     ["address", "address_type"]),
    ("common/geo.yaml", "compasspointbyname", ["sdirection", "aspect", "wind_direction"], ["sarrow_dir_count"]),
    ("common/science.yaml", "vernacularnamecommonnamebyname", ["common_name", "Common Name", "common_nam", "common_name_s"],
     ["common", "common_area"]),
    ("common/science.yaml", "speciesscientificbyname", ["scientific", "sci_name", "vegspecies", "tree_scientific_name"],
     ["scientist", "science"]),
    ("common/orgs.yaml", "tradingnamebyname", ["trading_name", "Trading name", "what_is_your_business_trading_name"], ["trading", "trade_name_count"]),
    ("common/useraccounts.yaml", "twitterusernamebyname", ["twitter", "Twitter", "twitter_handle", "X handle"], ["x", "tax", "twitters"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("au/au_council.yaml", "aunswlotidvalue", ["23/O/DP1417", "1//DP225807"], ["DP1417", "23/O"]),
    ("au/au_council.yaml", "auplanningapplicationnumbervalue", ["DA-404/2015", "TP-2014-43/A"], ["1501/2014/005613/2", "DA"]),
    ("au/au_council.yaml", "augeoscapepidvalue", ["lga94484cf6e0e2", "GANSW704411427"], ["lga94484cf6"]),
    ("common/assets.yaml", "electricpowervalue", ["80W", "350 kW"], ["350 kWh", "80"]),
    ("common/assets.yaml", "iso8601repeatingintervalvalue", ["R/2015-01-02/P2W", "R/P1Y"], ["P2W"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def test_name_rules_of_this_round_need_values():
    for path, rule_id, _, _ in FIELDS:
        spec = load(path, rule_id)
        if spec["match"] == "text":
            continue
        assert spec.get("validator") and spec.get("needs_values") is True, rule_id


def test_creditcard_names_need_card_numbers():
    # The off-street car parks of the City of Melbourne have a creditcard field of Yes and No.
    spec = load("pii/pii.yaml", "creditcardbyknown")
    assert spec["validator"].endswith("validate_card_number_text") and spec["needs_values"] is True
