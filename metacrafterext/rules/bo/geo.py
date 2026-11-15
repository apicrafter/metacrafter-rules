"""Bolivian geography found in the Bolivian files of metacrafter-testdata (2024 snapshots of the GeoNode of
the water information system SIARH of the Ministry of Environment and Water, the GeoNode of the Institute of
Geography of the Universidad Mayor de San Andrés and datos.gob.bo): the nine departments, the 112 provinces
and the 339 municipalities of the INE (Censo 2012) by name, and their INE codes, with the INE codes of
communities (localidades).

The INE codes nest: two digits for the department (01 Chuquisaca to 09 Pando), two for the province within
it, two for the municipal section (the municipality) and, for a community, two for the canton and three
for the locality: 02 La Paz, 0201 Murillo, 020105 El Alto, 02010501001. Spreadsheets drop the leading
zero (20105, 40302).

The names come from GIS layers whose text went through several code pages: PotosÃ­ (UTF-8 read as
cp1252), Potos? and Abun� (a lost character), Muńecas (cp1250), ZUDAÃEZ (a lost byte), and from
shapefiles that cut names at 20 characters (General Jose Balliv, Gualberto Villarroe). The validators
repair the first kind and let a lost character stand for any one letter.
"""
import re
import unicodedata

# ------------------------------------------------------------------ text folding
_SPANISH = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ü": "u", "ñ": "n", "à": "a", "è": "e", "ì": "i",
            "ò": "o", "ù": "u"}
_PUNCT = re.compile(r"[-‐-―.,;:()\[\]\"'’`/_*]+")
_TOKENS = {"gral": "general", "sud": "sur", "mcal": "mariscal", "sta": "santa", "sto": "santo", "sn": "san"}


def _repair(text):
    """UTF-8 text that was read as cp1252 or latin-1 and written again as UTF-8: PotosÃ­ for Potosí,
    ZUDAÃ\x91EZ (a C1 control character after the Ã) for ZUDAÑEZ."""
    if "Ã" not in text and "Â" not in text:
        return text
    raw = bytearray()
    for ch in text:
        if ord(ch) < 256:
            raw.append(ord(ch))
        else:
            try:
                raw += ch.encode("cp1252")
            except UnicodeEncodeError:
                return text
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return text


def _fold(text):
    """Lower case without accents, punctuation as spaces; any other non-ASCII character (a broken ñ
    such as ń or Ï, the replacement character, a question mark) becomes the wildcard ?."""
    out = []
    for ch in _repair(str(text)).replace("ï¿½", "?").lower():
        if ch in _SPANISH:
            out.append(_SPANISH[ch])
        elif ch.isascii():
            out.append(ch)
        elif unicodedata.category(ch).startswith("Z"):
            out.append(" ")
        else:
            out.append("?")
    folded = _PUNCT.sub(" ", "".join(out))
    return " ".join(_TOKENS.get(t, t) for t in folded.split())


class _Names:
    """Folded names with a lookup that lets a ? of the value stand for one letter of a name."""

    def __init__(self, names):
        self.names = frozenset(_fold(n) for n in names if n.strip())
        # Villa montes and Villamontes, SIPE SIPE and Sipesipe, CHOQUECOTA and Choque Cota.
        self.solid = frozenset(n.replace(" ", "") for n in self.names)
        self.by_length = {}
        for name in self.names:
            self.by_length.setdefault(len(name), []).append(name)

    def __contains__(self, key):
        if key in self.names or key.replace(" ", "") in self.solid:
            return True
        wild = key.count("?")
        if not wild or wild > 3 or len(key.replace("?", "").replace(" ", "")) < 4:
            return False
        pattern = re.compile(re.escape(key).replace(r"\?", "[a-z]"))
        return any(pattern.fullmatch(name) for name in self.by_length.get(len(key), ()))

    def startswith(self, key, minimum=15):
        """A name cut at a field length (General Jose Balliv): at least ``minimum`` characters."""
        if len(key) < minimum or "?" in key:
            return False
        return any(name.startswith(key) and name != key for name in self.names)


