"""Thai codes and words found in 2024 snapshots of Thai government CKAN catalogues (Dateno sources
cdi00001512, City Data Platform; cdi00001518, Department of Fisheries; cdi00001520, National Statistical
Office; cdi00001521, Office of the Civil Service Commission; cdi00001530, Public Debt Management Office;
cdi00001531, Office of the Vocational Education Commission; cdi00001532, Bangkok Metropolitan
Administration): administrative area codes, districts of Bangkok, regions, month names, dates with a Buddhist
era year, health facility codes, school codes, bond symbols, civil service position levels, sex and name
prefixes.
"""
import re

# The 77 province codes of the Department of Provincial Administration (ISO 3166-2:TH without TH-).
_PROVINCE = r"(?:1[0-9]|2[0-7]|[34][0-9]|5[0-8]|6[0-7]|7[0-7]|8[0-6]|9[0-6])"
_PROVINCE_CODE = re.compile(_PROVINCE)
_DISTRICT_CODE = re.compile(_PROVINCE + r"\d{2}")
_SUBDISTRICT_CODE = re.compile(_PROVINCE + r"\d{4}")

BANGKOK_DISTRICTS = frozenset((
    "พระนคร", "ดุสิต", "หนองจอก", "บางรัก", "บางเขน", "บางกะปิ", "ปทุมวัน", "ป้อมปราบศัตรูพ่าย", "พระโขนง", "มีนบุรี",
    "ลาดกระบัง", "ยานนาวา", "สัมพันธวงศ์", "พญาไท", "ธนบุรี", "บางกอกใหญ่", "ห้วยขวาง", "คลองสาน", "ตลิ่งชัน",
    "บางกอกน้อย", "บางขุนเทียน", "ภาษีเจริญ", "หนองแขม", "ราษฎร์บูรณะ", "บางพลัด", "ดินแดง", "บึงกุ่ม", "สาทร", "บางซื่อ",
    "จตุจักร", "บางคอแหลม", "ประเวศ", "คลองเตย", "สวนหลวง", "จอมทอง", "ดอนเมือง", "ราชเทวี", "ลาดพร้าว", "วัฒนา",
    "บางแค", "หลักสี่", "สายไหม", "คันนายาว", "สะพานสูง", "วังทองหลาง", "คลองสามวา", "บางนา", "ทวีวัฒนา", "ทุ่งครุ",
    "บางบอน",
))
# ป้อมปราบฯ is the usual short form of ป้อมปราบศัตรูพ่าย; รวม is the row of totals.
_DISTRICT_EXTRA = frozenset(("ป้อมปราบฯ", "ป้อมปราบ", "รวม"))

MONTHS = (
    "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม",
    "พฤศจิกายน", "ธันวาคม",
)
MONTH_ABBREVIATIONS = (
    "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค.",
)
_MONTHS = frozenset(MONTHS)
_MONTH_ANY = frozenset(MONTHS) | frozenset(MONTH_ABBREVIATIONS) | frozenset(
    a.rstrip(".") for a in MONTH_ABBREVIATIONS) | frozenset(a.replace(".", "") for a in MONTH_ABBREVIATIONS)
_MONTH_RE = "|".join(list(MONTHS) + [a.replace(".", r"\.?") for a in MONTH_ABBREVIATIONS])
_DATE_BE = re.compile(r"(?:0?[1-9]|[12]\d|3[01])[/.-](?:0?[1-9]|1[0-2])[/.-]2[4-6]\d{2}")
_DATE_THAI = re.compile(r"(?:0?[1-9]|[12]\d|3[01])[ -]?(?:" + _MONTH_RE + r")[ -]?(?:\d{2}|2[4-6]\d{2})")

_REGION = re.compile(
    r"(?:\d\)\s*)?(?:ภาค)?(?:เหนือ|กลาง|ตะวันออกเฉียงเหนือ|อีสาน|ใต้|ตะวันออก|ตะวันตก)(?:\s*\(.*\))?")
# Rows of totals and Bangkok, which the National Statistical Office lists beside its four regions.
_REGION_EXTRA = re.compile(
    r"(?:\d\)\s*)?(?:ทั่วราชอาณาจักร|ทั่วประเทศ|กรุงเทพมหานคร|กรุงเทพฯ|กทม\.?|รวม|ยอดรวม|กรุงเทพมหานครและปริมณฑล)")

_HCODE = re.compile(r"\d{5}|\d{9}")
_SCHOOL_CODE = re.compile(r"\d{10}")
_BOND_SYMBOL = re.compile(r"[A-Z]{2,6}\d{2}[1-9OND][A-Z]")

_LEVELS = (
    "ปฏิบัติงาน", "ชำนาญงาน", "อาวุโส", "ทักษะพิเศษ", "ปฏิบัติการ", "ชำนาญการ", "ชำนาญการพิเศษ", "เชี่ยวชาญ",
    "ทรงคุณวุฒิ",
)
_LEVEL = re.compile(
    r"(?:" + "|".join(sorted(_LEVELS, key=len, reverse=True)) + r")"
    r"|(?:ประเภท)?(?:อำนวยการ|บริหาร)\s?(?:ระดับ)?(?:ต้น|สูง)"
    r"|ประเภท(?:ทั่วไป|วิชาการ)\s?ระดับ(?:" + "|".join(sorted(_LEVELS, key=len, reverse=True)) + r")")

