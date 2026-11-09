"""Data rules against the positive and negative examples of their metacrafter-registry datatype.

The rules are compiled the way metacrafter compiles them: the pyparsing expression must match
the whole value, the value length must be within minlen/maxlen, and the validator must accept it.
"""
import importlib
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
    data = yaml.safe_load((RULES / relpath).read_text(encoding="utf-8"))
    rule = data["rules"][rule_id]
    assert rule["match"] == "ppr" and rule["type"] == "data"
    assert int(rule.get("minlen", 0)) <= int(rule.get("maxlen", 10**6))
    with warnings.catch_warnings():
        # Rule files use the camelCase pyparsing names that metacrafter provides (oneOf).
        warnings.simplefilter("ignore", DeprecationWarning)
        expression = eval(rule["rule"], NAMESPACE)
    parser = pyparsing.lineStart + expression + pyparsing.lineEnd
    validator = None
    if "validator" in rule:
        module, name = rule["validator"].rsplit(".", 1)
        validator = getattr(importlib.import_module(module), name)

    def accepts(value):
        if not int(rule.get("minlen", 0)) <= len(value) <= int(rule.get("maxlen", 10**6)):
            return False
        try:
            parser.parse_string(value)
        except pyparsing.ParseException:
            return False
        return validator is None or bool(validator(value))

    return accepts


