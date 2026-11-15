"""Brazilian codes found in the Brazilian files of metacrafter-testdata (2024 snapshots of five CKAN portals
of the Dateno catalogue: the Banco Central do Brasil, the BNDES, CAPES, the Jardim Botânico do Rio de Janeiro
and the Governo Aberto of the State of São Paulo):

- companies and banks: CNPJ numbers with their check digits (12.345.678/0001-95, 60.701.190.0001-04,
  5463212000129 without its leading zero, the alphanumeric CNPJ of 2026), the eight-digit CNPJ root, ISPB
  codes of the payment system, COMPE bank numbers, CNAE activity codes (4711-3/02, C1011200) and the Mercosur NCM goods codes (84328000, 8432.80.00);
- geography: the 27 federative units by code (SP, RJ) and by name (São Paulo, MINAS GERAIS, Ceara), the
  five regions (Norte, Centro-Oeste), the IBGE municipality codes with their check digit (3550308), CEP
  postal codes (01310-100, 89041002) and phone numbers in the national format ((19) 3472-9700);
- government: the 17-digit NUP protocol number with its two check digits (99903.000615/2016-03), the
  process numbers (TC 005.291/2021-6) and rulings (2726/2023-Plenário) of the Tribunal de Contas da União;
- higher education: CAPES programme codes (33003017040P8), CAPES institution codes (33003017), e-MEC
  institution codes, the 49 CAPES evaluation areas and the CAPES grades (1 to 7, A);
- the size class (porte) of a company: MICRO, PEQUENA, MÉDIA, GRANDE, ME, EPP;
- the six biomes (Amazônia, Cerrado, Mata Atlântica), alone or listed.

From the second Brazilian round (2024 snapshots of dados.mg.gov.br, dados.recife.pe.gov.br, dados.rs.gov.br
and the Dataverse repositories Arca Dados of Fiocruz, SciELO Data, CIDACS and FGV):

- the six-digit IBGE municipality code of DATASUS (355030), the two-digit IBGE code of a state (35), the
  15-digit census tract code (355030801000001, also 3.55030801000001E14), all also as spreadsheet floats;
- the INEP code of a school (26175347) and the CNES number of a health establishment (2446480, 0000957);
- the race or colour categories of IBGE (Branca, Parda, Indígena) and ICD-10 codes as DATASUS writes them
  (C159, W788).
"""
import re
import unicodedata


def _fold(value):
    """Lower case without accents, single spaces."""
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode()
    return " ".join(text.lower().split())


def _digits_only(value, allowed=" .-/"):
    """The digits of a value made of digits and the separators in allowed, or None."""
    text = str(value).strip()
    if not text or any(not (ch.isdigit() or ch in allowed) for ch in text):
        return None
    return "".join(ch for ch in text if ch.isdigit())


# --- CNPJ ---------------------------------------------------------------------------------------------

_CNPJ_W1 = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
_CNPJ_W2 = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
_CNPJ_FORMATTED = re.compile(r"[0-9A-Z]{2}\.[0-9A-Z]{3}\.[0-9A-Z]{3}[/.][0-9A-Z]{4}-\d{2}")


def _cnpj_dv(base):
    """The two check digits of the twelve characters of a CNPJ: digits, or since July 2026 also upper-case
    letters, each worth its ASCII code minus 48."""
    values = [ord(ch) - 48 for ch in base]
    s1 = sum(v * w for v, w in zip(values, _CNPJ_W1)) % 11
    d1 = 0 if s1 < 2 else 11 - s1
    s2 = sum(v * w for v, w in zip(values + [d1], _CNPJ_W2)) % 11
    d2 = 0 if s2 < 2 else 11 - s2
    return f"{d1}{d2}"


def _cnpj_ok(chars):
    if len(chars) != 14 or not chars[12:].isdigit() or len(set(chars)) == 1:
        return False
    if not all(ch.isdigit() or "A" <= ch <= "Z" for ch in chars[:12]):
        return False
    return _cnpj_dv(chars[:12]) == chars[12:]