# ------------------------------------------------------------------ departments
DEPARTMENTS = {1: "Chuquisaca", 2: "La Paz", 3: "Cochabamba", 4: "Oruro", 5: "Potosí", 6: "Tarija",
               7: "Santa Cruz", 8: "Beni", 9: "Pando"}
# LPZ, SCZ and CBBA are the usual abbreviations of the three largest departments. The department names
# are also the names of their capital municipalities but Sucre, Trinidad and Cobija: a column of
# municipalities passes too, which is why the rules need a department field name.
_DEPARTMENT_NAMES = _Names(list(DEPARTMENTS.values()) + ["El Beni", "LPZ", "SCZ", "CBBA"])
_DEPARTMENT_PREFIX = re.compile(r"^(?:\d{1,2} )?(?:(?:departamento|depto|dpto|dep) (?:de )?)?")


def validate_bo_department(value):
    """The name of a Bolivian department in a department field: La Paz, POTOSI, Potosí, PotosÃ­, Potos?,
    Departamento de Oruro, 09.PANDO (not a province, Bolivia or Total)."""
    key = _DEPARTMENT_PREFIX.sub("", _fold(value))
    return bool(key) and key in _DEPARTMENT_NAMES


def _integer(value):
    text = str(value).strip().strip("'\"")
    if re.fullmatch(r"\d+\.0+", text):
        text = text.split(".")[0]
    return text if text.isdigit() else ""


def validate_bo_department_code(value):
    """An INE department code: 01 (Chuquisaca) to 09 (Pando), or 1 to 9 without the zero, 2.0 of a
    spreadsheet (not 0, 10 or 001)."""
    text = _integer(value)
    return 1 <= len(text) <= 2 and 1 <= int(text) <= 9


# ------------------------------------------------------------------ provinces
# INE province codes with the official name first, then the short and older names the data use.
_PROVINCES = """
0101 Oropeza
0102 Juana Azurduy de Padilla | Azurduy | Juana Azurduy
0103 Jaime Zudáñez | Zudáñez
0104 Tomina
0105 Hernando Siles
0106 Yamparáez
0107 Nor Cinti
0108 Belisario Boeto
0109 Sud Cinti
0110 Luis Calvo
0201 Pedro Domingo Murillo | Murillo
0202 Omasuyos
0203 Pacajes
0204 Eliodoro Camacho | Camacho
0205 Muñecas
0206 Larecaja
0207 Franz Tamayo
0208 Ingavi
0209 Loayza
0210 Inquisivi
0211 Sud Yungas
0212 Los Andes
0213 Aroma
0214 Nor Yungas
0215 Abel Iturralde
0216 Bautista Saavedra
0217 Manco Kapac | Manco Capac
0218 Gualberto Villarroel
0219 General José Manuel Pando | José Manuel Pando
0220 Caranavi
0301 Cercado
0302 Narciso Campero | Campero
0303 Ayopaya
0304 Esteban Arce | Esteban Arze
0305 Arani
0306 Arque
0307 Capinota
0308 Germán Jordán
0309 Quillacollo
0310 Chapare
0311 Tapacarí
0312 Carrasco
0313 Mizque
0314 Punata
0315 Bolívar
0316 Tiraque
0401 Cercado
0402 Eduardo Abaroa | Abaroa | Avaroa | Eduardo Avaroa
0403 Carangas
0404 Sajama
0405 Litoral | Litoral de Atacama
0406 Poopó
0407 Pantaleón Dalence
0408 Ladislao Cabrera
0409 Sabaya | Atahuallpa
0410 Saucarí
0411 Tomás Barrón
0412 Sur Carangas
0413 San Pedro de Totora
0414 Sebastián Pagador
0415 Mejillones
0416 Nor Carangas
0501 Tomás Frías
0502 Rafael Bustillo
0503 Cornelio Saavedra
0504 Chayanta
0505 Charcas
0506 Nor Chichas
0507 Alonso de Ibáñez
0508 Sud Chichas
0509 Nor Lípez
0510 Sud Lípez
0511 José María Linares
0512 Antonio Quijarro
0513 General Bernardino Bilbao | Bernardino Bilbao | General Bilbao
0514 Daniel Campos
0515 Modesto Omiste
0516 Enrique Baldivieso
0601 Cercado
0602 Aniceto Arce | Arce
0603 Gran Chaco
0604 José María Avilés | Avilés | Avilez
0605 Eustaquio Méndez | Méndez
0606 Burnet O'Connor | O'Connor
0701 Andrés Ibáñez
0702 Ignacio Warnes | Warnes
0703 José Miguel de Velasco | Velasco
0704 Ichilo
0705 Chiquitos
0706 Sara
0707 Cordillera
0708 Vallegrande | Valle Grande
0709 Florida
0710 Obispo Santistevan | Obispo Santisteban
0711 Ñuflo de Chávez
0712 Ángel Sandoval
0713 Manuel María Caballero | Manuel M. Caballero
0714 Germán Busch
0715 Guarayos
0801 Cercado
0802 Vaca Díez
0803 General José Ballivián Segurola | José Ballivián | General José Ballivián | Ballivián
0804 Yacuma
0805 Moxos | Mojos
0806 Marbán
0807 Mamoré
0808 Iténez
0901 Nicolás Suárez
0902 Manuripi
0903 Madre de Dios
0904 Abuná
0905 Federico Román
"""
PROVINCES = {}
for _line in _PROVINCES.strip().splitlines():
    _code, _names = _line.split(" ", 1)
    PROVINCES[_code] = [n.strip() for n in _names.split("|")]
