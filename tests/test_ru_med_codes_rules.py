"""Russian medicine and classifier rules for the columns of an ESKLP export.

ESKLP (Единый справочник-каталог лекарственных препаратов) has the columns okpd2, ath,
std_mnn_name, norm_mnn, klp_all_list, klp_active_list, ftg and smnn_pe. See
apicrafter/metacrafter-rules#8, #9 and #10.

The rules are compiled the way metacrafter compiles them. A ppr expression must match the whole
string, and ppr field rules and field guards see the field name as it is (not lower-cased).
Text rules compare lower-cased names and values.
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
    "alphas": pyparsing.alphas,
    "alphanums": pyparsing.alphanums,
    "nums": pyparsing.nums,
    "printables": pyparsing.printables,
    "__builtins__": {},
}


def load_rules(relpath):
    return yaml.safe_load((RULES / relpath).read_text(encoding="utf-8"))["rules"]


def matcher(expression):
    """Return a function that tells whether the ppr expression matches a whole string."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        parser = pyparsing.lineStart + eval(expression, NAMESPACE) + pyparsing.lineEnd

    def matches(text):
        try:
            parser.parse_string(text)
        except pyparsing.ParseException:
            return False
        return True

    return matches


def keywords(rule_text):
    """Names or values of a text rule, as metacrafter reads them (split on commas, lower case)."""
    return set(map(str.lower, rule_text.split(",")))


def check(matches, positives, negatives):
    assert [name for name in positives if not matches(name)] == []
    assert [name for name in negatives if matches(name)] == []


# --- OKPD2 and OKVED (#8) ---------------------------------------------------------------


def test_okpd_field_rule():
    rule = load_rules("ru/ru_codes.yaml")["ruokpdknown"]
    assert rule["key"] == "okpd" and rule["type"] == "field" and rule["match"] == "text"
    assert {"okpd", "okpd2", "okpd_2", "okpd_code", "okpd2_code", "окпд", "окпд2", "код окпд",
            "код окпд2"} <= keywords(rule["rule"])


def test_okpd_value_rule_needs_okpd_in_field_name():
    rule = load_rules("ru/ru_codes.yaml")["ruokpdcodepat"]
    assert rule["key"] == "okpd" and rule["fieldrulematch"] == "ppr"
    check(matcher(rule["fieldrule"]),
          ["okpd2", "okpd", "okpd_2", "okpd2_code", "main_okpd2", "код окпд2", "Код по ОКПД2",
           "OKPD2", "kod_po_okpd2"],
          ["okved", "okved2", "ipv4", "smnn_code", "stokpd", "okp", "code"])


def test_okpd_imprecise_rule_is_the_value_rule_without_a_guard():
    rules = load_rules("ru/ru_codes.yaml")
    precise, imprecise = rules["ruokpdcodepat"], rules["ruokpdcodepatimprecise"]
    assert imprecise["key"] == "okpd" and imprecise["imprecise"] == 1
    assert "fieldrule" not in imprecise
    assert imprecise["rule"] == precise["rule"]
    assert (imprecise["minlen"], imprecise["maxlen"]) == (precise["minlen"], precise["maxlen"])


def test_okved_value_rule_guard_matches_okved_field_names():
    # The former guard, Optional(Word(printables)) + Literal('okved') + ..., never matched
    # okved or main_okved: Word(printables) consumed the whole name and pyparsing does not
    # backtrack.
    rule = load_rules("ru/ru_codes.yaml")["ruookvedcodepat"]
    assert rule["key"] == "okved" and rule["fieldrulematch"] == "ppr"
    check(matcher(rule["fieldrule"]),
          ["okved", "okved2", "okved_2", "main_okved", "okved_code", "OKVED", "main okved",
           "код оквэд", "ОКВЭД2", "код оквед"],
          ["okpd2", "mokved", "inn", "ogrn"])


# --- ESKLP medicine columns (#9) --------------------------------------------------------


def test_atc_field_names():
    rule = load_rules("ru/ru_med.yaml")["rumedicineatcbyknown"]
    assert rule["key"] == "atccode" and rule["type"] == "field"
    assert {"код атх", "код_атх", "атх", "ath", "atx"} <= keywords(rule["rule"])


