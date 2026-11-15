"""Validators for tourist accommodation: the type of an establishment (hotel, apart-hotel, hostería,
cabañas, camping, gîte, Ferienwohnung) and its star rating (3 ESTRELLAS, 4 étoiles, ****).

Found in the register of tourist accommodation of Mendoza (Datos Abiertos Mendoza) for
metacrafter-testdata.
"""
import re
import unicodedata


def _norm(value):
    text = unicodedata.normalize("NFKD", str(value).strip().lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("&", " and ")
    return " ".join(re.sub(r"[^\w']+", " ", text).split())


ACCOMMODATION_TYPES = frozenset((
    # Spanish (Argentina, Spain, Latin America)
    "hotel", "hoteles", "apart hotel", "aparthotel", "apart", "apart hotel boutique", "hotel boutique", "petit hotel",
    "hosteria", "hosteria rural", "hospedaje", "hospedaje rural", "hospedaje vivienda de alquiler", "hostal",
    "hostel", "hostels", "cabana", "cabanas", "motel", "camping", "campamento", "refugio", "albergue",
    "albergue juvenil", "residencial", "posada", "lodge", "alojamiento", "alojamiento rural", "casa de huespedes",
    "casa rural", "bed and breakfast", "b and b", "colonia de vacaciones", "col vacac", "complejo turistico",
    "compl tco", "viv uso tco", "vivienda de uso turistico", "vivienda turistica", "estancia", "estancia turistica",
    "departamento turistico", "apartamento turistico", "hotel apartamento", "pension", "parador",
    # English
    "guest house", "guesthouse", "inn", "campsite", "caravan park", "holiday park", "holiday cottage",
    "self catering", "serviced apartments", "apartment hotel", "resort", "youth hostel", "holiday rental",
    # French
    "gite", "gites", "chambre d'hotes", "chambres d'hotes", "residence de tourisme", "village vacances",
    "auberge de jeunesse", "meuble de tourisme", "hotel de tourisme", "parc residentiel de loisirs",
    # German
    "hotel garni", "gasthof", "gasthaus", "ferienwohnung", "ferienhaus", "campingplatz", "jugendherberge",
    "privatzimmer",
    # Italian and Portuguese
    "albergo", "agriturismo", "affittacamere", "campeggio", "ostello", "residence", "pousada", "albergaria",
    "parque de campismo", "alojamento local", "turismo rural",
))


def validate_accommodation_type(value):
    """A type of tourist accommodation: HOTEL, APART-HOTEL, CABAÑAS, Hostería, Camping, Bed &
    Breakfast, chambre d'hôtes, Ferienwohnung (not RESTAURANTE, DISPONIBLE or a name)."""
    text = _norm(value)
    return bool(text) and text in ACCOMMODATION_TYPES


def _fold(value):
    """Lower case without accents and with single spaces; symbols are kept."""
    text = unicodedata.normalize("NFKD", str(value).strip().lower())
    return " ".join("".join(ch for ch in text if not unicodedata.combining(ch)).split())


_STARS = re.compile(
    r"^(?:(?:[1-7]|un[ao]?|one|two|three|four|five|dos|tres|cuatro|cinco)\s*"
    r"(?:estrellas?|stars?|etoiles?|sterne?|stelle|estrelas?|\*)"
    r"|[*\u2605]{1,7})"
    r"(?:\s*(?:superior|sup\.?|s|plus|lujo|luxe|gran lujo))?$")
_UNRATED = frozenset(("sin categorizar", "sin categoria", "sin clasificar", "non classe", "unrated", "not rated",
                      "ohne klassifizierung"))


def validate_accommodation_star_rating(value):
    """A star rating of a hotel: 3 ESTRELLAS, 1 ESTRELLA, 4 étoiles, 4 Sterne Superior, 5 stars,
    3*, ****, Sin categorizar (not 4.5, 3 or a class of establishment)."""
    text = _fold(value)
    return bool(text) and (bool(_STARS.match(text)) or text in _UNRATED)
