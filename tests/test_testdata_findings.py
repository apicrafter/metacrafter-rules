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


# --- #46 URLs with character references --------------------------------------------

@pytest.mark.parametrize("value", [
    "https://www.paih.gov.pl/?post_type=events&#038;p=60566",
    "https://www.paih.gov.pl/?post_type=news&#038;p=60028",
    "https://example.org/?x=1&amp;y=2",
    "https://example.org/?a=1&copy=2",
    "http://nalog.ru",
])
def test_url_validator_accepts_urls_from_html_exports(value):
    from metacrafterext.rules.common.common import _validate_url

    assert _validate_url(value)


@pytest.mark.parametrize("value", ["not a url", "ftp//bad", "", None, "&#038;"])
def test_url_validator_rejects_other_text(value):
    from metacrafterext.rules.common.common import _validate_url

    assert not _validate_url(value)


def test_url_rules_use_the_url_validator():
    for path, rule_id in (("common/commonurl.yaml", "urlbyvalidators"), ("ext/ext_internet.yaml", "url")):
        assert load(path, rule_id)["rule"] == "metacrafterext.rules.common.common._validate_url"


# --- #47 unixtime, gender, HTTP status codes ---------------------------------------

def regex_field(path, rule_id):
    spec = load(path, rule_id)
    assert spec["type"] == "field" and spec["match"] == "regex"
    pattern = re.compile(spec["rule"])
    return lambda name: bool(pattern.fullmatch(name) or pattern.fullmatch(name.lower()))


def text_guard(path, rule_id):
    spec = load(path, rule_id)
    assert spec["fieldrulematch"] == "text"
    names = {name.strip().lower() for name in spec["fieldrule"].split(",")}
    return lambda name: name.lower() in names


@pytest.mark.parametrize("value", ["1471181882", "1652190194", "631152000", "2208988799", "1471181882123",
                                   "1652190195.25"])
def test_unixtime_value_accepts_timestamps(value):
    assert regex_values("common/dateandtime.yaml", "unixtimevalue")(value)


@pytest.mark.parametrize("value", ["0", "12345", "123456789", "3000000000", "99999999999999", "2021-09-17"])
def test_unixtime_value_rejects_other_numbers(value):
    assert not regex_values("common/dateandtime.yaml", "unixtimevalue")(value)


def test_unixtime_value_needs_a_timestamp_field():
    guard = field_guard("common/dateandtime.yaml", "unixtimevalue")
    for name in ("timestamp", "created_timestamp", "Event Timestamp", "created_ts", "epoch", "unix_time"):
        assert guard(name), name
    for name in ("inn", "phone", "posts", "id", "createdtimestamp"):
        assert not guard(name), name


def test_timestamp_name_pattern_reports_on_its_own():
    assert load("common/dateandtime.yaml", "timestampknownpat")["priority"] == 1


@pytest.mark.parametrize("name", ["sex", "Sex", "gender", "author_sex", "patient_gender", "sex_code",
                                  "Пол", "person sex"])
def test_gender_field_names(name):
    assert regex_field("pii/pii.yaml", "genderbyname")(name)


@pytest.mark.parametrize("name", ["essex", "sex_ratio", "unisex", "sexton", "polygon", "пол помещения"])
def test_gender_field_rejects_other_names(name):
    assert not regex_field("pii/pii.yaml", "genderbyname")(name)


def test_gender_values_need_a_gender_field():
    spec = load("pii/pii.yaml", "genderbyvalue")
    values = set(spec["rule"].split(","))
    assert {"м", "ж", "мужской", "женский", "m", "f", "male", "female"} <= values
    guard = text_guard("pii/pii.yaml", "genderbyvalue")
    assert guard("author_sex") and guard("Пол") and not guard("size")


@pytest.mark.parametrize("name", ["Statuscode", "status_code", "HTTP Status", "http_code", "response_code",
                                  "HttpStatusCode"])
def test_http_status_field_names(name):
    assert regex_field("common/internet.yaml", "httpstatuscodefield")(name)


@pytest.mark.parametrize("name", ["status", "code", "statuses", "zip_code"])
def test_http_status_field_rejects_other_names(name):
    assert not regex_field("common/internet.yaml", "httpstatuscodefield")(name)


def test_http_status_values():
    check = regex_values("common/internet.yaml", "httpstatuscodevalue")
    assert all(check(v) for v in ("200", "301", "404", "503", "101"))
    assert not any(check(v) for v in ("600", "99", "2000", "abc"))
    guard = text_guard("common/internet.yaml", "httpstatuscodevalue")
    assert guard("Statuscode") and not guard("status") and not guard("price")
