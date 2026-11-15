"""Validators for the open data of the province of Mendoza, Argentina (datosabiertos.mendoza.gov.ar):
the districts of its departments, the school numbers of the Dirección General de Escuelas, the
classifiers of the provincial budget (economic classification of expenditure, financing sources,
resource accounts, accounting units), the numbers of the administrative files before GDE, the
electricity distributors of Argentina and the categories of hazardous waste of Ley 24.051.

Found in a 2024 snapshot of Datos Abiertos Mendoza (Dateno source cdi00000026) for
metacrafter-testdata.
"""
import re
import unicodedata


def _norm(value):
    """Lower case, no accents, punctuation as spaces, single spaces."""
    text = unicodedata.normalize("NFKD", str(value).strip().lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(re.sub(r"[^\w]+", " ", text).split())


# ---------------------------------------------------------------- districts of Mendoza
# The districts (distritos) of the 18 departments, from the locality layer of the provincial
# environment secretariat (localidades-de-la-provincia-de-mendoza) and the district lists of
# the departments. The head town of each department is the district Ciudad; tables write it as
# the department name too, so the department names are districts here.
_DEPARTMENTS = (
    "capital", "general alvear", "godoy cruz", "guaymallen", "junin", "la paz", "las heras", "lavalle",
    "lujan de cuyo", "lujan", "maipu", "malargue", "rivadavia", "san carlos", "san martin", "san rafael",
    "santa rosa", "tunuyan", "tupungato",
)
_DISTRICTS = frozenset(_DEPARTMENTS + (
    "ciudad",
    # General Alvear
    "alvear oeste", "bowen", "carmensa", "san pedro del atuel", "corral de lorca", "colonia alvear",
    "los compartos",
    # Godoy Cruz
    "gobernador benegas", "las tortugas", "presidente sarmiento", "san francisco del monte", "trapiche",
    "villa marini", "villa hipodromo", "villa del parque",
    # Guaymallén
    "belgrano", "general belgrano", "bermejo", "buena nueva", "capilla del rosario", "colonia segovia",
    "dorrego", "el sauce", "jesus nazareno", "kilometro 8", "kilometro 11", "la primavera", "las canas",
    "los corralitos", "nueva ciudad", "pedro molina", "puente de hierro", "rodeo de la cruz", "san jose",
    "villa nueva",
    # Junín
    "algarrobo grande", "alto verde", "el mirador", "ingeniero giagnoni", "la colonia", "los barriales",
    "medrano", "mundo nuevo", "philips", "phillips", "rodriguez pena",
    # La Paz
    "desaguadero", "villa antigua",
    # Las Heras
    "capdevila", "capdeville", "el algarrobal", "el borbollon", "el challao", "el pastal", "el plumerillo",
    "el resguardo", "el zapallar", "la cieneguita", "la cienaguita", "las cuevas", "panquehua", "panqueua",
    "sierras de encalada", "uspallata",
    # Lavalle
    "villa tulumaya", "tulumaya", "costa de araujo", "el carmen", "el plumero", "el vergel", "gustavo andre",
    "ingeniero gustavo andre", "jocoli", "jocoli viejo", "la asuncion", "asuncion", "la holanda", "la palmera",
    "la pega", "las violetas", "paramillo", "san francisco", "san miguel", "tres de mayo", "3 de mayo",
    "lagunas del rosario", "laguna del rosario",
    # Luján de Cuyo
    "agrelo", "carrodilla", "chacras de coria", "el carrizal", "la puntilla", "las compuertas",
    "mayor drummond", "perdriel", "potrerillos", "ugarteche", "vistalba", "cacheuta",
    # Maipú
    "barrancas", "las barrancas", "coquimbito", "cruz de piedra", "fray luis beltran", "general gutierrez",
    "general ortega", "lunlunta", "luzuriaga", "rodeo del medio", "russell", "russel", "san roque",
    # Malargüe
    "agua escondida", "rio barrancas", "rio grande",
    # Rivadavia
    "andrade", "la central", "la libertad", "los arboles", "los campamentos", "los huarpes", "reduccion",
    "santa maria de oro", "san isidro",
    # San Carlos
    "villa san carlos", "chilecito", "eugenio bustos", "la consulta", "pareditas", "tres esquinas",
    # San Martín
    "alto salvador", "buen orden", "chapanay", "chivilcoy", "el central", "el divisadero", "el espino",
    "el ramblon", "las chimbas", "montecaseros", "nueva california", "palmira", "tres portenas",
    # San Rafael
    "25 de mayo", "veinticinco de mayo", "villa 25 de mayo", "canada seca", "cuadro benegas",
    "cuadro nacional", "el cerrito", "el nihuil", "el sosneado", "goudge", "jaime prats", "la llave",
    "las malvinas", "las paredes", "monte coman", "punta del agua", "punta de agua", "rama caida",
    "real del padre", "salto de las rosas", "villa atuel",
    # Santa Rosa
    "12 de octubre", "doce de octubre", "villa santa rosa", "la dormida", "las catitas", "nacunan",
    "villa cabecera",
    # Tunuyán
    "campo de los andes", "campo los andes", "colonia las rosas", "el totoral", "las pintadas",
    "los chacales", "los sauces", "villa seca", "vista flores", "los chayanes",
    # Tupungato
    "anchoris", "cordon del plata", "el peral", "el zampal", "el zampalito", "la arboleda", "santa clara",
    "villa bastias", "zapata", "villa de tupungato",
))
_DISTRICT_ABBREVIATIONS = {
    "va": "villa", "gdor": "gobernador", "gral": "general", "ing": "ingeniero", "pte": "presidente",
    "cnel": "coronel", "km": "kilometro", "sta": "santa", "cdad": "ciudad", "pdte": "presidente",
}
# The twelve sections of the Capital, by number or ordinal and with their names (Segunda Sección,
# 2° Sección, Sección 4ta, 4ª Sección Área Fundacional, Decima Seccion).
_ORDINALS = ("primera", "segunda", "tercera", "cuarta", "quinta", "sexta", "septima", "setima", "octava",
             "novena", "decima", "undecima", "decimoprimera", "duodecima", "decimosegunda")
_SECTION = re.compile(
    r"^(?:(?:(?:1[0-2]|[1-9])\s*(?:a|ra|da|ta|va|na|o|er|do|to)?|" + "|".join(_ORDINALS) + r")\s+seccion|"
    r"seccion\s+(?:(?:1[0-2]|[1-9])\s*(?:a|ra|da|ta|va|na|o)?|" + "|".join(_ORDINALS) + r"))(?:\s+[a-z ]+)?$")
# "San José (G)", "La Primavera (T)": the initial of the department of a district name that two
# departments share; "Medrano (R)".
_DEPARTMENT_INITIAL = re.compile(r"\s+[a-z]$")


def validate_ar_mendoza_district(value):
    """A district of a department of Mendoza: Rodeo de la Cruz, EL PLUMERILLO, Va. Hipódromo,
    San José (G), Ciudad de San Martín, Segunda Sección (not a barrio, a code or Total)."""
    text = _norm(value)
    if not text or text.isdigit():
        return False
    text = _DEPARTMENT_INITIAL.sub("", text)
    words = [_DISTRICT_ABBREVIATIONS.get(w, w) for w in text.split()]
    if words and words[0] == "distrito":
        words = words[1:]
    text = " ".join(words)
    if text in _DISTRICTS or _SECTION.match(text):
        return True
    for prefix in ("ciudad de ", "villa de ", "ciudad "):
        if text.startswith(prefix) and text[len(prefix):] in _DISTRICTS:
            return True
    return False


# ---------------------------------------------------------------- school numbers
# A digit for the level or kind of school (0 kindergartens, 1 primary, 2 special, 3 adults,
# 4 secondary, 8 vocational, 9 higher education) or a letter of the private and other schools
# (P private primary, PS / S private secondary, T higher, C and J kindergartens, Z schools of the
# Universidad Nacional de Cuyo), then three digits: 4-013, P-131, PS-046, P113.
_SCHOOL_NUMBER = re.compile(r"^(?:[0-9]|P|PS|PT|S|T|C|J|Z)-?\d{3}$")


def validate_ar_mendoza_school_number(value):
    """A school number of the Dirección General de Escuelas of Mendoza: 4-013, 1-123, P-131,
    PS-046, P113, 1152 (not a CUE of seven digits or 12-345)."""
    text = str(value).strip().upper().replace(" ", "")
    return bool(_SCHOOL_NUMBER.match(text))


# ---------------------------------------------------------------- electricity distributors
# Provincial distribution companies and concessionaires (the acronyms the regulators use).
_DISTRIBUTOR_ACRONYMS = frozenset((
    "edemsa", "edeste", "edestesa", "edenor", "edesur", "edelap", "edea", "eden", "edes", "epec", "epe",
    "epesf", "edet", "ejesa", "ejsedsa", "edesa", "edesal", "edecat", "edelar", "edese", "refsa",
    "secheep", "emsa", "enersa", "epen", "edersa", "dpec", "apelp", "spse", "esj", "cecsagal", "cospac",
))
_DISTRIBUTOR_NAMES = frozenset((
    "energia san juan", "energia de misiones", "empresa provincial de la energia de santa fe",
    "empresa provincial de energia de cordoba", "empresa distribuidora de electricidad de mendoza",
    "distribuidora de electricidad del este",
))
# Electricity cooperatives of Mendoza by their town, as the EPRE tables name them alone.
_COOPERATIVE_TOWNS = frozenset((
    "godoy cruz", "alto verde", "alto verde y algarrobo grande", "popular rivadavia", "pop rivadavia",
    "sud rio tunuyan", "bowen", "cospac de bowen", "cospac bowen", "monte coman", "medrano", "santa rosa",
    "cecsagal", "electrica de godoy cruz",
))
_COOPERATIVE = re.compile(r"^(?:coop(?:erativa)?)\b\s*(?:de\s+)?(?:electricidad\s+|electrica\s+)?(?:de\s+)?(.+)$")


def _distributor_key(value):
    """The normalized name, and acronyms written with dots joined (E.D.E.M.S.A. -> edemsa)."""
    text = _norm(value)
    return text, text.replace(" ", "") if re.fullmatch(r"(?:[a-z] )+[a-z]", text) else text


def validate_ar_electricity_distributor(value):
    """An Argentine electricity distributor by its acronym or as a cooperative: EDEMSA, E.D.E.M.S.A.,
    EDENOR, Coop. Godoy Cruz, Cooperativa Eléctrica de Godoy Cruz (not CAMMESA or a town alone)."""
    text, compact = _distributor_key(value)
    if not text:
        return False
    if text in _DISTRIBUTOR_ACRONYMS or compact in _DISTRIBUTOR_ACRONYMS or text in _DISTRIBUTOR_NAMES:
        return True
    match = _COOPERATIVE.match(text)
    if match:
        rest = match.group(1)
        return bool(rest) and not rest.isdigit()
    return False


def validate_ar_electricity_distributor_name(value):
    """An electricity distributor in a distribuidora field: also the cooperatives of Mendoza by
    their town alone (GODOY CRUZ, ALTO VERDE, SUD RIO TUNUYAN, MONTE COMAN)."""
    if validate_ar_electricity_distributor(value):
        return True
    return _norm(value) in _COOPERATIVE_TOWNS


# ---------------------------------------------------------------- budget classifiers
_ECONOMIC = re.compile(r"^([4-7])\d{4}(?:\s*-\s*|\s+)([A-Za-zÁÉÍÓÚÑáéíóúñ].*)$")
# The first words of the items of expenditure (41101 PERSONAL PERMANENTE, 41310 SERVICIOS
# PUBLICOS, 74102 AMORTIZACION DEUDA ACREEDORES VARIOS, 51201 TRABAJOS PUBLICOS).
_ECONOMIC_WORDS = frozenset((
    "personal", "bienes", "servicios", "serv", "trabajos", "locaciones", "aportes", "aporte", "credito",
    "alquiler", "alquileres", "gastos", "otros", "otras", "convenios", "sueldos", "acreedores", "residuos",
    "transferencias", "transferencia", "transf", "cont", "contrib", "contribuciones", "prestamos", "contratos",
    "contrat", "inversion", "inversiones", "pasivos", "remesas", "prestac", "prestaciones", "intereses",
    "juicios", "construccion", "construcciones", "terrenos", "part", "obras", "asignacion", "asignaciones",
    "participacion", "subsidios", "erogaciones", "indemnizaciones", "pasividades", "edificios", "aumento",
    "gratificacion", "amortizacion", "amort", "activos", "deuda", "honorarios", "becas",
))


def validate_ar_mendoza_economic_classification(value):
    """An item of the economic classification of expenditure of the budget of Mendoza with its
    code: 41101 PERSONAL PERMANENTE, 41100 - PERSONAL, 74102 AMORTIZACION DEUDA (not 1110100000-...)."""
    return bool(_ECONOMIC.match(str(value).strip()))


def validate_ar_mendoza_economic_classification_value(value):
    """An item of the economic classification whose first word is one of the items: for value
    rules that run on any field (12345 MAIN STREET is not one)."""
    match = _ECONOMIC.match(str(value).strip())
    if not match or match.group(1) == "6":
        return False
    first = _norm(match.group(2)).split()
    return bool(first) and first[0] in _ECONOMIC_WORDS


_FINANCING = re.compile(r"^\d{1,3}(?:\s*-\s*|\s+)[A-Za-zÁÉÍÓÚÑáéíóúñ][^\d].{1,}$")


def validate_ar_mendoza_financing_source(value):
    """A financing source of the budget of Mendoza with its code: 0 Rentas Generales, 000 - Rentas
    Generales, 21 Tasa de Justicia, 186 Impuesto p/I.Brutos afec.a Bib.Popul (not 2019/01 or a code
    alone)."""
    return bool(_FINANCING.match(str(value).strip()))


_RESOURCE = re.compile(r"^(?:\d{5}\s+)?[1-3]\d{9}\s*-\s*[A-Za-zÁÉÍÓÚÑáéíóúñ]")


def validate_ar_mendoza_resource_account(value):
    """A resource account of the budget of Mendoza with its name: 1110100000-IMPUESTO SOBRE LAS
    ACTIVIDADES, 1120202000 - INT. GANADOS PRESTAMOS, 90604 1110101000-Impuesto sobre los ingresos
    brutos (not a number alone)."""
    return bool(_RESOURCE.match(str(value).strip()))


_CUC = re.compile(r"^\d{3}(?:\s*-\s*[A-Za-zÁÉÍÓÚÑáéíóúñ].*)?$")


def validate_ar_mendoza_cuc(value):
    """An accounting unit of the public sector of Mendoza: 906-Administración Central, 259-Hospital
    Central, or the three digits alone (not 0 Rentas Generales)."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return bool(_CUC.match(text))


# ---------------------------------------------------------------- administrative files
# Number, initial, year (two or four digits; one file of the civil service competitions has a
# typing error, 20169) and the office of five digits, after hyphens or slashes. A cell may go on
# with the files joined to it (1373/G/02/30091 acum. Nº 1219/G/00/03834).
_EXPEDIENTE = re.compile(r"^\d{1,6}\s*([-/])\s*[A-Za-z]\s*\1\s*(?:\d{2}|\d{4,5})(?:\s*\1\s*(\d{4,5}))?(?=$|\s|,|;)")


def validate_ar_mendoza_expediente_number(value):
    """A file number of the government of Mendoza before GDE: 4259-D-2015-03834, 1310/G/07/03834,
    203-D-2014-18007, 3451-N-1943 (not EX-2018-01621874-GDEMZA-DPA#SAYOT or 2018-01-01)."""
    return bool(_EXPEDIENTE.match(str(value).strip()))


def validate_ar_mendoza_expediente_number_with_office(value):
    """A file number with the office of five digits (4259-D-2015-03834), for value rules on any
    field."""
    match = _EXPEDIENTE.match(str(value).strip())
    return bool(match) and bool(match.group(2)) and len(match.group(2)) == 5


# ---------------------------------------------------------------- hazardous waste categories
_WASTE_CODE = re.compile(r"^Y(?:[1-9]|[1-3]\d|4[0-5]|48)$")
_OPERATION_CODE = re.compile(r"^(?:R(?:[1-9]|1[0-3])|D(?:[1-9]|1[0-5]))$")
_WASTE_SPLIT = re.compile(r"\s*(?:[-,;/+]|\s+e\s+|\s+y\s+|\s)\s*")


def validate_ar_hazardous_waste_categories(value):
    """Categories of hazardous waste under control of Ley 24.051, one or several in a cell: Y48,
    Y8-Y9-Y48, Y8, Y9, Y11, Y8 / Y9 / Y48, with the Basel operations R9 or D10 (not free text with
    a code in it, Y46 or Y49)."""
    tokens = [t for t in _WASTE_SPLIT.split(str(value).strip().upper()) if t]
    if not tokens or len(tokens) > 60:
        return False
    if not all(_WASTE_CODE.match(t) or _OPERATION_CODE.match(t) for t in tokens):
        return False
    return any(_WASTE_CODE.match(t) for t in tokens)
