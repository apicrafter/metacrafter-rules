"""Values of the asset registers and observations of council and utility portals, found in the Opendatasoft
portals of the City of Melbourne, the City of Greater Geelong (with the Barwon Water layers), Liverpool City
Council and Peclet (metacrafter-testdata, 2024 snapshots): pipe materials, the useful life expectancy and the
age class of trees, electric power with its unit, ISO 8601 repeating intervals and the severity of road
crashes."""
import re


def _text(value):
    return " ".join(str(value).strip().split())


# ------------------------------------------------------------------ pipe materials
# Words of the materials of water, sewer and drainage pipes (Barwon Water: Ductile Iron Concrete Lined,
# Asbestos or Fibro Cement, Polypropylene Twin Wall Corrugated, Brute PVC) and the abbreviations of the
# water industry and of the Greater Geelong drainage register (RCP, DICL, ACP, FRC, EWP, HDPVC).
_PIPE_WORDS = re.compile(
    r"\b(?:asbestos|fibro|cement|concrete|cast iron|ductile iron|mild steel|stainless steel|steel|galvani[sz]ed"
    r"|iron|copper|brass|lead|polyvinyl|poly vinyl|pvc|upvc|mpvc|opvc|polyethylene|polypropylene|hdpe|mdpe"
    r"|polybutylene|vitreous clay|clay|earthenware|glass reinforced|fibreglass|fiberglass|grp|brick|masonry"
    r"|timber|wood|plastic|metal|abs|bitumen)\b",
    re.I)
PIPE_CODES = frozenset("""
ac acp ab abs bc bb brk bwk ci cicl cl conc cu di dicl dics diel dipl ewp frc gi grp gs hdpe hdpvc mdpe ms
mscl msel mspl pe pp pvc upvc mpvc opvc rc rcp rrj sgw ss stel vc vcp ewp gsp
""".split())
_NOT_PIPE = frozenset(("unk", "unknown", "other", "not known", "n/a", "na", "none", "lined", "grate", "earth",
                       "permeable", "arm"))


def validate_pipe_material(value):
    """A material of a pipe or a fitting, in words or a water industry code: Ductile Iron Concrete Lined,
    Vitreous Clay, Poly Vinyl Chloride (PVC), Asbestos or Fibro Cement, Copper Pipe, RCP, DICL, uPVC (not
    Unknown, Fair, 375 or Stormwater)."""
    text = _text(value)
    low = text.lower()
    if not text or low in _NOT_PIPE:
        return False
    if low in PIPE_CODES:
        return True
    return len(text) <= 60 and bool(_PIPE_WORDS.search(text)) and not any(c.isdigit() for c in text)


# ------------------------------------------------------------------ trees
_TREE_ULE = re.compile(
    r"^(?:[<>]\s*)?\d{1,3}\s*(?:(?:-|–|to)\s*\d{1,3}\s*|\+\s*)?(?:years?|yrs?)(?:\s*\([^)]*\))?$", re.I)


def validate_tree_useful_life_expectancy(value):
    """A useful life expectancy class of a tree: 31-60 years, 61+ years, 6-10 years (>50% canopy),
    <1 year, 20+ years, 10 - 20 years, < 5 years (not 35, Mature or 2019)."""
    return bool(_TREE_ULE.match(_text(value)))


TREE_AGE_CLASSES = frozenset((
    "new", "young", "juvenile", "semi-mature", "semi mature", "semimature", "early mature",
    "early-mature", "mature", "over-mature", "over mature", "overmature", "senescent", "veteran", "ancient",
    "established",
))


def validate_tree_age_class(value):
    """An age class of a tree: Semi-Mature, Mature, Over-mature, Juvenile, New, Young, Senescent (not 35,
    Good, Developer Maintained or Old Gum)."""
    return _text(value).lower() in TREE_AGE_CLASSES


# ------------------------------------------------------------------ electric power
_POWER = re.compile(
    r"^\d+(?:[.,]\d+)?\s*(?:(?:-|–|to)\s*\d+(?:[.,]\d+)?\s*)?(?:w|kw|mw|gw|watts?|kilowatts?|megawatts?)$", re.I)


def validate_electric_power(value):
    """An electric power with its unit: 80W, 150 W, 350 kW, 50 - 350 kW, 6.6 kW, 1.5 MW (not 350 kWh,
    80, kW or 50 kVA)."""
    return bool(_POWER.match(_text(value)))


# ------------------------------------------------------------------ ISO 8601 repeating intervals
_INSTANT = r"\d{4}-?\d{2}-?\d{2}(?:T\d{2}(?::?\d{2}(?::?\d{2}(?:[.,]\d+)?)?)?(?:Z|[+-]\d{2}(?::?\d{2})?)?)?"
_DURATION = r"P(?=\d|T\d)(?:\d+(?:[.,]\d+)?Y)?(?:\d+(?:[.,]\d+)?M)?(?:\d+(?:[.,]\d+)?W)?(?:\d+(?:[.,]\d+)?D)?" \
            r"(?:T(?=\d)(?:\d+(?:[.,]\d+)?H)?(?:\d+(?:[.,]\d+)?M)?(?:\d+(?:[.,]\d+)?S)?)?"
_REPEATING_INTERVAL = re.compile(
    rf"^R\d*/(?:{_INSTANT}/{_DURATION}|{_DURATION}/{_INSTANT}|{_INSTANT}/{_INSTANT}|{_DURATION})$")


def validate_iso8601_repeating_interval(value):
    """An ISO 8601 repeating interval: R/2015-01-02/P2W, R5/2008-03-01T13:00:00Z/P1Y2M10DT2H30M, R/P1Y,
    R12/P1M/2024-12-31 (not P2W, R/2015-01-02 or R/P)."""
    return bool(_REPEATING_INTERVAL.match(_text(value)))


# ------------------------------------------------------------------ road crash severity
CRASH_SEVERITIES = frozenset(s.lower() for s in (
    "Fatal", "Fatality", "Fatal crash", "Serious", "Serious injury", "Serious Injury Crash", "Hospitalisation",
    "Hospitalised", "Admitted to hospital", "Minor", "Minor injury", "Other injury", "Other Injury Crash",
    "Moderate injury", "First Aid", "Medical treatment", "Medical Treatment", "Injury", "Injury crash",
    "Non-injury", "Non injury", "Non Injury Accident", "No injury", "Property Damage Only", "Property damage",
    "PDO", "Tow-away", "Tow away", "Not known", "Unknown", "KSI", "Killed", "Slight",
))
# Values that are a severity on their own (a field of Unknown and Not known alone is not one).
_CRASH_SEVERITY_SIGNS = CRASH_SEVERITIES - {"not known", "unknown", "serious", "minor", "slight"}


def validate_crash_severity(value):
    """A road crash severity in words: Fatal, Serious, Minor, First Aid, Property Damage Only, Serious
    Injury, Other Injury Crash, Not known (not Daylight, Sealed or 3)."""
    return _text(value).lower() in CRASH_SEVERITIES


def validate_crash_severity_sign(value):
    """A crash severity that does not depend on its field name: Fatal, Property Damage Only, First Aid,
    Serious Injury (not Serious, Minor or Unknown alone)."""
    return _text(value).lower() in _CRASH_SEVERITY_SIGNS
