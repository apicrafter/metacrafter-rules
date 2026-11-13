"""Rules from the second metacrafter-testdata baseline (#60, #61, #62, #63).

Matched as tests/test_testdata_baseline.py matches them. A field rule's ``validator`` checks the
values of the field (metacrafter keeps the name match when at least half of them pass).
"""
import importlib

import pytest

from metacrafterext.rules.common.generic import (
    has_legal_form,
    validate_bic_value,
    validate_content_license,
    validate_ev_connectors,
    validate_name_text,
    validate_date_value,
    validate_not_bare_year,
    validate_place_name,
    validate_software_license_text,
    validate_vehicle_number_text,
)
from metacrafterext.rules.common.identifiers import (
    validate_gr_gemi,
    validate_hu_giro,
    validate_isrc,
    validate_se_orgnr,
    validate_us_dea,
)
from metacrafterext.rules.common.software import validate_semver
from tests.test_testdata_baseline import field_matches, guarded_by, load, value_matches


def validator_accepts(path, rule_id, value):
    module, name = load(path, rule_id)["validator"].rsplit(".", 1)
    return bool(getattr(importlib.import_module(module), name)(value))


# --- #62 and #63: rules for the datatypes of registry #161 and #163-#168 -----------------
# rule file, rule id, key, values (registry examples, test data), refused values, a field name
# of the guard (None: no guard).
NEW_TYPES = [
    # #161 / #62
    ("us/us_orgs.yaml", "usnteecodevalue", "us_ntee_code", ["B71Z", "J40", "D200"], ["71Z", "B7"], "NTEE_CD"),
    ("common/orgs.yaml", "gleifracodevalue", "gleif_ra_code", ["RA000554", "RA999999"], ["RA00554", "XA000554"], None),
    ("ru/ru_finances.yaml", "rucbrregnumvalue", "ru_cbr_regnum", ["3116", "3553-К", "3349/76", "1/4"], ["12345"], "@RegN"),
    ("common/legal.yaml", "contentlicensevalue", "content_license",
     ["cc-by", "cc-by-nc-nd", "CC_BY_4_0", "CC0-1.0", "http://creativecommons.org/publicdomain/zero/1.0/legalcode"],
     ["MIT", "other-oa", "https://openalex.org/licenses/cc-by"], None),
    ("common/geo.yaml", "gadmgidvalue", "gadm_gid", ["VNM.25_1", "VNM.25.13_1", "VNM.25.13.2_1"], ["VNM", "VNM.25"], None),
    ("common/science.yaml", "dwctaxonomicstatusvalue", "dwc_taxonomic_status",
     ["ACCEPTED", "SYNONYM", "heterotypicSynonym"], ["VALID", "REORGANIZED"], "taxonomicStatus"),
    ("common/science.yaml", "dwctaxonrankvalue", "dwc_taxon_rank", ["SPECIES", "GENUS", "subspecies"], ["ACCEPTED"],
     "taxonRank"),
    # #163
    ("gr/gr_common.yaml", "grschoolcodevalue", "gr_school_code", ["9000714", "903010"], ["1000714", "90007140"],
     "school_code"),
    ("nz/nz_orgs.yaml", "nzcompanynumbervalue", "nz_company_number", ["50166612", "213565"], ["N/A", "-"],
     "CompaniesOfficeNumber"),
    ("eu/eu_funding.yaml", "eupicvalue", "eu_pic", ["999997930", "990797674"], ["99999793"], "organisationID"),
    ("eu/eu_funding.yaml", "eugrantagreementvalue", "eu_grant_agreement_number", ["101069506", "101045989", "283595"],
     ["12345", "201069506"], "projectID"),
    ("tr/tr_gov.yaml", "trikinvalue", "tr_ikn", ["2026/1947326", "2026/25"], ["1947326"], "Ihaleno"),
    ("ro/ro_common.yaml", "rolmicodevalue", "ro_lmi_code", ["IS-II-m-A-03957.01", "B-II-m-B-18332", "AG-IV-m-B-13976"],
     ["IS-V-m-A-03957", "IS-II-x-A-03957"], None),
    ("lt/lt_common.yaml", "ltkvrcodevalue", "lt_kvr_code", ["29912", "9583"], ["2991200"], "unikalus_kodas"),
    ("cz/cz_common.yaml", "czlibraryregnumvalue", "cz_library_registration_number", ["5539", "2187"], ["55390"],
     "EVIDENČNÍ_ČÍSLO_KNIHOVNY"),
    # #164
    ("hu/hu_common.yaml", "hugirocodevalue", "hu_giro_code", ["10002003", "10023002", "10032000"], ["10002004"],
     "Branch office code"),
    ("ua/ua_finances.yaml", "uamfovalue", "ua_mfo", ["300119", "300335"], ["400119"], "GLMFO"),
    ("in/in_finances.yaml", "inmicrvalue", "in_micr", ["395437002", "384437002"], ["39543700"], "MICR"),
    # #165
    ("ro/ro_common.yaml", "rosiiircodevalue", "ro_siiir_code", ["0161102892", "0361106988"], ["161102892"],
     "Cod SIIIR unitate"),
    ("ro/ro_common.yaml", "rosiruescodevalue", "ro_sirues_code", ["306167", "1180302"], ["30616"], "Cod SIRUES"),
    ("rs/rs_education.yaml", "rsjispidvalue", "rs_jisp_id", ["3950", "795"], ["395000"], "JISP ID"),
    ("fi/fi_education.yaml", "fioppilaitosnumerovalue", "fi_oppilaitosnumero", ["08888", "03117"], ["3117"], "tunn"),
    ("za/za_education.yaml", "zaemisnumbervalue", "za_emis_number", ["700400412", "700310045"], ["70040041"],
     "EMIS NUMBER"),
    ("id/id_education.yaml", "idnpsnvalue", "id_npsn", ["20502415"], ["2050241"], "NPSN"),
    ("ke/ke_medical.yaml", "kemflcodevalue", "ke_mfl_code", ["25720", "25699"], ["2572"], "MFL_CODE"),
    ("hu/hu_common.yaml", "huneakcodevalue", "hu_neak_code", ["U912", "R730", "1122"], ["U91"], "NEAK kód"),
    ("vn/vn_medical.yaml", "vnkcbcodevalue", "vn_kcb_code", ["31107", "31030"], ["3110"], "Mã cơ sở KCB (cũ)"),
    ("id/id_medical.yaml", "idpuskesmascodevalue", "id_puskesmas_code", ["P5201010101"], ["5201010101"], "KODE_PUSKE"),
    # #166
    ("bg/bg_geo.yaml", "bgoblastcodevalue", "bg_nsi_oblast_code", ["VTR", "SFO"], ["VTR13"], "oblast"),
    ("bg/bg_geo.yaml", "bgobshtinacodevalue", "bg_nsi_obshtina_code", ["GAB05", "VTR13"], ["VTR"], "obshtina"),
    ("bg/bg_geo.yaml", "bgkmetstvocodevalue", "bg_nsi_kmetstvo_code", ["GAB05-00", "PER51-00"], ["GAB05"], "kmetstvo"),
    ("hu/hu_common.yaml", "hujarascodevalue", "hu_jaras_code", ["085 0", "164 0"], ["0850"], "Járás kódja"),
    ("ee/ee_geo.yaml", "eeehakvalue", "ee_ehak", ["0353", "0037"], ["353"], "OKOOD"),
    ("se/se_geo.yaml", "selanskodvalue", "se_lanskod", ["01", "06", "14", "25"], ["02", "11", "26"], "länskod"),
    ("lt/lt_common.yaml", "ltmunicipalityvalue", "lt_municipality_code", ["13", "19"], ["130"], "SAV_KODAS"),
    ("eu/eu_geo.yaml", "eulaucodevalue", "eu_lau_code", ["RO_1017", "RO_1213"], ["RO1017"], "LAU"),
    ("common/geo.yaml", "hdxpcodevalue", "hdx_pcode", ["GE11", "GE44"], ["GEO", "GE-11"], "adm1_pcode"),
    ("cz/cz_geo.yaml", "czruianaddresspointvalue", "cz_ruian_address_point", ["17242606", "3333833"], ["1724260611"],
     "AdresniBod"),
    ("lv/lv_common.yaml", "lvvaraddresscodevalue", "lv_var_address_code", ["105617436", "101456850"], ["205617436"],
     "addressRegisterCode"),
    ("ee/ee_geo.yaml", "eeadsadridvalue", "ee_ads_adr_id", ["121731", "120275"], ["ADR121731"], "ADR_ID"),
    # #167
    ("kz/kz_industry.yaml", "kzkpvedvalue", "kz_kpved", ["A", "01", "011112"], ["01.11", "1"], "КПВЭД"),
    ("lt/lt_common.yaml", "ltevrkvalue", "lt_evrk", ["949900", "410010"], ["94.99"], "evrk_subclass_code"),
    ("se/se_industry.yaml", "sessykvalue", "se_ssyk", ["2221", "2227"], ["22210"], "SSYK"),
    ("common/transport.yaml", "evconnectortypevalue", "ev_connector_type",
     ["Typ 2;CCS2;CHAdeMO", "CCS2;;", "TYP 2;TYP 2;", "CCS2;ChadeMO;Typ 2"], ["230 V", ";;"], "standard_konektoru"),
    # #168
    ("common/transport.yaml", "erarinfopidvalue", "era_rinf_op_id", ["HR71402", "DE000BL"], ["71402", "hr-71402"], "UOPID"),
    ("common/dateandtime.yaml", "excelserialdatevalue", "excel_serial_date", ["36872", "42367"], ["2015", "62367"], "date"),
    ("th/th_datetime.yaml", "thyearbevalue", "year_th_be", ["2561", "2563"], ["2018"], "ปี"),
    ("ar/ar_datetime.yaml", "armonthvalue", "ar_month", ["مارس", "يوليوز", "دجنبر", "كانون الثاني"], ["رمضان"], None),
    ("se/se_culture.yaml", "selibrisidvalue", "libris_id", ["http://libris.kb.se/bib/tcltrxl5r1tz1ltx"],
     ["https://libris.kb.se/", "http://libris.kb.se/bib/"], None),
    # #60: Canadian province codes
    ("ca/ca_geo.yaml", "caprovincecodevalue", "caprovincecode", ["ON", "BC", "QC"], ["XX", "Ontario"], "Province"),
]


