"""Rules for the data.gov.uk files of metacrafter-testdata: ONS geography codes, NHS ODS codes,
Ordnance Survey grid references, postcode districts and sectors, NaPTAN and NPTG codes, energy
certificates, planning application references, Ofsted URNs, civil service grades, cattle breed
codes, VOA codes, UK VAT and Companies House numbers, MCC and OECD CRS purpose codes; and the
guards that stop Thai passport, ICD-10 and OpenAlex rules on those codes.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.common.identifiers import (
    validate_crs_purpose_code,
    validate_iati_org_ref,
    validate_mcc,
)
from metacrafterext.rules.gb.codes import (
    validate_cattle_breed_code,
    validate_ccg_ods_code,
    validate_civil_service_grade,
    validate_companies_house_number,
    validate_epc_rating,
    validate_gb_postcode_district,
    validate_gb_postcode_sector,
    validate_gb_vat,
    validate_naptan_code,
    validate_nhs_ods_code,
    validate_nptg_locality_code,
    validate_os_grid_reference,
    validate_os_grid_reference_spaced,
    validate_planning_application_ref,
    validate_voa_description_code,
)
from tests.test_testdata_baseline import field_matches, guarded_by, load, value_matches

VALIDATORS = [
    (validate_os_grid_reference, ["SD 97624 17311", "TQ 873 846", "TL97441340", "SE1735221689", "NU 123 399", "SU48760530"],
     ["SD 9762 173", "XY 123 456", "TI 123 456", "TQ", "OC387148", "TL9744134"]),
    (validate_os_grid_reference_spaced, ["SD 97624 17311", "TQ 873 846"], ["TL97441340", "SC068179", "SC086146"]),
    (validate_gb_postcode_district, ["LS13", "NW1", "WC1H", "N6", "LS8 "], ["LS13 5", "LS13 5LP", "1234", "ABC1"]),
    (validate_gb_postcode_sector, ["LS27 9", "WF3 1", "LS15 8"], ["LS27", "LS27 9AB", "LS279"]),
    (validate_ccg_ods_code, ["02T", "99A", "13T"], ["E38000025", "QWO", "RXF", "2T"]),
    (validate_nhs_ods_code, ["QWO", "QF7", "Y55", "02T", "A81001", "RXF"], ["E54000054", "qwo", "AB", "A810011"]),
    (validate_nptg_locality_code, ["E0029368", "N0075002", "ES001234"], ["T1036257", "E002936", "1800WKH4032"]),
    (validate_naptan_code, ["MANJMGMW", "nwmjwpgm", "4501234A"], ["1800WKH4032", "12345678", "MAN"]),
    (validate_epc_rating, ["A", "A+", "D", "g"], ["H", "112", "AB"]),
    (validate_planning_application_ref, ["14/01103/FUL", "2019/1602/P", "17/00003/CLOPUD"], ["14/01103", "15/09/00002", "12/04/2017"]),
    (validate_civil_service_grade, ["G7", "HEO", "SCS1A", "G7 National", "HEO (UKHO B2)", "Grade 6", "SCS Pay Band 2", "AA/AO"],
     ["A", "B", "MHI", "Q1", "G8"]),
    (validate_cattle_breed_code, ["AA", "AAX", "BAZ X", "BABX", "ALL"], ["A", "AA1", "ABERDEEN ANGUS"]),
    (validate_voa_description_code, ["CO", "CS", "CP1", "IF3", "CS10"], ["C", "CS100", "W027A"]),
    (validate_gb_vat, ["673598875", "GB 446 0099 53", "744 3643 29", "GB654935407", "GB123456789001"], ["Omitted", "7914524215", "12345"]),
    (validate_companies_house_number, ["04832101", "4832101", "OC387148", "SC086146", "10703888"], ["-", "12345", "123456", "XX123456"]),
    (validate_mcc, ["5411", "0742", "7399"], ["541", "54111", "abcd"]),
    (validate_crs_purpose_code, ["41030", "31210", "31110"], ["410", "99999", "10000"]),
    (validate_iati_org_ref, ["GB-7", "GB-GOV-1", "XM-DAC-41114"], ["DEFRA", "GB7", "gb-7"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


GSS = [
    ("gb/gb_geo.yaml", "ukoutputareacodevalue", ["E00054810", "W00000001"], ["E01010876"]),
    ("gb/gb_geo.yaml", "gbregioncodevalue", ["E12000001"], ["E92000001"]),
    ("gb/gb_geo.yaml", "ukcountrygsscodevalue", ["E92000001", "N92000002", "K02000001"], ["E12000001", "K05000001"]),
    ("gb/gb_geo.yaml", "gbcountycodevalue", ["E10000008", "E11000001"], ["E06000001"]),
    ("gb/gb_geo.yaml", "gbcombinedauthoritycodevalue", ["E47000001"], ["E07000026"]),
    ("gb/gb_geo.yaml", "ukeuropeanelectoralregioncodevalue", ["E15000001", "W08000001", "S15000001", "N07000001"], ["E12000001"]),
    ("gb/gb_geo.yaml", "gbcensusmergedwardcodevalue", ["E36000001", "W39000001"], ["E05008942"]),
    ("gb/gb_geo.yaml", "gbcensusmergedladcodevalue", ["E41000001", "W40000001"], ["E06000001"]),
    ("gb/gb_geo.yaml", "gbbuacodevalue", ["E34000201", "W37000001", "K05000001"], ["E35000742"]),
    ("gb/gb_geo.yaml", "gbbuasdcodevalue", ["E35000742", "W38000154", "K06000002"], ["E34000201"]),
    ("gb/gb_geo.yaml", "gbcountyelectoraldivisioncodevalue", ["E58000301"], ["E05001371"]),
    ("gb/gb_geo.yaml", "gbcommunitysafetypartnershipcodevalue", ["E22000001", "W14000001"], ["E23000001"]),
    ("gb/gb_geo.yaml", "gbnideacodevalue", ["N10000101"], ["N09000004"]),
    ("gb/gb_geo.yaml", "gbscotlanddatazonecodevalue", ["S01006556"], ["S02001236"]),
    ("gb/gb_med.yaml", "gbccgcodevalue", ["E38000025"], ["E54000054"]),
    ("gb/gb_med.yaml", "gbstpcodevalue", ["E54000054"], ["E38000025"]),
    ("gb/gb_med.yaml", "gbcanceralliancecodevalue", ["E56000030", "E57000001"], ["E54000054"]),
    ("gb/gb_realestate.yaml", "gbepcrrnvalue", ["0991-0918-6260-8900-9092"], ["0991-0918-6260-8900", "09910918626089009092"]),
    ("gb/gb_realestate.yaml", "gbplanningapplicationrefvalue", ["14/01103/FUL", "2019/1602/P"], ["15/09/00002"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", GSS, ids=[g[1] for g in GSS])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


FIELDS = [
    ("gb/gb_geo.yaml", "ukgsscodebyonsfield", ["CAUTH19CD", "eer18cd", "cmwd11cd", "CTYUA16CD", "CSP19CD"], ["CCG20CDH", "ctyua16cdo", "code"]),
    ("gb/gb_geo.yaml", "gbpostcodedistrictfield", ["Postcode District", "postcode_district", "outward code"], ["Postcode", "PostCodeSector"]),
    ("gb/gb_geo.yaml", "gbpostcodesectorfield", ["PostCodeSector", "postcode sector"], ["Postcode", "Postcode District"]),
    ("gb/gb_geo.yaml", "gbcountynamebyonsfield", ["CTY19NM", "cty16nmw"], ["CTY19CD", "County"]),
    ("gb/gb_geo.yaml", "gbgeoxlongitudefield", ["GeoX", "geo_x"], ["X", "GeoY"]),
    ("gb/gb_med.yaml", "gbccgodscodefield", ["CCG20CDH", "ccg18cdh", "CCG ODS code"], ["CCG20CD", "CCG20NM"]),
    ("gb/gb_med.yaml", "gbnhsodscodefield", ["STP20CDH", "NHSER18CDH", "ODS code", "Trust Code", "Practice Code"], ["STP20CD", "ORG_NAME"]),
    ("gb/gb_transport.yaml", "gbnaptancodefield", ["NaptanCode", "naptan_code"], ["AtcoCode"]),
    ("gb/gb_realestate.yaml", "gbepcratingfield", ["ENERGY_RATING_BAND", "CURRENT_ENERGY_RATING", "potential_energy_rating", "Display Energy Certificates rating"],
     ["ENERGY_RATING", "TOTAL_CO2_EMISSIONS"]),
    ("gb/gb_realestate.yaml", "gbvoadescriptioncodefield", ["VOA Code", "voa_code"], ["VOA description", "Description code"]),
    ("gb/gb_orgs.yaml", "gbcompanieshousenumberfield", ["Company Registration Number", "Supplierregisteredcompanynumber", "company number", "CRN"],
     ["Company Name", "Supplier ID"]),
    ("gb/gb_finances.yaml", "gbvatfield", ["VAT Registration Number", "Vat Registration Num", "VAT Reg No", "vat_number"], ["Irrecoverable VAT", "VAT amount"]),
    ("gb/gb_agriculture.yaml", "gbcattlebreedcodefield", ["Breed Code", "DAM BREED CODE", "breed_code"], ["Breed Description", "DAM BREED"]),
    ("gb/gb_agriculture.yaml", "animalbreedfield", ["Breed Description", "DAM BREED", "breed"], ["Breed Code", "DAM BREED CODE", "Breed Type"]),
    ("common/crossborder_finance.yaml", "mccfield", ["MCC", "merchant category code", "mcc_code"], ["MCC Description", "Merchant Category"]),
    ("common/intcodes.yaml", "oecdcrspurposecodefield", ["Sector code", "CRS purpose code", "dac sector code"], ["Sector", "Sector name"]),
    ("common/intcodes.yaml", "iatiorganisationreffield", ["IATI Identifer", "IATI identifier", "reporting-org ref"], ["IATI activity", "Identifier"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


def test_dun_and_bradstreet_field_names():
    assert field_matches("common/orgs.yaml", "dunsfield", "D-U-N-S Number")


def _regex_guard(path, rule_id, name):
    import re

    spec = load(path, rule_id)
    return bool(re.search(spec["fieldregex"], name)) or name.lower() in {
        k.strip().lower() for k in spec.get("fieldrule", "").split(",")}


GUARDS = [
    ("gb/gb_geo.yaml", "gbosgridreferencefieldvalue", ["GridReference", "NGR", "Grid_ref", "os grid reference"], ["URN", "Company Number", "Reference"]),
    ("gb/gb_education.yaml", "gbofstedurnvalue", ["URN", "Provider URN", "ofsted_urn"], ["Company Number", "Registration"]),
    ("gb/gb_transport.yaml", "gbnptglocalitycodevalue", ["NptgLocalityCode", "nptg_locality_code"], ["Job Number", "Passport"]),
    ("gb/gb_orgs.yaml", "gbcivilservicegradevalue", ["Grade", "Grade (or equivalent)", "Civil Service Grade"], ["Upgrade date", "Quality grade of meat"]),
    ("pii/th/th_pii.yaml", "thpassportvalue", ["passport_no", "Thai passport"], ["NptgLocalityCode", "Job Number"]),
    ("th/th_persons.yaml", "th_persons_thpassportvalue", ["หนังสือเดินทาง"], ["NptgLocalityCode"]),
    ("en/en_med.yaml", "enicd10value", ["icd10", "ICD-10 code", "diagnosis", "cause_of_death"], ["Default aid type", "NoticeTypeCode", "Camera ID", "Agencies"]),
    ("de/de_med.yaml", "deicd10value", ["Diagnose", "ICD"], ["Default aid type"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", GUARDS, ids=[g[1] for g in GUARDS])
def test_field_guards(path, rule_id, good, bad):
    for name in good:
        assert _regex_guard(path, rule_id, name), name
    for name in bad:
        assert not _regex_guard(path, rule_id, name), name


def test_openalex_needs_six_digits():
    assert value_matches("common/science.yaml", "openalexidbyvalue", "W2741809807")
    assert value_matches("common/science.yaml", "openalexidbyvalue", "I136199984")
    assert not value_matches("common/science.yaml", "openalexidbyvalue", "A81001")


def test_gp_practice_code_needs_an_organisation_code_field():
    assert value_matches("gb/gb_med.yaml", "gbgppracticecodevalue", "A81001")
    assert guarded_by("gb/gb_med.yaml", "gbgppracticecodevalue", "ORG_CODE")
    assert not guarded_by("gb/gb_med.yaml", "gbgppracticecodevalue", "Supplier ID")
