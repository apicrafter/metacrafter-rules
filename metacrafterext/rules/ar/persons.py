"""Arabic values of person attributes in statistics tables: sex, nationality, marital status,
religion and level of education.

The Bahrain Open Data Portal (data.gov.bh, a 2024 snapshot in metacrafter-testdata) gives every
census, vital and labour table two columns per attribute, the English one and the Arabic one, whose
header the portal writes with the Arabic letters transliterated (الجنس -> ljns, الجنسية -> ljnsy,
الحالة الزواجية -> lhl_lzwjy, الديانة -> ldyn). The Arabic values are a small vocabulary: ذكر and
أنثى (also انثى), بحريني and غير بحريني, متزوج, مسلم, ابتدائي. Values are compared after
``fold_arabic`` (hamza forms, ta marbuta, final yeh, tatweel and vowel marks).
"""
import re

from metacrafterext.rules.ar.countries import fold_arabic, has_arabic


# --- sex -------------------------------------------------------------------------------------

_GENDER = frozenset(fold_arabic(w) for w in (
    "ذكر", "أنثى", "انثى", "ذكور", "إناث", "اناث", "رجل", "امرأة", "رجال", "نساء", "الذكور", "الإناث",
))


def validate_ar_gender(value):
    """Sex in Arabic: ذكر, أنثى (also انثى), ذكور, إناث, رجال, نساء."""
    return fold_arabic(value) in _GENDER


# --- nationality -----------------------------------------------------------------------------

# Adjectives of the countries and groups that Arab statistics label nationalities with, masculine
# (the feminine adds ة: بحرينية). Folded: أ إ آ -> ا, ة -> ه, ى -> ي.
_NATIONALITY_STEMS = (
    "بحريني", "سعودي", "اماراتي", "كويتي", "قطري", "عماني", "يمني", "عراقي", "اردني", "سوري",
    "لبناني", "فلسطيني", "مصري", "سوداني", "ليبي", "تونسي", "جزائري", "مغربي", "موريتاني", "صومالي",
    "جيبوتي", "جزر قمري", "قمري", "اريتري", "اثيوبي", "كيني", "نيجيري", "جنوب افريقي", "اوغندي", "تنزاني",
    "هندي", "باكستاني", "بنغالي", "بنجلاديشي", "بنغلاديشي", "سريلانكي", "نيبالي", "افغاني", "ايراني",
    "تركي", "فلبيني", "اندونيسي", "ماليزي", "تايلندي", "تايلاندي", "صيني", "ياباني", "كوري", "فيتنامي",
    "ميانماري", "امريكي", "كندي", "مكسيكي", "برازيلي", "ارجنتيني", "بريطاني", "انجليزي", "فرنسي",
    "الماني", "ايطالي", "اسباني", "برتغالي", "هولندي", "بلجيكي", "سويسري", "سويدي", "نرويجي", "دنماركي",
    "فنلندي", "روسي", "اوكراني", "بولندي", "يوناني", "ايرلندي", "استرالي", "نيوزيلندي",
    "خليجي", "عربي", "اسيوي", "اوروبي", "افريقي", "امريكي شمالي", "امريكي جنوبي", "اجنبي",
    "مواطن", "وافد", "اخر", "اخري", "اخرون", "اخريات", "عرب", "عرب اخرون", "عربي اخر", "جنسيات اخري",
)
_NATIONALITY = frozenset(fold_arabic(s) for s in _NATIONALITY_STEMS)


def _nationality_word(text):
    if text in _NATIONALITY:
        return True
    # The feminine and plural forms: بحرينية, بحرينيون, بحرينيين.
    for suffix in ("ه", "ون", "ين", "يه"):
        if text.endswith(suffix) and text[: -len(suffix)] in _NATIONALITY:
            return True
    return False


_NATIONALITY_GROUPS_ONLY = frozenset(fold_arabic(w) for w in (
    "آخر", "أخرى", "آخرون", "أخريات", "جنسيات أخرى", "مواطن", "وافد", "أجنبي", "عرب",
))


def validate_ar_nationality_value(value):
    """A nationality in Arabic as a value of its own column (validate_ar_nationality without the
    article and without the words that also end other lists: أخرى, آخرون). البحريني and السعودي
    name the origin of crude oil in the Bahrain refinery tables; a column of مسلم and أخرى is a
    religion."""
    text = fold_arabic(value)
    if text.startswith("ال") or text in _NATIONALITY_GROUPS_ONLY:
        return False
    return validate_ar_nationality(value)


def validate_ar_nationality(value):
    """A nationality in Arabic: بحريني, بحرينية, سعودي, هندي, the negated form غير بحريني, and the
    groups of nationality tables (خليجي, عربي آخر, آسيوي, أخرى). A country name (البحرين) is not."""
    text = fold_arabic(value)
    if not text or not has_arabic(text) or len(text) > 40:
        return False
    if text.startswith("غير "):
        text = text[4:].strip()
    if text.startswith("ال") and text[2:] and _nationality_word(text[2:]):
        return True
    return _nationality_word(text)


