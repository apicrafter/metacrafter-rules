"""Spanish vocabularies of municipal open data (datosabiertos.mercedes.gob.ar, metacrafter-testdata): the
common names of street trees (Fresno Americano, Plátano, Ligustro Variegado) and medical specialties
(CARDIOLOGÍA, CLÍNICA MÉDICA, Pediatría), with the English specialties."""
import re
import unicodedata

#: U+FFFD, which a decoder puts for the bytes of a letter it cannot read (a Latin-1 á in UTF-8 text).
REPLACEMENT = "\ufffd"


def _fold(value):
    """Lower case without accents and without the replacement character of a broken accent
    (Pl?tano), single spaces, no dots at the ends."""
    text = unicodedata.normalize("NFKD", str(value).strip())
    text = "".join(ch for ch in text if not unicodedata.combining(ch)).lower()
    return re.sub(r"\s+", " ", text).strip(" .")


# --- Street trees --------------------------------------------------------------------------------

# Common names of the trees of streets and parks of Argentina, Uruguay and Spain, folded: the street
# tree inventories (arbolado urbano) of Mercedes, Buenos Aires, Rosario, Montevideo and Madrid give
# the species this way. Names that are also ordinary words or places alone (Paraíso, Sauce, Álamo,
# Roble, Pino) count only beside the others: a field of them is a field of trees.
TREE_NAMES = frozenset((
    "acacia", "acacia blanca", "acacia bola", "acacia de constantinopla", "acacia negra", "acacia visco",
    "acer", "acer negundo", "aguaribay", "alamo", "alamo blanco", "alamo carolina", "alamo plateado",
    "algarrobo", "aliso", "arce", "arce negundo", "arce tridente", "araucaria", "abedul", "abeto",
    "brachichiton", "braquiquito", "casuarina", "catalpa", "cedro", "ceibo", "cerezo", "cina cina",
    "cipres", "ciruelo", "ciruelo de jardin", "ciruelo japones", "crespon", "durazno",
    "eucalipto", "falso arce", "fotinia", "fresno", "fresno americano", "fresno dorado", "fresno europeo",
    "gingko", "ginkgo", "gomero", "grevillea", "guaran amarillo", "higuera", "jacaranda", "laurel",
    "lapacho", "lapacho rosado", "lapacho amarillo", "ligustrina", "ligustro", "ligustro comun",
    "ligustro variegado", "limonero", "limpia tubo", "limpiatubos", "liquidambar", "magnolia", "manzano",
    "mandarino", "melia", "mora", "morera", "naranjo", "naranjo amargo", "nispero", "nogal", "olivo",
    "olmo", "olmo bola", "olmo siberiano", "palmera", "palmera pindo", "palo borracho", "paraiso",
    "paraiso sombrilla", "peral", "peral de flor", "pezuna de vaca", "pino", "platano", "pata de vaca",
    "pimentero", "roble", "roble americano", "sauce", "sauce criollo", "sauce lloron",
    "sofora", "tilo", "timbo", "tipa", "tuya", "acer campestre", "almez", "castano de indias", "aligustre",
    "arbol del cielo", "ailanto", "celtis", "ombu", "espinillo", "chanar", "quebracho", "jabonero de la china",
))
# Words that are names of trees and also places, things or surnames.
_AMBIGUOUS_TREES = frozenset(("paraiso", "sauce", "alamo", "roble", "pino", "olmo", "cedro", "laurel", "mora",
                              "olivo", "nogal", "tilo", "arce", "aliso", "tipa", "timbo", "ombu"))


def validate_es_tree_name(value):
    """A common name of a street tree: Fresno Americano, Plátano, Pl?tano, Ligustro Variegado, Acacia
    Bola, Ciruelo de Jardín, Crespón (not Otros, a street or a scientific name)."""
    folded = _fold(value)
    text = folded.replace(REPLACEMENT, "")
    if not 3 <= len(text) <= 40:
        return False
    if text in TREE_NAMES:
        return True
    if text == folded or len(text) < 4:
        return False
    # an accent that did not decode (Pl?tano, S?fora, Cresp?n) left out a letter
    return any(len(name) == len(text) + 1 and _without_one(name, text) for name in TREE_NAMES if name[0] == text[0])


def _without_one(name, text):
    """True when text is name without one of its letters."""
    for i in range(len(name)):
        if name[:i] + name[i + 1:] == text:
            return True
    return False


def validate_es_tree_name_value(value):
    """A common name of a street tree that is no ordinary word (validate_es_tree_name): Fresno
    Americano, Plátano, Ligustro (not Paraíso or Sauce alone, which are also places)."""
    return validate_es_tree_name(value) and _fold(value) not in _AMBIGUOUS_TREES


# --- Medical specialties ---------------------------------------------------------------------------

MEDICAL_SPECIALTIES = frozenset((
    # Spanish (specialties and the services that health centres count beside them)
    "alergia", "alergologia", "anatomia patologica", "anestesiologia", "cardiologia", "cardiologia infantil",
    "cirugia", "cirugia general", "cirugia plastica", "cirugia vascular", "clinica", "clinica medica",
    "dermatologia", "diabetologia", "endocrinologia", "enfermeria", "estimulacion temprana",
    "fisiatria", "fonoaudiologia", "gastroenterologia", "geriatria", "ginecologia", "ginecologia y obstetricia",
    "hematologia", "hepatologia", "infectologia", "kinesiologia", "medicina familiar", "medicina general",
    "medicina interna", "medicina del trabajo", "nefrologia", "neonatologia", "neumonologia", "neumologia",
    "neurocirugia", "neurologia", "nutricion", "obstetricia", "odontologia", "odontopediatria", "oftalmologia",
    "oncologia", "ortopedia", "otorrinolaringologia", "pediatria", "psicologia", "psicopedagogia",
    "psiquiatria", "psiquiatria infantil", "radiologia", "reumatologia", "salud mental", "terapia ocupacional",
    "tocoginecologia", "traumatologia", "urologia", "urgencias", "guardia", "emergencias", "diabetes",
    # English
    "allergy", "anesthesiology", "anaesthesia", "cardiology", "dermatology", "emergency medicine",
    "endocrinology", "family medicine", "gastroenterology", "general practice", "general surgery",
    "geriatrics", "gynecology", "gynaecology", "hematology", "haematology", "internal medicine", "nephrology",
    "neurology", "neurosurgery", "obstetrics", "obstetrics and gynecology", "oncology", "ophthalmology",
    "orthopedics", "orthopaedics", "otolaryngology", "pediatrics", "paediatrics", "psychiatry", "pulmonology",
    "radiology", "rheumatology", "surgery", "urology", "dentistry",
))


def validate_medical_specialty(value):
    """A medical specialty: CARDIOLOGÍA, CLÍNICA MÉDICA, Pediatría, KINESIOLOGIA, Cardiology (not
    LABORATORIO, a person or a school subject)."""
    text = _fold(value)
    return 4 <= len(text) <= 40 and text in MEDICAL_SPECIALTIES
