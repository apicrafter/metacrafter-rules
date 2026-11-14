"""Armenian place names: the provinces (marzer) and the capital Yerevan.

Found in the administrative boundaries of the Armenian Soil Information System (ArmSIS) of
metacrafter-testdata (marz.csv, Armenian and English names) and in the mineral resource list of
data.gov.am (Aragatsotn Province).
"""
import re

_EN = (r"Yerevan|Erevan|Aragatsotn|Aragacotn|Ararat|Armavir|Gegharkunik|Geghark'unik'?|Kotayk'?|Kotayq|Lori|"
       r"Shirak|Syunik'?|Siunik|Tavush|Tavoush|Vayots[' -]{1,2}Dzor")
_HY = r"Երևան|Երեւան|Արագածոտն|Արարատ|Արմավիր|Գեղարքունիք|Կոտայք|Լոռի|Շիրակ|Սյունիք|Տավուշ|Վայոց ձոր"
_RU = r"Ереван|Арагацотн|Арарат|Армавир|Гегаркуник|Котайк|Лори|Ширак|Сюник|Тавуш|Вайоц[ -]Дзор"
_MARZ = re.compile(
    rf"^(?:(?:{_EN})(?: (?:Province|Marz|Region))?|(?:Province|Marz|Region) of (?:{_EN})|"
    rf"(?:{_HY})(?:ի? մարզ)?|Լոռու մարզ|(?:{_RU})(?: (?:марз|область))?)$",
    re.I,
)
# Names of a province that are also the names of other places: Armavir is a city in Russia,
# Ararat a city in Armenia and Australia, Lori a given name. A column of these alone is not a
# column of provinces.
_AMBIGUOUS = frozenset(("ararat", "armavir", "lori", "yerevan", "erevan", "ереван", "арарат", "армавир", "лори",
                        "երևան", "երեւան", "արարատ", "արմավիր", "լոռի"))


def validate_am_marz(value):
    """A province (marz) of Armenia or Yerevan: Gegharkunik, Vayots Dzor, Aragatsotn Province,
    Վայոց Ձոր, Շիրակի մարզ, Сюник."""
    text = re.sub(r"\s+", " ", str(value).strip())
    return 4 <= len(text) <= 40 and bool(_MARZ.match(text))


def validate_am_marz_by_value(value):
    """A province name that names nothing else: not Ararat, Armavir, Lori or Yerevan alone."""
    text = re.sub(r"\s+", " ", str(value).strip())
    return validate_am_marz(text) and text.lower() not in _AMBIGUOUS
