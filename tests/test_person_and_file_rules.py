"""Person name and file extension rules report the universal metacrafter-registry datatypes.

In the registry, ``person_name`` is a Chinese record (country CN), and ``firstname`` and
``lastname`` are Indian records (country IN). Rules for other countries report
``person_fullname``, ``person_firstname`` and ``person_surname``. See apicrafter/metacrafter#42.
"""
import pathlib
import warnings

import pyparsing
import yaml

RULES = pathlib.Path(__file__).resolve().parent.parent / "rules"

NAMESPACE = {
    "Word": pyparsing.Word,
    "Literal": pyparsing.Literal,
    "Optional": pyparsing.Optional,
    "alphas": pyparsing.alphas,
    "alphanums": pyparsing.alphanums,
    "__builtins__": {},
}

# Rule files whose full-name rules are for Chinese names, the registry record person_name.
PERSON_NAME_FILES = {"cn/cn_persons.yaml", "zh/zh_persons.yaml"}


def rule_files():
    for path in sorted(RULES.rglob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        yield path.relative_to(RULES).as_posix(), data


def load(relpath):
    return yaml.safe_load((RULES / relpath).read_text(encoding="utf-8"))


def keywords(rule):
    """Field names of a text rule, as metacrafter reads them (split on commas, lower case)."""
    return set(map(str.lower, rule["rule"].split(",")))


def test_country_specific_person_keys_only_for_their_country():
    wrong = []
    for relpath, data in rule_files():
        for rule_id, rule in (data.get("rules") or {}).items():
            key = rule.get("key")
            if key in ("firstname", "lastname") or (key == "person_name" and relpath not in PERSON_NAME_FILES):
                wrong.append(f"{relpath}: {rule_id} -> {key}")
    assert not wrong, "rules report a CN/IN registry record for other countries:\n" + "\n".join(wrong)


def test_universal_full_name_rule():
    data = load("common/persons.yaml")
    assert data["country_code"] == "xx"
    rule = data["rules"]["fullname"]
    assert rule["key"] == "person_fullname"
    assert {"full_name", "person_name"} <= keywords(rule)


def test_au_in_sg_rules_report_universal_keys():
    assert load("au/au_persons.yaml")["rules"]["aupersonnameknown"]["key"] == "person_fullname"
    assert load("sg/sg_common.yaml")["rules"]["sgpersonnameknown"]["key"] == "person_fullname"
    rules = load("in/in_persons.yaml")["rules"]
    assert rules["inpersonnameknown"]["key"] == "person_fullname"
    assert rules["infirstnameknown"]["key"] == "person_firstname"
    assert rules["inlastnameknown"]["key"] == "person_surname"


def test_last_name_is_a_surname_not_a_middle_name():
    rules = load("common/persons.yaml")["rules"]
    assert "last name" in keywords(rules["surname"])
    assert "last name" not in keywords(rules["midname"])
    assert {"given_name"} <= keywords(rules["firstname"])
    assert {"family_name"} <= keywords(rules["surname"])


def test_file_extension_field_rule():
    data = load("common/common.yaml")
    assert data["country_code"] == "xx"
    rule = data["rules"]["fileextensionbyknown"]
    assert rule["key"] == "file_extension" and rule["type"] == "field"
    assert {"file_extension", "file_ext"} <= keywords(rule)


def test_file_extension_value_rule():
    rule = load("common/common.yaml")["rules"]["fileextensionbyvalue"]
    assert rule["key"] == "file_extension" and rule["type"] == "data"
    assert rule["fieldrulematch"] == "text"
    assert {"extension", "ext"} <= set(rule["fieldrule"].split(","))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        expression = eval(rule["rule"], NAMESPACE)
    # metacrafter anchors ppr data rules at both ends.
    parser = pyparsing.lineStart + expression + pyparsing.lineEnd

    def accepts(value):
        if not int(rule["minlen"]) <= len(value) <= int(rule["maxlen"]):
            return False
        try:
            parser.parse_string(value)
        except pyparsing.ParseException:
            return False
        return True

    # Registry positive examples of file_extension and GeoNode links.extension values.
    for value in ["pdf", ".docx", "CSV", "zip", "png", "mp3"]:
        assert accepts(value), value
    # A file name (registry negative example), compound or overlong suffixes, and phone
    # extensions, which share the field name "extension".
    for value in ["report.pdf", "tar.gz", "abcdefghijk", ".", "1234", "101"]:
        assert not accepts(value), value
