"""Rules for the ACT files of metacrafter-testdata (a 2024 snapshot of www.data.act.gov.au, the Socrata open
data portal of the Australian Capital Territory Government): ACT districts, sections and blocks, incorporated
association numbers and Tenders ACT RFx numbers; ABS SA1, SA3, State Suburb and 2006 Collection District codes;
RTO and VET qualification codes; AS 1742 traffic sign codes; political parties, conservation status in words;
GTFS Realtime vehicle stop status, congestion level and schedule relationship, trip ids and bearings of the
Canberra light rail archives; Socrata location columns, and the fixes of names and false labels found there.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.au.act import (
    validate_au_act_association_number,
    validate_au_act_block,
    validate_au_act_district,
    validate_au_act_rfx_number,
    validate_au_act_rfx_number_new,
    validate_au_act_section,
    validate_au_census_cd_code,
    validate_au_road_sign_code,
    validate_au_rto_code,
    validate_au_sa1_code,
    validate_au_sa3_code,
    validate_au_ssc_code,
    validate_au_vet_qualification_code,
)
from metacrafterext.rules.common.generic import validate_latlon_pair
from metacrafterext.rules.common.identifiers import validate_hs_code_digits
from metacrafterext.rules.common.observations import validate_bearing
from metacrafterext.rules.common.politics import validate_political_party
from metacrafterext.rules.common.software import validate_semver
from metacrafterext.rules.common.taxa import validate_conservation_status
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (validate_au_act_district, ["Canberra Central", "Woden Valley", "Paddys River", "Paddy's River", "MOLONGLO VALLEY", "TUGG", "BELC"],
     ["North Canberra", "Phillip", "Fyshwick", "Queanbeyan", "tugg", "1.5", ""]),
    (validate_au_act_section, ["21", "124", "0", "1234", "21.0"], ["21A", "12345", "1/2", "-", ""]),
    (validate_au_act_block, ["2", "1333", "14+15+16+17+18", "3, 4"], ["B12", "12345", "-", ""]),
    (validate_au_act_association_number, ["A00336", "A01685", "a06159"], ["A0336", "00336", "AB00336", "CO-0201"]),
    (validate_au_act_rfx_number, ["50019-RFT-006", "30874-RFQ-110", "81492-REOI-001", "31050-RFT-210-01", "GGS456-RFT-003",
                                  "31106.110", "2014.22462.300", "2018.29133.110.011", "2017.29059.110 LRS2", "GS001025.110",
                                  "SL170497", "ACT31092.110", "VC.2019.100", "2016-LRS02-001", "L170250"],
     ["12345", "2.5", "RFT-006", "50019-ABC-006", "Hello", "01/02/2019", ""]),
    (validate_au_act_rfx_number_new, ["50019-RFT-006", "81492-REOI-001", "GGS456-RFT-003", "JACS437-REOI-001"],
     ["31106.110", "GS001025.110", "50019-RFT-6", "RFT-006"]),
    (validate_au_sa1_code, ["80105105102", "11001100101", "8105102", "80105105102.0"], ["801051051", "00105105102", "123456789012"]),
    (validate_au_sa3_code, ["80101", "80103", "'80101'"], ["801", "801051051", "08010", "8010"]),
    (validate_au_ssc_code, ["81051", "81421", "SAL10001", "ssc80014"], ["2601", "810510", "SAL1000"]),
    (validate_au_census_cd_code, ["8013604", "8014903", "1010101"], ["0013604", "801360", "80136040"]),
    (validate_au_rto_code, ["0101", "90821", "'91664'", "'6187'", '"0101"'], ["101", "1234567", "RTO1", ""]),
    (validate_au_vet_qualification_code, ["BSB50120", "AUR30212", "SIT20207", "10964NAT", "BSB50120-BBI", "chc33015"],
     ["BSB5012", "ABC90123", "BSB501201", "Certificate III", ""]),
    (validate_au_road_sign_code, ["R1-1", "W3-1", "G9-21", "R4-1(60)", "R2-3(L)", "R5-41/4", "R7-1-4", "G9-15MOD1", "DS13-12/2", "H1",
                                  "D4-1-2", "W8-2(55)"],
     ["A1-1", "1-1", "STOP", "R", "R1-1-1-1", ""]),
    (validate_political_party, ["Australian Labor Party", "Liberal Party", "Canberra Liberals", "The Greens", "Community Alliance",
                                "Australian Motorist Party", "Independent", "Ungrouped"],
     ["JSC Pty Ltd", "W.R Electrical Pty Ltd", "John Smith", "12345", "Coombs Dam", ""]),
    (validate_conservation_status, ["Critically Endangered", "Vulnerable", "Endangered", "Regionally Conservation Dependent",
                                    "Least concern", "Extinct in the Wild"],
     ["VU", "CR", "Bird", "Current", "Expired", ""]),
    (validate_bearing, ["126.8724594116211", "0", "270", "360", "45°"], ["NE", "361", "-5", "north", ""]),
    (validate_latlon_pair, ["(-35.318906, 149.132104)", "(-35.2761, 149.12948)", "-35.341635,149.051601", "[46.51, 6.63]"],
     ["POINT (149.13 -35.31)", "(1, 2, 3)", "(-95.1, 149.1)", "Calwell Shops - Webber Street"]),
    (validate_hs_code_digits, ["01", "0101", "01.01", "010121", "0101.21", "8471300000", "847130.0"],
     ["Free_1_hr", "SS06_2P", "Free", "1"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


def test_procurement_file_numbers_are_no_semver():
    # The ACT contracts register and Tenders ACT number files with the year and a five-digit serial.
    for value in ("2014.24010.110", "2018.29133.110", "2014.22462.300"):
        assert not validate_semver(value), value
    for value in ("1.2.3", "2024.1.0", "10.15.7"):
        assert validate_semver(value), value


FIELDS = [
    ("au/au_act.yaml", "auactdistrictbyname", ["District", "District_Notified", "District_Current", "ACT District", "dist",
                                               "district_name"],
     ["districts", "distance", "district_code", "Division_Notified"]),
    ("au/au_act.yaml", "auactsectionbyname", ["Section_Notified", "Section_Current", "Section No.", "section_number", "SECTION NO"],
     ["Section", "SECTION", "section_arts", "Notified Under Section", "ID_SECTION"]),
    ("au/au_act.yaml", "auactblockbyname", ["Block_Notified", "Block_Current", "Block No.", "block_number", "BLOCK NO"],
     ["block", "Block", "Address Block", "blocks"]),
    ("au/au_act.yaml", "auactassociationnumberbyname", ["A_Number", "Association Number", "assoc_no", "Incorporation Number"],
     ["number", "Phone Number", "associations"]),
    ("au/au_act.yaml", "auactrfxnumberbyname", ["RFx No", "Rfx Number", "RFT No", "RFQ Number", "rfx_id", "Tender Number", "tender_ref"],
     ["RFx Title", "RFx Closing Date", "rfx", "tender"]),
    ("au/au_geo.yaml", "ausa1codebyname", ["SA1", "sa1_main16", "SA1_7DIGITCODE_2011", "SA1 code", "SA1_CODE21", "sa1_maincode_2016"],
     ["sa1_name", "SA12", "sa2_code"]),
    ("au/au_geo.yaml", "ausa3codebyname", ["SA3 Code", "sa3_code16", "SA3_CODE_2021", "sa3_code"], ["SA3 Name", "sa3", "sa2_code"]),
    ("au/au_geo.yaml", "ausscccodebyname", ["State Suburb Code", "SSC_CODE16", "SAL_CODE_2021", "ssc", "ssc_code"],
     ["suburb", "sal", "salary_code"]),
    ("au/au_geo.yaml", "aucensuscdcodebyname", ["CD", "CD_CODE", "cd_2006", "Collection District", "census_cd"], ["cds", "cd_name", "acd"]),
    ("au/au_geo.yaml", "ausuburbbyname", ["Suburb", "SUBURB_LOCATION", "suburb_name"], ["suburbs_count"]),
    ("au/au_education.yaml", "aurtocodebyname", ["RTO Code", "RTO", "rto_id", "Training Organisation Code",
                                                 "Registered Training Organisation Code"],
     ["Registered Training Organisation Trading Name", "rto_name", "proto"]),
    ("au/au_education.yaml", "auvetqualificationcodebyname", ["Qual Code", "Qualification Code", "Course Code", "National Code", "qual_id"],
     ["Qualification Name", "qualification", "course"]),
    ("au/au_transport.yaml", "auroadsigncodebyname", ["SIGN CODE", "Sign_Code", "Sign Type Code", "sign_no", "Sign Number"],
     ["SIGN TYPE", "SIGN TEXT", "sign", "signature_code"]),
    ("au/au_finances.yaml", "auabnacnbyname", ["ABN", "ABN:", "Supplier ABN", "AFS_LIC_ABN_ACN"], ["ABN Name", "abnormal"]),
    ("au/au_industry.yaml", "auanzsicbyname", ["ANZSIC Subdivision Code", "anzsic_code", "primary_anzsic_class_code", "ANZSIC Division Name"],
     ["industry", "anzsco_code"]),
    ("common/transport.yaml", "gtfstripidbyfield", ["tripID", "trip.trip_id", "trip_update.trip.trip_id"],
     ["trip_id", "TRIP_ID", "trip", "trip_headsign", "trips"]),
    ("common/transport.yaml", "gtfsstopidbyfield", ["stop_id", "stopID", "parent_station"], ["stop", "stop_name"]),
    ("common/transport.yaml", "gtfsrtvehiclestopstatusbyfield", ["current_status", "currentStatus"], ["status", "currentstate"]),
    ("common/transport.yaml", "gtfsrtcongestionlevelbyfield", ["congestion_level", "congestionLevel"], ["congestion", "level"]),
    ("common/transport.yaml", "gtfsrtschedulerelationshipbyfield", ["schedule_relationship", "tripScheduleRelationship",
                                                                    "tripUpdateSchedulerelationship", "stop_time_update_schedule_relationship"],
     ["schedule", "relationship", "scheduled"]),
    ("common/transport.yaml", "bearingbyname", ["bearing", "Bearing", "heading", "vehicle_bearing", "heading_deg", "direction_degrees"],
     ["bearings", "header", "direction", "course"]),
    ("common/geo.yaml", "geopointsocratalocationbyname", ["Location", "Location 1", "Location_1", "location_3", "GPS", "Long/Lat",
                                                          "lat/long", "Camera Location"],
     ["Location Description", "locations", "LOCATION_CODE", "Location Name"]),
    ("common/geo.yaml", "suburbbyname", ["Suburb", "SUBURB_LOCATION", "Street Suburb"], ["suburban", "suburb_code"]),
    ("common/common.yaml", "colourbyfield", ["colour", "color", "fill_colou", "stroke_col", "text_color", "route_color", "fill_color"],
     ["colours_count", "column", "stroke"]),
    ("common/science.yaml", "conservationstatusbyname", ["status", "sourceStatus", "conservation_status", "EPBC status", "IUCN category",
                                                         "threatened_status", "listing"],
     ["statuses", "status_date", "conservation"]),
    ("common/politics.yaml", "politicalpartybyname", ["Party", "Party/Group", "Party/ Group", "party_name", "political_party", "PartyName"],
     ["Party 1 surname", "partly", "third_party_id"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("au/au_act.yaml", "auactrfxnumbervalue", ["50019-RFT-006", "81492-REOI-001", "GGS456-RFT-003", "31050-RFT-210-01"],
     ["31106.110", "GS001025.110", "RFT-006"]),
    ("au/au_education.yaml", "auvetqualificationcodevalue", ["BSB50120", "AUR30212", "10964NAT"], ["BSB5012", "ABCD1234"]),
    ("common/transport.yaml", "gtfsrtvehiclestopstatusvalue", ["STOPPED_AT", "IN_TRANSIT_TO", "INCOMING_AT"], ["STOPPED", "AT"]),
    ("common/transport.yaml", "gtfsrtcongestionlevelvalue", ["RUNNING_SMOOTHLY", "STOP_AND_GO", "SEVERE_CONGESTION"],
     ["CONGESTION", "SMOOTH"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def test_name_rules_of_codes_need_values():
    for path, rule_id, _, _ in FIELDS:
        spec = load(path, rule_id)
        if spec["match"] == "text":
            continue
        if rule_id == "gtfsrtschedulerelationshipbyfield":
            continue
        assert spec.get("validator") and spec.get("needs_values") is True, rule_id


def test_hs_code_names_need_digits():
    # The smart parking lots of the ACT have a TariffCode of Free_1_hr and SS06_2P.
    spec = load("common/trade.yaml", "hscodebyfield")
    assert spec["validator"].endswith("validate_hs_code_digits") and spec["needs_values"] is True
    assert field_matches("common/trade.yaml", "hscodebyfield", "TariffCode")
    assert not validate_hs_code_digits("Free_1_hr")
