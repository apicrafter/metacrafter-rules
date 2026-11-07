"""ppr field guards of data rules against typical field names (apicrafter/metacrafter-rules#17).

metacrafter compiles a ``fieldrulematch: ppr`` guard as ``lineStart + expr + lineEnd`` and
matches it against the field name as it is (not lower-cased). pyparsing does not backtrack, so
a guard such as ``Optional(Word(printables)) + Literal('year') + Optional(Word(printables))``
never matches ``birth_year``: ``Word(printables)`` consumes the whole name. Such guards made
their value rules run only for names like ``birth year``.
"""
import pathlib
import warnings

import pyparsing
import pytest
import yaml

RULES = pathlib.Path(__file__).resolve().parent.parent / "rules"

NAMESPACE = {
    "Word": pyparsing.Word,
    "Literal": pyparsing.Literal,
    "CaselessLiteral": pyparsing.CaselessLiteral,
    "Optional": pyparsing.Optional,
    "ZeroOrMore": pyparsing.ZeroOrMore,
    "oneOf": pyparsing.oneOf,
    "LineStart": pyparsing.LineStart,
    "LineEnd": pyparsing.LineEnd,
    "lineStart": pyparsing.lineStart,
    "lineEnd": pyparsing.lineEnd,
    "alphas": pyparsing.alphas,
    "alphanums": pyparsing.alphanums,
    "hexnums": pyparsing.hexnums,
    "nums": pyparsing.nums,
    "printables": pyparsing.printables,
    "__builtins__": {},
}


def load_rule(relpath, rule_id):
    return yaml.safe_load((RULES / relpath).read_text(encoding="utf-8"))["rules"][rule_id]


def guard_matcher(expression):
    """Return a function that tells whether a field guard accepts a field name."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        parser = pyparsing.lineStart + eval(expression, NAMESPACE) + pyparsing.lineEnd

    def matches(name):
        try:
            parser.parse_string(name)
        except pyparsing.ParseException:
            return False
        return True

    return matches


def all_ppr_guards():
    for path in sorted(RULES.rglob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for rule_id, rule in (data.get("rules") or {}).items():
            if rule.get("fieldrulematch") == "ppr":
                yield path.relative_to(RULES).as_posix(), rule_id, rule["fieldrule"]


COUNTRY_NAMES = ["country", "Country", "COUNTRY", "country_code", "countrycode", "CountryCode",
                 "birth_country", "birth-country", "birth country", "country_of_birth",
                 "place_of_birth_country", "Country (ISO)", "country2"]
COUNTRY_OTHER = ["birthcountry", "county", "code", "cntry", "region"]

CASES = [
    *[("common/intcodes.yaml", rule_id, COUNTRY_NAMES, COUNTRY_OTHER)
      for rule_id in ["iso3166-alpha2", "iso3166-alpha3", "iso3166-alpha2imprecise",
                      "iso3166-alpha3imprecise"]],
    ("common/dateandtime.yaml", "yearbydatafiltered",
     ["year", "Year", "YEAR", "birth_year", "year_built", "yearofbirth", "fiscal_year",
      "build-year", "year2", "Year of birth"],
     ["birthyear", "yr", "date", "month"]),
    ("common/dateandtime.yaml", "yearbydataimprecise",
     ["year", "date", "time", "birth_year", "created_date", "start_time", "date_of_birth"],
     ["birthdate", "updated", "month"]),
    ("common/geo.yaml", "latitudevalue",
     ["lat", "Lat", "LAT", "geo_lat", "point_lat", "lat_wgs84", "lat2", "start-lat", "gps lat"],
     ["latest", "latest_value", "lateness", "flat", "plate", "geolat", "lon"]),
    ("common/geo.yaml", "longitudevalue",
     ["lon", "lng", "Lon", "LNG", "geo_lon", "point_lng", "lon_wgs84", "lon2", "gps lng"],
     ["long", "long_name", "lonely", "salon", "lat"]),
    ("ru/ru_geo.yaml", "rupostindex",
     ["индекс", "Индекс", "почтовый индекс", "почтовый_индекс", "индекс_почтовый",
      "Почтовый индекс получателя", "indeks", "post_index", "postal_index", "postindex",
      "Post Index", "address_post_index"],
     ["index", "row_index", "index_id", "zip", "почта"]),
]


@pytest.mark.parametrize("relpath,rule_id,positives,negatives", CASES, ids=[c[1] for c in CASES])
def test_guard_on_field_names(relpath, rule_id, positives, negatives):
    rule = load_rule(relpath, rule_id)
    assert rule["type"] == "data" and rule["fieldrulematch"] == "ppr"
    matches = guard_matcher(rule["fieldrule"])
    assert [name for name in positives if not matches(name)] == []
    assert [name for name in negatives if matches(name)] == []


@pytest.mark.parametrize("relpath,rule_id,expression", list(all_ppr_guards()),
                         ids=[guard[1] for guard in all_ppr_guards()])
def test_no_guard_starts_with_a_greedy_word(relpath, rule_id, expression):
    """A guard that starts with Word(printables) consumes the whole name and needs a space."""
    guard_matcher(expression)
    compact = expression.replace(" ", "")
    assert not compact.startswith(("Word(printables", "Optional(Word(printables"))


def test_postindex_value_rule_checks_values():
    # rupostindex was a field rule, so its value pattern was matched against field names.
    rule = load_rule("ru/ru_geo.yaml", "rupostindex")
    assert rule["key"] == "postindex" and rule["rule"] == "Word(nums, exact=6)"
    assert (rule["minlen"], rule["maxlen"]) == (6, 6)


def test_one_atc_value_rule():
    """ATC codes are language independent: one value rule, not one per language file."""
    value_rules = [(path, rule_id) for path in RULES.rglob("*.yaml")
                   for rule_id, rule in (yaml.safe_load(path.read_text(encoding="utf-8"))
                                         .get("rules") or {}).items()
                   if rule.get("key") == "atccode" and rule.get("type") == "data"]
    assert [rule_id for _, rule_id in value_rules] == ["atcvalue"]
    data = yaml.safe_load((RULES / "common/medical.yaml").read_text(encoding="utf-8"))
    assert data["lang"] == "common"
