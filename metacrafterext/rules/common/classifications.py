"""Titles and codes of international statistical classifications: ISIC Rev. 4 sections, ICD-10
chapters and COICOP codes, in English and Arabic.

Found in the April 2024 snapshot of the Bahrain Open Data Portal (data.gov.bh) of
metacrafter-testdata: foreign investment stocks by ISIC section (Manufacturing, الصناعة التحويلية),
deaths by underlying cause and ICD-10 chapter (D50 - D89, Diseases of the Blood & Blood Forming
Organs) and the consumer price index by COICOP division, group and class (01.1.7). Publishers
reword and misspell the titles, so a title is compared by its words with those of the official one.
"""
import re

from metacrafterext.rules.ar.countries import fold_arabic, has_arabic

# --- ISIC Rev. 4 sections --------------------------------------------------------------------

_ISIC_SECTIONS_EN = (
    "Agriculture, forestry and fishing",
    "Mining and quarrying",
    "Manufacturing",
    "Electricity, gas, steam and air conditioning supply",
    "Water supply; sewerage, waste management and remediation activities",
    "Construction",
    "Wholesale and retail trade; repair of motor vehicles and motorcycles",
    "Transportation and storage",
    "Accommodation and food service activities",
    "Information and communication",
    "Financial and insurance activities",
    "Real estate activities",
    "Professional, scientific and technical activities",
    "Administrative and support service activities",
    "Public administration and defence; compulsory social security",
    "Education",
    "Human health and social work activities",
    "Arts, entertainment and recreation",
    "Other service activities",
    "Activities of households as employers; undifferentiated goods- and services-producing activities"
    " of households for own use",
    "Activities of extraterritorial organizations and bodies",
)
_ISIC_SECTIONS_AR = (
    "الزراعة والحراجة وصيد الأسماك",
    "التعدين واستغلال المحاجر",
    "الصناعة التحويلية",
    "إمدادات الكهرباء والغاز والبخار وتكييف الهواء",
    "إمدادات المياه وأنشطة الصرف الصحي وإدارة النفايات ومعالجتها",
    "التشييد",
    "تجارة الجملة والتجزئة وإصلاح المركبات ذات المحركات والدراجات النارية",
    "النقل والتخزين",
    "أنشطة خدمات الإقامة والطعام",
    "المعلومات والاتصالات",
    "الأنشطة المالية وأنشطة التأمين",
    "الأنشطة العقارية",
    "الأنشطة المهنية والعلمية والتقنية",
    "أنشطة الخدمات الإدارية وخدمات الدعم",
    "الإدارة العامة والدفاع والضمان الاجتماعي الإلزامي",
    "التعليم",
    "أنشطة الصحة البشرية والعمل الاجتماعي",
    "الفنون والترفيه والتسلية",
    "أنشطة الخدمات الأخرى",
    "أنشطة الأسر المعيشية التي تستخدم أفرادا لإدارة الأعمال المنزلية",
    "أنشطة المنظمات والهيئات غير الخاضعة للولاية الوطنية",
)
_EN_STOP = frozenset(("and", "of", "the", "activities", "activity", "service", "services", "supply",
                      "supplies", "industry", "industries", "sector", "field", "in", "for", "own", "use"))
_EN_SYNONYMS = {"sewage": "sewerage", "defense": "defence", "organisations": "organizations",
                "transport": "transportation", "finance": "financial", "insurances": "insurance"}
_AR_STOP = frozenset(fold_arabic(w) for w in ("أنشطة", "نشاط", "خدمات", "في", "مجال", "ذات", "من", "التي"))
_AR_SYNONYMS = {fold_arabic(k): fold_arabic(v) for k, v in {
    "تمويل": "مالية", "انسان": "بشرية", "بشري": "بشرية", "صحه": "صحة", "تعدين": "تعدين",
}.items()}


def _en_words(text):
    words = re.split(r"[^a-z]+", str(text).lower().replace("&", " and "))
    return frozenset(_EN_SYNONYMS.get(w, w) for w in words if w and w not in _EN_STOP)


