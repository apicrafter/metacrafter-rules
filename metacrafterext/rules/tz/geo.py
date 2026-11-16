"""Tanzanian geography: the 31 regions (mikoa), in English and Swahili names."""
import re
import unicodedata


def _norm(value):
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", text)


TZ_REGIONS = (
    "Arusha", "Dar es Salaam", "Dodoma", "Geita", "Iringa", "Kagera", "Katavi", "Kigoma", "Kilimanjaro",
    "Lindi", "Manyara", "Mara", "Mbeya", "Morogoro", "Mtwara", "Mwanza", "Njombe", "Pwani", "Rukwa",
    "Ruvuma", "Shinyanga", "Simiyu", "Singida", "Songwe", "Tabora", "Tanga",
    # Zanzibar
    "Kaskazini Pemba", "Kusini Pemba", "Kaskazini Unguja", "Kusini Unguja", "Mjini Magharibi",
)
_ALIASES = ("Coast", "Dar-es-salaam", "Dar es salam", "Pemba North", "Pemba South", "North Pemba", "South Pemba",
            "Zanzibar North", "Zanzibar South", "Zanzibar South and Central", "Zanzibar Central/South",
            "Zanzibar Urban/West", "Zanzibar West", "Zanzibar Urban", "Unguja North", "Unguja South",
            "Mjini Magharibi Unguja", "Kaskazini-Pemba", "Kusini-Pemba", "Kaskazini-Unguja", "Kusini-Unguja",
            "Mtwara & Lindi")
_REGION_NAMES = frozenset(_norm(n) for n in TZ_REGIONS + _ALIASES)
_REGION_WORD = re.compile(r"(?i)\s+region$|^mkoa\s+wa\s+")


def validate_tz_region(value):
    """A Tanzanian region: Dodoma, Dar es Salaam, Coast (Pwani), Kaskazini Pemba, Tabora Region;
    not a district (Kongwa) or Zanzibar alone."""
    return _norm(_REGION_WORD.sub("", str(value).strip())) in _REGION_NAMES


def validate_tz_region_by_value(value):
    """A Tanzanian region by value alone: as ``validate_tz_region``, but a bare Coast, the English name of
    Pwani, is any coast (the water body types Coast, Open Sea and Estuary of a marine monitoring table)."""
    return validate_tz_region(value) and _norm(str(value).strip()) != _norm("Coast")
