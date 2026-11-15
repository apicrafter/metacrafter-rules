"""What survey platforms and city open data portals record about respondents and their sessions, found
in the Edmonton Insight Community surveys and the Calgary and Edmonton census tables (metacrafter-testdata,
2024 snapshots of data.edmonton.ca and data.calgary.ca, Dateno sources cdi00000289 and cdi00000286): the
device type, browser and operating system of a session, housing tenure, home languages, the mode of
transport of a commute and municipal wards."""
import re
import unicodedata


def _text(value):
    return " ".join(str(value).strip().split())


def _fold(value):
    text = unicodedata.normalize("NFKD", _text(value).lower())
    return "".join(c for c in text if not unicodedata.combining(c))


# Answers that are no answer: they pass, so a column of real answers and these is still the type, but
# a column of these alone proves nothing (the callers ask for a real value among the words).
_NO_ANSWER = frozenset((
    "unknown", "other", "others", "other (specify)", "other (please specify)", "prefer not to answer",
    "prefer not to say", "i prefer not to answer", "don't know", "dont know", "not applicable", "n/a",
    "na", "none", "no response", "not stated", "unspecified", "total", "did not answer",
))

# ------------------------------------------------------------------ device, browser, operating system
_DEVICE_TYPES = frozenset((
    "desktop", "phone", "tablet", "mobile", "smartphone", "mobile phone", "laptop", "computer", "pc",
    "tv", "smart tv", "smarttv", "console", "game console", "wearable", "e-reader", "ereader", "bot",
    "desktop/laptop", "desktop or laptop", "mobile device", "feature phone", "set-top box", "kiosk",
))
_BROWSERS = frozenset((
    "chrome", "google chrome", "safari", "mobile safari", "firefox", "mozilla firefox", "edge",
    "microsoft edge", "internet explorer", "ie", "msie", "opera", "opera mini", "samsung internet",
    "samsung browser", "uc browser", "android browser", "android webview", "chrome mobile",
    "chrome webview", "safari (in-app)", "chromium", "brave", "vivaldi", "yandex browser", "silk",
    "amazon silk", "blackberry", "netscape", "seamonkey", "duckduckgo", "firefox mobile",
    "chrome mobile ios", "edge mobile", "facebook", "instagram", "webkit", "konqueror",
))
_OPERATING_SYSTEMS = frozenset((
    "windows", "ios", "android", "macos", "mac os", "mac os x", "mac (os x)", "os x", "macintosh", "mac",
    "linux", "chrome os", "chromeos", "chromium os", "ubuntu", "windows phone", "windows mobile",
    "blackberry", "blackberry os", "ipados", "unix", "freebsd", "symbian", "tizen", "fire os", "kaios",
    "harmonyos", "debian", "fedora",
))
_OS_VERSION = re.compile(r"^(windows|android|ios|ipados|macos|mac os x|os x|ubuntu)[ ]?(?:nt )?[0-9a-z.]{1,8}$")


def _in(value, words):
    text = _fold(value)
    return text in words or text in _NO_ANSWER


def validate_device_type(value):
    """A class of device: Desktop, Phone, Tablet, Mobile, Smartphone, Smart TV, Unknown (not iPhone 12,
    Chrome or 3)."""
    return _in(value, _DEVICE_TYPES)


def validate_web_browser(value):
    """A web browser by name: Google Chrome, Chrome, Safari, Firefox, Internet Explorer, Microsoft Edge,
    Opera, Unknown (not Windows, Desktop or 87.0)."""
    return _in(value, _BROWSERS)


def validate_operating_system(value):
    """An operating system by name, with or without its version: Windows, iOS, Mac (OS X), macOS,
    Android, Linux, Windows 10, Unknown (not Chrome, Desktop or 10)."""
    text = _fold(value)
    return text in _OPERATING_SYSTEMS or text in _NO_ANSWER or bool(_OS_VERSION.match(text))


# ------------------------------------------------------------------ housing tenure
_TENURE = frozenset((
    "own", "rent", "owned", "rented", "owner", "renter", "owners", "renters", "tenant", "owner-occupied",
    "owner occupied", "renter-occupied", "renter occupied", "own with mortgage", "own without mortgage",
    "own outright", "owned outright", "owned with a mortgage", "owned with mortgage", "rent-free",
    "rent free", "neither", "band housing", "private rental", "social rental", "social housing",
    "owner occupier", "private renter", "social renter", "co-op", "housing co-operative", "own home",
    "rent home", "homeowner", "home owner",
))


def validate_housing_tenure(value):
    """A housing tenure: Own, Rent, Owner, Renter, Owner-occupied, Rent-free, Band housing, Prefer not
    to answer (not Yes, 3 or Apartment)."""
    return _in(value, _TENURE)