_PROVINCE_NAMES = _Names([n for names in PROVINCES.values() for n in names])
PROVINCE_COUNT = {}
for _code in PROVINCES:
    PROVINCE_COUNT[int(_code[:2])] = max(PROVINCE_COUNT.get(int(_code[:2]), 0), int(_code[2:]))
_PROVINCE_PREFIX = re.compile(r"^(?:\d{1,4} )?(?:(?:provincia|prov) (?:de )?)?")


def validate_bo_province(value):
    """The name of a Bolivian province in a province field: Murillo, SUD YUNGAS, Sur Yungas, Andrés Ibáñez,
    Andres Iba?ez, ZUDAÃEZ, Muńecas, General Jose Balliv (cut at 20 characters), Provincia Cercado (not a
    department or a municipality alone: Potosí, El Alto)."""
    key = _PROVINCE_PREFIX.sub("", _fold(value))
    return bool(key) and (key in _PROVINCE_NAMES or _PROVINCE_NAMES.startswith(key))


def _province_ok(code):
    return len(code) == 4 and 1 <= int(code[:2]) <= 9 and 1 <= int(code[2:]) <= PROVINCE_COUNT[int(code[:2])]


def validate_bo_province_code(value):
    """An INE province code: the department code and the province number, 0201 (Murillo, La Paz) to
    0905 (Federico Román, Pando), 201 without the zero (not 0221, 0617 or 1001)."""
    text = _integer(value)
    return 3 <= len(text) <= 4 and _province_ok(text.zfill(4))


