"""Macedonian names and words found in a 2024 snapshot of the open data portal of North Macedonia
(data.gov.mk, Dateno source cdi00001115): municipalities, phone numbers, months and coordinates.
"""
import re

# The 80 municipalities since 2013, ten of them in the City of Skopje.
MUNICIPALITIES = frozenset(name.lower() for name in (
    "Берово", "Чешиново-Облешево", "Делчево", "Карбинци", "Кочани", "Македонска Каменица", "Пехчево", "Пробиштип",
    "Штип", "Виница", "Зрновци", "Кратово", "Крива Паланка", "Куманово", "Липково", "Ранковце", "Старо Нагоричане",
    "Битола", "Демир Хисар", "Долнени", "Кривогаштани", "Крушево", "Могила", "Новаци", "Прилеп", "Ресен",
    "Боговиње", "Брвеница", "Гостивар", "Јегуновце", "Маврово и Ростуша", "Теарце", "Тетово", "Врапчиште", "Желино",
    "Аеродром", "Арачиново", "Бутел", "Чаир", "Центар", "Чучер Сандево", "Гази Баба", "Ѓорче Петров", "Илинден",
    "Карпош", "Кисела Вода", "Петровец", "Сарај", "Сопиште", "Студеничани", "Шуто Оризари", "Зелениково",
    "Богданци", "Босилово", "Гевгелија", "Дојран", "Конче", "Ново Село", "Радовиш", "Струмица", "Валандово",
    "Василево", "Центар Жупа", "Дебар", "Дебарца", "Кичево", "Македонски Брод", "Охрид", "Пласница", "Струга",
    "Вевчани", "Чашка", "Демир Капија", "Градско", "Кавадарци", "Неготино", "Росоман", "Свети Николе", "Лозово",
    "Велес",
))
_MUNICIPALITY_PREFIX = re.compile(r"^(?:општина|град)\s+")
# 070 235 790, 047275166, 02/3071-657, +389 75 396 926, and numbers that lost the zero (70673427, 3061922).
_PHONE = re.compile(r"(?:\+|00)?389\d{8,9}|0?\d{6,8}")
_PHONE_SEPARATORS = re.compile(r"(?<=\d)[ /-](?=\d)|(?<=^\+389) ")
_MONTHS = frozenset((
    "јануари", "февруари", "март", "април", "мај", "јуни", "јули", "август", "септември", "октомври", "ноември",
    "декември",
))
_DEGREES = re.compile(r"-?\d{1,3}[.,]\d{2,}")


def _text(value):
    if value is None or isinstance(value, bool):
        return ""
    return " ".join(str(value).split())


def validate_mk_municipality(value):
    """A municipality of North Macedonia in Macedonian: Крушево, КРУШЕВО, Демир Хисар, Општина Карпош,
    Чучер-Сандево."""
    text = _MUNICIPALITY_PREFIX.sub("", _text(value).lower())
    return text in MUNICIPALITIES or text.replace("-", " ") in MUNICIPALITIES


def validate_mk_phone(value):
    """A phone number of North Macedonia as tables write it: 070235790, 075/423-125, 02/3071-657,
    +389075396926, 70673427."""
    return bool(_PHONE.fullmatch(_PHONE_SEPARATORS.sub("", _text(value))))


def validate_mk_month(value):
    """A month by its number (1 to 12) or its Macedonian name (јануари, Декември)."""
    text = _text(value).lower()
    if text in _MONTHS:
        return True
    return bool(re.fullmatch(r"0?[1-9]|1[0-2]", text))


def validate_decimal_degrees(value):
    """A coordinate in decimal degrees: 41.22472, 21,5403 (not 41.279.567 or 21090710)."""
    text = _text(value)
    if not _DEGREES.fullmatch(text):
        return False
    return -180 <= float(text.replace(",", ".")) <= 180
