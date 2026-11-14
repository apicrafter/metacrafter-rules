"""INDEC census geography of Argentina, found in the files of the statistics office of the province
of Córdoba (Dirección General de Estadística y Censos, datosestadistica.cba.gov.ar) in
metacrafter-testdata: census radius and fraction codes (nine and seven digits, or the radius and
fraction numbers alone), radius types (urbano, rural, mixto), the department, locality and local
government parts of the INDEC codes in columns of their own (PROV 14, CODDEPTO 098, CODLOC 050,
COD_MUNI 0196) and department names.

The codes nest: province (2 digits) + department (3) + fraction (2) + radius (2) is the nine-digit
radius code 140070101 (LINK of the INDEC census cartography). Department parts are mostly multiples
of seven (007 Calamuchita, 014 Capital); the validators of full codes check the department against
the georef list, so that a nine-digit number with a province prefix is not taken for a radius.
"""
import re
import unicodedata

from metacrafterext.rules.ar_country.codes import INDEC_PROVINCES

# departments:start (scripts/update_ar_departments.py, 529 departments of georef)
_GEOREF_DEPARTMENT_CODES = """
    02007 02014 02021 02028 02035 02042 02049 02056 02063 02070 02077 02084 02091 02098 02105
    06007 06014 06021 06028 06035 06042 06049 06056 06063 06070 06077 06084 06091 06098 06105
    06112 06119 06126 06134 06140 06147 06154 06161 06168 06175 06182 06189 06196 06203 06210
    06218 06224 06231 06238 06245 06252 06260 06266 06270 06274 06277 06280 06287 06294 06301
    06308 06315 06322 06329 06336 06343 06351 06357 06364 06371 06385 06392 06399 06406 06408
    06410 06412 06413 06420 06427 06434 06441 06448 06455 06462 06466 06469 06476 06483 06490
    06497 06505 06511 06515 06518 06525 06532 06539 06547 06553 06560 06568 06574 06581 06588
    06595 06602 06609 06616 06623 06630 06638 06644 06648 06651 06655 06658 06665 06672 06679
    06686 06693 06700 06707 06714 06721 06728 06735 06742 06749 06756 06760 06763 06770 06778
    06784 06791 06798 06805 06812 06819 06826 06833 06840 06847 06854 06861 06868 06875 06882
    10007 10014 10021 10028 10035 10042 10049 10056 10063 10070 10077 10084 10091 10098 10105
    10112 14007 14014 14021 14028 14035 14042 14049 14056 14063 14070 14077 14084 14091 14098
    14105 14112 14119 14126 14133 14140 14147 14154 14161 14168 14175 14182 18007 18014 18021
    18028 18035 18042 18049 18056 18063 18070 18077 18084 18091 18098 18105 18112 18119 18126
    18133 18140 18147 18154 18161 18168 18175 22007 22014 22021 22028 22036 22039 22043 22049
    22056 22063 22070 22077 22084 22091 22098 22105 22112 22119 22126 22133 22140 22147 22154
    22161 22168 26007 26014 26021 26028 26035 26042 26049 26056 26063 26070 26077 26084 26091
    26098 26105 30008 30015 30021 30028 30035 30042 30049 30056 30063 30070 30077 30084 30088
    30091 30098 30105 30113 34007 34014 34021 34028 34035 34042 34049 34056 34063 38007 38014
    38021 38028 38035 38042 38049 38056 38063 38070 38077 38084 38094 38098 38105 38112 42007
    42014 42021 42028 42035 42042 42049 42056 42063 42070 42077 42084 42091 42098 42105 42112
    42119 42126 42133 42140 42147 42154 46007 46014 46021 46028 46035 46042 46049 46056 46063
    46070 46077 46084 46091 46098 46105 46112 46119 46126 50007 50014 50021 50028 50035 50042
    50049 50056 50063 50070 50077 50084 50091 50098 50105 50112 50119 50126 54007 54014 54021
    54028 54035 54042 54049 54056 54063 54070 54077 54084 54091 54098 54105 54112 54119 58007
    58014 58021 58028 58035 58042 58049 58056 58063 58070 58077 58084 58091 58098 58105 58112
    62007 62014 62021 62028 62035 62042 62049 62056 62063 62070 62077 62084 62091 66007 66014
    66021 66028 66035 66042 66049 66056 66063 66070 66077 66084 66091 66098 66105 66112 66119
    66126 66133 66140 66147 66154 66161 70007 70014 70021 70028 70035 70042 70049 70056 70063
    70070 70077 70084 70091 70098 70105 70112 70119 70126 70133 74007 74014 74021 74028 74035
    74042 74049 74056 74063 78007 78014 78021 78028 78035 78042 78049 82007 82014 82021 82028
    82035 82042 82049 82056 82063 82070 82077 82084 82091 82098 82105 82112 82119 82126 82133
    86007 86014 86021 86028 86035 86042 86049 86056 86063 86070 86077 86084 86091 86098 86105
    86112 86119 86126 86133 86140 86147 86154 86161 86168 86175 86182 86189 90007 90014 90021
    90028 90035 90042 90049 90056 90063 90070 90077 90084 90091 90098 90105 90112 90119 94008
    94011 94015 94021 94028
"""
_GEOREF_DEPARTMENT_NAMES = """
    1 de mayo
    12 de octubre
    2 de abril
    25 de mayo
    9 de julio
    adolfo alsina
    adolfo gonzales chaves
    aguirre
    albardon
    alberdi
    alberti
    almirante brown
    alumine
    ambato
    ancasti
    andalgala
    anelo
    angaco
    angel vicente penaloza
    anta
    antartida argentina
    antofagasta de la sierra
    apostoles
    arauco
    arrecifes
    atamisqui
    atreuco
    avellaneda
    ayacucho
    azul
    bahia blanca
    balcarce
    banda
    baradero
    bariloche
    belen
    belgrano
    bella vista
    benito juarez
    berazategui
    berisso
    bermejo
    beron de astrada
    biedma
    bolivar
    bragado
    brandsen
    burruyacu
    cachi
    cafayate
    cainguas
    calamuchita
    caleu caleu
    calingasta
    campana
    candelaria
    canuelas
    capayan
    capital
    capitan sarmiento
    carlos casares
    carlos tejedor
    carmen de areco
    caseros
    castellanos
    castelli
    castro barros
    catan lil
    catrilo
    caucete
    cerrillos
    chacabuco
    chalileo
    chamical
    chapaleufu
    chascomus
    chical co
    chicligasta
    chicoana
    chilecito
    chimbas
    chivilcoy
    chos malal
    choya
    cochinoca
    collon cura
    colon
    comandante fernandez
    comuna 1
    comuna 10
    comuna 11
    comuna 12
    comuna 13
    comuna 14
    comuna 15
    comuna 2
    comuna 3
    comuna 4
    comuna 5
    comuna 6
    comuna 7
    comuna 8
    comuna 9
    concepcion
    concordia
    conesa
    confluencia
    conhelo
    constitucion
    copo
    coronel de marina leonardo rosales
    coronel dorrego
    coronel pringles
    coronel suarez
    corpen aike
    cruz alta
    cruz del eje
    curaco
    curuzu cuatia
    cushamen
    daireaux
    deseado
    diamante
    dolores
    dr manuel belgrano
    el alto
    el carmen
    el cuy
    eldorado
    empedrado
    ensenada
    escalante
    escobar
    esquina
    esteban echeverria
    exaltacion de la cruz
    ezeiza
    famailla
    famatina
    federacion
    federal
    feliciano
    figueroa
    florencio varela
    florentino ameghino
    formosa
    fray justo santa maria de oro
    fray mamerto esquiu
    futaleufu
    gaiman
    garay
    gastre
    general alvarado
    general alvear
    general arenales
    general belgrano
    general donovan
    general felipe varela
    general guemes
    general guido
    general jose de san martin
    general juan facundo quiroga
    general juan madariaga
    general la madrid
    general lamadrid
    general las heras
    general lavalle
    general lopez
    general manuel belgrano
    general obligado
    general ortiz de ocampo
    general paz
    general pedernera
    general pinto
    general pueyrredon
    general roca
    general rodriguez
    general san martin
    general taboada
    general viamonte
    general villegas
    gobernador dupuy
    godoy cruz
    goya
    graneros
    guachipas
    gualeguay
    gualeguaychu
    guamini
    guarani
    guasayan
    guatrache
    guaymallen
    guer aike
    hipolito yrigoyen
    hucal
    huiliches
    humahuaca
    hurlingham
    iglesia
    iguazu
    independencia
    iriondo
    iruya
    ischilin
    islas del atlantico sur
    islas del ibicuy
    itati
    ituzaingo
    jachal
    jimenez
    jose c paz
    juan bautista alberdi
    juan felipe ibarra
    juan martin de pueyrredon
    juarez celman
    junin
    la caldera
    la candelaria
    la capital
    la cocha
    la costa
    la matanza
    la paz
    la plata
    la poma
    la vina
    lacar
    lago argentino
    lago buenos aires
    laishi
    languineo
    lanus
    laprida
    las colonias
    las flores
    las heras
    lavalle
    leales
    leandro n alem
    ledesma
    lezama
    libertad
    libertador general san martin
    lihuel calel
    limay mahuida
    lincoln
    loberia
    lobos
    lomas de zamora
    loncopue
    loreto
    los andes
    los lagos
    loventue
    lujan
    lujan de cuyo
    lules
    magallanes
    magdalena
    maipu
    malargue
    malvinas argentinas
    mar chiquita
    maraco
    marcos juarez
    marcos paz
    martires
    matacos
    mayor luis j fontana
    mburucuya
    mercedes
    merlo
    metan
    minas
    mitre
    molinos
    monte
    monte caseros
    monte hermoso
    montecarlo
    monteros
    moreno
    moron
    navarro
    necochea
    nogoya
    norquin
    norquinco
    o'higgins
    obera
    ojo de agua
    olavarria
    oran
    paclin
    palpala
    parana
    paso de indios
    paso de los libres
    patagones
    patino
    pehuajo
    pehuenches
    pellegrini
    pergamino
    pichi mahuida
    picun leufu
    picunches
    pila
    pilagas
    pilar
    pilcaniyeu
    pilcomayo
    pinamar
    pirane
    pocho
    pocito
    poman
    presidencia de la plaza
    presidente peron
    presidente roque saenz pena
    puan
    puelen
    punilla
    punta indio
    quebrachos
    quemu quemu
    quilmes
    quitilipi
    ramallo
    ramon lista
    rancul
    rauch
    rawson
    realico
    rinconada
    rio chico
    rio cuarto
    rio grande
    rio hondo
    rio primero
    rio seco
    rio segundo
    rio senguer
    rivadavia
    robles
    rojas
    roque perez
    rosario
    rosario de la frontera
    rosario de lerma
    rosario vera penaloza
    saavedra
    saladas
    saladillo
    salavina
    salliquelo
    salto
    san alberto
    san andres de giles
    san antonio
    san antonio de areco
    san blas de los sauces
    san carlos
    san cayetano
    san cosme
    san cristobal
    san fernando
    san ignacio
    san isidro
    san javier
    san jeronimo
    san justo
    san lorenzo
    san luis del palmar
    san martin
    san miguel
    san nicolas
    san pedro
    san rafael
    san roque
    san salvador
    san vicente
    sanagasta
    santa barbara
    santa catalina
    santa lucia
    santa maria
    santa rosa
    santa victoria
    santo tome
    sargento cabral
    sarmiento
    sauce
    silipica
    simoca
    sobremonte
    suipacha
    susques
    tafi del valle
    tafi viejo
    tala
    tandil
    tapalque
    tapenaga
    tehuelches
    telsen
    tercero arriba
    tigre
    tilcara
    tinogasta
    toay
    tolhuin
    tordillo
    tornquist
    totoral
    trancas
    trenel
    trenque lauquen
    tres arroyos
    tres de febrero
    tres lomas
    tulumba
    tumbaya
    tunuyan
    tupungato
    ullum
    union
    uruguay
    ushuaia
    utracan
    valcheta
    valle fertil
    valle grande
    valle viejo
    vera
    vicente lopez
    victoria
    villa gesell
    villaguay
    villarino
    vinchina
    yavi
    yerba buena
    zapala
    zarate
    zonda
"""
# departments:end