# ------------------------------------------------------------------ municipalities
# INE municipality codes of the Censo 2012 with the name of the INE first, then the other names of the
# municipality or its seat that the data use.
_MUNICIPALITIES = """
010101 Sucre
010102 Yotala
010103 Poroma
010201 Azurduy
010202 Tarvita
010301 Zudáñez
010302 Presto
010303 Mojocoya
010304 Icla | Villa Ricardo Mujía | Villa Ricardo Mugía - Icla | Villa Ricardo Mujía - Icla
010401 Padilla
010402 Tomina
010403 Sopachuy
010404 Villa Alcalá | Alcalá
010405 El Villar
010501 Monteagudo
010502 Huacareta
010601 Tarabuco
010602 Yamparáez
010701 Camargo
010702 San Lucas
010703 Incahuasi
010704 Villa Charcas | Villa Charca
010801 Villa Serrano | Serrano
010901 Villa Abecia | Camataquí
010902 Culpina
010903 Las Carreras
011001 Muyupampa | Villa Vaca Guzmán
011002 Huacaya
011003 Macharetí
020101 La Paz | Nuestra Señora de La Paz
020102 Palca
020103 Mecapaca
020104 Achocalla
020105 El Alto
020201 Achacachi
020202 Ancoraimes | Villa Ancoraimes
020203 Chua Cocani | Chúa Cocani
020204 Huarina
020205 Santiago de Huata
020206 Huatajata
020301 Corocoro | Coro Coro
020302 Caquiaviri
020303 Calacoto
020304 Comanche
020305 Charaña
020306 Waldo Ballivián | Tumarapi
020307 Nazacara de Pacajes | Nazacara
020308 Callapa | Santiago de Callapa
020401 Puerto Acosta
020402 Mocomoco
020403 Puerto Carabuco | Carabuco | Puerto Mayor de Carabuco
020404 Humanata
020405 Escoma
020501 Chuma
020502 Ayata
020503 Aucapata
020601 Sorata
020602 Guanay
020603 Tacacoma
020604 Quiabaya
020605 Combaya
020606 Tipuani
020607 Mapiri
020608 Teoponte
020701 Apolo
020702 Pelechuco
020801 Viacha
020802 Guaqui | Puerto Mayor de Guaqui
020803 Tiahuanacu | Tiwanaku | Tiahuanaco | Tiawanacu
020804 Desaguadero
020805 San Andrés de Machaca | Andrés de Machaca
020806 Jesús de Machaca
020807 Taraco
020901 Luribay
020902 Sapahaqui
020903 Yaco
020904 Malla
020905 Cairoma
021001 Inquisivi
021002 Quime
021003 Cajuata
021004 Colquiri
021005 Ichoca
021006 Villa Libertad Licoma | Licoma Pampa | Licoma
021101 Chulumani
021102 Irupana
021103 Yanacachi
021104 Palos Blancos
021105 La Asunta
021201 Pucarani
021202 Laja
021203 Batallas
021204 Puerto Pérez
021301 Sica Sica
021302 Umala
021303 Ayo Ayo
021304 Calamarca
021305 Patacamaya
021306 Colquencha
021307 Collana
021401 Coroico
021402 Coripata
021501 Ixiamas
021502 San Buenaventura
021601 Charazani
021602 Curva
021701 Copacabana
021702 San Pedro de Tiquina | Tiquina
021703 Tito Yupanqui | Tito Yupanki
021801 San Pedro de Curahuara | Curahuara | San Pedro de Cuarahuara
021802 Papel Pampa
021803 Chacarilla
021901 Santiago de Machaca
021902 Catacora
022001 Caranavi
022002 Alto Beni
030101 Cochabamba
030201 Aiquile
030202 Pasorapa
030203 Omereque
030301 Independencia | Ayopaya | Ayopaya (V. de Independencia) | Villa de Independencia
030302 Morochata
030303 Cocapata
030401 Tarata
030402 Anzaldo
030403 Arbieto
030404 Sacabamba
030501 Arani
030502 Vacas
030601 Arque
030602 Tacopaya
030701 Capinota
030702 Santiváñez | Santivañes
030703 Sicaya
030801 Cliza
030802 Toco | Toko
030803 Tolata
030901 Quillacollo
030902 Sipesipe
030903 Tiquipaya
030904 Vinto
030905 Colcapirhua
031001 Sacaba
031002 Colomi
031003 Villa Tunari
031101 Tapacarí
031201 Totora
031202 Pojo
031203 Pocona
031204 Chimoré
031205 Puerto Villarroel
031206 Entre Ríos | Bulo Bulo
031301 Mizque
031302 Vila Vila
031303 Alalay
031401 Punata
031402 Villa Rivero
031403 San Benito
031404 Tacachi
031405 Cuchumuela
031501 Bolívar
031601 Tiraque
031602 Shinahota | Shinaota
040101 Oruro
040102 Caracollo
040103 El Choro
040104 Pari - Paria - Soracachi | Soracachi | Paria
040201 Challapata
040202 Quillacas | Santuario de Quillacas
040301 Corque
040302 Choque Cota
040401 Curahuara de Carangas
040402 Turco
040501 Huachacalla
040502 Escara
040503 Cruz de Machacamarca
040504 Yunguyo de Litoral | Yunguyo del Litoral
040505 Esmeralda
040601 Poopó
040602 Pazña
040603 Antequera
040701 Huanuni
040702 Machacamarca
040801 Salinas de Garci Mendoza | Salinas
040802 Pampa Aullagas
040901 Sabaya
040902 Coipasa
040903 Chipaya
041001 Toledo
041101 Eucaliptus
041201 Santiago de Andamarca | Andamarca
041202 Belén de Andamarca
041301 San Pedro de Totora
041401 Huari | Santiago de Huari
041501 La Rivera
041502 Todos Santos
041503 Carangas
041601 Huayllamarca | Santiago de Huayllamarca
050101 Potosí
050102 Tinguipaya | Tinquipaya
050103 Yocalla
050104 Urmiri | Belén de Urmiri
050201 Uncía
050202 Chayanta
050203 Llallagua
050204 Chuquihuta | Chuquihuta Ayllu Jucumani | Chuquiuta
050301 Betanzos
050302 Chaquí
050303 Tacobamba
050401 Colquechaca
050402 Ravelo
050403 Pocoata
050404 Ocurí
050501 San Pedro de Buena Vista | S. P. de Buena Vista
050502 Toro Toro | Torotoro
050601 Cotagaita
050602 Vitichi | Vitiche
050701 Villa de Sacaca | Sacaca
050702 Caripuyo
050801 Tupiza
050802 Atocha
050901 Colcha "K" | Colcha K Villa Martín | Villa Martín
050902 San Pedro de Quemes
051001 San Pablo de Lípez
051002 Mojinete
051003 San Antonio de Esmoruco | Esmoruco
051101 Puna | Villa Talavera
051102 Caiza "D"
051103 Ckochas | Cochas
051201 Uyuni
051202 Tomave
051203 Porco
051301 Arampampa
051302 Acasio | Acacio
051401 Llica
051402 Tahua
051501 Villazón
051601 San Agustín
060101 Tarija
060201 Padcaya
060202 Bermejo
060301 Yacuiba
060302 Caraparí
060303 Villamontes
060401 Uriondo
060402 Yunchará
060501 Villa San Lorenzo | San Lorenzo
060502 El Puente
060601 Entre Ríos
070101 Santa Cruz de la Sierra | Santa Cruz
070102 Cotoca
070103 Porongo
070104 La Guardia
070105 El Torno
070201 Warnes
070202 Okinawa Uno | Okinawa
070301 San Ignacio de Velasco
070302 San Miguel de Velasco | San Miguel
070303 San Rafael
070401 Buena Vista
070402 San Carlos
070403 Yapacaní
070404 San Juan de Yapacaní | San Juan
070501 San José de Chiquitos | San José
070502 Pailón
070503 Roboré
070601 Portachuelo
070602 Santa Rosa del Sara
070603 Colpa Bélgica
070701 Lagunillas
070702 Charagua
070703 Cabezas
070704 Cuevo
070705 Gutiérrez
070706 Camiri
070707 Boyuibe
070801 Vallegrande | Valle Grande
070802 Trigal
070803 Moro Moro
070804 Postrer Valle
070805 Pucará
070901 Samaipata
070902 Pampa Grande
070903 Mairana
070904 Quirusillas
071001 Montero
071002 Gral. Saavedra | General Saavedra
071003 Mineros
071004 Fernández Alonso
071005 San Pedro
071101 Concepción
071102 San Javier
071103 San Ramón
071104 San Julián
071105 San Antonio de Lomerío
071106 Cuatro Cañadas
071201 San Matías
071301 Comarapa
071302 Saipina
071401 Puerto Suárez
071402 Puerto Quijarro
071403 Carmen Rivero Tórrez | Carmen Rivero Torres | El Carmen Rivero Tórrez | Carmen Rivero | Carmen Rivero T.
071501 Ascensión de Guarayos | Ascensión | Ascención de Guarayos
071502 Urubichá
071503 El Puente
080101 Trinidad | Santísima Trinidad
080102 San Javier
080201 Riberalta | Riveralta
080202 Guayaramerín
080301 Reyes
080302 San Borja
080303 Santa Rosa | Santa Rosa de Yacuma
080304 Rurrenabaque
080401 Santa Ana de Yacuma | Santa Ana
080402 Exaltación
080501 San Ignacio | San Ignacio de Moxos
080601 Loreto
080602 San Andrés
080701 San Joaquín
080702 San Ramón
080703 Puerto Siles
080801 Magdalena
080802 Baures
080803 Huacaraje | Huaracaje
090101 Cobija
090102 Porvenir
090103 Bolpebra
090104 Bella Flor
090201 Puerto Rico
090202 San Pedro
090203 Filadelfia
090301 Puerto Gonzalo Moreno
090302 San Lorenzo
090303 Sena
090401 Santa Rosa | Santa Rosa del Abuná
090402 Ingavi | Humaita
090501 Nueva Esperanza
090502 Villa Nueva (Loma Alta) | Villa Nueva | Loma Alta
090503 Santos Mercado
"""
MUNICIPALITIES = {}
for _line in _MUNICIPALITIES.strip().splitlines():
    _code, _names = _line.split(" ", 1)
    MUNICIPALITIES[_code] = [n.strip() for n in _names.split("|")]