@pytest.mark.parametrize("path,rule_id,key,good,bad,guard", NEW_TYPES, ids=[t[1] for t in NEW_TYPES])
def test_rules_for_new_types(path, rule_id, key, good, bad, guard):
    spec = load(path, rule_id)
    assert spec["key"] == key and spec["type"] == "data"
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value
    if guard is None:
        assert "fieldrule" not in spec
    else:
        assert guarded_by(path, rule_id, guard), guard
        assert not guarded_by(path, rule_id, "name"), "guard too broad"


# Field rules with a value check: rule file, rule id, key, names, other names, values that fit,
# values that do not.
FIELD_RULES = [
    ("gr/gr_common.yaml", "grgemibyfield", "gr_gemi", ["Αριθμός Γ.Ε.ΜΗ.", "GEMI", "αριθμός γεμη"],
     ["Gemischtwaren", "Αριθμός"], ["124956721000", "51772519000", "51772519000.0"], ["ΕΙΡΗΝΟΔΙΚΕΙΟ ΑΘΗΝΩΝ", "1234"]),
    ("common/geo.yaml", "adminarea3byfield", "admin_area_3", ["kecamatan", "thathmblnm", "ตำบล"], ["kabupaten"],
     ["Gamping", "ในเมือง"], ["101"]),
    ("common/generic.yaml", "provincebyfield", "province", ["province", "Province", "provincia", "PROVINCE_NAME"],
     ["province_code", "cod_provincia"], ["Kénitra", "ON", "MI"], ["13", "https://example.org/p/1"]),
    ("common/crossborder_finance.yaml", "bicfield", "bic", ["BIC", "BIC code", "BIC kód (SWIFT)", "SWBICS.@SWBIC", "swift"],
     ["bicycle", "basic"], ["DEUTDEFF", "MKKBHUHB"], ["STIMMBEZIRK", "12345678"]),
]


