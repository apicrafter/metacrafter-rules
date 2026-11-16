"""Rules for the openAFRICA files of metacrafter-testdata (a May 2024 snapshot of open.africa, the
pan-African open data portal of Code for Africa, Dateno source cdi00000008): Kenyan counties and
sub-counties, Nigerian states, LGAs and the LGA and ward codes of GRID3, Sierra Leonean chiefdoms,
Tanzanian regions, South African provinces, budget vote numbers and economic classification items,
the GADM and OCHA division fields (HASC, NAME_1, Adm3_Name, TYPE_2), ODK geopoints, OurAirports
codes, Sensor.Community sensor models and value types, World Bank project and trust fund numbers;
and the fixes of the Australian LGA, UK parish and ward, IATA airline and FQDN rules on those files.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.au.codes import validate_au_lga_code, validate_au_lga_name_plain
from metacrafterext.rules.common.admin import (
    validate_admin_area_type,
    validate_continent_code,
    validate_hasc,
    validate_hdx_pcode,
    validate_ocd_division_id,
    validate_odk_geopoint,
)
from metacrafterext.rules.common.generic import (
    validate_airport_type,
    validate_gss_code,
    validate_iata_airport_code,
    validate_icao_airport_code,
)
from metacrafterext.rules.common.internet import is_fqdn
from metacrafterext.rules.common.sensors import validate_air_sensor_model, validate_sensor_community_value_type
from metacrafterext.rules.ke.geo import validate_ke_county, validate_ke_subcounty
from metacrafterext.rules.ng.geo import (
    validate_ng_lga,
    validate_ng_lga_code,
    validate_ng_state,
    validate_ng_state_code,
    validate_ng_ward_code,
)
from metacrafterext.rules.tz.geo import validate_tz_region
from metacrafterext.rules.za.finances import validate_za_economic_classification, validate_za_vote_number
from metacrafterext.rules.za.geo import validate_za_province
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (validate_ke_county,
     ["Mombasa", "Taita/Taveta", "Taita Taveta", "Tharaka-Nithi", "Tharaka Nithi", "Murang'a", "Muranga",
      "Nairobi City", "Nairobi", "Elgeyo Marakwet", "Homa Bay", "Kilifi County", "KILIFI"],
     ["Rift Valley", "Coast", "Kenya", "Rural", "1", "Kampala", "Kasese", ""]),
    (validate_ke_subcounty,
     ["Changamwe", "Jomvu", "Lungalunga", "Embakasi East", "Kirinyaga North/Mwea West", "Mvita Sub County",
      "Thika Town"],
     ["Abarilela", "Aber", "Abim", "Kasese", "12", ""]),
    (validate_ng_state,
     ["Kaduna", "Akwa Ibom", "Cross River", "Kano State", "FCT", "Federal Capital Territory", "Nassarawa",
      "Nasarawa", "Lagos"],
     ["Northern Nigeria", "KD", "TOTAL", "Kenya", "Kasese", ""]),
    (validate_ng_state_code, ["KD", "FC", "ak"], ["NG", "KDS", "XX", "1"]),
    (validate_ng_lga,
     ["Birnin Gwari", "Chikun", "Aba North", "Isiala-Ngwa South", "Isiala Ngwa North", "Ado-Odo/Ota",
      "Arochukw", "Ikeja LGA", "Abuja Municipal Area Council"],
     ["Kaduna State", "19001", "Gayam", "Mombasa", "Albury", ""]),
    (validate_ng_lga_code, ["19001", "19023", "01001", "37014"], ["38001", "00001", "19000", "1900", "KD0101"]),
    (validate_ng_ward_code, ["KD0101", "KD0201", "FC0110"], ["E05000026", "XX0101", "KD0001", "KD010"]),
    (validate_tz_region,
     ["Dodoma", "Dar es Salaam", "Coast", "Pwani", "Kaskazini Pemba", "Mtwara & Lindi", "Tabora Region"],
     ["Kongwa", "Zanzibar", "Uyui", "Kenya", ""]),
    (validate_za_province,
     ["KwaZulu-Natal", "MPUMALANGA", "North West", "Free State Province", "Northern Cape", "Kwa-Zulu Natal"],
     ["South Africa", "ZA-GP", "Pretoria", "Eastern", ""]),
    (validate_za_economic_classification,
     ["Compensation of employees", "Goods And Services", "Transfers and subsidies", "Current payments",
      "Consumables: Stationery, printing and office supplies", "Communication (G&S)", "GOODS AND SERVICES"],
     ["Administration", "Empty", "The Presidency", "0", ""]),
    (validate_za_vote_number, ["1", "14", "40", "10.0"], ["0", "60", "152061", "01", "Vote 1"]),
    (validate_hasc, ["TZ.AS.AS", "ZM.CE.CB", "FR.NC", "US.CA.LO"], ["tz.as.as", "www.ke", "TZ", "TZ.AS.ASA"]),
    (validate_hdx_pcode, ["SL0101", "SLE03040102", "GE11"], ["19001", "KD0101K", "sle0101"]),
    (validate_admin_area_type, ["Local Authority", "Wilaya", "District", "Water body", "Province"],
     ["Arusha", "1", ""]),
    (validate_ocd_division_id,
     ["ocd-division/country:ug/region:eastern/subregion:sebbei/district:kween/constituency:kween_county",
      "ocd-division/country:us/state:ca"],
     ["area/kawempe_division_north", "https://example.org/ocd-division/country:ug"]),
    (validate_odk_geopoint,
     ["11.48131371 5.19336324 461.20001220703125 5.0", "9.140918333333333 7.496761666666667 697.0 4.5",
      "5.1297 7.1592 73.3 5"],
     ["9.14, 7.49", "123629.78 379674.57", "95.1 7.1 0 5", "a b c d", "53 004 085 616", "22 24 90 90"]),
    (validate_continent_code, ["AF", "EU", "SA", "oc"], ["Africa", "AR", "A"]),
    (validate_air_sensor_model, ["SDS011", "pms5003", "DHT22", "BME280", "BAM 1020", "SPH0645_MIC", "MQ-7"],
     ["P2", "DHT", "Nairobi", ""]),
    (validate_sensor_community_value_type, ["P1", "P2", "P0", "temperature", "humidity", "noise_Leq", "durP1"],
     ["PM2.5", "P3", "Temperature", ""]),
    (validate_iata_airport_code, ["JMY", "FNA"], ["EB", "GFLL", "jmy"]),
    (validate_icao_airport_code, ["GFLL", "EDDF"], ["PLM", "SL-0001", "gfll"]),
    (validate_airport_type, ["small_airport", "medium_airport", "heliport"], ["closed", "airport"]),
    (validate_au_lga_code, ["10050", "24600", "19399", "89399", "19499"], ["19001", "19002", "357", "01005"]),
    (validate_au_lga_name_plain, ["Albury (C)", "Gympie", "Norwood Payneham St Peters"],
     ["Birnin Gwari", "Chikun", "Giwa", "10050"]),
    (validate_gss_code, ["E05000026", "E04000001"], ["KD0101", "Busunga", "Railway ward"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


def test_fqdn_refuses_hasc_codes():
    assert not is_fqdn("TZ.AS.AS") and not is_fqdn("ZM.CE.CB")
    assert is_fqdn("www.statistics.go.tz") and is_fqdn("open.africa")


FIELDS = [
    ("ke/ke_geo.yaml", "kecountybyname", ["County", "county_name", "County Name", "NAME_1", "Adm1_Name"],
     ["Sub county", "county_code", "Countyid", "Country"]),
    ("ke/ke_geo.yaml", "kesubcountybyname", ["Sub county", "subCounty", "sub_county", "Sub-County"],
     ["County", "subcounty_code"]),
    ("ng/ng_geo.yaml", "ngstatebyname", ["State", "state_name", "Location by state", "NAME_1", "statename"],
     ["State Code", "statecode", "state_id", "estate"]),
    ("ng/ng_geo.yaml", "ngstatecodebyname", ["State Code", "statecode", "state_abbr"], ["State", "state_name"]),
    ("ng/ng_geo.yaml", "nglgabyname", ["Lga", "lga_name", "LGA Name", "Local Government Area", "NAME_2", "lganame"],
     ["Lga Code", "lgacode", "unique_lga_id"]),
    ("ng/ng_geo.yaml", "nglgacodebyname", ["Lga Code", "lgacode", "lga_id"], ["Lga", "lga_name"]),
    ("ng/ng_geo.yaml", "ngwardcodebyname", ["Ward Code", "wardcode", "ward_id"], ["Ward", "ward_name"]),
    ("sl/sl_geo.yaml", "slchiefdombyname", ["CHIEFDOM", "chiefdom_name", "Chiefdom"], ["SECTION", "district"]),
    ("tz/tz_geo.yaml", "tzregionbyname", ["Region", "region_name", "NAME_1", "Mkoa"], ["Regional", "region_code"]),
    ("za/za_geo.yaml", "zaprovincebyname", ["Province", "province_name", "Government", "prov"],
     ["Provincial", "province_code"]),
    ("za/za_finances.yaml", "zaeconomicclassificationbyname",
     ["EconomicClassification3", "Econ2", "econClass_L4", "economic_classification_1", "IYM_econLowestLevel"],
     ["Economic", "econ", "EconomicSector"]),
    ("za/za_finances.yaml", "zabudgetvotenumberbyname", ["VoteNumber", "vote_number", "Vote No#", "VoteNo", "voteno"],
     ["Votes", "TOTAL VOTES", "VALD VOTES", "vote"]),
    ("common/admin_areas.yaml", "hascbyname", ["HASC_2", "HASC_1", "hasc", "hasc_code"], ["hash", "HASC_2_name"]),
    ("common/admin_areas.yaml", "adminarea1gadmbyname", ["NAME_1", "ADM1_EN", "Adm1_Name", "admin1Name_en"],
     ["NAME_12", "NAME_0", "NL_NAME_1"]),
    ("common/admin_areas.yaml", "adminarea2gadmbyname", ["NAME_2", "ADM2_EN", "Adm2_Name", "ADM2_NAM_1"],
     ["NAME_23", "VARNAME_2"]),
    ("common/admin_areas.yaml", "adminarea3gadmbyname", ["NAME_3", "Adm3_Name", "ADM3_NAM_1"], ["Adm4_Name"]),
    ("common/admin_areas.yaml", "adminareatypebyname", ["TYPE_2", "ENGTYPE_2", "admin_type", "administrative_unit_type"],
     ["type", "TYPE", "facility_type"]),
    ("common/admin_areas.yaml", "continentcodebyname", ["continent", "continent_code", "continentcode"],
     ["continent_name", "continents"]),
    ("common/environment.yaml", "airsensormodelbyname", ["sensor_type", "sensor_model", "sensortype"],
     ["sensor_id", "type"]),
    ("common/environment.yaml", "sensorcommunityvaluetypebyname", ["value_type", "valuetype"], ["value", "type"]),
    ("common/geo_text.yaml", "iso3166subdivisionbyname", ["iso_region", "iso_3166_2", "iso_id"], ["region"]),
    ("common/transport.yaml", "icaoairportcodebycode", ["gps_code", "ident", "icao_code"], ["iata_code", "code"]),
    ("common/transport.yaml", "iataairportcodebycode", ["iata_code", "IATA"], ["icao_code", "airline_code"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


def test_new_field_rules_need_values():
    for path, rule_id, _, _ in FIELDS:
        spec = load(path, rule_id)
        assert spec.get("validator") and spec.get("needs_values") is True, rule_id


VALUES = [
    ("ke/ke_geo.yaml", "kecountyvalue", ["Mombasa", "Taita/Taveta"], ["Rift Valley", "Kenya"]),
    ("ng/ng_geo.yaml", "ngstatevalue", ["Kaduna", "Federal Capital Territory"], ["Northern Nigeria"]),
    ("ng/ng_geo.yaml", "nglgavalue", ["Birnin Gwari", "Aba North"], ["Gayam", "19001"]),
    ("tz/tz_geo.yaml", "tzregionvalue", ["Dodoma", "Pwani", "Coast Region"], ["Kongwa", "Coast"]),
    ("za/za_geo.yaml", "zaprovincevalue", ["KwaZulu-Natal", "MPUMALANGA"], ["South Africa"]),
    ("za/za_finances.yaml", "zaeconomicclassificationvalue", ["Compensation of employees"], ["Administration"]),
    ("common/admin_areas.yaml", "hascvalue", ["TZ.AS.AS"], ["tz.as.as"]),
    ("common/admin_areas.yaml", "ocddivisionidvalue", ["ocd-division/country:ug/district:kween"], ["area/kween"]),
    ("common/admin_areas.yaml", "odkgeopointvalue", ["9.140918 7.496761 697.0 4.5"], ["9.14 7.49"]),
    ("common/environment.yaml", "airsensormodelvalue", ["SDS011", "DHT22"], ["P2"]),
    ("common/transport.yaml", "airporttypevalue", ["medium_airport", "heliport"], ["closed", "airport"]),
    ("common/development_finance.yaml", "wbprojectidvalue", ["P099939"], ["P09993", "TF053509"]),
    ("common/development_finance.yaml", "wbtrustfundnumbervalue", ["TF053509", "TF093541"], ["P099939", "TF5350"]),
    ("common/geo.yaml", "hdxpcodevalue", ["SLE03040102", "SL0101"], ["19001"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def test_place_value_rules_skip_town_fields():
    """The value rules of county, state, LGA and region names are guarded against fields of towns
    and lower divisions, which repeat the names of the larger division."""
    import re

    for path, rule_id in (("ke/ke_geo.yaml", "kecountyvalue"), ("ng/ng_geo.yaml", "ngstatevalue"),
                          ("ng/ng_geo.yaml", "nglgavalue"), ("tz/tz_geo.yaml", "tzregionvalue")):
        guard = re.compile(load(path, rule_id)["fieldregex"], re.IGNORECASE)
        assert guard.search("name") and guard.search("Region") and guard.search("NAME_1"), rule_id
        for name in ("city", "osm:addr:city", "town", "village", "community"):
            assert not guard.search(name), (rule_id, name)


def test_uk_parish_and_ward_codes_need_gss_codes():
    for path, rule_id in (("gb/gb_geo.yaml", "ukparishcodefield"), ("gb/gb_geo.yaml", "ukwardcodebyknown")):
        spec = load(path, rule_id)
        assert spec["validator"].endswith("validate_gss_code") and spec["needs_values"] is True


def test_iata_code_is_no_longer_an_airline_code_by_name_alone():
    names = {k.strip() for k in load("common/transport.yaml", "iataairlinecodefield")["rule"].split(",")}
    assert "iata_code" not in names
    names = {k.strip() for k in load("common/transport.yaml", "icaoairlinecodefield")["rule"].split(",")}
    assert "icao_code" not in names


def test_timestamp_name_needs_unix_seconds():
    from metacrafterext.rules.common.dateandtime import validate_unixtime_seconds

    spec = load("common/dateandtime.yaml", "timestampknown")
    assert spec["validator"].endswith("validate_unixtime_seconds")
    for value in ("1471181882", "1471181882.5", "915148800"):
        assert validate_unixtime_seconds(value), value
    for value in ("2021-12-01T00:01:53.614385+00:00", "1793960864568", "31/07/2023 15:36:17", ""):
        assert not validate_unixtime_seconds(value), value
