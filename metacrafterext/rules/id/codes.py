"""Indonesian codes and words found in a 2024 snapshot of the open data portal of Tangerang Regency
(opendata.tangerangkab.go.id, Dateno source cdi00000904): administrative area codes of the Ministry of Home
Affairs, month names, civil servant grades, sex, religion and levels of education.
"""
import re

_KODE_WILAYAH = re.compile(r"\d{2}(?:\.\d{2}(?:\.\d{2,5}(?:\.\d{4})?)?)?")
_GOLONGAN = re.compile(r"I{1,3}[/. ]?[A-D]|IV[/. ]?[A-E]", re.I)

MONTHS = frozenset((
    "januari", "februari", "maret", "april", "mei", "juni", "juli", "agustus", "september", "oktober", "november",
    "desember",
))
MONTH_ABBREVIATIONS = frozenset((
    "jan", "feb", "mar", "apr", "mei", "jun", "jul", "agu", "agt", "ags", "sep", "okt", "nov", "des",
))
_SEX = frozenset((
    "laki-laki", "laki laki", "laki_laki", "lakilaki", "laki - laki", "pria", "perempuan", "wanita", "l", "p",
    "lk", "pr", "laki-laki dan perempuan", "laki-laki + perempuan", "jumlah", "total",
))
# The six religions on Indonesian identity cards and the belief systems (kepercayaan), with the spellings
# of the tables of Tangerang (KHATOLIK, BUDHA, KONGHUCU).
_RELIGION = frozenset((
    "islam", "kristen", "kristen protestan", "protestan", "katolik", "katholik", "khatolik", "kristen katolik",
    "hindu", "buddha", "budha", "konghucu", "khonghucu", "kong hu cu", "khong hu cu", "kepercayaan",
    "aliran kepercayaan", "kepercayaan terhadap tuhan yme", "lainnya",
))
# School levels and degrees: SD, SLTP/SMP, SLTA/SMA/SMK, the diplomas DI to DIV and the degrees S1 to S3.
_EDUCATION = re.compile(
    r"(?:tidak|belum)(?:[ /]+(?:belum|tidak))? (?:pernah )?sekolah|(?:tidak|belum) tamat sd(?:/sederajat)?"
    r"|tamat sd(?:/sederajat)?|tk|paud|sd|mi|sd/mi|sltp|smp|mts|smp/mts|sltp/sederajat|slta|sma|smk|ma|smu"
    r"|sma/smk|sma/ma|slta/sederajat|d[- ]?(?:[1-4]|i{1,3}|iv)|d(?:i|1)/d(?:ii|2)|d(?:iv|4)/s1"
    r"|diploma (?:[1-4]|i{1,3}|iv)(?:/(?:ii|strata i))?|akademi/diploma iii/s\. ?muda|sarjana(?: muda)?"
    r"|s[- ]?[1-3]|strata (?:[1-3]|i{1,3})|pasca ?sarjana|magister|doktor|profesi|spesialis",
    re.I)


def _text(value):
    if value is None or isinstance(value, bool):
        return ""
    return " ".join(str(value).split())


def validate_id_kode_wilayah(value):
    """An administrative area code of the Ministry of Home Affairs: 36 (province), 36.03 (regency),
    36.03.01 (district), 36.03.01.2001 (village), not a number without the groups of two digits."""
    return bool(_KODE_WILAYAH.fullmatch(_text(value)))


def validate_id_kode_wilayah_dotted(value):
    """An administrative area code below the province, with its dots: 36.03, 36.03.01, 36.03.01.2001."""
    text = _text(value)
    return "." in text and bool(_KODE_WILAYAH.fullmatch(text))


def validate_id_month(value):
    """A month by its Indonesian name: Januari, MARET, Agustus, Desember (not March, Mai or Senin)."""
    return _text(value).lower() in MONTHS


def validate_id_month_or_abbreviation(value):
    """A month by its Indonesian name or abbreviation: Januari, Agt, Okt, Des."""
    text = _text(value).lower().rstrip(".")
    return text in MONTHS or text in MONTH_ABBREVIATIONS


def validate_id_pns_golongan(value):
    """A grade of an Indonesian civil servant: I/a, II.c, III/d, IV/e, IIIa (not I/e, V/a or 3A)."""
    return bool(_GOLONGAN.fullmatch(_text(value)))


def validate_id_sex(value):
    """The sex of a person in Indonesian: Laki-laki, LAKI_LAKI, Perempuan, Pria, Wanita, L, P, and the
    total row of a table (Jumlah)."""
    return _text(value).lower() in _SEX


def validate_id_religion(value):
    """A religion in Indonesian: Islam, Kristen, Katolik, Hindu, Buddha, Konghucu, Kepercayaan."""
    return _text(value).lower() in _RELIGION


def validate_id_education_level(value):
    """A level of education in Indonesian: SD, SLTP, SLTA, DIII, DIV/S1, S2, TIDAK/BELUM SEKOLAH,
    TIDAK TAMAT SD."""
    return bool(_EDUCATION.fullmatch(_text(value)))
