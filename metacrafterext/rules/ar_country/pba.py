"""Validators for the open data of the municipalities of Buenos Aires Province (datosabiertos.mercedes.gob.ar,
a 2024 snapshot and the portal of 2026; metacrafter-testdata): the designations of the schools of the
Dirección General de Cultura y Educación (EP N° 1, EES N° 8, JARDÍN 901), the numbers of the private
schools (DIPREGEP) and the numbers of municipal tenders (Licitación Pública N° 12/2021, LPub Nº 03/2018)."""
import re
import unicodedata


def _fold_upper(value):
    """Upper case without accents, single spaces, no spaces at the ends."""
    text = unicodedata.normalize("NFKD", str(value).strip())
    text = "".join(ch for ch in text if not unicodedata.combining(ch)).upper()
    return re.sub(r"\s+", " ", text)


# --- Schools of the DGCyE -----------------------------------------------------------------------

# Abbreviations of the levels and modalities of the DGCyE, longest first: escuela primaria (EP),
# secundaria (ES, EES, ESB), técnica (EET, EEST), agraria (EESA), especial (EEE), primaria de adultos
# (EEPA), jardín de infantes (JI, JIRIMM rural de matrícula mínima), centro educativo complementario
# (CEC), de educación física (CEF), agrario (CEA), para la producción total (CEPT), de formación
# profesional or laboral (CFP, CFL), de nivel secundario (CENS), de atención temprana (CATDI),
# institutos superiores (ISFD, ISFDYT, ISFT).
_SCHOOL_KINDS = ("EEST", "EESA", "EEPA", "EES", "EET", "EEE", "ESB", "EP", "ES", "JIRIMM", "JIRMM", "JI",
                 "CEPT", "CENS", "CATDI", "CEC", "CEF", "CEA", "CFP", "CFL", "ISFDYT", "ISFDT", "ISFD", "ISFT")
_SCHOOL_KIND = "|".join(r"\.?".join(kind) for kind in _SCHOOL_KINDS)
# N°, Nº, Nª (a typo), NRO, N. and no sign (the folding turns º into O and ª into A); a kindergarten
# is also JARDIN 901 or JARDIN DE INFANTES N° 901.
_SIGN = r"(?:N ?[°OA]\.?|NRO\.?|N\.)"
_SCHOOL_SIGN = _SIGN + "?"
_SCHOOL = re.compile(
    rf"^(?:NORMAL )?(?:(?:{_SCHOOL_KIND})\.?|JARDIN(?: DE INFANTES)?) ?{_SCHOOL_SIGN} ?(?P<num>\d{{1,4}})"
    r"(?P<rest>(?:\b| ).{0,30})$"
)
_SCHOOL_WITH_SIGN = re.compile(rf"^(?:NORMAL )?(?:(?:{_SCHOOL_KIND})\.?|JARDIN(?: DE INFANTES)?) ?{_SIGN} ?\d")


def validate_ar_pba_school_service(value):
    """A school of Buenos Aires Province by its kind and number: EP Nº 1, E.S Nº3 NACIONAL, E.E.S Nº8,
    EET Nº1, JARDÍN 901, JIRMM Nº1, CEF N° 193, CFP Nº 401, NORMAL ISFD Nº137, E.S Nº9 (EPNº12) (not
    Escuela N° 12 D.E. 5, EP 0, a bare CFL or a word with a number)."""
    match = _SCHOOL.match(_fold_upper(value))
    return bool(match) and int(match.group("num")) > 0


def validate_ar_pba_school_service_value(value):
    """A school of Buenos Aires Province written with the number sign (EP Nº 1, E.S. N° 7, CEF N° 193)
    or as JARDÍN 901: EP 12 alone is also an episode or a page."""
    text = _fold_upper(value)
    if not validate_ar_pba_school_service(text):
        return False
    return bool(_SCHOOL_WITH_SIGN.match(text)) or text.startswith("JARDIN")


def validate_ar_pba_dipregep_number(value):
    """A DIPREGEP number of a private school: 1 to 9999, also as 1750.0 (not 0, 604988 or text)."""
    text = str(value).strip()
    match = re.match(r"^(\d{1,4})(?:\.0+)?$", text)
    return bool(match) and int(match.group(1)) > 0


# --- Tenders -------------------------------------------------------------------------------------

_TENDER = re.compile(
    r"^(?:LICITACION (?:PUBLICA|PRIVADA)|CONCURSO DE PRECIOS|CONTRATACION DIRECTA|LPUB|LPRIV|LPR|LP|CP|CD|L\. ?P\.)"
    rf" ?{_SIGN}? ?(?P<num>\d{{1,5}}) ?/ ?(?P<year>\d{{2}}|\d{{4}})$"
)


def validate_ar_licitacion_number(value):
    """The number of a tender with its kind and year: LPub Nº 03/2018, Lpriv Nº 29/2018, Licitación
    Pública N° 12/2021, Concurso de Precios N° 3/2019, LP 5/2020 (not 452-0001-LPU17, 12/2021 alone or
    Licitación Pública without a number)."""
    match = _TENDER.match(_fold_upper(value))
    if not match or int(match.group("num")) == 0:
        return False
    year = int(match.group("year"))
    return len(match.group("year")) == 2 or 1950 <= year <= 2100