# rule file, rule id, registry positive examples, registry negative examples
CASES = [
    ("basic/identifiers.yaml", "ulidvalue",
     ["01ARZ3NDEKTSV4RRFFQ69G5FAV", "01AN4Z07BY79KA1307SR9X4MV3", "7ZZZZZZZZZZZZZZZZZZZZZZZZZ"],
     ["8ZZZZZZZZZZZZZZZZZZZZZZZZZ", "01ARZ3NDEKTSV4RRFFQ69G5FAU", "01ARZ3NDEKTSV4RRFFQ69G5FA"]),
    ("de/de_transport.yaml", "devehicleplatevalue",
     ["AB CD 123H", "M-XY 1234", "B-AB 1234", "HH-AB 12", "LÖ-A 1E"],
     ["B-AB 0123", "M-ÄB 123", "M-XY 12345"]),
    ("eu/eu_tax.yaml", "vatvalue",
     ["ATU13585627", "DE136695976", "ESB64717838", "FR40303265045", "IT00743110157",
      "NL004495445B01", "PL8567346215", "SE556012579001", "SK2022749619", "XI432525179"],
     ["GR072830684", "DE 136695976", "DE13669597", "DE136695978", "FRIO334175221"]),
    ("fr/fr_tax.yaml", "frvatvalue",
     ["FR40303265045", "FR23334175221", "FRK7399859412"],
     ["FRIO334175221", "FR4030326504", "FR41303265045"]),
    ("common/internet.yaml", "asnbyprefixname",
     ["AS64496", "AS174", "AS4294967295"],
     ["AS0", "AS4294967296", "AS012"]),
    ("us/us_finances.yaml", "cusipvalue",
     ["037833100", "38259P508", "30303M102", "DUS0421C5", "91324PAE2"],
     ["DUS0421CN"]),
    ("eg/eg_finances.yaml", "egibanvalue",
     ["EG380019000500000000263180002"],
     ["EG38001900050000000026318000"]),
    ("de/de_tax.yaml", "deustvalue",
     ["DE136695976", "DE649565454"],
     ["DE13669597", "136695976", "DE136695978"]),
    ("eu/eu_tax.yaml", "eu_tax_ibanvalue",
     ["GB82WEST12345698765432", "GB82 WEST 1234 5698 7654 32", "DE89370400440532013000"],
     ["GB82WEST12345698765433"]),
    ("common/crossborder_finance.yaml", "ibanvalue",
     ["GB82WEST12345698765432", "GB82 WEST 1234 5698 7654 32", "DE89370400440532013000"],
     ["GB82WEST12345698765433"]),
    ("pii/de/de_pii.yaml", "de_pii_ibanvalue",
     ["DE89370400440532013000", "DE89 3704 0044 0532 0130 00"],
     ["DE89370400440532013001", "DE8937040044053201300"]),
    ("common/objects.yaml", "isbn13valuewithdashes",
     ["978-0-521-29366-2", "978-0-521-22151-1", "978-1107075412", "978-94-6298-380-9"],
     ["978-0-521-29366-3", "9780521293662"]),
    ("ext/ext_objects.yaml", "isbn13",
     ["978-0-521-29366-2", "978-0-521-22151-1", "978-1107075412", "978-94-6298-380-9"],
     ["978-0-521-29366-3"]),
    ("common/objects.yaml", "isbn10valuewithdashes",
     ["0-521-29366-9", "0-521-22151-X", "0-306-40615-2"],
     ["0-521-29366-8", "0521293669"]),
    ("ext/ext_objects.yaml", "isbn10",
     ["0-521-29366-9", "0-521-22151-X"],
     ["0-521-29366-8"]),
    ("common/media.yaml", "isbnvalue",
     ["9780521293662", "0-521-29366-9", "052122151X", "978-94-6298-380-9"],
     ["9770521293662", "0-521-29366-8"]),
    ("es/es_datetime.yaml", "esmonthbydatafiltered",
     ["1", "01", "9", "10", "11", "12"],
     ["0", "00", "13", "20", "123"]),
    # Substance-level ATC codes (7 characters); group codes such as A13A are not matched.
    ("common/medical.yaml", "atcvalue",
     ["D08AX08", "A02BC04", "M04AA03", "J05AR21"],
     ["A13A", "M04A03", "12345AB", "L03AX", "W01AA01"]),
    ("ru/ru_codes.yaml", "ruokpdcodepat",
     ["35.30.12.130", "91.01.11", "21.20.10.226", "21.20.1", "21.20"],
     ["35-30-12", "192.168.1.1", "21.20.10.22", "1.20.10.226", "21.20.10.2260"]),
    ("common/objects.yaml", "wikidataidvalue",
     ["Q12345", "Q234511", "Q1057890", "Q1"],
     ["P6782", "Q01", "Q0", "Q12345678901"]),
    # ISSN with and without the hyphen, with the X check character.
    *[(relpath, rule_id,
       ["0028-0836", "1476-4687", "0261-3077", "0960-894X", "00280836", "0960894X"],
       ["0028-0837", "0028-083", "0028-08361", "00280-836"])
      for relpath, rule_id in [("common/media.yaml", "issnvalue"),
                               ("common/objects.yaml", "objects_issnvalue"),
                               ("common/objects.yaml", "issnvaluewithoutdash")]],
    # ORCID and ISNI use the ISO 7064 MOD 11-2 check character (#23).
    ("common/science.yaml", "orcidbyvalue",
     ["0000-0002-1003-5675", "0000-0002-1825-0097", "0009-0001-2345-6786"],
     ["0000-0002-1825-0098", "0000000218250097", "0008-0001-2345-6786"]),
    ("common/science.yaml", "science_isnivalue",
     ["0000000123317789", "000000006629310X", "0000000121416409", "0000000122974701"],
     ["0000000122974702", "0000000066293100"]),
    ("common/science.yaml", "isnivaluewithspaces",
     ["0000 0001 2297 4701", "0000 0001 2141 6409", "0000 0000 6629 310X"],
     ["0000 0001 2297 4702"]),
    ("common/objects.yaml", "isnivalue",
     ["0000000123317789", "0000000121416409", "0000000122974701"],
     ["0000000122974702"]),
    # ISRC country codes: ISO 3166-1 alpha-2 or a code of the International ISRC Agency (#23).
    ("common/objects.yaml", "objects_isrcvalue",
     ["USRC17607839", "GBAYE7700223", "GBAYE7800109", "QMRC17607839"],
     ["USRC1760783", "XXRC17607839"]),
]