def validate_cnpj(value):
    """A CNPJ whose check digits are right, formatted (12.345.678/0001-95, 60.701.190.0001-04 with a dot for
    the slash) or as digits (60746948000112, and 12 or 13 digits when a spreadsheet dropped the leading
    zeros: 5463212000129), also the alphanumeric CNPJ issued since July 2026 (12.ABC.345/01DE-35). All
    zeros (00.000.000.0000-00) and other repeated digits fail."""
    text = str(value).strip().upper()
    if _CNPJ_FORMATTED.fullmatch(text):
        return _cnpj_ok(re.sub(r"[./-]", "", text))
    if re.fullmatch(r"\d{12,14}", text):
        return _cnpj_ok(text.zfill(14))
    if re.fullmatch(r"[0-9A-Z]{12}\d{2}", text) and not text.isdigit():
        return _cnpj_ok(text)
    return False


def validate_cnpj_formatted(value):
    """A CNPJ in its printed form, with its check digits: 12.345.678/0001-95 or 60.701.190.0001-04."""
    text = str(value).strip().upper()
    return bool(_CNPJ_FORMATTED.fullmatch(text)) and _cnpj_ok(re.sub(r"[./-]", "", text))


def validate_br_cnpj_root(value):
    """The CNPJ root (CNPJ básico), the eight digits shared by every establishment of a company: 23862762,
    02658435, 60.701.190. A full CNPJ fails."""
    digits = _digits_only(value, allowed=".")
    return bool(digits) and len(digits) == 8


# --- banks ---------------------------------------------------------------------------------------------


def validate_br_ispb(value):
    """An ISPB code of the Brazilian payment system: eight digits, the CNPJ root of the institution
    (00000000 Banco do Brasil, 00360305 Caixa); also 360305 without its leading zeros."""
    text = str(value).strip()
    return bool(re.fullmatch(r"\d{6,8}", text))


def validate_br_compe_code(value):
    """A COMPE bank number of the Brazilian clearing house: three digits (001 Banco do Brasil, 237 Bradesco),
    also without the leading zeros (1, 70)."""
    text = str(value).strip()
    return bool(re.fullmatch(r"\d{1,3}", text)) and int(text) > 0


# --- CNAE and NCM ---------------------------------------------------------------------------------------

_CNAE_SECTIONS = {
    "A": range(1, 4), "B": range(5, 10), "C": range(10, 34), "D": (35,), "E": range(36, 40),
    "F": range(41, 44), "G": range(45, 48), "H": range(49, 54), "I": (55, 56), "J": range(58, 64),
    "K": range(64, 67), "L": (68,), "M": range(69, 76), "N": range(77, 83), "O": (84,), "P": (85,),
    "Q": range(86, 89), "R": range(90, 94), "S": range(94, 97), "T": (97,), "U": (99,),
}
_CNAE_DIVISIONS = {d for divisions in _CNAE_SECTIONS.values() for d in divisions}
_CNAE = re.compile(
    r"([A-U])?\s?(\d{2})(?:\.?(\d)(?:(\d)-?(\d)(?:/?(\d{2}))?)?)?"
)


def validate_br_cnae(value):
    """A CNAE 2 code of the Brazilian classification of economic activities: a division (47), group (47.1),
    class with its check digit (47.11-3, 4711-3, 47113) or subclass (4711-3/02, 4711302), also after the
    letter of its section as the BNDES writes them (C1011200, O8411600, F42). The division must exist and
    agree with the section letter."""
    text = str(value).strip().upper()
    match = _CNAE.fullmatch(text)
    if not match:
        return False
    section, division, group, klass, dv, subclass = match.groups()
    if klass is not None and dv is None:
        return False
    division = int(division)
    if division not in _CNAE_DIVISIONS:
        return False
    if section is not None:
        return division in _CNAE_SECTIONS[section]
    # Without a section letter, a bare division or group is just a number: ask for a class.
    return klass is not None or "." in text


_NCM = re.compile(r"(\d{4})\.?(\d{2})\.?(\d{2})")


def validate_mercosur_ncm(value):
    """A code of the Mercosur Common Nomenclature (NCM): eight digits, the HS subheading and two Mercosur
    digits (84328000, 8432.80.00); the HS chapter (01 to 97, not 77) must exist."""
    match = _NCM.fullmatch(str(value).strip())
    if not match:
        return False
    chapter = int(match.group(1)[:2])
    return 1 <= chapter <= 97 and chapter != 77


# --- geography -------------------------------------------------------------------------------------------

