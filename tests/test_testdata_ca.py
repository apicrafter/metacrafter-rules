"""Rules for the Canadian files of metacrafter-testdata (2024 snapshots of the Dateno catalogue: the Canadian
Watershed Information Network, canwinmap.ad.umanitoba.ca, cdi00000267, and the open data portals of the City
of Calgary, data.calgary.ca, cdi00000286, and the City of Edmonton, data.edmonton.ca, cdi00000289): Water
Survey of Canada station numbers and drainage area codes, DGUIDs and SGC codes of Statistics Canada, Dominion
Land Survey land descriptions, postal codes and forward sortation areas, municipal wards, and what a survey
platform records about a respondent and a session (device type, browser, operating system, housing tenure,
home language, mode of transport, education, age bands).

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.au.planning import validate_au_council_ward, validate_not_au_council_ward
from metacrafterext.rules.ca.geo import (
    validate_ca_dguid,
    validate_ca_dls_land_description,
    validate_ca_postcode,
    validate_ca_sgc_code,
    validate_ca_wsc_drainage_area_code,
    validate_ca_wsc_station_number,
)
from metacrafterext.rules.common.directories import validate_education_level
from metacrafterext.rules.common.fieldwork import validate_cardinal_direction, validate_compass_point
from metacrafterext.rules.common.respondents import (
    validate_device_type,
    validate_housing_tenure,
    validate_language_name,
    validate_municipal_ward,
    validate_operating_system,
    validate_transport_mode_word,
    validate_web_browser,
)
from metacrafterext.rules.common.survey import validate_age_band, validate_age_range_value
from tests.test_testdata_baseline import field_matches

VALIDATORS = [
    (validate_ca_wsc_station_number, ["05BH004", "08MF005", "05LJ021", "11AA001", "05bh013"],
     ["12AB001", "00AB001", "MB05LDS002", "05BH04", "5BH004", "501001", "11AAA00", ""]),
    (validate_ca_wsc_drainage_area_code, ["05", "5", "10", "11", "05L", "05LJ", "11A", "02Y"],
     ["12", "00", "501", "05L1", "50", "11AFA", "Nelson River", ""]),
    (validate_ca_dguid, ["2021A000011124", "2021A000248", "2021S051248112107", "2021A0011T3A", "2016S0503825", "2011S0503825"],
     ["4811", "2021X000248", "2021A0002", "1FTFW1ET5DFC10312", ""]),
    (validate_ca_sgc_code, ["48", "59", "4806", "4811", "4806016", "48.0", "10", "62"], ["73", "99", "480", "9906016", "48112107", "AB", ""]),
    (validate_ca_dls_land_description, ["NE-20-52-25-W4", "SE28 21 30 W1", "SE03 37 12 W2", "SW-33-12-8-E1", "20-52-25-W4", "nw-32-3-15-w1"],
     ["NE-40-52-25-W4", "20-52-25", "SE28", "Plan 6042KS Blk 2 Lot 5", "2021-05-12", "12-34-56-W9", ""]),
    (validate_ca_postcode, ["T2G 2M2", "T5H1E8", "t6a3j6", "K1A 0B1", "H2X-1Y4"], ["T5H", "D1A 1A1", "T2G 2M", "SW1A 1AA", "T6L***", "12345", ""]),
    (validate_device_type, ["Desktop", "Phone", "Tablet", "Mobile", "Smart TV", "Unknown"], ["iPhone 12", "Google Chrome", "Windows", "3", ""]),
    (validate_web_browser, ["Google Chrome", "Chrome", "Safari", "Firefox", "Internet Explorer", "Microsoft Edge", "Unknown"],
     ["Windows", "Desktop", "87.0", ""]),
    (validate_operating_system, ["Windows", "iOS", "Mac (OS X)", "macOS", "Android", "Linux", "Windows 10", "Unknown"],
     ["Google Chrome", "Desktop", "10", ""]),
    (validate_housing_tenure, ["Own", "Rent", "Owner", "Renter", "Owner-occupied", "Prefer not to answer"], ["Yes", "3", "Apartment", ""]),
    (validate_language_name, ["English", "French", "Panjabi (Punjabi)", "Tagalog (Pilipino, Filipino)", "Persian (Farsi)", "English Only",
                              "Other (Specify)", "Mandarin", "Cantonese"],
     ["Canadian", "Yes", "en", "270", "Calgary", ""]),
    (validate_transport_mode_word, ["Car/truck/Van as DRIVER", "Car/truck/van as PASSENGER", "Public Transit", "Walk", "Bicycle",
                                    "Car/Truck/Van (as Driver)", "Transit", "Taxi", "Motorcycle"],
     ["Yes", "3", "Monday", "Residential", "Only have one mode of transportation", ""]),
    (validate_municipal_ward, ["Ward 14", "WARD 7", "14", "05", "9.0", "Ward A", "papastew Ward", "Métis Ward", "North Ward", "EPSB Ward A",
                               "Anirniq", "O-day'min", "Nakota Isga", "73"],
     ["123", "0", "Calgary", "Ward", "Ward End", "CALGARY PARKS", ""]),
    # the Edmonton Insight Community surveys
    (validate_education_level, ["College / technical school graduate", "Post-graduate degree", "Post-graduate degree (e.g. Masters, PhD)",
                                "University undergraduate degree", "High school graduate", "Elementary/grade school graduate",
                                "Professional school graduate (e.g. medicine, law)", "Some university"],
     ["Prefer not to answer", "Yes", "38", ""]),
    (validate_age_band, ["35-39", '"35-39"', "35 - 39", "65+"], ["Did not answer", "35", '""', ""]),
    (validate_age_range_value, ['"30-34"', "30-34", "7"], ["Did not answer", ""]),
    # NB, SB, EB, WB of traffic counts are directions in words; N and NE stay compass points
    (validate_cardinal_direction, ["NB", "SB", "EB", "WB", "Northbound", "North"], ["N", "NE", "NSEW", "EW", "NB 2", ""]),
    (validate_compass_point, ["NE", "SW", "N"], ["NB", "NEAST", ""]),
    # a ward of any municipality is municipal_ward, not an ONS ward name
    (validate_not_au_council_ward, ["Abbey", "Castle", "Ward End", "St Helier"],
     ["North Ward", "Ward 2", "EPSB Ward A", "papastew Ward", "Anirniq", "Métis", "14"]),
    (validate_au_council_ward, ["North Ward", "Ward 2", "Division 3"], ["Camden", "Anirniq"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ + str(i) for i, v in enumerate(VALIDATORS)])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("ca/ca_codes.yaml", "cawscstationnumberbyname", ["Station Number", "STATION_NU", "STATION_ID", "station_no", "wsc_station", "hydat_id", "station"],
     ["STATION_NA", "Station Name", "STATION_TY", "Station Description", "station_lat"]),
    ("ca/ca_codes.yaml", "cawscdrainageareacodebyname", ["WSCMDA", "WSCSDA", "WSCSSDA", "WSCSSDA1", "WSCSDA_1", "FDA", "SUB_EC", "SUB_4C", "SUBBASIN_C",
                                                        "SUBSUBBASI", "drainage_area_code"],
     ["WSCMDANAME", "WSCSDA_EN", "SUBBASIN_P", "SUBBASIN_1", "SUB_PF", "MAJOR_BASI", "drainage_area"]),
    ("ca/ca_codes.yaml", "cadguidbyname", ["DGUID", "dguid", "IDUGD"], ["DGUIDP", "GUID", "DAUID"]),
    ("ca/ca_codes.yaml", "casgcbyname", ["PRUID", "CDUID", "CSDUID", "sgc_code", "SGC"], ["DAUID", "CCSUID", "CMAUID", "HYDROUID", "PRNAME"]),
    ("ca/ca_geo.yaml", "cafsabyname", ["FSA", "CFSAUID", "FORWARD SORTATION AREA", "postal code 3", "homefsa", "postal_fsa"],
     ["Postal Code", "DGUID", "fsa_count"]),
    ("common/survey.yaml", "devicetypebyname", ["DeviceType", "device_type", "device_category", "device", "user_device_class"],
     ["device_id", "DeviceName", "devices"]),
    ("common/survey.yaml", "webbrowserbyname", ["BrowserType", "browser", "browser_name", "user_browser"], ["BrowserVersion", "browser_id"]),
    ("common/survey.yaml", "operatingsystembyname", ["OSType", "os", "os_name", "operating_system", "Operating System"], ["os_version", "cost", "pos"]),
    ("common/survey.yaml", "housingtenurebyname", ["Q3_Own_Rent", "Own_Rent", "own_or_rent", "tenure", "housing_tenure", "tenure_type"],
     ["owner", "rent", "Rented", "tenure_years"]),
    ("en/en_common.yaml", "enlanguagenamebyname", ["language", "LANGUAGE", "Q11_Home_Language", "home_language", "mother_tongue", "Top_language",
                                                  "Top_2_language", "LANGUAGE1", "Language"],
     ["Top_2_language_num", "Top_language_per", "Total_language", "Official_languages_count", "language_code", "programming_language"]),
    ("en/en_common.yaml", "entransportmodebyname", ["Q14a_Primary_Transportation", "Q14b_Secondary_Transportation", "Mode of Transportation",
                                                   "MAIN_MODE_OF_TRANSPORTATION_FROM_HOME_TO_WORK", "travel_mode", "commute_mode", "transport_mode"],
     ["transportation_cost", "Transit", "mode", "Educational Services"]),
    ("common/admin_areas.yaml", "municipalwardbyname", ["ward", "WARD", "Ward", "WARD_NUM", "ward_name", "Civic Ward", "CIVIC_WARD", "wardname",
                                                       "WardNumber", "wards", "Ward Name"],
     ["STEWARD", "WARD_ID", "Ward Latitude", "Total Ward Stations", "GRANT_AWARD", "EDWARD TSE", "towards"]),
    ("common/directories.yaml", "educationlevelbyname", ["Q16_Education", "q5_education", "education_level"], ["Education", "Educational Services", "education_budget"]),
    ("pii/pii.yaml", "agerangebyname", ["Age_Rollup_Detailed", "age_rollup", "age_group", "AGE_RANGE"], ["age", "Rollup"]),
    ("common/geo.yaml", "compasspointbyname", ["QUADRANT", "Quadrant", "city_quadrant", "direction"], ["QUADRANT_CODE", "quadrant_area"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_names(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


def test_guarded_value_rules():
    """Station numbers fit the pattern of Armenian vehicle plates, a 17-character DGUID the format of a VIN and
    language names the nationality list: the value rules run only in fields named for them."""
    from tests.test_testdata_baseline import load
    for path, rule_id in (("ca/ca_codes.yaml", "cawscstationnumbervalue"), ("ca/ca_codes.yaml", "cadguidvalue"),
                          ("en/en_common.yaml", "enlanguagenamevalue")):
        assert load(path, rule_id)["fieldregex"], rule_id
    assert "provcd_1" in load("ca/ca_geo.yaml", "caprovincecodevalue")["fieldrule"].split(",")
