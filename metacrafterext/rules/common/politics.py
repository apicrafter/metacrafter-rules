"""Political parties: the names of parties and registered groups in election results and lists of
office holders (Australian Labor Party, Canberra Liberals, The Greens)."""
import re

# Words that name a party or group in English and in the languages of the test data; a party name
# without one of them (a one-word brand such as Podemos) is left to the field name of other rules.
_PARTY_WORDS = re.compile(
    r"(?i)\b(?:party|parties|labou?r|liberals?|greens?|nationals?|democrats?|democratic|socialists?|"
    r"conservatives?|republicans?|communists?|alliance|coalition|front|movement|union|congress|league|"
    r"bloc|independents?|ungrouped|one nation|partei|parti|partido|partito|partij|partia|партия)\b"
)
# Companies and people named as the party of an agreement or a contract (JSC Pty Ltd).
_NOT_PARTY = re.compile(r"(?i)\b(?:pty|ltd|limited|inc|llc|gmbh|corp(?:oration)?|p/l|plc|s\.?a\.?|trust)\b|\d{3,}")


def validate_political_party(value):
    """A political party or group: Australian Labor Party, Liberal Party, Canberra Liberals, The Greens,
    Independent, Ungrouped (not JSC Pty Ltd, a person or a number)."""
    text = " ".join(str(value).strip().split())
    if not 2 <= len(text) <= 100 or _NOT_PARTY.search(text):
        return False
    return bool(_PARTY_WORDS.search(text))