# --- marital status --------------------------------------------------------------------------

_MARITAL = frozenset(fold_arabic(w) for w in (
    "أعزب", "عزباء", "عازب", "عازبة", "متزوج", "متزوجة", "مطلق", "مطلقة", "أرمل", "أرملة", "منفصل",
    "منفصلة", "لم يسبق له الزواج", "لم يسبق لها الزواج", "لم يتزوج", "لم تتزوج", "عقد قران", "عاقد",
    "متزوج / متزوجة", "مطلق / مطلقة", "أرمل / أرملة",
))


def validate_ar_marital_status(value):
    """A marital status in Arabic: أعزب, متزوج, مطلق, أرمل and the feminine forms, لم يسبق له الزواج."""
    text = fold_arabic(value)
    return text in _MARITAL or " ".join(text.split()) in _MARITAL


# --- religion --------------------------------------------------------------------------------

_RELIGION_WORDS = frozenset((
    "muslim", "muslims", "islam", "islamic", "sunni", "shia", "shiite", "christian", "christians",
    "christianity", "catholic", "catholics", "orthodox", "protestant", "evangelical", "jewish", "jew",
    "jews", "judaism", "hindu", "hindus", "hinduism", "buddhist", "buddhists", "buddhism", "sikh",
    "sikhs", "sikhism", "bahai", "baha'i", "zoroastrian", "jain", "taoist", "shinto", "atheist",
    "agnostic", "none", "no", "religion", "other", "others", "religions", "unknown", "not", "stated",
))
_RELIGION_CORE = frozenset((
    "muslim", "muslims", "islam", "islamic", "sunni", "shia", "shiite", "christian", "christians",
    "christianity", "catholic", "catholics", "orthodox", "protestant", "evangelical", "jewish", "jew",
    "jews", "judaism", "hindu", "hindus", "hinduism", "buddhist", "buddhists", "buddhism", "sikh",
    "sikhs", "sikhism", "bahai", "baha'i", "zoroastrian", "jain", "taoist", "shinto", "atheist",
    "agnostic", "other", "others",
))
_RELIGION_AR = frozenset(fold_arabic(w) for w in (
    "مسلم", "مسلمة", "مسلمون", "الإسلام", "إسلام", "سني", "شيعي", "مسيحي", "مسيحية", "مسيحيون",
    "المسيحية", "يهودي", "يهودية", "اليهودية", "هندوسي", "هندوسية", "بوذي", "بوذية", "سيخ", "سيخي",
    "بهائي", "أخرى", "آخرون", "ديانات أخرى", "أديان أخرى", "لا دين", "بدون",
))


def validate_religion(value):
    """A religion or denomination in English or Arabic: Muslim, Christian, Hindu, Buddhist, Others,
    مسلم, مسيحي, أخرى."""
    if has_arabic(value):
        return fold_arabic(value) in _RELIGION_AR
    words = [w for w in re.split(r"[\s/,;()&-]+", str(value).strip().lower()) if w]
    return bool(words) and all(w in _RELIGION_WORDS for w in words) and any(w in _RELIGION_CORE for w in words)


# --- level of education ----------------------------------------------------------------------

_EDUCATION_AR = frozenset(fold_arabic(w) for w in (
    "أمي", "أمية", "أمي / يقرأ فقط", "يقرأ فقط", "يقرأ ويكتب", "تقرأ وتكتب", "يقرأ و يكتب", "أمي/ يقرأ ويكتب",
    "أمية/ تقرأ وتكتب", "ملم", "ابتدائي", "ابتدائية", "إعدادي", "إعدادية", "متوسط", "متوسطة", "ثانوي",
    "ثانوية", "فوق الثانوي", "فوق الثانوي / دبلوم", "دبلوم", "دبلوم عالي", "دبلوم متوسط", "جامعي",
    "جامعية", "بكالوريوس", "ليسانس", "ماجستير", "دكتوراه", "دكتوراة", "الدراسات العليا", "دراسات عليا",
    "رياض الأطفال", "روضة", "بدون مؤهل", "غير متعلم",
))


_EDUCATION_AR_KEYS = frozenset(" ".join(w.replace("/", " / ").split()) for w in _EDUCATION_AR)


def validate_ar_education_level(value):
    """A level of education in Arabic: أمي, يقرأ ويكتب, ابتدائي, إعدادي, ثانوي, فوق الثانوي / دبلوم,
    بكالوريوس, ماجستير, دكتوراه."""
    return " ".join(fold_arabic(value).replace("/", " / ").split()) in _EDUCATION_AR_KEYS