_MUNICIPALITY_NAMES = _Names([n for names in MUNICIPALITIES.values() for n in names])
SECTION_COUNT = {}
for _code in MUNICIPALITIES:
    SECTION_COUNT[_code[:4]] = max(SECTION_COUNT.get(_code[:4], 0), int(_code[4:]))
_MUNICIPALITY_PREFIX = re.compile(
    r"^(?:\d{5,6} )?(?:(?:gobierno autonomo municipal|g a m|gam|municipio|municipalidad|seccion municipal|ciudad)"
    r" (?:de )?)?")
# ENTRE RIOS CBBA and ENTRE RIOS TRJ, SAN RAMON BENI and SAN RAMON SCZ: a department after a name that
# several departments share.
_DEPARTMENT_SUFFIX = re.compile(r" (?:cbba|cba|trj|tja|tarija|beni|scz|lpz|pts|oru|chq|pando|cochabamba|santa cruz|la paz)$")
_PARENTHESES = re.compile(r"\(([^()]*)\)")


def validate_bo_municipality(value):
    """The name of a Bolivian municipality in a municipality field: El Alto, SACABA, Nuestra Señora de La Paz,
    Villa Tunari, Soracachi (Paria), Colcha "K", Muyupampa, Tiwanaku, Municipio de Sucre, PotosÃ­ (not a
    province, a community or Total)."""
    text = _repair(str(value))
    candidates = [text, _PARENTHESES.sub(" ", text)] + _PARENTHESES.findall(text)
    for candidate in candidates:
        key = _MUNICIPALITY_PREFIX.sub("", _fold(candidate))
        if key and (key in _MUNICIPALITY_NAMES or _DEPARTMENT_SUFFIX.sub("", key) in _MUNICIPALITY_NAMES):
            return True
    return False


