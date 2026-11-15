"""Validators of the Bahraini names and codes found in the data.gov.bh files of metacrafter-testdata.

The Bahrain Open Data Portal (data.gov.bh, Opendatasoft; snapshot of April 2024) publishes the
statistics of the Information & eGovernment Authority and of the ministries with every label in
English and Arabic (governorate, المحافظة): census tables by governorate, directories of places
(mosques, embassies, petrol stations, banks) with the block of each place, and the foreign trade of
Bahrain by commodity of the GCC Common Customs Tariff.

Each function takes one value and returns True when it has the form of the name or code.
"""
import re

from metacrafterext.rules.ar.countries import fold_arabic, has_arabic

# The four governorates since September 2014 and the Central governorate (الوسطى) that was divided
# among them, in English with transliterations and in Arabic. ISO 3166-2: BH-13 Capital, BH-14
# Southern, BH-15 Muharraq, BH-17 Northern (BH-16 Central, deleted).
_GOVERNORATES = {
    "capital": "13", "alasimah": "13", "alasima": "13", "asimah": "13", "manama": None,
    "southern": "14", "aljanubiyah": "14", "janubiyah": "14", "aljanubiya": "14", "south": None,
    "muharraq": "15", "almuharraq": "15", "muharaq": "15",
    "central": "16", "alwusta": "16", "wusta": "16",
    "northern": "17", "ashshamaliyah": "17", "alshamaliyah": "17", "shamaliyah": "17", "alshamaliya": "17",
    "العاصمه": "13", "الجنوبيه": "14", "المحرق": "15", "الوسطي": "16", "الشماليه": "17",
}


def _key(value):
    text = str(value).strip()
    if has_arabic(text):
        text = fold_arabic(text)
        text = re.sub(r"^(?:محافظه|المحافظه)\s+", "", text)
        text = re.sub(r"\s+(?:محافظه|المحافظه)$", "", text)
        return text.replace(" ", "")
    text = re.sub(r"(?i)\bgovernorate\b|\bgov\.?$|\bmuhafazat?\b", " ", text)
    return re.sub(r"[^a-z]", "", text.lower())


def validate_bh_governorate(value):
    """A governorate of Bahrain in English or Arabic: Capital, Muharraq, Northern, Southern, the
    former Central, with or without the word Governorate (Northern Governorate, محافظة المحرق) and in
    transliterations (Al Asimah, Al Janubiyah). A city (Manama, Riffa), the country and the total row
    (Total, الجملة) are not."""
    key = _key(value)
    return bool(key) and _GOVERNORATES.get(key) is not None


_BLOCK = re.compile(r"^(?:1[0-2]|[1-9])\d{2}$")


def validate_bh_block(value):
    """A block number of the Bahraini address system: three or four digits from 101 to 1299 (the
    leading one or two digits are one of the twelve municipalities), also written as a float (305.0).
    The block is the postal code of the address."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return bool(_BLOCK.match(text)) and int(text) % 100 != 0


_TARIFF = re.compile(r"^\d{8}$")


def validate_gcc_customs_tariff_code(value):
    """An eight-digit code of the GCC Common Customs Tariff (95030090, 04090000): the HS chapter of
    the first two digits is 01 to 97 (98 and 99 hold national goods such as personal effects).
    A float (95030090.0) is read as the code."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return bool(_TARIFF.match(text)) and 1 <= int(text[:2]) <= 99