BR_STATE_CODES = {
    "AC": "12", "AL": "27", "AP": "16", "AM": "13", "BA": "29", "CE": "23", "DF": "53", "ES": "32", "GO": "52",
    "MA": "21", "MT": "51", "MS": "50", "MG": "31", "PA": "15", "PB": "25", "PR": "41", "PE": "26", "PI": "22",
    "RJ": "33", "RN": "24", "RS": "43", "RO": "11", "RR": "14", "SC": "42", "SP": "35", "SE": "28", "TO": "17",
}
_IBGE_UF = set(BR_STATE_CODES.values())
BR_STATES = (
    "Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal", "Espírito Santo", "Goiás",
    "Maranhão", "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais", "Pará", "Paraíba", "Paraná", "Pernambuco",
    "Piauí", "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia", "Roraima",
    "Santa Catarina", "São Paulo", "Sergipe", "Tocantins",
)
_STATE_NAMES = {_fold(name) for name in BR_STATES}


def validate_br_state_code(value):
    """The abbreviation of one of the 27 federative units: SP, RJ, DF (also lower case and padded: ' SP')."""
    return str(value).strip().upper() in BR_STATE_CODES


def validate_br_state(value):
    """The name of one of the 27 federative units, with or without accents and in any case: São Paulo,
    MINAS GERAIS, Ceara, Espirito Santo."""
    return _fold(value) in _STATE_NAMES


_REGIONS = {"norte", "nordeste", "sudeste", "sul", "centro-oeste", "centro oeste", "centrooeste"}


def validate_br_region(value):
    """One of the five regions of Brazil: Norte, Nordeste, Sudeste, Sul, Centro-Oeste (also SUDESTE,
    Região Sul)."""
    text = _fold(value)
    if text.startswith("regiao "):
        text = text[7:]
    return text in _REGIONS


# Municipalities created before the check digit rule whose code does not follow it (IBGE).
_IBGE_DV_EXCEPTIONS = {"2201919", "2201988", "2202251", "2611533", "3117836", "3152131", "4305871", "5203939",
                       "5203962"}


def _ibge_dv(d6):
    total = 0
    for i, ch in enumerate(d6):
        p = int(ch) * (1 if i % 2 == 0 else 2)
        total += p // 10 + p % 10
    return str((10 - total % 10) % 10)


