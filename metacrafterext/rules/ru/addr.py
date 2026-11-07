# coding=utf-8

import re
from pyparsing import oneOf, Word, alphas, alphanums, Literal, lineStart, lineEnd, Optional, nums, printables, alphas8bit, ParseException
__author__ = 'ibegtin'

RUSSIAN_ALPHABET = (u"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
                    u"абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
                    u'-')
TINDEX_PATTERN = Word(nums, exact=6).setResultsName('postindex') + Optional(',').suppress()

REGOBL_TEXTS = [u'область', u'обл.', u'обл']
REGOBL_PATTERNS = Word(RUSSIAN_ALPHABET + alphas).setResultsName('region') + oneOf(REGOBL_TEXTS, caseless=True)
REGAREA_TEXTS = [u'край', u'кр.']
REGAREA_PATTERNS = Word(RUSSIAN_ALPHABET).setResultsName('region') + oneOf(REGAREA_TEXTS, caseless=True)
REGRESP_TEXTS = [u'респ.', u'республика']
REGRESP_PATTERNS = oneOf(REGRESP_TEXTS, caseless=True) + Word(RUSSIAN_ALPHABET).setResultsName('region')

REGION_PATTERNS = (REGOBL_PATTERNS | REGAREA_PATTERNS | REGRESP_PATTERNS) + Optional(',').suppress()


CITY_TEXTS = [u'г.', u'город', u'г']
CITY_PATTERN_ONE = oneOf(CITY_TEXTS, caseless=True).setResultsName('key_city') + Word(RUSSIAN_ALPHABET).setResultsName('city')
CITY_PATTERN_TWO = Word(RUSSIAN_ALPHABET).setResultsName('city') + oneOf(CITY_TEXTS, caseless=True).setResultsName('key_city')
CITY_PATTERNS = (CITY_PATTERN_ONE | CITY_PATTERN_TWO) + Optional(',').suppress()

STREET_TEXTS = [u'ул.', u'улица']
STREET_PATTERN = oneOf(STREET_TEXTS, caseless=True) + Word(RUSSIAN_ALPHABET).setResultsName('street_1') + Optional(Word(RUSSIAN_ALPHABET).setResultsName('street_2')) + Optional(',').suppress()

PROSPECT_TEXTS = [u'проспект', u'пр.', u'пр-т']
PROSPECT_PATTERN = Word(RUSSIAN_ALPHABET).setResultsName('street') + oneOf(PROSPECT_TEXTS, caseless=True) | oneOf(PROSPECT_TEXTS, caseless=True) + Word(RUSSIAN_ALPHABET).setResultsName('street')

RUSSIA_TEXTS = [u'рф', u'РФ', u'россия', u'Россия', u'РОССИЯ', u'Российская Федерация']
RUSSIA_PATTERN = oneOf(RUSSIA_TEXTS).setResultsName('key_country') + Optional(',').suppress()

HOUSE_TEXTS = [u'дом', u'д.']
HOUSE_PATTERN = Optional(oneOf(HOUSE_TEXTS, caseless=True)) + Word(nums+'/').setResultsName('house') + Optional(Literal(RUSSIAN_ALPHABET).setResultsName('houselett')) + Optional(',').suppress()


OFFICE_TEXTS = [u'офис', u'оф.']
OFFICE_PATTERN = oneOf(OFFICE_TEXTS, caseless=True) + Word(RUSSIAN_ALPHABET+nums).setResultsName('office') + Optional(',').suppress()

BUILDING_TEXTS = [u'строение', u'стр.']
BUILDING_PATTERN = oneOf(BUILDING_TEXTS, caseless=True) + Word(RUSSIAN_ALPHABET+nums).setResultsName('building') + Optional(',').suppress()

BASE_ADDRESS_PATTERNS = {
    "r:addr:indexbase" : lineStart + TINDEX_PATTERN + REGION_PATTERNS + CITY_PATTERNS + STREET_PATTERN + HOUSE_PATTERN + lineEnd,
    "r:addr:indexbase_prosp" : lineStart + TINDEX_PATTERN + REGION_PATTERNS + CITY_PATTERNS + PROSPECT_PATTERN + HOUSE_PATTERN + lineEnd,

    "r:addr:indexbase_rus" : lineStart + TINDEX_PATTERN + RUSSIA_PATTERN + REGION_PATTERNS + CITY_PATTERNS + STREET_PATTERN + HOUSE_PATTERN + lineEnd,
    "r:addr:indexbase_rus_prosp" : lineStart + TINDEX_PATTERN + RUSSIA_PATTERN + REGION_PATTERNS + CITY_PATTERNS + PROSPECT_PATTERN + HOUSE_PATTERN + lineEnd,


    "r:addr:noindexbase" : lineStart + REGION_PATTERNS  + CITY_PATTERNS + STREET_PATTERN + HOUSE_PATTERN + lineEnd,
    "r:addr:noindexbase_prosp" : lineStart + REGION_PATTERNS  + CITY_PATTERNS + PROSPECT_PATTERN + HOUSE_PATTERN + lineEnd,

    "r:addr:indexcity" : lineStart + TINDEX_PATTERN  + CITY_PATTERNS + STREET_PATTERN + HOUSE_PATTERN + lineEnd,
    "r:addr:indexcity_prosp" : lineStart + TINDEX_PATTERN + CITY_PATTERNS + PROSPECT_PATTERN + HOUSE_PATTERN + lineEnd,

    "r:addr:indexcity_rus" : lineStart + RUSSIA_PATTERN + TINDEX_PATTERN  + CITY_PATTERNS + STREET_PATTERN + HOUSE_PATTERN + lineEnd,
    "r:addr:indexcity_rus_prosp" : lineStart + RUSSIA_PATTERN + TINDEX_PATTERN  + CITY_PATTERNS + PROSPECT_PATTERN + HOUSE_PATTERN + lineEnd,


    "r:addr:noindexcity" : lineStart + CITY_PATTERNS + STREET_PATTERN + HOUSE_PATTERN + lineEnd,
    "r:addr:noindexcity_prosp" : lineStart + CITY_PATTERNS + PROSPECT_PATTERN + HOUSE_PATTERN + lineEnd,
    "r:addr:indexbase_incomplete" : lineStart + TINDEX_PATTERN + REGION_PATTERNS,
    "r:addr:indexcity_incomplete" : lineStart + TINDEX_PATTERN + CITY_PATTERNS,
#    "r:addr:indexshort_nosh" : lineStart + TINDEX_PATTERN,
#    "r:addr:indexcity_noindex" : lineStart + CITY_PATTERNS + STREET_PATTERN + HOUSE_PATTERN,
}