@pytest.mark.parametrize("path,rule_id,key,names,others,fit,unfit", FIELD_RULES, ids=[t[1] for t in FIELD_RULES])
def test_field_rules_with_value_checks(path, rule_id, key, names, others, fit, unfit):
    assert load(path, rule_id)["key"] == key
    for name in names:
        assert field_matches(path, rule_id, name), name
    for name in others:
        assert not field_matches(path, rule_id, name), name
    for value in fit:
        assert validator_accepts(path, rule_id, value), value
    for value in unfit:
        assert not validator_accepts(path, rule_id, value), value


# --- #60: field-name rules on parts of names and values that contradict them -----------
@pytest.mark.parametrize("rule_id,names", [
    ("categorybyfield", ["external_ids.type.grid.all", "external_ids.type.fundref.preferred", "links.type.website",
                         "links.type.wikipedia"]),
    ("orgnamebyfield", ["primary_location.source.host_organization.id", "Nosaukums"]),
    ("citybyfield", ["address.city.code"]),
])
def test_names_hold_the_keyword_in_their_last_part(rule_id, names):
    for name in names:
        assert not field_matches("common/generic.yaml", rule_id, name), name


@pytest.mark.parametrize("rule_id,names", [
    ("categorybyfield", ["Expense Type", "company_status", "attributes.entity.category", "properties.tipologia"]),
    ("orgnamebyfield", ["primary_location.source.host_organization", "Razon Social", "properties.BETREIBER"]),
    ("citybyfield", ["address.city", "municipality", "properties.Gemeinde"]),
])
def test_last_part_still_matches(rule_id, names):
    for name in names:
        assert field_matches("common/generic.yaml", rule_id, name), name


