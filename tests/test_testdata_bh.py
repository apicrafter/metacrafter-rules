"""Rules for the files of the Bahrain Open Data Portal (data.gov.bh, Opendatasoft; an April 2024 snapshot)
in metacrafter-testdata: Bahraini governorates and address blocks, GCC Common Customs Tariff codes; Arabic
sex, nationality, marital status, religion, education, age bands, months and quarters under the
transliterated Opendatasoft field names (ljns, ljnsy, lhl_lzwjy, ldyn, fy_t_lsn, lshhr, lrb); ISIC Rev. 4
section titles, ICD-10 chapters and COICOP codes; the UM unit column and the UN code country column of the
trade tables.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.ar.dates import validate_ar_month
from metacrafterext.rules.ar.persons import (
    validate_ar_education_level,
    validate_ar_gender,
    validate_ar_marital_status,
    validate_ar_nationality,
    validate_ar_nationality_value,
    validate_religion,
)
from metacrafterext.rules.bh.geo import (
    validate_bh_block,
    validate_bh_governorate,
    validate_bh_governorate_value,
    validate_gcc_customs_tariff_code,
)
from metacrafterext.rules.common.classifications import (
    validate_coicop_code,
    validate_icd10_chapter,
    validate_icd10_chapter_or_other,
    validate_isic_section_name,
    validate_isic_section_name_value,
    validate_trade_unit_code,
)
from metacrafterext.rules.common.directories import validate_education_level
from metacrafterext.rules.common.survey import validate_age_range_value
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (validate_bh_governorate,
     ["Capital", "Muharraq", "Northern", "Southern", "Central", "Northern Governorate", "Capital Governorate",
      "Al Asimah", "العاصمة", "المحرق", "الشمالية", "الجنوبية", "الوسطى", "محافظة المحرق"],
     ["Manama", "Riffa", "Total", "الجملة", "Not Stated", "غير مبين", "Cairo", "Isa Town", ""]),
    (validate_bh_block, ["305", "305.0", "101", "1203", "1218", "317.0"],
     ["100", "300", "1300", "99", "12", "B12", "14+15", ""]),
    (validate_gcc_customs_tariff_code, ["95030090", "04090000", "84091000", "95030090.0"],
     ["0409", "040900", "950300900", "00090000", "9503 00 90", ""]),
    (validate_ar_gender, ["ذكر", "أنثى", "انثى", "ذكور", "إناث"], ["المجموع", "Male", "بحريني", ""]),
    (validate_ar_nationality,
     ["بحريني", "غير بحريني", "بحرينية", "غير بحرينية", "بحرينـي", "إماراتي", "سعودي", "عماني", "قطري", "كويتي",
      "خليجي", "عربي آخر", "عرب آخرون", "آسيوي", "أوروبية", "أمريكي شمالي", "فلبينية", "أخرى", "البحريني"],
     ["البحرين", "الهند", "الأسر البحرينية", "دول مجلس التعاون", "آسيا", "الجملة", "Bahraini", ""]),
    (validate_ar_nationality_value, ["بحريني", "غير بحرينية", "خليجي", "إماراتي"],
     ["البحريني", "الســعودي", "أخرى", "آخرون", "مسلم", ""]),
    (validate_ar_marital_status, ["متزوج", "أرمل", "لم يسبق له الزواج", "مطلق", "مطلقة", "أعزب"],
     ["الجملة", "الأول", "Married", ""]),
    (validate_religion, ["Muslim", "Others", "Christian", "Hindu", "مسلم", "أخرى", "مسيحي"],
     ["Total", "Not Stated", "الجملة", "Bahraini", ""]),
    (validate_ar_education_level,
     ["أمي / يقرأ فقط", "يقرأ ويكتب", "ابتدائي", "إعدادي", "ثانوي", "فوق الثانوي / دبلوم", "فوق الثانوي",
      "بكالوريوس", "دبلوم عالي", "ماجستير", "دكتوراه", "أمي/يقرأ ويكتب", "أمية/ تقرأ وتكتب"],
     ["الجملة", "بحريني", "Primary", ""]),
    (validate_education_level,
     ["Illiterate / Read Only", "Read & Write", "Illiterate/ Read & Write", "Preparatory", "Intermediate",
      "Above  Secondary", "Above Secondary / Diploma", "High Diploma", "Graduate Studies", "ابتدائي"],
     ["Total", "Read", "Male", ""]),
    (validate_age_range_value, ["15 - 19", "65 Years & Above", "65 سنة فأكثر", "< 15 Years", "50 +", "أقل من 15"],
     ["Total", "2019", "الجملة", ""]),
    (validate_ar_month, ["مارس", "03 مارس", "01 يناير", "سبتمبـر", "كانون الثاني", "12 ديسمبر"],
     ["03", "April", "13 مارس", "الربع الأول", ""]),
    (validate_isic_section_name,
     ["Manufacturing", "Construction", "Education", "Mining & Quarrying", "Real Estate Activities",
      "Wholesale and Retail Trade Repair of Motor Vehicles and Motorcycles",
      "Water Supply, Sewage Waste Management and Remediation Activities",
      "Electricity, Gas Steam and Air Conditioning Supply", "Activities in the field of Human Health and Social Work",
      "Other Service Activities", "الصناعة التحويلية", "التشييد", "أنشطة التمويل والتأمين", "الفنون والترفية والتسلية",
      "تجارة الجملة والتجزئة ، إصلاح المركبات ذات المحركات والدراجات النارية", "النقل و التخزين"],
     ["Mining", "Trade Activities", "Health", "The financial Sector", "Crude Petroleum & Natural Gas", "Hotels",
      "Private Activities and Repair Activities", "المناجم", "الزراعة", "Total", ""]),
    (validate_icd10_chapter,
     ["A00 - B99", "C00 - D49", "D50 - D89", "E00 - E99", "G00 -G99", "S00 - T99", "V00 - Y99", "A00-B99",
      "Neoplasms", "Diseases of the Circulatory System", "Congential Anomalies", "Mental Disorder",
      "Conditions Originating in the Perinental Period", "Undefined illness",
      "Injuries, Poisoning & Certain Other Consequences of External Causes", "الأورام", "أمراض الجهاز الدوري",
      "العيوب والتشوهات خلقية"],
     ["C18-C21", "J11", "-", "Others", "Slight Injury", "Serious Injury", "Death", "Eye clinic", "Blood donation", ""]),
    (validate_bh_governorate_value, ["Muharraq", "Northern Governorate", "العاصمة", "الوسطى"],
     ["Capital", "Northern", "Central", "Southern", "North", ""]),
    (validate_isic_section_name_value,
     ["Mining & Quarrying", "Real Estate Activities", "الصناعة التحويلية",
      "Agriculture, Forestry and Fishing"],
     ["Education", "Construction", "education", "Financial And Insurance Services", "Other Services", "Other Service Activities",
      "Administrative And Support Services", "التشييد", ""]),
    (validate_icd10_chapter_or_other, ["Others", "أخرى", "D50 - D89"], ["Total", "Slight Injury", ""]),
    (validate_coicop_code, ["01.1.7", "10.4", "08", "0", "12", "13.1", "01.1.1.1"], ["14", "2019", "A01", ""]),
    (validate_trade_unit_code, ["KG", "NO", "L", "T", "CUM", "SQM", "MTR", "G", "KGM"], ["Yes", "km/h", "Male", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("bh/bh_geo.yaml", "bhgovernoratebyname", ["governorate", "Governorate", "lmhfz", "lmhfzt", "المحافظة",
                                              "governorate_name", "governorate_en"],
     ["government", "governor", "region", "mkn_qm_l_m_lm_td"]),
    ("bh/bh_geo.yaml", "bhblockbyname", ["block", "Block", "block_no", "Block Number", "رقم المجمع"],
     ["blocked", "block_group", "blockchain", "road"]),
    ("bh/bh_trade.yaml", "gcccustomstariffcodebyname", ["commodity_no", "Commodity No", "commodity_number",
                                                        "رقم السلعة"],
     ["commodity", "commodity_code", "commodity_name"]),
    ("ar/ar_persons.yaml", "argenderbyname", ["ljns", "jns", "الجنس"], ["ljnsy", "jnsy_lzwj", "sex"]),
    ("ar/ar_persons.yaml", "arnationalitybyname",
     ["ljnsy", "jnsy_lzwj", "jnsy_lzwj_lmtlq", "mjmw_t_ljnsy", "الجنسية", "جنسية الزوجة"], ["ljns", "nationality"]),
    ("ar/ar_persons.yaml", "armaritalstatusbyname", ["lhl_lzwjy", "lhl_lzwjy_lsbq", "الحالة الزواجية"],
     ["lhl", "marital_status"]),
    ("ar/ar_persons.yaml", "religionbyarabicname", ["ldyn", "الديانة"], ["ldwl", "dyn_lzwj"]),
    ("ar/ar_persons.yaml", "areducationlevelbyname",
     ["l_mw_hl_lmy", "l_thsyl_lmy", "l_thsyl_lmy_llzwj", "l_thsyl_t_lymy_llzwj", "lmrhl_lt_lymy", "أعلى مؤهل علمي"],
     ["lmhfz", "lthsyl"]),
    ("ar/ar_persons.yaml", "aragerangebyname", ["fy_t_lsn", "fy_t_l_mr", "فئات السن", "الفئة العمرية"],
     ["fy_t_l_jr_lshhry_bldynr_lbhryny", "lsn"]),
    ("ar/ar_geo.yaml", "arnamebytransliteratedname", ["l_sm", "l_sm_bl_rby", "name_arabic", "Name_AR", "arabic_name"],
     ["name", "l_smh", "name_english", "lsm_lmht"]),
    ("ar/ar_datetime.yaml", "armonthbytransliteratedname", ["lshhr", "shhr"], ["lshh", "shahr_value"]),
    ("ar/ar_datetime.yaml", "arquarterbytransliteratedname", ["lrb", "alrb"], ["rb", "lrbh"]),
    ("pii/pii.yaml", "religionbyname", ["religion", "Religion", "religion_name", "religious_affiliation"],
     ["religious_places", "region"]),
    ("pii/pii.yaml", "agerangebyname", ["age_group", "age_group_of_mother", "age_groups_of_husband", "agegroups"],
     ["age", "mother_age"]),
    ("common/directories.yaml", "educationlevelbyname",
     ["highest_educational_level", "highest_educational_attainment", "highest_educational_attainment_of_husband",
      "highest_education_attainment_of_wife", "schooling_stage", "education_level"], ["education", "school"]),
    ("common/classifications.yaml", "isicsectionnamebyname", ["isic", "lnsht", "lnsht_isic", "lqt", "industry",
                                                              "sector", "economic_activity"],
     ["isic_code", "sub_sector_code", "lqt_l_s_r_ljry"]),
    ("common/classifications.yaml", "icd10chapterbyname",
     ["international_disease_code", "cause_of_death", "sbb_lwf", "سبب الوفاة"], ["disease", "cause"]),
    ("common/classifications.yaml", "coicopbyname", ["coicop", "coicop_code", "COICOP Code"],
     ["coicop_division_group", "code"]),
    ("common/trade.yaml", "unitofmeasurebyshortname", ["um", "UM", "U.M."], ["umbrella", "uom_code_name"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name
    spec = load(path, rule_id)
    assert spec.get("validator") and spec.get("needs_values") is True, rule_id


GUARDED = [
    ("bh/bh_geo.yaml", "bhgovernoratevalue", ["Muharraq", "الشمالية"], ["Manama", "Central", "Capital"]),
    ("ar/ar_persons.yaml", "argendervalue", ["ذكر", "انثى"], ["أخرى"]),
    ("ar/ar_persons.yaml", "arnationalityvalue", ["غير بحريني", "سعودية"], ["أخرى", "البحريني"]),
    ("ar/ar_persons.yaml", "armaritalstatusvalue", ["لم يسبق له الزواج"], ["الأول"]),
    ("ar/ar_datetime.yaml", "armonthnumberedvalue", ["01 يناير", "04 أبريل"], ["مارس", "13 مارس"]),
    ("common/classifications.yaml", "isicsectionnamevalue", ["Mining & Quarrying"], ["Mining", "Education", "Other Services"]),
    ("common/classifications.yaml", "icd10chaptervalue", ["D50 - D89", "Neoplasms"], ["Others", "Slight Injury"]),
    ("common/intcodes.yaml", "iso3166alpha2byuncodefield", ["ae", "in"], ["xs"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", GUARDED, ids=[g[1] for g in GUARDED])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value