# text data rules: rule file, rule id, registry positive examples, registry negative examples
TEXT_CASES = [
    ("ru/ru_geo.yaml", "rusfeddistrict",
     ["Центральный федеральный округ", "Приволжский федеральный округ", "ЦФО", "СЗФО", "УрФО", "ДФО"],
     ["Крымский федеральный округ", "Приволжский", "Центральный"]),
    ("ru/ru_geo.yaml", "rusfeddistrictbyfield",
     ["Центральный федеральный округ", "Приволжский федеральный округ", "Приволжский", "ЦФО", "СЗФО",
      "УрФО", "Северо-Кавказский", "Дальневосточный"],
     ["Крымский федеральный округ", "Крымский", "Ленинский"]),
]


@pytest.mark.parametrize("relpath,rule_id,positives,negatives", CASES, ids=[c[1] for c in CASES])
def test_rule_on_registry_examples(relpath, rule_id, positives, negatives):
    accepts = load_rule(relpath, rule_id)
    assert [v for v in positives if not accepts(v)] == []
    assert [v for v in negatives if accepts(v)] == []


@pytest.mark.parametrize("relpath,rule_id,positives,negatives", TEXT_CASES, ids=[c[1] for c in TEXT_CASES])
def test_text_rule_on_registry_examples(relpath, rule_id, positives, negatives):
    data = yaml.safe_load((RULES / relpath).read_text(encoding="utf-8"))
    rule = data["rules"][rule_id]
    assert rule["match"] == "text" and rule["type"] == "data"
    keywords = {keyword.strip().lower() for keyword in rule["rule"].split(",")}
    assert [v for v in positives if v.lower() not in keywords] == []
    assert [v for v in negatives if v.lower() in keywords] == []


def test_rusfeddistrict_short_names_need_the_field_name():
    rules = yaml.safe_load((RULES / "ru/ru_geo.yaml").read_text(encoding="utf-8"))["rules"]
    guarded = rules["rusfeddistrictbyfield"]
    assert guarded["fieldrulematch"] == "text"
    assert {"федеральный округ", "federal_district"} <= set(guarded["fieldrule"].split(","))
    assert "fieldrule" not in rules["rusfeddistrict"]
    unguarded = set(rules["rusfeddistrict"]["rule"].split(","))
    assert unguarded < set(guarded["rule"].split(","))


def test_esmonthbydatafiltered_is_a_month_rule():
    data = yaml.safe_load((RULES / "es/es_datetime.yaml").read_text(encoding="utf-8"))
    assert data["rules"]["esmonthbydatafiltered"]["key"] == "month"


def test_modules_compile_without_syntax_warnings():
    package = RULES.parent / "metacrafterext"
    for path in sorted(package.rglob("*.py")):
        with warnings.catch_warnings():
            warnings.simplefilter("error", SyntaxWarning)
            compile(path.read_text(encoding="utf-8"), str(path), "exec")


# Regex rules (metacrafter-registry#175 examples): rule file, rule id, positives, negatives.
REGEX_CASES = [
    ("de/de_tax.yaml", "dehrbvalue",
     ["HRA 11223", "HRB 12345 B", "GnR 11223", "HRB12345", "VR 4711", "Aachen HRA 11223",
      "Frankfurt/Oder GnR 11223"],
     ["HRC 44123", "H12345", "HRB 0123", "HRB 1234567", "Aachen HRC 44123"]),
    ("eu/eu_tax.yaml", "euidvalue",
     ["CYDRCOR.HE139104", "DKCVR.11845118", "DEX1517R.HRB395KI", "MTROC.C22796", "ELGEMI.077700527000",
      "BEKBOBCE.1014.559.919"],
     ["CYDRCORHE139104", "FR1234567890"]),
]


@pytest.mark.parametrize("relpath,rule_id,positives,negatives", REGEX_CASES, ids=[c[1] for c in REGEX_CASES])
def test_regex_rule_on_registry_examples(relpath, rule_id, positives, negatives):
    from tests.test_testdata_baseline import value_matches

    assert [v for v in positives if not value_matches(relpath, rule_id, v)] == []
    assert [v for v in negatives if value_matches(relpath, rule_id, v)] == []
