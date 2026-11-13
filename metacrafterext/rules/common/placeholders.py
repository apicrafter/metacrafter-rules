"""
Placeholder values: numbers that pass check digit validation by chance, and texts for a
missing value.

A number made of one repeated digit (0000000000, 1111111111) passes most weighted-sum
checks: every weighted sum of zeros is 0. Such values fill empty identifier columns of
exports (a budget classifier with ``itemcode`` 0000000000), so a checksum match on them is
no evidence for any identifier.

Texts for a missing value (n/a, Non renseigné, нет данных) are no evidence against a field
name either: value checks of field-name rules let them pass (``is_missing_text``).
"""
import functools
import re

_SEPARATORS = re.compile(r"[\s\-./]")


def is_repeated_digit(value):
    """True when ``value`` without spaces, dashes, dots and slashes is one digit repeated."""
    if value is None:
        return False
    text = _SEPARATORS.sub("", str(value))
    return len(text) > 1 and text.isdigit() and len(set(text)) == 1


def rejects_repeated_digits(validator):
    """Wrap a check digit validator so that it rejects values made of one repeated digit."""

    @functools.wraps(validator)
    def wrapper(value, *args, **kwargs):
        if is_repeated_digit(value):
            return False
        return validator(value, *args, **kwargs)

    return wrapper


# Texts that stand for a missing value in exports: an id_station_local of "Non renseigné"
# says nothing about the type of the field.
_MISSING_TEXTS = frozenset(
    text.strip()
    for text in """
    n/a|n.a.|none|null|unknown|not available|not applicable|not specified|not provided|missing
    non renseigné|non renseigne|non communiqué|non communique|inconnu|sans objet|néant|neant
    non applicable|non disponible|non précisé|non precise|keine angabe|k.a.|k. a.|unbekannt
    entfällt|sin dato|sin datos|s/d|desconocido|no aplica|no disponible|não informado
    nao informado|sem informação|non disponibile|non specificato|n.d.|нет данных|не указано
    неизвестно|отсутствует|нет|-|--|—|?
    """.replace("\n", "|").split("|")
    if text.strip()
)


def is_missing_text(value):
    """True when ``value`` is a placeholder for a missing value: n/a, Non renseigné, нет данных."""
    if value is None:
        return False
    return " ".join(str(value).split()).casefold() in _MISSING_TEXTS
