"""German field values about people and time found in the 2024 snapshots of the Swiss open data portals of
the Dateno catalogue (data.bl.ch, data.bs.ch, data.sz.ch, data.sbb.ch): forms of address, weekdays, years
of birth and street addresses."""
import re


def _text(value):
    return " ".join(str(value).strip().split())


SALUTATIONS = frozenset((
    "herr", "frau", "hr.", "fr.", "hr", "fr", "herrn", "fräulein", "frl.", "divers", "familie", "firma", "herr und frau",
    "herr dr.", "frau dr.", "herr prof.", "frau prof.", "herr prof. dr.", "frau prof. dr.", "monsieur", "madame", "m.",
    "mme", "mme.", "mlle", "signor", "signora", "sig.", "sig.ra", "keine angabe", "keine", "-"))


def validate_de_salutation(value):
    """A German form of address (also the French and Italian ones of Swiss registers): Herr, Frau, Hr.,
    Frau Dr., Monsieur, Madame (not Müller, Dr. med. or 1)."""
    return _text(value).lower() in SALUTATIONS


_WEEKDAYS = ("montag", "dienstag", "mittwoch", "donnerstag", "freitag", "samstag", "sonnabend", "sonntag")
_WEEKDAY_ABBR = frozenset(("mo", "di", "mi", "do", "fr", "sa", "so"))
_WEEKDAY_NUMBERED = re.compile(r"^[1-7][ .:)-]+")
_WEEKDAY_RANGE = re.compile(r"^(mo|di|mi|do|fr|sa|so)\.? ?[-–/+] ?(mo|di|mi|do|fr|sa|so)\.?$")


def validate_de_weekday(value):
    """A weekday in German: Montag, Mittwoch, Mo, Fr., 4 Mittwoch, Mo-Fr (not Monday, Januar, 4 or
    Mo-Fr Mittagstisch)."""
    text = _WEEKDAY_NUMBERED.sub("", _text(value).lower())
    if text in _WEEKDAYS or text.rstrip(".") in _WEEKDAY_ABBR:
        return True
    return bool(_WEEKDAY_RANGE.match(text))


def validate_birth_year(value):
    """A year of birth as four digits, 1850 to 2030: 1968, 2000, 1984.0 (not 68, 20230101, 1700 or
    unbekannt)."""
    text = _text(value)
    m = re.match(r"^(\d{4})(?:\.0+)?$", text)
    return bool(m) and 1850 <= int(m.group(1)) <= 2030


# Hardstrasse 71, Wölferstrasse 5, Zu den drei Linden 80, St. Johanns-Vorstadt 12a, Hauptstr. 4/6
_STREET_NUMBER = re.compile(r"^[^\W\d_][\w .'’/\-]*[^\W\d_.]\.? \d{1,4} ?[a-zA-Z]?(?: ?[-/+] ?\d{1,4} ?[a-zA-Z]?)?$")


# A post office box has the shape of a street with a number (Postfach 12, Postboks 8132 Dep).
_PO_BOX = re.compile(r"(?i)^(?:postfach|postboks|postbus|postbox|case postale|casella postale|boks|p\.? ?o\.? ?box)\b")


def validate_de_street_address(value):
    """A street with a house number as German addresses write it, the number last: Hardstrasse 71,
    Zu den drei Linden 80, St. Johanns-Vorstadt 12a, Hauptstr. 4/6 (not Hardstrasse, 71, 4102 Binningen,
    Hardstrasse 71, 4410 Liestal or Postfach 12)."""
    text = _text(value)
    if _PO_BOX.match(text):
        return False
    return len(text) <= 80 and bool(_STREET_NUMBER.match(text))


_DATE_DMYY = re.compile(r"^(0[1-9]|[12]\d|3[01])\.(0[1-9]|1[0-2])\.\d{2}$")


def validate_de_date_dmyy(value):
    """A date as day, month and two-digit year with dots: 13.03.16, 11.12.16, 01.01.04 (not 1.2.3,
    13.13.16 or 11.12.2016)."""
    return bool(_DATE_DMYY.match(_text(value)))