def test_name_checks_of_generic_rules():
    for path, rule_id in (("common/generic.yaml", "orgnamebyfield"), ("common/generic.yaml", "citybyfield"),
                          ("common/geo.yaml", "cityknown")):
        assert not validator_accepts(path, rule_id, "5")  # IRS organization code, Kirkanta city id
        assert not validator_accepts(path, rule_id, "https://openalex.org/P4310320990")
    assert validate_name_text("Pilskalns") and validate_name_text("SIA Latvijas Gāze")
    assert not validate_place_name("Gia Dinh Park, Hoang Minh Giam Steet, Hauh Thong Commute, Ho Chi Minh City")
    assert validate_place_name("BENONI") and validate_place_name("Washington, D.C.") and not validate_place_name("ON")


def test_province_is_not_an_indian_state_and_suburb_not_a_city():
    assert not field_matches("in/in_geo.yaml", "instateknown", "Province")
    assert field_matches("in/in_geo.yaml", "instateknown", "STATE")
    assert not field_matches("au/au_geo.yaml", "aucityknown", "SUBURB")


def test_nosaukums_is_a_name():
    assert load("lv/lv_common.yaml", "lvnamebyfield")["key"] == "name"
    assert field_matches("lv/lv_common.yaml", "lvnamebyfield", "Nosaukums")


def test_registration_number_is_not_a_license_number():
    assert not field_matches("common/legal.yaml", "licensenumberknown", "Registration_number")
    assert field_matches("common/legal.yaml", "licensenumberknown", "license_number")


def test_isbn_field_is_isbn():
    assert not field_matches("common/objects.yaml", "isbn10field", "isbn")
    assert field_matches("common/media.yaml", "isbnfield" if "isbnfield" in _rules("common/media.yaml") else
                         next(k for k, r in _rules("common/media.yaml").items() if r["key"] == "isbn" and r["type"] == "field"),
                         "isbn")
    assert not validator_accepts("common/objects.yaml", "isbn10field", "9789113140360")
    assert validator_accepts("common/objects.yaml", "isbn10field", "0306406152")


def _rules(path):
    import pathlib

    import yaml
    root = pathlib.Path(__file__).resolve().parent.parent / "rules"
    return yaml.safe_load((root / path).read_text(encoding="utf-8"))["rules"]


def test_dates_by_name_are_not_years():
    assert not validate_not_bare_year("2024") and not validate_not_bare_year("[2024]")
    assert validate_not_bare_year("2024-05-01") and validate_not_bare_year("36872")
    # validate_date_value (#69) also rejects bare years, and other numbers of up to four digits
    assert load("common/dateandtime.yaml", "dateknown")["validator"].endswith("validate_date_value")
    assert not validate_date_value("2024") and not validate_date_value("[2024]") and validate_date_value("36872")