# ------------------------------------------------------------------ languages by English name
_LANGUAGES = frozenset((
    "english", "french", "spanish", "german", "italian", "portuguese", "russian", "ukrainian", "polish",
    "dutch", "greek", "arabic", "hebrew", "turkish", "persian", "farsi", "dari", "pashto", "kurdish",
    "urdu", "hindi", "punjabi", "panjabi", "gujarati", "bengali", "tamil", "telugu", "malayalam",
    "kannada", "marathi", "nepali", "sinhala", "sinhalese", "mandarin", "cantonese", "chinese",
    "japanese", "korean", "vietnamese", "thai", "khmer", "lao", "burmese", "tagalog", "filipino",
    "pilipino", "ilocano", "cebuano", "indonesian", "malay", "somali", "amharic", "tigrinya", "oromo",
    "swahili", "yoruba", "igbo", "hausa", "akan", "twi", "afrikaans", "zulu", "romanian", "hungarian",
    "czech", "slovak", "croatian", "serbian", "bosnian", "bulgarian", "albanian", "macedonian",
    "slovenian", "lithuanian", "latvian", "estonian", "finnish", "swedish", "norwegian", "danish",
    "icelandic", "armenian", "georgian", "azerbaijani", "kazakh", "uzbek", "mongolian", "tibetan",
    "cree", "ojibwe", "ojibway", "inuktitut", "dene", "blackfoot", "michif", "stoney", "welsh", "irish",
    "gaelic", "catalan", "basque", "latin", "esperanto", "creole", "haitian creole", "hmong", "sindhi",
    "assyrian", "aramaic", "tigrigna", "kinyarwanda", "lingala", "shona", "wolof", "maltese",
    "american sign language", "sign language", "asl", "taiwanese", "hakka", "min nan", "wu",
    "serbo-croatian", "flemish", "yiddish", "konkani", "odia", "oriya", "assamese", "kashmiri",
))
_PAREN = re.compile(r"\s*\([^()]*\)")
_LANGUAGE_EXTRA = re.compile(r"\s+(?:only|languages?|n\.?[ioe]\.?[es]\.?)$")


def validate_language_name(value):
    """A language by its English name: English, French, Panjabi (Punjabi), Tagalog (Pilipino,
    Filipino), Persian (Farsi), English Only, Other (Specify) (not Canadian, Yes, en or 270)."""
    text = _fold(value)
    if text in _NO_ANSWER:
        return True
    text = _LANGUAGE_EXTRA.sub("", _PAREN.sub("", text)).strip()
    return text in _LANGUAGES or all(part.strip() in _LANGUAGES for part in re.split(r"\s*(?:/|,| and | & )\s*", text) if part.strip()) and bool(text)


# ------------------------------------------------------------------ mode of transport of a trip
_MODE_CORE = frozenset((
    "car", "truck", "van", "bus", "transit", "walk", "walking", "walked", "bicycle", "bike", "cycling",
    "cycle", "train", "rail", "lrt", "subway", "metro", "tram", "streetcar", "taxi", "motorcycle",
    "carpool", "rideshare", "ferry", "scooter", "skateboard", "auto", "vehicle", "pedestrian", "cyclist",
    "air", "sea", "road", "water", "pipeline", "rollerblade", "motorbike", "uber", "foot", "automobile",
    "wheelchair", "boat", "plane", "airplane", "drive", "drove", "driving",
))
_MODE_WORDS = _MODE_CORE | frozenset((
    "as", "a", "driver", "passenger", "public", "private", "or", "and", "by", "on", "to", "the", "of",
    "e", "electric", "ride", "share", "sharing", "hailing", "light", "commuter", "school", "city",
    "personal", "alone", "with", "others", "other", "motor", "mode", "active", "transportation",
    "transport", "work", "from", "home", "at", "worked", "s", "service", "limousine", "pool", "in",
))


def validate_transport_mode_word(value):
    """A mode of transport of a trip in words: Car/truck/Van as DRIVER, Public Transit, Walk, Bicycle,
    Car/Truck/Van (as Passenger), Taxi, Bus, Rail (not Yes, 3, Monday or Residential)."""
    text = _fold(value)
    if text in _NO_ANSWER:
        return True
    words = [w for w in re.split(r"[\s/,;()+&-]+", text) if w]
    return bool(words) and len(words) <= 8 and all(w in _MODE_WORDS for w in words) and any(w in _MODE_CORE for w in words)


# ------------------------------------------------------------------ municipal wards
# Ward 14, WARD 7, 14, Ward A, papastew Ward, North Ward, EPSB Ward A.
_WARD = re.compile(r"^(?:(?:ward )?(?:0?[1-9]|[1-9]\d)|ward [a-z]|[^\d\W][\w'’.-]*(?: [\w'’.-]+){0,3} ward(?: [a-z0-9]{1,2})?)$",
                   re.I)


def validate_municipal_ward(value):
    """A ward of a municipality in a field named for wards: Ward 14, WARD 7, 14, 05, Ward A, papastew
    Ward, Métis Ward, North Ward, EPSB Ward A, and the Edmonton wards by name alone (Anirniq, O-day'min) (not 123, Calgary, Ward or Ward End)."""
    text = _text(value)
    if _FLOAT_WARD.match(text):
        text = text[:-2]
    return bool(_WARD.match(text)) or _fold(text).replace("’", "'") in _NAMED_WARDS


_FLOAT_WARD = re.compile(r"^\d{1,2}\.0$")
# The twelve wards of the City of Edmonton since 2021 have Indigenous names, written without Ward.
_NAMED_WARDS = frozenset((
    "nakota isga", "anirniq", "tastawiyiniwak", "dene", "o-day'min", "metis", "sipiwiyiniwak", "papastew",
    "pihesiwin", "ipiihkoohkanipiaohtsi", "karhiio", "sspomitapi",
))
_WARD_WORDED = re.compile(r"\bward\b", re.I)


def validate_municipal_ward_name(value):
    """A ward written with the word Ward (Ward 14, papastew Ward), not a bare number: what a field
    without a ward name must hold to be read as wards (LABEL: WARD 5)."""
    text = _text(value)
    return bool(_WARD.match(text)) and bool(_WARD_WORDED.search(text))