def _municipality_ok(code):
    """Department, province and a section within the sections of the province in 2012, plus one for a
    municipality created later (Raqaypampa, 2017, the fourth section of Mizque)."""
    return len(code) == 6 and _province_ok(code[:4]) and 1 <= int(code[4:]) <= SECTION_COUNT[code[:4]] + 1


def validate_bo_municipality_code(value):
    """An INE municipality code: department, province and municipal section, 020105 (El Alto) or 20105
    without the zero, 070101.0 (not 020109, the Murillo province having five sections, 260101 or 0201)."""
    text = _integer(value)
    return 5 <= len(text) <= 6 and _municipality_ok(text.zfill(6))


def validate_bo_community_code(value):
    """An INE community (localidad) code: the municipality code, two digits for the canton and three for
    the locality, 02010501001 or 2010501001 without the zero; layers of 2012 append three digits for a
    part of a dispersed community (01010105005001). Not a municipality code alone or 00000000000."""
    text = _integer(value)
    if len(text) in (10, 13):
        text = "0" + text
    if len(text) not in (11, 14) or not _municipality_ok(text[:6]):
        return False
    return int(text[6:8]) >= 1 and int(text[8:11]) >= 1


def validate_bo_municipality_code_known(value):
    """The code of one of the 339 municipalities of the Censo 2012 (020105, 70101 without the zero): the
    check of a field named only codigo, where a Peruvian ubigeo (010101) has the same form."""
    text = _integer(value)
    return 5 <= len(text) <= 6 and text.zfill(6) in MUNICIPALITIES
