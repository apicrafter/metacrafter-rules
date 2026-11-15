"""Codes of education statistics and registers: ISCED 2011 programme and attainment codes, ISCED-F 2013
fields of education, and ETER identifiers of higher education institutions. Found in the files of ARES
and the Fédération Wallonie-Bruxelles (metacrafter-testdata, Belgian round) and of Strasbourg."""
import re


def _code(value):
    text = " ".join(str(value).strip().split()).strip("'\"")
    if re.fullmatch(r"\d+\.0+", text):
        text = text.split(".")[0]
    return text


_ISCED2011 = re.compile(r"0[12]0|100|[2-4][45][1-4]|5[45][0-4]|[67][456][0-8]|8[456][0-4]")


def validate_isced2011_programme_code(value):
    """A three-digit ISCED 2011 programme (ISCED-P) or attainment (ISCED-A) code: level, category and
    sub-category (645 academic Bachelor's, 747 academic Master's, 655, 554, 844). Not a level alone
    (6), an ISCED-F field (0413) or a code whose category the level does not have (615)."""
    return bool(_ISCED2011.fullmatch(_code(value)))


# The broad fields of ISCED-F 2013 (00 to 10, 99) and the narrow and detailed fields under them:
# a narrow field repeats the broad one and adds a digit (041), a detailed one adds another (0413);
# the generic last digits are 8 (inter-disciplinary) and 9 (not elsewhere classified).
_ISCEDF = re.compile(r"(?:0\d|10|99)(?:\d(?:\d)?)?")


def validate_isced_f_2013(value):
    """An ISCED-F 2013 field of education and training code of two to four digits: a broad field (00
    to 10, 99), a narrow (041) or a detailed field (0413, 0011). Not a number of more digits (12345),
    a broad field above 10 (11) or an ISCED 2011 level code (645)."""
    text = _code(value)
    if not _ISCEDF.fullmatch(text):
        return False
    # Narrow and detailed fields are numbered from 1 within the field above (041 and 0413, not 040
    # or 0410).
    return "0" not in text[2:]


_ETER = re.compile(r"[A-Z]{2}\d{4}")


def validate_eter_id(value):
    """An ETER identifier: the country code (EL for Greece, UK) and four digits (BE0041, FR0149)."""
    return bool(_ETER.fullmatch(_code(value)))
