"""South African provinces."""
import re
import unicodedata


def _norm(value):
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", text)


ZA_PROVINCES = ("Eastern Cape", "Free State", "Gauteng", "KwaZulu-Natal", "Limpopo", "Mpumalanga", "North West",
                "Northern Cape", "Western Cape")
_ALIASES = ("Kwa-Zulu Natal", "KZN", "Northern Province", "North-West", "Orange Free State")
_PROVINCE_NAMES = frozenset(_norm(n) for n in ZA_PROVINCES + _ALIASES)
_PROVINCE_WORD = re.compile(r"(?i)\s+province$")


def validate_za_province(value):
    """A South African province: KwaZulu-Natal, MPUMALANGA, North West, Free State Province; not South
    Africa, a code (ZA-GP) or a municipality."""
    return _norm(_PROVINCE_WORD.sub("", str(value).strip())) in _PROVINCE_NAMES