def validate_br_municipality_code(value):
    """The seven-digit IBGE code of a municipality: the IBGE code of its state (35 São Paulo), four digits
    and a check digit (3550308 São Paulo, 5300108 Brasília); also 3550308.0. 9999999 and 0 fail."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    if not re.fullmatch(r"\d{7}", text) or text[:2] not in _IBGE_UF:
        return False
    return text in _IBGE_DV_EXCEPTIONS or _ibge_dv(text[:6]) == text[6]


def _spreadsheet_integer(value):
    """The digits of an integer written by a spreadsheet or a statistics package: 355030, 355030.0,
    3.55030801000001E14 (Dataverse and SPSS exports of codes saved as numbers). None for anything else."""
    text = str(value).strip()
    if re.fullmatch(r"\d+", text):
        return text
    if re.fullmatch(r"\d+\.0+", text):
        return text.split(".")[0]
    match = re.fullmatch(r"(\d)\.(\d+)[eE]\+?(\d{1,2})", text)
    if match:
        digits, exponent = match.group(1) + match.group(2), int(match.group(3))
        if len(digits) - 1 <= exponent:
            return digits + "0" * (exponent - len(digits) + 1)
    return None


def validate_br_municipality_code_6(value):
    """The six-digit IBGE code of a municipality without its check digit, as DATASUS writes it: the IBGE
    code of its state and four digits (355030 São Paulo, 310620 Belo Horizonte); also 355030.0. Seven
    digits (3550308) and 999999 fail."""
    text = _spreadsheet_integer(value)
    return bool(text) and len(text) == 6 and text[:2] in _IBGE_UF


def validate_br_state_ibge_code(value):
    """The two-digit IBGE code of one of the 27 federative units (11 Rondônia, 35 São Paulo, 53 Distrito
    Federal); also 35.0. 34, 99 and SP fail."""
    text = _spreadsheet_integer(value)
    return text in _IBGE_UF


def validate_br_census_tract_code(value):
    """The 15-digit IBGE code of a census tract: a municipality code with its check digit, two digits of
    the district, two of the subdistrict and four of the tract (355030801000001); also as a float of a
    spreadsheet export (3.55030801000001E14)."""
    text = _spreadsheet_integer(value)
    return bool(text) and len(text) == 15 and validate_br_municipality_code(text[:7])


def validate_br_inep_school_code(value):
    """The eight-digit INEP code of a school, which begins with the IBGE code of its state (26175347 a school
    of Recife, Pernambuco); also 26175347.0. Eight digits after a state code fit CAPES institution codes
    too (33003017): the field name tells them apart."""
    text = _spreadsheet_integer(value)
    return bool(text) and len(text) == 8 and text[:2] in _IBGE_UF


def validate_br_cnes(value):
    """The seven-digit CNES number of a health establishment (2446480, 0000957); a spreadsheet drops the
    leading zeros (957, 2446480.0). Fewer than three significant digits (1, 2, 98) and 0000000 fail."""
    text = _spreadsheet_integer(value)
    if not text or len(text) > 7:
        return False
    return len(text.lstrip("0")) >= 3


# --- health and persons -------------------------------------------------------------------------------

# The race or colour (raça/cor) categories of IBGE and of the health information systems, with the
# markers of an unknown value they add (SIM, SINAN: Ignorado).
_RACE_COLOUR = {"branca", "branco", "preta", "preto", "parda", "pardo", "amarela", "amarelo", "indigena",
                "negra", "negro", "ignorado", "ignorada", "nao declarado", "nao declarada", "sem declaracao",
                "nao informado", "nao informada"}


def validate_br_race_colour(value):
    """A race or colour category of IBGE: Branca, Preta, Parda, Amarela, Indígena (also in upper case and in
    the masculine), or Ignorado and Não declarado of the health records; codes (1 to 5) fail."""
    return _fold(value) in _RACE_COLOUR


_ICD10_DATASUS = re.compile(r"[A-Z]\d{2}(?:\.?\d|X|-)?")


def validate_icd10_datasus(value):
    """An ICD-10 (CID-10) code as the Brazilian health information systems write it: a letter, two digits
    and a subcategory digit without the dot (C159, W788, I209), the category alone (C20), with an X for a
    category without subcategories (I10X) or with the dot (C15.9)."""
    return bool(_ICD10_DATASUS.fullmatch(str(value).strip().upper()))


def validate_br_postcode(value):
    """A CEP postal code: 01310-100, 01.310-100 or eight digits (89041002); 00000-000 fails."""
    text = str(value).strip()
    if not re.fullmatch(r"\d{5}-?\d{3}|\d{2}\.\d{3}-\d{3}", text):
        return False
    return text.replace("-", "").replace(".", "") != "00000000"


def validate_br_postcode_formatted(value):
    """A CEP postal code with its hyphen: 01310-100, 13469-070."""
    text = str(value).strip()
    return bool(re.fullmatch(r"\d{5}-\d{3}", text)) and text != "00000-000"


_DDD = {
    11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 24, 27, 28, 31, 32, 33, 34, 35, 37, 38, 41, 42, 43, 44, 45, 46,
    47, 48, 49, 51, 53, 54, 55, 61, 62, 63, 64, 65, 66, 67, 68, 69, 71, 73, 74, 75, 77, 79, 81, 82, 83, 84, 85,
    86, 87, 88, 89, 91, 92, 93, 94, 95, 96, 97, 98, 99,
}
# The area code in parentheses may keep the trunk prefix 0 ((019) 3472-9700); written bare it may not, as
# 0 and the area code are how other countries start their numbers (Vietnam: 02253534622).
_BR_PHONE = re.compile(r"(?:\+?55[\s.-]?)?(?:\(0?(\d{2})\)|(\d{2}))[\s.-]?(9?\d{4})[\s.-]?(\d{4})")


def validate_br_phone_national(value):
    """A Brazilian phone number in the national format, with its area code (DDD): (19) 3472-9700,
    (11) 98765-4321, 19 3472 9700, +55 61 3414-1414. A landline has eight digits from 2 to 5, a mobile nine
    digits from 9. A bare leading 0 fails (02253534622 is Vietnamese)."""
    match = _BR_PHONE.fullmatch(str(value).strip())
    if not match:
        return False
    ddd = match.group(1) or match.group(2)
    first = match.group(3)
    if int(ddd) not in _DDD:
        return False
    if len(first) == 5:
        return first[0] == "9"
    return first[0] in "2345"


def validate_br_phone_formatted(value):
    """A Brazilian phone number with its area code in parentheses, as directories print it: (19) 3472-9700,
    (11) 98765-4321, (61) 3414 1414."""
    text = str(value).strip()
    return bool(re.fullmatch(r"\(0?\d{2}\)\s?9?\d{4}[\s-]\d{4}", text)) and validate_br_phone_national(text)


# --- government ---------------------------------------------------------------------------------------------


def _nup_dv(d15):
    out = ""
    for n in (15, 16):
        digits = (d15 + out)[:n]
        total = sum(int(ch) * w for ch, w in zip(digits, range(n + 1, 1, -1)))
        out += str((11 - total % 11) % 10)
    return out


_NUP_FORMATTED = re.compile(r"(\d{5})\.(\d{6})/(\d{4})-(\d{2})")


def validate_br_nup(value):
    """The Número Único de Protocolo of the federal government: the code of the unit, a sequence number,
    the year and two check digits, as 99903.000615/2016-03 or 17 digits (99903000615201603)."""
    text = str(value).strip()
    match = _NUP_FORMATTED.fullmatch(text)
    digits = "".join(match.groups()) if match else text
    if not re.fullmatch(r"\d{17}", digits):
        return False
    year = int(digits[11:15])
    return 1900 <= year <= 2099 and _nup_dv(digits[:15]) == digits[15:]


def validate_br_nup_number(value):
    """A NUP, or its part after the code of the unit as the Banco Central do Brasil lists its documents
    (029358/2019-39: sequence number, year, check digits)."""
    text = str(value).strip()
    if validate_br_nup(text):
        return True
    match = re.fullmatch(r"\d{6}/(\d{4})-\d{2}", text)
    return bool(match) and 1900 <= int(match.group(1)) <= 2099


_TCU_PROCESS = re.compile(r"(?:TC[\s-]*)?(\d{3})\.(\d{3})/((?:19|20)\d{2})-(\d)", re.I)


def validate_br_tcu_process_number(value):
    """A process number of the Tribunal de Contas da União: TC 005.291/2021-6 (also without TC)."""
    return bool(_TCU_PROCESS.fullmatch(str(value).strip()))


def validate_br_tcu_process_number_tc(value):
    """A TCU process number with its TC prefix: TC 005.291/2021-6, TC-036.817/2018-0."""
    text = str(value).strip()
    return text[:2].upper() == "TC" and validate_br_tcu_process_number(text)


_TCU_RULING = re.compile(
    r"(?:ac[oó]rd[aã]o\s+(?:n[ºo°.]*\s*)?)?(\d{1,5})/((?:19|20)\d{2})\s*[-–]\s*(?:tcu\s*[-–]\s*)?"
    r"(?:plen[aá]rio|(?:1|2)[ªa°º]?\s*c[aâ]mara|primeira\s+c[aâ]mara|segunda\s+c[aâ]mara)",
    re.I,
)


def validate_br_tcu_ruling(value):
    """A ruling (acórdão) of the Tribunal de Contas da União: its number, year and the plenary or chamber
    (2726/2023-Plenário, 13262/2023-1ª Câmara, Acórdão 1234/2020 - TCU - Plenário)."""
    return bool(_TCU_RULING.fullmatch(" ".join(str(value).split())))


# --- higher education -----------------------------------------------------------------------------------------


def validate_br_capes_program_code(value):
    """The code of a graduate programme at CAPES: the eight-digit CAPES code of the institution, three
    digits, P and a digit (33003017040P8, 10001018016P2)."""
    text = str(value).strip().upper()
    return bool(re.fullmatch(r"[1-5]\d{10}P\d", text))


def validate_br_capes_institution_code(value):
    """The CAPES code of a higher education institution: eight digits whose first is the region (1 Norte to
    5 Centro-Oeste): 33003017 UNICAMP, 10001018 UNIR, 40001016 UFPR."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return bool(re.fullmatch(r"[1-5]\d{7}", text))