def test_mnn_field_names():
    rules = load_rules("ru/ru_med.yaml")
    assert "наименование мнн" in keywords(rules["rumnnknownfull"]["rule"])
    rule = rules["rumnnbyname"]
    assert rule["key"] == "rumedmnn" and rule["type"] == "field" and rule["match"] == "ppr"
    # A bare mnn is matched by the text rule rumnnknownshort.
    check(matcher(rule["rule"]),
          ["std_mnn_name", "mnn_name", "norm_mnn", "MNN_NAME", "Std_Mnn", "mnn_names", "std-mnn"],
          ["mnn", "std_mnn_gid", "mnn_id", "mnn_code", "smnn_pe", "smnn_gid", "mnnx", "amnn",
           "solemnness", "column_name", "x_mnnx", "std mnn name"])


def test_trade_name_field_names():
    rules = load_rules("ru/ru_med.yaml")
    assert {"торговое наименование", "торговое_наименование"} <= keywords(
        rules["rumedicinetradenamebyknown"]["rule"])
    rule = rules["rumedicinetradenamebyklp"]
    assert rule["key"] == "rumedicinetradename" and rule["type"] == "field"
    # ESKLP also has smnn_all_klp_count and smnn_active_klp_count: counts, not names.
    check(matcher(rule["rule"]),
          ["klp_all_list", "klp_active_list", "klp_name", "KLP_NAME", "std_klp_name"],
          ["klp", "klp_gid", "klp_code", "smnn_all_klp_count", "smnn_active_klp_count",
           "klp_all_list_count", "sklp_name", "klpx_name"])


def test_pharmacotherapeutic_group_field_names():
    rule = load_rules("ru/ru_med.yaml")["rumedicationclassbyknown"]
    assert rule["key"] == "medication_class" and rule["type"] == "field"
    assert keywords(rule["rule"]) == {"ftg", "фтг", "фармакотерапевтическая группа"}


# --- OKEI unit symbols (#10) ------------------------------------------------------------

# Values of the ESKLP column smnn_pe without the one-letter symbols г and л.
ESKLP_UNITS = ["шт.", "мл", "мг", "доз(а)", "ЕД", "МЕ", "МБк", "млн.МЕ", "мкг", "усл. ед",
               "млн.ЕД", "м3", "кг"]


def test_unit_symbols_by_value():
    rule = load_rules("ru/ru_codes.yaml")["ruokeisymbol"]
    assert rule["key"] == "unit_of_measure" and rule["type"] == "data" and rule["match"] == "text"
    assert "fieldrule" not in rule
    symbols = keywords(rule["rule"])
    assert [value for value in ESKLP_UNITS if value.lower() not in symbols] == []
    # One-letter symbols are ambiguous: г (город, год), м (a gender), л, т.
    assert [symbol for symbol in symbols if len(symbol) < 2] == []
    assert not {"г.", "м.", "л.", "т.", "год", "мин"} & symbols


def test_unit_symbols_with_unit_field_name():
    rules = load_rules("ru/ru_codes.yaml")
    rule = rules["ruokeisymbolbyfield"]
    assert rule["key"] == "unit_of_measure" and rule["fieldrulematch"] == "text"
    symbols = keywords(rule["rule"])
    assert keywords(rules["ruokeisymbol"]["rule"]) <= symbols
    assert {"г", "м", "л", "т", "%"} <= symbols
    assert {"ед_изм", "единица измерения", "unit", "uom"} <= keywords(rule["fieldrule"])


@pytest.mark.parametrize("rule_id", ["ruokeisymbol", "ruokeisymbolbyfield"])
def test_unit_symbols_have_no_empty_or_padded_values(rule_id):
    values = load_rules("ru/ru_codes.yaml")[rule_id]["rule"].split(",")
    assert [value for value in values if not value or value != value.strip()] == []
    assert len(values) == len(set(map(str.lower, values)))


def test_esklp_code_by_value():
    rule = load_rules("ru/ru_med.yaml")["ruesklpcodevalue"]
    assert rule["key"] == "ru_esklp_code"
    check(
        matcher(rule["rule"]),
        [
            "21.20.10.226-000001-1-00008-0000000000000",
            "21.20.10.194-000111-1-00001-0000000000000",
            "21.20.21.120-000097-1-00072-0000000000000",
        ],
        ["21.20.10.226", "21.20.10.226-000001-1-00008", "21.20.10.226-000001-1-00008-000000000000", "21.20.10.22-000001-1-00008-0000000000000"],
    )
    assert all(rule["minlen"] <= len(v) <= rule["maxlen"] for v in ["21.20.10.226-000001-1-00008-0000000000000"])


def test_esklp_code_field_names():
    rule = load_rules("ru/ru_med.yaml")["ruesklpcodeknown"]
    assert {"smnn_code", "klp_code", "esklp_code", "код есклп"} <= keywords(rule["rule"])
