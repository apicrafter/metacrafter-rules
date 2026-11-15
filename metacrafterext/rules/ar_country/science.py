"""Argentine science and technology codes found in the SICYTAR files of metacrafter-testdata (a 2024
snapshot of datasets.datos.mincyt.gob.ar, the open data portal of the Argentine science ministry):
project codes of the ANPCyT (PICT-2015-1234, ANR 600 NA093/08) and of CONICET (11220150100433CO), the
ANPCyT funds, the equipment codes of the Sistemas Nacionales (SNM-826), the categories of CONICET
staff and the eleven-digit BAHRA settlement codes."""
import re
import unicodedata

from metacrafterext.rules.ar_country.census import validate_ar_indec_department_part
from metacrafterext.rules.ar_country.codes import INDEC_PROVINCES

# FONCYT research projects: PICT-2015-1234, PICTO-2009-0012, PID-2011-0002; SICYTAR has a few
# PICT codes whose year lost a digit (PICT- 201-0031).
_ANPCYT_RESEARCH = re.compile(r"(?:PICTO?|PICT-O|PID|PICTO?-[A-Z]+)-\s?\d{3,4}-\d{3,4}")
# FONTAR, FONSOFT and FONARSEC instruments: the acronym of the instrument, then the call, the
# province of the company and a number with the year (ANR 600 NA093/08, CF BA 001/07,
# CRE+CO 0062/12, EMP FONSOFT NA038/07, FITAP 001 A03, LEY 2011/047, ARSET-I 0015).
_ANPCYT_INSTRUMENT = re.compile(
    r"(?:ANR|CF|CAE|CRE\+CO|EMP|FITAP|FIT|FITR|FITS|FSBIO|FSNANO|FSTICS|FSAGRO|FSSALUD|FSENERGIA|PDP|LEY|ARSET-I|PFIP|PRH|PAE)"
    r"\s[A-Za-z0-9+./\- ]{2,28}"
)
_CONICET = re.compile(r"\d{3}(?:19|20)\d{2}01\d{5}CO")


def validate_ar_anpcyt_project_code(value):
    """A project code of the ANPCyT: PICT-2015-1234, PICTO-2009-0012, PID-2011-0002, or an instrument
    acronym with a number (ANR 600 NA093/08, CF BA 001/07, CRE+CO 0062/12). A CONICET code fails."""
    text = " ".join(str(value).split())
    if _ANPCYT_RESEARCH.fullmatch(text):
        return True
    return bool(_ANPCYT_INSTRUMENT.fullmatch(text)) and any(ch.isdigit() for ch in text)


def validate_ar_conicet_project_code(value):
    """A CONICET project code: three digits of the call, the year, 01, five digits and CO
    (11220150100433CO)."""
    return bool(_CONICET.fullmatch(str(value).strip()))


def validate_ar_cyt_project_code(value):
    """A project code of one of the national funders of research in Argentina, as the SICYTAR projects
    list mixes them in one column: an ANPCyT or a CONICET code."""
    return validate_ar_anpcyt_project_code(value) or validate_ar_conicet_project_code(value)


_FUNDS = frozenset({"FONCYT", "FONTAR", "FONSOFT", "FONARSEC"})


def validate_ar_anpcyt_fund(value):
    """An ANPCyT fund: FONCYT, FONTAR, FONSOFT, FONARSEC (also FONCyT)."""
    return str(value).strip().upper() in _FUNDS


# The Sistemas Nacionales of the science ministry: microscopy (SNM), mass spectrometry (SNEM),
# X-rays (SNRX), magnetic resonance (SNRM), animal facilities (SNB), high-performance computing
# (SNCAD), flow cytometry (SNCF), magnetometry (SNMAG), lasers (SINALA), genomic data (SNDG),
# biological data (SNDB).
_EQUIPMENT = re.compile(r"(?:SNM|SNEM|SNRX|SNRM|SNB|SNCAD|SNCF|SNMAG|SINALA|SNDG|SNDB)-\d{1,5}")


def validate_ar_mincyt_equipment_id(value):
    """The code of an instrument of a Sistema Nacional of the science ministry: SNM-826, SNCAD-483,
    SINALA-1021."""
    return bool(_EQUIPMENT.fullmatch(str(value).strip().upper()))


def _fold(value):
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")
    return " ".join(text.lower().split())


_CONICET_CLASSES = ("asistente", "adjunto", "adjunta", "independiente", "principal", "superior",
                    "superior emerito", "correspondiente")
_CONICET_OTHER = frozenset({
    "becario doctoral", "becaria doctoral", "becario postdoctoral", "becaria postdoctoral",
    "becario", "becaria", "personal de apoyo", "gestion cyt", "pasante", "otro personal conicet",
    "no pertenece a conicet",
})


def validate_ar_conicet_category(value):
    """A CONICET staff category by value: a class of the research career with the word Investigador
    (Investigador asistente, Investigadora principal, Investigador superior emérito), a fellowship
    (Becario doctoral), the support staff (Personal de apoyo) or No pertenece a Conicet. A bare class
    (PRINCIPAL, Superior) is another enumeration's, and Profesor titular and Técnico principal fail."""
    text = _fold(value)
    if text in _CONICET_OTHER:
        return True
    m = re.match(r"investigador(?:a)?\s+(.+)", text)
    return bool(m) and m.group(1) in _CONICET_CLASSES


def validate_ar_conicet_category_name(value):
    """A CONICET staff category in a field named after CONICET: also a bare class of the research
    career (asistente, Adjunto, principal)."""
    return validate_ar_conicet_category(value) or _fold(value) in _CONICET_CLASSES


def validate_ar_bahra_department_part(value):
    """The department part of a BAHRA code (084, 441, 7): an INDEC department part, or 000 for the
    City of Buenos Aires, one department in BAHRA (02000010000)."""
    return str(value).strip() == "000" or validate_ar_indec_department_part(value)


def validate_ar_bahra_code(value):
    """An eleven-digit BAHRA settlement code: an INDEC province, department and census locality and
    three digits for the settlement (02000010000, 06441030015), also without the leading zero."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    if not text.isdigit() or len(text) not in (10, 11):
        return False
    return text.zfill(11)[:2] in INDEC_PROVINCES