# Codes of census files of earlier years that georef no longer uses: the comunas of the City of
# Buenos Aires as 02001 to 02015 (georef: 02007 to 02105), and Río Grande 94007 and Ushuaia 94014 of
# Tierra del Fuego before Tolhuin became a department in 2017 (georef: 94008, 94015).
_OLDER_DEPARTMENT_CODES = ["02%03d" % i for i in range(1, 16)] + ["94007", "94014"]

DEPARTMENT_CODES = frozenset(_GEOREF_DEPARTMENT_CODES.split()) | frozenset(_OLDER_DEPARTMENT_CODES)
# The three-digit department parts as numbers: 7 for 007, 98 for 098.
DEPARTMENT_PARTS = frozenset(int(code[2:]) for code in DEPARTMENT_CODES)


def _digits(value):
    """The text of value without surrounding spaces and a float's trailing .0."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return text


def _full_code(value, width):
    """The digits of a code that nests in a department (radius 9, fraction 7 digits), padded when
    the leading zero of the province was dropped; None unless the department is known."""
    text = _digits(value)
    if not text.isdigit() or len(text) not in (width - 1, width):
        return None
    text = text.zfill(width)
    return text if text[:5] in DEPARTMENT_CODES else None


def _number(value, max_digits, lowest=1):
    """The number of a short code (a radius or fraction number alone, 01, 7, 001), or None."""
    text = _digits(value)
    if not text.isdigit() or len(text) > max_digits:
        return None
    number = int(text)
    return number if number >= lowest else None


def validate_ar_indec_census_radius_link(value):
    """A nine-digit census radius code of a known department, fraction and radius not 00:
    140070101, 020010101 (2010 comuna numbering), or 20010101 without the leading zero."""
    code = _full_code(value, 9)
    return code is not None and code[5:7] != "00" and code[7:] != "00"


def validate_ar_indec_census_radius_code(value):
    """A census radius code (140070101) or the radius number alone in a RADIO column (01, 7, 23)."""
    return validate_ar_indec_census_radius_link(value) or _number(value, 2) is not None


def validate_ar_indec_census_fraction_code(value):
    """A seven-digit census fraction code (1400701) or the fraction number alone (01, 27, 001)."""
    code = _full_code(value, 7)
    if code is not None:
        return code[5:] != "00"
    return _number(value, 3) is not None


RADIUS_TYPES = frozenset(("u", "r", "m", "urbano", "rural", "mixto"))


def validate_ar_indec_census_radius_type(value):
    """A census radius type: U, R, M (urbano, rural, mixto), or the word."""
    return str(value).strip().lower() in RADIUS_TYPES


def validate_ar_indec_department_part(value):
    """The department part of an INDEC code alone (098, 007, 7 without the zeros), or a full
    department code (14098, 06014)."""
    text = _digits(value)
    if not text.isdigit():
        return False
    if len(text) <= 3:
        return int(text) in DEPARTMENT_PARTS
    return len(text) in (4, 5) and text.zfill(5) in DEPARTMENT_CODES


def validate_ar_indec_locality_part(value):
    """The three-digit locality part of an INDEC census locality code alone (050, 010; 000 for a
    radius outside any locality)."""
    text = _digits(value)
    return len(text) == 3 and text.isdigit()


def validate_ar_indec_local_government_part(value):
    """The four-digit part of an INDEC local government code alone (0196, 2630, 7 without the
    zeros), or a full six-digit code (140196)."""
    text = _digits(value)
    if not text.isdigit():
        return False
    if len(text) <= 4:
        return int(text) > 0
    return len(text) in (5, 6) and text.zfill(6)[:2] in INDEC_PROVINCES


def _norm(name):
    text = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode().lower()
    return " ".join(text.replace(".", " ").replace(",", " ").split())


DEPARTMENT_NAMES = frozenset(_GEOREF_DEPARTMENT_NAMES.split("\n")) - {""}
DEPARTMENT_NAMES = frozenset(n.strip() for n in DEPARTMENT_NAMES)
_NAMES_BY_LENGTH = {}
for _name in DEPARTMENT_NAMES:
    _NAMES_BY_LENGTH.setdefault(len(_name.split()), []).append(_name.split())

# Abbreviations of provincial tables: Gral. San Martín, Pte. Roque S. Peña, Cnel. Pringles.
_ABBREVIATIONS = {
    "gral": "general", "pte": "presidente", "pdte": "presidente", "cnel": "coronel", "dr": "doctor",
    "tte": "teniente", "gdor": "gobernador", "cmte": "comandante", "sgto": "sargento", "ing": "ingeniero",
    "sta": "santa", "sto": "santo", "pto": "puerto",
}
_PREFIX = re.compile(r"^(?:departamento|depto|dpto|partido(?: de)?|comuna)\s+")


def validate_ar_department_name(value):
    """The name of an Argentine department, as written in national and provincial tables:
    Calamuchita, RIO CUARTO, Gral. San Martín, Pte. Roque S. Peña, Departamento Capital, Comuna 1
    (not Total Provincia or a code)."""
    words = _norm(value)
    if not words or words.isdigit():
        return False
    if words in DEPARTMENT_NAMES:
        return True
    stripped = words if words.startswith("comuna ") else _PREFIX.sub("", words)
    tokens = [_ABBREVIATIONS.get(t, t) for t in stripped.split()]
    if " ".join(tokens) in DEPARTMENT_NAMES:
        return True
    # Initials (Pte. Roque S. Peña): a one-letter word stands for any word with that letter.
    if any(len(t) == 1 for t in tokens):
        for name in _NAMES_BY_LENGTH.get(len(tokens), ()):
            if all(t == w or (len(t) == 1 and w.startswith(t)) for t, w in zip(tokens, name)):
                return True
    return False
