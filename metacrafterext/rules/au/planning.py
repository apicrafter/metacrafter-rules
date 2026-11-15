"""Local government data of New South Wales found in the Camden Council open data of
metacrafter-testdata (data.camden.nsw.gov.au, Opendatasoft): council wards, the environmental planning
instruments and development control plans of the NSW planning system, the heritage items of a local
environmental plan with their significance, and the blue-green algae alert levels of recreational
waters."""
import re

from metacrafterext.rules.common.respondents import validate_municipal_ward

# North Ward, Central Ward, Bass Hill Ward, Ward 1, A Ward, Division 3 (Queensland), Unsubdivided.
_COUNCIL_WARD = re.compile(
    r"^(?:(?:[A-Z][\w'’.-]*)(?: [A-Z][\w'’.-]*){0,3} Ward|Ward (?:\d{1,2}|[A-Z])|[A-Z] Ward|Division \d{1,2})$", re.I)
_WARD_WORD = re.compile(r"\bward\b", re.I)


def validate_au_council_ward(value):
    """A ward of an Australian council: North Ward, Central Ward, SOUTH WARD, Bass Hill Ward, Ward 1,
    A Ward, Division 3, Unsubdivided (not Camden, North, Ward End or Ward 123)."""
    text = " ".join(str(value).split())
    if text.lower() in ("unsubdivided", "undivided"):
        return True
    return bool(_COUNCIL_WARD.match(text))


def validate_not_au_council_ward(value):
    """A UK ward name with letters that is not an Australian council ward named Ward (Abbey, Castle,
    Ward End, St Helier pass; North Ward, Ward 2 fail)."""
    text = str(value).strip()
    if not any(ch.isalpha() for ch in text):
        return False
    # A ward of any municipality written with the word Ward (EPSB Ward A, papastew Ward) or one of the
    # Edmonton wards by name alone (Anirniq, O-day'min) is municipal_ward, not an ONS name.
    if validate_municipal_ward(text):
        return False
    return not (_WARD_WORD.search(text) and validate_au_council_ward(text))


# Camden Local Environmental Plan 2010, Camden LEP 2010, State Environmental Planning Policy
# (Precincts—Western Parkland City) 2021, SEPP (Precincts—Western Parkland City) 2021 – Camden Growth
# Centres (Appendix 5), State Environmental Planning Policy No 19—Bushland in Urban Areas, Sydney
# Regional Environmental Plan No 20, Interim Development Order No 1.
_EPI_KIND = (r"(?:Local Environmental Plan|LEP|State Environmental Planning Policy|SEPP"
             r"|(?:Sydney |Regional |Deemed )?(?:Regional )?Environmental Plan|S?REP|Interim Development Order|IDO)")
# The kind of instrument after at most seven words of its place or subject; the rest is free.
_EPI_TITLE = re.compile(r"^(?:[A-Z][\w'’.&-]*\s){0,7}" + _EPI_KIND + r"(?=$|[\s(—–-])")
_EPI_YEAR_OR_NUMBER = re.compile(r"\b(?:1[89]\d{2}|20\d{2})\b|\bNo\.? ?\d{1,3}\b")
# CLEP2010, SEPP2021, LEP 2013, SREP20.
_EPI_ABBREVIATION = re.compile(r"^[A-Z]{0,6}(?:LEP|SEPP|REP|IDO) ?(?:\d{4}|\d{1,3})$")


def validate_au_nsw_epi(value):
    """The title of a NSW environmental planning instrument with its year or number: Camden Local
    Environmental Plan 2010, Camden LEP 2010, SEPP (Precincts—Western Parkland City) 2021, State
    Environmental Planning Policy No 19—Bushland in Urban Areas (not Camden DCP 2019 or LEP)."""
    text = " ".join(str(value).split())
    if not 7 <= len(text) <= 250 or not _EPI_YEAR_OR_NUMBER.search(text):
        return False
    if re.search(r"\b(?:DCP|Development Control Plan)\b", text):
        return False
    return bool(_EPI_TITLE.match(text))


def validate_au_nsw_epi_or_abbreviation(value):
    """A NSW EPI title or the abbreviation of a planning register: Camden LEP 2010, CLEP2010, SEPP2021."""
    text = str(value).strip()
    return bool(_EPI_ABBREVIATION.match(text)) or validate_au_nsw_epi(text)


# Camden DCP 2019, Camden Growth Centre Precincts DCP, Oran Park DCP Appendices and Attachments,
# Hornsby Development Control Plan 2013, DCP No 5, Camden Growth Centre Precincts DCP – Schedule 7.
_DCP_TITLE = re.compile(
    r"^(?:[A-Z(][\w'’.&()-]*\s|(?:and|of|for|to|the)\s){0,8}(?:DCP|Development Control Plan)(?=$|[\s—–-])")


def validate_au_nsw_dcp(value):
    """The title of a NSW development control plan: Camden DCP 2019, Camden Growth Centre Precincts DCP,
    Turner Road DCP, Hornsby Development Control Plan 2013 (not Camden LEP 2010 or DCP alone)."""
    text = " ".join(str(value).split())
    if not 5 <= len(text) <= 250 or text.upper() == "DCP":
        return False
    return bool(_DCP_TITLE.match(text))


# I38, I122, I90A; A12 (archaeological), C3 (conservation area); a few SEPP items are plain numbers.
_HERITAGE_ITEM = re.compile(r"^[IAC] ?\d{1,4}[A-Z]?$")


def validate_au_nsw_heritage_item_number(value):
    """A heritage item number of a NSW LEP schedule: I38, I122, I90A, A12, C3 (not 38, I12345 or IA)."""
    return bool(_HERITAGE_ITEM.match(str(value).strip().upper()))


AU_HERITAGE_SIGNIFICANCE = frozenset(("local", "state", "national", "world", "commonwealth", "local and state",
                                      "state and local", "regional and local"))


def validate_au_heritage_significance(value):
    """A heritage significance level: Local, State, National, World, Commonwealth (not High or 3)."""
    return " ".join(str(value).split()).lower() in AU_HERITAGE_SIGNIFICANCE


# Green alert, Amber alert, Red alert, No alert and the NHMRC wording (Green level surveillance, Amber
# alert level, Red level). A bare colour is a traffic light of anything: only in a field named for algae.
_ALGAE_ALERT = re.compile(
    r"^(?:(?:green|amber|red)[ -](?:alert|level|warning)(?: (?:level|surveillance|mode))*"
    r"|(?:green|amber|red) level surveillance(?: mode)?|no (?:current )?alerts?|white alert)$", re.I)
_ALGAE_COLOUR = re.compile(r"^(?:green|amber|red|white|none|no alert)$", re.I)


def validate_au_algae_alert_level(value):
    """A blue-green algae alert level: Green alert, Amber alert, Red alert, No alert, Green level
    surveillance (not Red alone, Yellow warning, High or Amber Alert 2023-01)."""
    return bool(_ALGAE_ALERT.match(" ".join(str(value).split())))


def validate_au_algae_alert_colour(value):
    """An alert level in a field named for blue-green algae, also as a bare colour: Green, Amber, Red,
    Green alert (not Yellow or High)."""
    text = " ".join(str(value).split())
    return bool(_ALGAE_COLOUR.match(text)) or validate_au_algae_alert_level(text)