def _ar_word(word):
    # The conjunction و is written on the word (والغاز, وإصلاح): drop it, then the article ال.
    if word.startswith("و") and len(word) > 3:
        word = word[1:]
    if word.startswith("ال") and len(word) > 3:
        word = word[2:]
    return _AR_SYNONYMS.get(word, word)


def _ar_words(text):
    words = (_ar_word(w) for w in re.split(r"[\s،؛,;/()-]+", fold_arabic(text)) if w)
    return frozenset(w for w in words if w and w not in _AR_STOP and w != "و")


_ISIC_EN = tuple(_en_words(t) for t in _ISIC_SECTIONS_EN)
_ISIC_AR = tuple(_ar_words(t) for t in _ISIC_SECTIONS_AR)


def _matches_section(words, sections):
    """The words are a part of the words of a section title, at least half of them; a single word
    is only a section of one word (Manufacturing, Construction, Education): Mining, Financial or
    Trade alone also name the activities of national accounts and the sectors of other tables."""
    return bool(words) and any(
        words <= s and 2 * len(words) >= len(s) and (len(words) > 1 or len(s) == 1) for s in sections)


def validate_isic_section_name(value):
    """The title of an ISIC Rev. 4 section in English or Arabic, also shortened or reworded:
    Manufacturing, Mining & Quarrying, Wholesale and Retail Trade Repair of Motor Vehicles and
    Motorcycles, Water Supply, Sewage Waste Management and Remediation Activities, الصناعة التحويلية,
    أنشطة التمويل والتأمين. National accounts activities (Crude Petroleum & Natural Gas, Hotels) are not."""
    text = str(value).strip()
    if not text or len(text) > 160:
        return False
    if has_arabic(text):
        return _matches_section(_ar_words(text), _ISIC_AR)
    return _matches_section(_en_words(text), _ISIC_EN)


# --- ICD-10 chapters -------------------------------------------------------------------------

# First and last codes of the 22 chapters of ICD-10 (WHO 2019) and the rounded ends national tables
# use (C00-D49, E00-E99, H60-H99, K00-K99, P00-P99, S00-T99, V00-Y99).
_ICD_CHAPTER_STARTS = frozenset(("A00", "C00", "D50", "E00", "F00", "G00", "H00", "H60", "I00", "J00",
                                 "K00", "L00", "M00", "N00", "O00", "P00", "Q00", "R00", "S00", "V00",
                                 "V01", "Z00", "U00"))
_ICD_CHAPTER_ENDS = frozenset(("B99", "D48", "D49", "D89", "E90", "E99", "F99", "G99", "H59", "H95",
                               "H99", "I99", "J99", "K93", "K99", "L99", "M99", "N99", "O99", "P96",
                               "P99", "Q99", "R99", "T98", "T99", "Y98", "Y99", "Z99", "U85", "U99"))
_ICD_RANGE = re.compile(r"^([A-Z]\d{2})\s*[-–]\s*([A-Z]\d{2})$")
_ICD_TITLE_EN = re.compile(
    r"infectious|parasitic|neoplasm|diseases? of the blood|blood[- ]forming|endocrine|nutritional|metabolic"
    r"|mental|behaviou?ral|nervous system|of the eye|\beye\b|mastoid|of the ear|circulatory|respiratory"
    r"|digestive|of the skin|subcutaneous|musculoskel|connective tissue|genitourinary|urinary|pregnancy"
    r"|child-?birth|puerperium|perin[a-z]*al|congen[a-z]*|congent[a-z]*|malformation|chromosomal"
    r"|symptoms|ill-defined|undefined|abnormal clinical|poisoning|external causes"
    r"|factors influencing|special purposes")
_ICD_DISEASE_EN = re.compile(
    r"diseases?|disorders?|neoplasms?|anomalies|malformations?|conditions?|poisoning"
    r"|causes|factors|symptoms|signs|illness|infectious|pregnancy|purposes")
