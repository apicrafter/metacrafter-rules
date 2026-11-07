"""Rules fixed after a scan of real exports (metacrafter-testdata, #44-#47).

Rules are matched the way metacrafter matches them: regex rules with ``fullmatch`` on the
value (field rules also on the lower-cased name), text rules by lower-cased membership, ppr
field guards anchored at both ends.
"""
import pathlib
import re

import pyparsing
import pytest
import yaml

RULES = pathlib.Path(__file__).resolve().parent.parent / "rules"


def load(path, rule_id):
    return yaml.safe_load((RULES / path).read_text(encoding="utf-8"))["rules"][rule_id]


def regex_values(path, rule_id):
    spec = load(path, rule_id)
    assert spec["type"] == "data" and spec["match"] == "regex"
    pattern = re.compile(spec["rule"])
    low, high = int(spec.get("minlen", 1)), int(spec.get("maxlen", 10 ** 6))
    return lambda value: low <= len(value) <= high and pattern.fullmatch(value) is not None


# --- #44 mimetype -------------------------------------------------------------------

@pytest.mark.parametrize("value", [
    "image/png", "image/gif", "text/csv", "text/xml", "text/html", "image/svg+xml", "video/mp4",
    "audio/mpeg", "image/webp", "application/xml", "application/pdf",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/html; charset=utf-8", "IMAGE/JPEG",
])
def test_mimetype_value_accepts_media_types(value):
    assert regex_values("common/common.yaml", "mimetypebyvalue")(value)


@pytest.mark.parametrize("value", ["image/2018/03", "image", "text/", "foo/bar", "and/or", "24/7"])
def test_mimetype_value_rejects_other_text(value):
    assert not regex_values("common/common.yaml", "mimetypebyvalue")(value)


# --- #45 is_/has_/show_ boolean guards ---------------------------------------------

PPR = {name: getattr(pyparsing, name) for name in (
    "Word", "Literal", "CaselessLiteral", "Optional", "ZeroOrMore", "oneOf", "printables", "alphanums", "nums")}
PPR["__builtins__"] = {}


def field_guard(path, rule_id):
    spec = load(path, rule_id)
    assert spec["fieldrulematch"] == "ppr"
    grammar = pyparsing.lineStart + eval(spec["fieldrule"], PPR) + pyparsing.lineEnd  # noqa: S307

    def matches(name):
        try:
            grammar.parseString(name)
            return True
        except pyparsing.ParseException:
            return False

    return matches


@pytest.mark.parametrize("rule_id,names,others", [
    ("isprefixrule", ["is_active", "IS_ACTIVE", "is-deleted", "isActive", "IsPublished"],
     ["iso", "ISO", "Iso", "isbn", "issue", "issued", "island", "is", "is_"]),
    ("hasprefixrule", ["has_photo", "hasPhoto", "HAS_IMAGE"], ["hash", "hashtag", "hashrate", "haste"]),
    ("showprefixrule", ["show_price", "showPrice", "SHOW_ALL"], ["shower", "showroom", "showcase"]),
])
def test_boolean_prefix_guards_need_a_word_boundary(rule_id, names, others):
    guard = field_guard("common/boolean.yaml", rule_id)
    for name in names:
        assert guard(name), name
    for name in others:
        assert not guard(name), name
