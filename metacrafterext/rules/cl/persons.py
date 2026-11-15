"""Indigenous peoples of Chile as surveys of the Chilean files of metacrafter-testdata ask them (the NEMS-P-Ch
pilot survey of the food environment, datos.uchile.cl: ¿Usted se considera perteneciente a algún pueblo
originario? mapuche, diaguitas, quechua, ninguna_no_sabe).

The peoples are those of the Indigenous Law 19.253 and its amendments: Mapuche, Aymara, Rapa Nui, Atacameño
(Lickanantay), Quechua, Colla, Kawésqar, Yagán, Diaguita, Chango and Selk'nam, with the names of Mapuche groups
that respondents give (Huilliche, Pehuenche, Lafkenche).
"""
import re
import unicodedata

_PEOPLES = frozenset((
    "mapuche", "aymara", "aimara", "rapa nui", "rapanui", "pascuense", "atacameno", "atacamena", "lickanantay",
    "likan antai", "likanantai", "quechua", "colla", "kolla", "coya", "kawesqar", "kawashkar", "kawashkar",
    "alacalufe", "yagan", "yamana", "diaguita", "chango", "selk'nam", "selknam", "selk nam", "ona",
    "huilliche", "williche", "pehuenche", "lafkenche", "lafquenche", "picunche",
))
_NONE = frozenset((
    "ninguno", "ninguna", "ninguno de los anteriores", "ninguna no sabe", "no pertenece", "no pertenece a ninguno",
    "no pertenece a ningun pueblo", "no pertenece a ningun pueblo indigena", "otro", "otra", "otros", "otro pueblo",
    "no sabe", "no responde", "no sabe no responde", "ns nr", "no", "sin informacion", "no aplica",
))
_SPLIT = re.compile(r"[\s_/,;()-]+")
_LEAD = re.compile(r"^(?:pueblo )?")


def _fold(value):
    text = unicodedata.normalize("NFKD", str(value).strip().lower().replace("’", "'"))
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(w for w in _SPLIT.split(text) if w)


def _people(text):
    if text in _PEOPLES:
        return True
    # the plural of a form option (diaguitas, mapuches, collas) and the Atacameño with the other name
    if text.endswith("s") and text[:-1] in _PEOPLES:
        return True
    parts = [p for p in re.split(r" (?:o|u|y) ", text) if p]
    return len(parts) > 1 and all(p in _PEOPLES or (p.endswith("s") and p[:-1] in _PEOPLES) for p in parts)


def validate_cl_indigenous_people(value):
    """An indigenous people of Chile: Mapuche, Aymara, Rapa Nui, diaguitas, Atacameño o Lickanantay,
    Kawésqar, Selk'nam, Huilliche (not Guaraní, Chilena or a number)."""
    text = _fold(value)
    return bool(text) and len(text) <= 60 and _people(_LEAD.sub("", text))


def validate_cl_indigenous_people_answer(value):
    """An answer to the question on belonging to an indigenous people: a people, or none, other and
    does not know (ninguna_no_sabe, Otro, No pertenece a ningún pueblo indígena)."""
    return validate_cl_indigenous_people(value) or _fold(value) in _NONE