_ICD_TITLE_AR = tuple(fold_arabic(w) for w in (
    "الأمراض المعدية", "الطفيلية", "الأورام", "أمراض الدم", "الغدد الصماء", "التغذية", "الاضطرابات العقلية",
    "الإضطرابات العقلية", "الاضطرابات النفسية", "الجهاز العصبي", "أمراض العين", "أمراض الأذن", "الجهاز الدوري",
    "الجهاز التنفسي", "الجهاز الهضمي", "أمراض الجلد", "الجهاز الهيكلي", "الجهاز العضلي", "التناسلي البولي",
    "البولي التناسلي", "الحمل والولادة", "حول الولادة", "حول موعد الولادة", "التشوهات", "العيوب الخلقية",
    "الأعراض والعلامات", "الإصابات والتسمم", "الأسباب الخارجية", "العوامل المؤثرة",
))
_OTHERS = frozenset(("other", "others", "other causes", "all other causes", "other diseases"))
_OTHERS_AR = frozenset(fold_arabic(w) for w in ("أخرى", "آخرى", "أسباب أخرى", "أمراض أخرى"))


def validate_icd10_chapter(value):
    """An ICD-10 chapter by its code range (A00-B99, C00 - D49, D50-D89; the range must run from the
    first code of a chapter to its last, also as national tables round it) or by its title in English
    or Arabic (Neoplasms, Diseases of the Circulatory System, Congential Anomalies, أمراض الجهاز الدوري).
    A block of codes (C18-C21) or a single code (J11) is icd10."""
    text = " ".join(str(value).strip().split())
    if not text or len(text) > 160:
        return False
    match = _ICD_RANGE.match(text.upper())
    if match:
        return match.group(1) in _ICD_CHAPTER_STARTS and match.group(2) in _ICD_CHAPTER_ENDS
    if has_arabic(text):
        folded = fold_arabic(text)
        return any(k in folded for k in _ICD_TITLE_AR)
    lower = text.lower().replace("&", "and")
    return bool(_ICD_TITLE_EN.search(lower)) and bool(_ICD_DISEASE_EN.search(lower))


def validate_icd10_chapter_or_other(value):
    """An ICD-10 chapter (validate_icd10_chapter) or the row of the other causes (Others, أخرى) that
    tables by chapter add."""
    text = " ".join(str(value).strip().split())
    if has_arabic(text):
        if fold_arabic(text) in _OTHERS_AR:
            return True
    elif text.lower().rstrip("*") in _OTHERS:
        return True
    return validate_icd10_chapter(value)


# --- COICOP ----------------------------------------------------------------------------------

_COICOP = re.compile(r"^(?:0?[1-9]|1[0-3])(?:\.\d{1,2}){0,3}$")


def validate_coicop_code(value):
    """A COICOP code: division (01 to 12, 13 in COICOP 2018), group (01.1), class (01.1.7) or
    subclass (01.1.1.1); 0 or 00 is the all-items index of a CPI table."""
    text = str(value).strip()
    if text in ("0", "00", "0.0"):
        return True
    return bool(_COICOP.match(text))


# --- units of trade statistics -----------------------------------------------------------------

# The units of quantity that customs declarations and trade tables give in a short column (UM of the
# Bahrain imports and exports: KG, NO, L, T, CUM, SQM, MTR, G), with the UN/ECE Recommendation 20
# codes of the same units (KGM, LTR, MTK, MTQ, NAR, PCE, TNE).
_TRADE_UNITS = frozenset((
    "KG", "KGS", "KGM", "G", "GR", "GRM", "T", "TN", "TNE", "TON", "TONS", "MT", "L", "LT", "LTR", "LTRS",
    "ML", "MLT", "HL", "M", "MTR", "M2", "SQM", "MTK", "M3", "CUM", "CBM", "MTQ", "NO", "NOS", "NUM", "NR",
    "NAR", "U", "UN", "UNIT", "UNITS", "PCE", "PCS", "PC", "PR", "PRS", "PAIR", "PAIRS", "DOZ", "DZN",
    "CT", "CTN", "CAR", "KWH", "MWH", "GWH", "TJ", "BBL", "CARAT", "2U", "12U",
))


def validate_trade_unit_code(value):
    """A short unit of quantity of trade data: KG, NO, L, T, CUM, SQM, MTR, G, PCS, or the UN/ECE
    Recommendation 20 code (KGM, LTR, MTK, NAR)."""
    return str(value).strip().upper().rstrip(".") in _TRADE_UNITS