def test_licenses_of_works_are_no_software_licenses_or_plates():
    cc = "http://creativecommons.org/publicdomain/zero/1.0/legalcode"
    assert validate_content_license(cc) and validate_content_license("cc-by-nc-nd")
    assert not validate_software_license_text(cc) and not validate_software_license_text("cc-by")
    assert validate_software_license_text("MIT") and validate_software_license_text("Apache-2.0")
    assert not validate_vehicle_number_text(cc) and not validate_vehicle_number_text("cc-by")
    assert validate_vehicle_number_text("AB 123 C")
    assert load("common/software.yaml", "licensebyknown")["validator"].endswith("validate_software_license_text")
    assert load("common/vehicles.yaml", "vehiclenumberbyfieldname")["validator"].endswith("validate_vehicle_number_text")


# --- #61: value rules that labelled other codes -------------------------------------------
def test_gleif_registration_authority_is_not_a_nino():
    assert not value_matches("gb/gb_persons.yaml", "enniivalue", "RA000554")
    assert value_matches("gb/gb_persons.yaml", "enniivalue", "AB123456C")


def test_status_words_are_not_bics():
    for word in ("ACCEPTED", "DECISION", "REORGANIZED"):
        assert not value_matches("common/crossborder_finance.yaml", "bicvalue", word), word
    assert validate_bic_value("NWBKGB2L") and validate_bic_value("DEUTDEFFXXX") and not validate_bic_value("DEUTDEFF")


def test_isins_are_not_isrcs():
    assert not validate_isrc("DE0006201106") and not validate_isrc("BE0003790079")
    assert validate_isrc("USRC17607839") and validate_isrc("UKAAA0500001")


def test_instrument_names_have_no_legal_form():
    assert not has_legal_form("Veritas Pharma Inc. Registered Shares o.N.")
    assert not has_legal_form("Nemetschek SE Inhaber-Aktien o.N.")
    assert not has_legal_form("Vigo System Ord Shs")
    assert has_legal_form("Tomra Systems ASA") and has_legal_form("ACT Health Pty Ltd")


def test_estonian_procurement_ids_are_not_swedish_org_numbers():
    assert not validate_se_orgnr("314983-0000")
    assert validate_se_orgnr("556016-0680") and validate_se_orgnr("202100-5489")
    assert not validate_se_orgnr("850101-1234")  # a personal identity number (third digit 0)
    assert load("se/se_finances.yaml", "seorgnumbervalue")["validator"].endswith("validate_se_orgnr")


def test_contract_numbers_are_not_dea_numbers_or_passports():
    assert not validate_us_dea("EC2017481") and validate_us_dea("AB1234563")
    for path, rule_id in (("us/us_persons.yaml", "us_persons_usdeanumbervalue"), ("pii/us/us_pii.yaml", "usdeanumbervalue")):
        assert not value_matches(path, rule_id, "EC2017481")
    for path, rule_id in (("pl/pl_persons.yaml", "pl_persons_plpassportvalue"), ("pii/pl/pl_pii.yaml", "plpassportvalue")):
        assert guarded_by(path, rule_id, "numer paszportu") and not guarded_by(path, rule_id, "contract_number")


def test_country_packs_need_their_own_names():
    assert not guarded_by("gb/gb_geo.yaml", "ukwardnamebyknown", "Ward")
    assert guarded_by("gb/gb_geo.yaml", "ukwardnamebyknown", "WD23NM")
    assert not guarded_by("ru/ru_geo.yaml", "ruregioncode", "region_code")
    assert not guarded_by("ru/ru_geo.yaml", "ruregioncode", "region")
    assert guarded_by("ru/ru_geo.yaml", "ruregioncode", "kod_regiona")
    assert not guarded_by("tr/tr_finances.yaml", "trtaxnumbervalue", "Apgrutinajuma_kods")
    assert guarded_by("tr/tr_finances.yaml", "trtaxnumbervalue", "vergi_no")
    assert not guarded_by("ca/ca_orgs.yaml", "caextraProvvalue", "object_zipcode")
    assert guarded_by("ca/ca_orgs.yaml", "caextraProvvalue", "extra_provincial_registration_number")


def test_open_ended_validity_date_is_not_a_version():
    assert not validate_semver("31.12.9999") and validate_semver("1.2.3")


def test_ev_connector_lists():
    assert validate_ev_connectors("Typ 2;CCS2;CHAdeMO") and not validate_ev_connectors("Typ 2;230 V")


def test_new_validators_of_identifiers():
    assert validate_hu_giro("10002003") and not validate_hu_giro("1000200")
    assert validate_gr_gemi("028223912000") and not validate_gr_gemi("12495672")