# Parts of a Russian address separated by commas, in any order: the registers of
# accredited organizations write "ул. Родионова, д.23, г. Нижний Новгород, Нижегородская
# обл., 603093", with the street first and the postal code last.
_ADDR_PART_PATTERNS = (
    ('index', re.compile(r'\d{6}')),
    ('country', re.compile(r'россия|рф|российская федерация')),
    ('region', re.compile(r'(?:[а-я-]+ )*[а-я-]+ (?:обл\.?|область|край|автономный округ|ао)'
                          r'|(?:респ\.?|республика) [а-я -]+(?:\([а-я]+\))?|г\.? ?(?:москва|санкт-петербург|севастополь)')),
    ('district', re.compile(r'(?:[а-я-]+ )*[а-я-]+ (?:р-н|район|р-он|м\.?о\.?|муниципальный округ)|(?:р-н|район) [а-я -]+')),
    ('city', re.compile(r'(?:г|город|с|село|пос|поселок|п|дер|деревня|пгт|рп|ст-ца|станица|х|хутор)(?:\. ?| )[а-я][а-я -]*'
                        r'|[а-я][а-я -]* г\.?|москва|санкт-петербург|севастополь')),
    ('street', re.compile(r'(?:ул|улица|пер|переулок|пр-т|пр-кт|просп|проспект|пр|ш|шоссе|б-р|бульвар|наб|набережная'
                          r'|пл|площадь|проезд|пр-д|туп|тупик|аллея|линия|мкр|микрорайон|кв-л|квартал)\.? ?\S.*'
                          r'|.*\S (?:ул|улица|пер|переулок|пр-т|проспект|шоссе|ш|б-р|бульвар|наб|набережная|пл'
                          r'|площадь|проезд|туп|тупик)\.?')),
    ('house', re.compile(r'(?:д|дом|вл|владение|здание|зд)\.? ?\d+[а-я]?(?:[/-]\d+[а-я]?)?(?: .*)?|\d+[а-я]?(?:/\d+[а-я]?)?')),
    ('extra', re.compile(r'(?:кв|квартира|оф|офис|корп|кор|корпус|к|стр|строение|пом|помещение|литер|лит|эт|этаж'
                         r'|ком|комн|комната)\.? ?\S.*')),
)
_ADDR_HOUSE_INSIDE = re.compile(r'(?:^| )(?:д|дом)\.? ?\d')


def _address_part_kind(part):
    for kind, pattern in _ADDR_PART_PATTERNS:
        if pattern.fullmatch(part):
            return kind
    return None


def is_russian_address_parts(s):
    """Russian address written as comma-separated parts in any order.

    It needs a street, a house number or a postal code, and a city, region or postal code;
    at most one part may be unknown (a building number such as "3.9.11").
    """
    if not isinstance(s, str) or ',' not in s or len(s) > 300:
        return False
    parts = [' '.join(p.lower().replace('ё', 'е').split()) for p in s.split(',')]
    parts = [p for p in parts if p]
    if len(parts) < 3:
        return False
    kinds, unknown = set(), 0
    for part in parts:
        kind = _address_part_kind(part)
        if kind is None:
            unknown += 1
            continue
        kinds.add(kind)
        if kind == 'street' and _ADDR_HOUSE_INSIDE.search(part):
            kinds.add('house')
    if unknown > 1:
        return False
    return 'street' in kinds and bool(kinds & {'house', 'index'}) and bool(kinds & {'city', 'region', 'index'})


def is_russian_address(s):
    """Simple matcher of string against russian address types patterns"""
    for key, pat in BASE_ADDRESS_PATTERNS.items():
        try:
            res = pat.parseString(s)
            return True
        except ParseException:
            pass
    return is_russian_address_parts(s)


def validate_okato(s):
    return True


def validate_oktmo(s):
    return True