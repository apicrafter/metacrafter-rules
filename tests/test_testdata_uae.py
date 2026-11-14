"""Rules for the files of the UAE Open Data portal (opendata.fcsc.gov.ae, Federal Competitiveness and
Statistics Centre) in metacrafter-testdata (an April 2024 snapshot): emirates and the regions of Abu
Dhabi in English and Arabic, Dubai community numbers and names, DEWA contract accounts, country names
in Arabic, P.O. Boxes, and the generic rules the snapshot showed gaps or false positives in (CAS
numbers, ICD-10 ranges with titles, coordinates as text, eight-digit dates, quarters, serial numbers,
revisions and sizes).

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.ae.geo import (
    COMMUNITY_CODES,
    validate_ae_abu_dhabi_region,
    validate_ae_city,
    validate_ae_dewa_contract_account,
    validate_ae_dubai_community,
    validate_ae_dubai_community_code,
    validate_ae_emirate,
    validate_ae_po_box,
)
from metacrafterext.rules.ar.countries import COUNTRY_NAMES, fold_arabic, validate_ar_country_name
from metacrafterext.rules.common.chemistry import validate_casrn
from metacrafterext.rules.common.generic import (
    validate_compact_date,
    validate_geopoint_text,
    validate_icd10_with_label,
    validate_quarter_value,
)
from metacrafterext.rules.common.software import validate_commit_hash, validate_datasize_value
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (validate_ae_emirate,
     ["Abu Dhabi", "Abu  Dhabi", "Dubai", "Sharjah", "Ajman", "Umm Al - Quwain", "Umm Al Qaiwain", "Umm-Alquwain",
      "U.A.Q.", "UMQ", "Ras Al-Khaimah", "R.A.K.", "RAS AL KHAIMA", "Fujairah", "Fujeira", "Sharjah1",
      "Emirate of Sharjah", "أبوظبي", "أبو ظبي", "إبوظبي", "أبو ظــــــبي", "دبى", "الشارقـة", "أم القيوين",
      "ام القيوين", "رأس الخيمة", "راس الخيمه", "الفجيرة", "إمارة دبي"],
     ["Al Ain", "Western Region", "Al Dhafra", "UAE", "Total", "الجملة", "العين", "Dubai Airport", "Jeddah", ""]),
    (validate_ae_abu_dhabi_region,
     ["Abu Dhabi", "Al Ain", "Al Dhafra", "Western Region", "Al Dhafra Region", "Al Gharbia", "أبوظبي",
      "العين", "الظفرة", "المنطقة الغربية", "الغربیـــه"],
     ["Dubai", "Sharjah", "Al Khatim", "Abu-Kariah", "Central", "دبي", "الختم", ""]),
    (validate_ae_dubai_community_code, ["123", "312", "621", "101", "991", "124.0"],
     ["-1", "100", "999", "1234", "12", "AREA 313", ""]),
    (validate_ae_dubai_community,
     ["AL MUTEENA", "Al Muteena", "AL DAGHAYA", "Al Dhagaya", "AL KHABAISI", "AL SOUQ AL KABEER",
      "Muhaisnah Fourth", "MUHAISANAH FOURTH", "Al Barsha 2", "Al Qusais", "Oud Metha", "Al Ras", "NAIF",
      "HOR AL ANZ EAST", "المطينة", "منخول", "المنخول", "القوز الأولى", "ند حصة"],
     ["Dubai", "Abu Dhabi", "Sharjah", "Deira", "Rose", "Main", "London", "Paris", "123", ""]),
    (validate_ae_dewa_contract_account, ["2002323313", "2025340770", "3002431058", "2002323313.0"],
     ["2002323314", "1002323313", "200232331", "20023233130", "4002323313", ""]),
    (validate_ae_po_box, ["2623", "234140", "1", "PO Box 16080", "ص.ب 123"], ["0", "1234567", "P.O. Box", "NIL", ""]),
    (validate_ae_city, ["Dubai", "Abu Dhabi", "Al Ain", "AlAin", "Khor Fakkan", "Khoor Fakan", "خورفكان", "الشارقة"],
     ["Doha", "Ad Dammam", "London", ""]),
    (validate_ar_country_name,
     ["المملكة العربية السعودية", "السعودية", "جمهورية  إيران الإسلامية", "جمهوريّة إيران الإسلاميّة",
      "المملكة المتحدة لبريطانيا العظمى وايرلندا الشمالية", "بريطانيا", "الولايات المتحدة", "أمريكا",
      "بنجلاديش", "بنغلاديش", "أنجولا", "اثيوبيا", "أسبانيا", "سلطنة عمان", "قطر", "الهند", "سورية",
      "جمهورية مصرالعربية", "الإمارات العربية المتحدة"],
     ["أخرى", "الجملة", "مواطن", "غير مواطن", "دول مجلس التعاون", "دبي", "India", "Saudi Arabia", ""]),
    (validate_casrn, ["534-52-1", "608-73-1", "7732-18-5", "50-00-0", "68359–37–5"],
     ["534-52-2", "2019-05-1", "12-34-5", "……………", "and others", "62476-59-9 [50594-66-6]"]),
    (validate_icd10_with_label,
     ["C18-C21 Colorectal", "C23, C24 Gallbladder, other and unspecified", "C50 Breast",
      "C00-C14 Lip, Oral cavity & pharynx", "C91-C95 Leukemia", "C50"],
     ["Total", "All sites", "Colorectal", "18-21"]),
    (validate_geopoint_text,
     ["24.4539° N, 54.3773° E", "25.276987,55.296249", "25°17'29.7\"N 55°30'01.6\"E", "33.86° S, 151.21° E"],
     ["Dubai", "24.4539", "124.4539° N, 54.3773° E", "25°17'N 55.5° E"]),
    (validate_compact_date, ["20171119", "20170704", "19991231"], ["20171301", "20170230", "2017111", "12345678"]),
    (validate_quarter_value, ["Q1", "q4", "3", "Q1-2015", "2015 Q2", "First Quarter", "الربع الأول"],
     ["Q5", "0", "5", "2015", "January"]),
    (validate_datasize_value, ["2048", "5.2 GB", "12 MB"], ["MAJOR", "MINOR", "General", "Local"]),
    (validate_commit_hash, ["a1b2c3d", "9fceb02d0ae598e95dc970b74767f19372d61af8"], ["Revision 1", "R4"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


def test_lists():
    # 226 communities of the Dubai Statistics Center bulletin of 2021; the 83 codes of the RTA
    # parking zone list are among them.
    assert len(COMMUNITY_CODES) == 226
    assert {"111", "123", "312", "621", "991"} <= COMMUNITY_CODES
    assert len(COUNTRY_NAMES) > 500
    assert fold_arabic("أبو ظــبي") == "ابو ظبي"
    assert fold_arabic("جمهوريّة  مصر") == "جمهوريه مصر"


FIELDS = [
    ("ae/ae_geo.yaml", "aeemiratebyname",
     ["Emirate", "emirate_en", "Emirate_AR", "Emirates En", "emirates_ ar", "Emirates _EN", "emirate_name",
      "EmirateTitleEn", "childEmiratesAr", "emirate ar", "Emirates-EN", "emirate.1", "الإمارة", "الامارة"],
     ["EmirateCode", "emirate_code", "emirates_id", "region", "city"]),
    ("ae/ae_geo.yaml", "aeabudhabiregionbyname", ["Region", "Region_EN", "Region_AR", "regions", "المنطقة"],
     ["region_of_embarkation", "regional_office", "area"]),
    ("ae/ae_geo.yaml", "aedubaicommunitycodebyname", ["community", "community_num", "community_number", "comm_no"],
     ["community_name_en", "communities_served"]),
    ("ae/ae_geo.yaml", "aedubaicommunitybyname", ["community", "community_name_en", "community_name_ar", "Community Name"],
     ["community_num", "community_id"]),
    ("ae/ae_geo.yaml", "aepoboxbyname", ["p_o_box", "pobox", "PO Box", "P.O. Box", "po_box_no", "صندوق البريد"],
     ["box", "postbox", "postcode", "postOfficeBox", "addresses.postOfficeBox"]),
    ("ae/ae_finances.yaml", "aedewacontractaccountbyname",
     ["contract_account", "Contract Account", "contract_account_number", "contractaccount"],
     ["account", "business_partner", "contract_type"]),
    ("ar/ar_geo.yaml", "arcountrynamebyname",
     ["Country(Arabic)", "Country (Arabic)", "Country_AR", "country_name_ar", "country - arabic", "اسم الدولة"],
     ["Country(English)", "Country_EN", "country", "countryside_ar"]),
    ("common/chemistry.yaml", "casrnbyfieldname", ["CAS No.", "cas_no", "CAS Number", "CASRN", "cas", "CAS RN"],
     ["cases", "Cases (number)", "casual", "case_no"]),
    ("common/geo.yaml", "geopointtextbyname", ["Coordinates", "coordinates", "coords", "latlng", "Lat_Long", "الإحداثيات"],
     ["coordinator", "lat", "longitude"]),
    ("common/geo.yaml", "latitudebyshortname", ["point_y", "POINT_Y", "stop_location_latitiude", "lat"], ["point_x", "plate"]),
    ("common/geo.yaml", "longitudebyshortname", ["point_x", "POINT_X", "stop_location_longitiude", "lng"], ["point_y", "long"]),
    ("common/dateandtime.yaml", "compactdatebyname", ["loading_date", "date", "posting_date", "issue date", "creat_dt"],
     ["update", "dated_by", "candidate"]),
    ("common/dateandtime.yaml", "quarterbyname", ["Quarter", "quarter_ar", "qtr", "الربع"], ["headquarters", "quarterly_report"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name
    spec = load(path, rule_id)
    assert spec.get("validator") and spec.get("needs_values") is True, rule_id


def test_bare_serial_number_and_revision():
    # A smart meter serial number is no VIN and no ISSN; a drawing revision is no commit hash.
    for path, rule_id in (("common/vehicles.yaml", "vinbyfieldname"), ("common/objects.yaml", "objects_issnfield")):
        assert not field_matches(path, rule_id, "serial_number"), rule_id
    assert load("common/software.yaml", "commithashbyknown").get("needs_values") is True


GUARDED = [
    ("ae/ae_geo.yaml", "aeabudhabiregionvalue", ["Al Ain", "الظفرة"], ["Dubai"]),
    ("ae/ae_geo.yaml", "aedubaicommunityvalue", ["Al Qusais", "AL MUTEENA"], ["Dubai"]),
    ("ae/ae_geo.yaml", "aecityvalue", ["Khor Fakkan", "Dubai"], ["Doha"]),
    ("ae/ae_finances.yaml", "aedewacontractaccountvalue", ["2002323313"], ["2002323314"]),
    ("common/dateandtime.yaml", "compactdatevalue", ["20171119"], ["20171301"]),
    ("common/dateandtime.yaml", "quartervalue", ["Q2", "Q1-2015"], ["Q5"]),
    ("en/en_med.yaml", "enicd10labelvalue", ["C18-C21 Colorectal"], ["Total"]),
    ("ae/ae_geo.yaml", "aeemiratevalue", ["R.A.K.", "أم القيوين"], ["Al Ain"]),
    ("ar/ar_geo.yaml", "arcountrynamevalue", ["المملكة العربية السعودية"], ["أخرى"]),
    ("common/chemistry.yaml", "casrnvalue", ["534-52-1"], ["534-52-2"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", GUARDED, ids=[g[1] for g in GUARDED])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value