_SEX = frozenset(("ชาย", "หญิง", "เพศชาย", "เพศหญิง", "รวม", "ยอดรวม", "1. ชาย", "2. หญิง", "ไม่ระบุ", "ไม่ระบุเพศ"))
_NAME_PREFIX = frozenset((
    "นาย", "นาง", "นางสาว", "น.ส.", "ด.ช.", "ด.ญ.", "เด็กชาย", "เด็กหญิง", "ดร.", "ผศ.", "รศ.", "ศ.", "ผศ.ดร.",
    "รศ.ดร.", "ศ.ดร.", "นพ.", "พญ.", "ทพ.", "ทญ.", "ว่าที่ร้อยตรี", "ว่าที่ ร.ต.", "พระ", "พระครู", "พระมหา", "คุณ",
))


def _text(value):
    if value is None or isinstance(value, bool):
        return ""
    return " ".join(str(value).split())


def validate_th_province_code(value):
    """A Thai province code: 10 (Bangkok), 83 (Phuket), 55 (Nan), not 28 or 99."""
    return bool(_PROVINCE_CODE.fullmatch(_text(value)))


def validate_th_district_code(value):
    """A Thai district code: 1001 (Phra Nakhon), 8301 (Mueang Phuket), a province code and two digits."""
    return bool(_DISTRICT_CODE.fullmatch(_text(value)))


def validate_th_subdistrict_code(value):
    """A Thai subdistrict code: 100101, a district code and two digits."""
    return bool(_SUBDISTRICT_CODE.fullmatch(_text(value)))


def validate_th_bangkok_district(value):
    """One of the 50 districts of Bangkok by its Thai name: พระนคร, จตุจักร (not เขตจตุจักร, not เชียงใหม่)."""
    return _text(value) in BANGKOK_DISTRICTS


def validate_th_bangkok_district_or_total(value):
    """A district of Bangkok as tables write it: จตุจักร, เขตจตุจักร, สำนักงานเขตจตุจักร, ป้อมปราบฯ, or the row
    of totals (รวม)."""
    text = _text(value)
    for prefix in ("สำนักงานเขต", "เขต"):
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
            break
    return text in BANGKOK_DISTRICTS or text in _DISTRICT_EXTRA


def validate_th_region(value):
    """A region of Thailand: ภาคเหนือ, กลาง, 4) ภาคตะวันออกเฉียงเหนือ, ภาคกลาง(ไม่รวมกรุงเทพมหานคร)."""
    return bool(_REGION.fullmatch(_text(value)))


def validate_th_region_or_total(value):
    """A region of Thailand or what statistical tables list beside the regions: the whole kingdom
    (ทั่วราชอาณาจักร), Bangkok, the row of totals."""
    text = _text(value)
    return bool(_REGION.fullmatch(text) or _REGION_EXTRA.fullmatch(text))


def validate_th_month(value):
    """A month by its full Thai name: มกราคม, ตุลาคม (not ม.ค., not จันทร์)."""
    return _text(value) in _MONTHS


def validate_th_month_or_abbreviation(value):
    """A month by its Thai name or abbreviation (ม.ค., พ.ย, ตค), or the row of totals (รวม)."""
    text = _text(value)
    return text in _MONTH_ANY or text == "รวม"


def validate_date_th_be(value):
    """A date with a Buddhist era year: 17/06/2567, 19/2/2563 (not 17/06/2024)."""
    return bool(_DATE_BE.fullmatch(_text(value)))


def validate_date_thai(value):
    """A date with a Thai month name: 24 กรกฎาคม 2566, 17 มิ.ย.2556, 1-พ.ย.-65."""
    return bool(_DATE_THAI.fullmatch(_text(value)))


def validate_th_hcode(value):
    """A Thai health facility code of five or nine digits: 10741, 001074100."""
    return bool(_HCODE.fullmatch(_text(value)))


def validate_th_school_code(value):
    """A Thai school code of ten digits: 1310016101."""
    return bool(_SCHOOL_CODE.fullmatch(_text(value)))


def validate_th_bond_symbol(value):
    """A ThaiBMA bond symbol: LB436A, LB27NA, ESGLB376A, SRT33DA (not TH0623037304, not TL267A)."""
    return bool(_BOND_SYMBOL.fullmatch(_text(value)))


def validate_th_civil_service_position_level(value):
    """A position level of the Thai civil service: ชำนาญการพิเศษ, ปฏิบัติงาน, อำนวยการสูง,
    ประเภทบริหาร ระดับต้น."""
    return bool(_LEVEL.fullmatch(_text(value)))


def validate_th_sex(value):
    """Sex in Thai: ชาย, หญิง, with the row of totals (รวม)."""
    return _text(value) in _SEX


def validate_th_sex_word(value):
    """Sex in Thai without the totals: ชาย, หญิง."""
    return _text(value) in ("ชาย", "หญิง", "เพศชาย", "เพศหญิง")


def validate_th_name_prefix(value):
    """A Thai name prefix: นาย, นาง, นางสาว, ด.ช., ดร."""
    return _text(value) in _NAME_PREFIX