def validate_br_emec_institution_code(value):
    """The code of a higher education institution in e-MEC, the register of the Ministry of Education:
    a number of one to six digits (699, 1, 23412)."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return bool(re.fullmatch(r"[1-9]\d{0,5}", text))


CAPES_EVALUATION_AREAS = (
    "Matemática / Probabilidade e Estatística", "Ciência da Computação", "Astronomia / Física", "Química",
    "Geociências", "Ciências Biológicas I", "Biodiversidade", "Ciências Biológicas II", "Ciências Biológicas III",
    "Engenharias I", "Artes", "Engenharias II", "Engenharias III", "Engenharias IV", "Medicina I", "Medicina II",
    "Medicina III", "Odontologia", "Farmácia", "Enfermagem", "Educação Física", "Saúde Coletiva",
    "Zootecnia / Recursos Pesqueiros", "Medicina Veterinária", "Ciência de Alimentos", "Direito",
    "Administração Pública e de Empresas, Ciências Contábeis e Turismo", "Economia",
    "Arquitetura, Urbanismo e Design", "Planejamento Urbano e Regional / Demografia", "Comunicação e Informação",
    "Serviço Social", "Filosofia", "Sociologia", "Antropologia / Arqueologia", "Geografia", "Psicologia",
    "Educação", "Ciência Política e Relações Internacionais", "História", "Linguística e Literatura",
    "Ciências Agrárias I", "Ciências da Religião e Teologia", "Interdisciplinar", "Ensino", "Materiais",
    "Biotecnologia", "Ciências Ambientais", "Nutrição",
    # Names before the 2017 evaluation
    "Letras / Linguística", "Administração, Ciências Contábeis e Turismo", "Ciências Sociais Aplicadas I",
    "Filosofia / Teologia: subcomissão Filosofia", "Filosofia / Teologia: subcomissão Teologia",
    "Engenharias", "Arquitetura e Urbanismo", "Ensino de Ciências e Matemática", "Ciências Agrárias",
    "Ciências Biológicas", "Planejamento Urbano e Regional", "Educação Física, Fisioterapia, Fonoaudiologia",
    "Teologia", "Filosofia/Teologia",
)
_CAPES_AREAS = {re.sub(r"\s*/\s*", "/", _fold(area)) for area in CAPES_EVALUATION_AREAS}


def validate_br_capes_evaluation_area(value):
    """One of the 49 evaluation areas of CAPES (ENGENHARIAS III, CIÊNCIAS BIOLÓGICAS I, ASTRONOMIA / FÍSICA,
    INTERDISCIPLINAR), also the names used before the 2017 evaluation (LETRAS / LINGUÍSTICA)."""
    return re.sub(r"\s*/\s*", "/", _fold(value)) in _CAPES_AREAS


def validate_br_capes_grade(value):
    """A CAPES grade (conceito) of a graduate programme: 1 to 7, or A for a programme not yet graded."""
    text = str(value).strip().upper()
    if text.endswith(".0"):
        text = text[:-2]
    return text in {"1", "2", "3", "4", "5", "6", "7", "A"}


# --- companies --------------------------------------------------------------------------------------------------

_COMPANY_SIZES = {
    "micro", "microempresa", "micro empresa", "pequena", "pequena empresa", "empresa de pequeno porte", "media",
    "media empresa", "grande", "grande empresa", "me", "epp", "mei", "microempreendedor individual", "demais",
    "media-grande", "media grande", "pessoa fisica", "micro empresa (me)", "empresa de pequeno porte (epp)",
}


def validate_br_company_size(value):
    """The size class (porte) of a Brazilian company: MICRO, PEQUENA, MÉDIA, GRANDE, also ME, EPP, MEI,
    Microempresa, Empresa de Pequeno Porte, Demais. The sizes of municipalities (Pequeno 1, Metrópole) fail."""
    return _fold(value) in _COMPANY_SIZES


# --- biomes ---------------------------------------------------------------------------------------------------------

_BIOMES = {"amazonia", "caatinga", "cerrado", "mata atlantica", "pampa", "pantanal"}


def validate_br_biome(value):
    """One of the six biomes of Brazil (Amazônia, Caatinga, Cerrado, Mata Atlântica, Pampa, Pantanal), or
    several of them as the CNCFlora lists them (Amazônia, Mata Atlântica, Cerrado)."""
    parts = [p.strip() for p in re.split(r"[,;/|]| e ", _fold(value))]
    return bool(parts) and all(p in _BIOMES for p in parts)
