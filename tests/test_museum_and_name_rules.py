"""Rules for museum object data and name-guarded rules (metacrafter-rules#11-#15,
metacrafter-registry#135-#138).

Values come from the metacrafter-registry examples and from an export of museum objects
(ar.culture.ru), where these rules found no match or a wrong one.
"""
import importlib
import pathlib
import re

import pytest
import yaml

from metacrafterext.rules.common.dating import is_historical_dating
from metacrafterext.rules.common.identifiers import validate_oid, validate_oid_value
from metacrafterext.rules.common.internet import is_fqdn
from metacrafterext.rules.ru.dating import is_ru_historical_dating

RULES = pathlib.Path(__file__).resolve().parent.parent / "rules"


def rule(relpath, rule_id):
    return yaml.safe_load((RULES / relpath).read_text(encoding="utf-8"))["rules"][rule_id]


def regex_accepts(relpath, rule_id):
    spec = rule(relpath, rule_id)
    assert spec["match"] == "regex"
    pattern = re.compile(spec["rule"])
    low, high = int(spec.get("minlen", 1)), int(spec.get("maxlen", 256))
    return lambda value: low <= len(value) <= high and pattern.fullmatch(value) is not None


# --- #11 fqdn ---------------------------------------------------------------------

@pytest.mark.parametrize("value", [
    "ec2-35-160-210-253.us-west-2.compute.amazonaws.com", "xn--kxae4bafwg.xn--pxaix.gr",
    "example.com", "слово.рф",
])
def test_fqdn_accepts_domains(value):
    assert is_fqdn(value)


@pytest.mark.parametrize("value", [
    "ニコラ･プッサン。リナルドとアルミーダ", "abc。com", "abc．com", "abc｡com",
    "did:web:w3c-ccg.github.io", "my host.example.com", "localhost", "",
])
def test_fqdn_rejects_text_with_ideographic_full_stops(value):
    assert not is_fqdn(value)


@pytest.mark.parametrize("value", [
    # SharePoint type names and WordPress thumbnail file names (#43): no such TLD.
    "SP.ContentType", "SP.ContentTypeId", "2-150x150.png", "cave-768x470.png", "report.pdf",
    "data.csv", "index.html",
])
def test_fqdn_rejects_names_without_a_delegated_tld(value):
    assert not is_fqdn(value)


@pytest.mark.parametrize("value", ["gov.ru", "www.osm.gov.ru", "EXAMPLE.ORG", "a.b.c.xn--p1ai", "test.москва"])
def test_fqdn_accepts_delegated_tlds(value):
    assert is_fqdn(value)


def test_tld_list_is_the_iana_root_zone():
    from metacrafterext.rules.common.tlds import TLDS

    assert len(TLDS) > 1000
    assert {"ru", "com", "xn--p1ai", "zip"} <= TLDS
    assert not {"png", "pdf", "csv", "contenttype"} & TLDS


def test_fqdn_rule_uses_is_fqdn():
    assert rule("common/commonurl.yaml", "fqdnbyvalidators")["rule"] == "metacrafterext.rules.common.internet.is_fqdn"


# --- #12 oid ----------------------------------------------------------------------

@pytest.mark.parametrize("value", ["1.3.6.1.4.1.343", "2.5.4.87", "2.5.4", "0.9.2342.19200300.100.1.1"])
def test_oid_value_accepts_oids(value):
    assert validate_oid_value(value)


@pytest.mark.parametrize("value", ["0.1", "0.39106583072100315", "0.15255723781388478", "1.5", "0.0391", "1.40.1", "1.03.6"])
def test_oid_value_rejects_fractions(value):
    assert not validate_oid_value(value)


def test_oid_keeps_two_arcs_and_drops_invalid_second_arcs():
    assert validate_oid("2.5")
    assert not validate_oid("0.39106583072100315")
    assert rule("common/objects.yaml", "oidvalue")["validator"].endswith(".validate_oid_value")


# --- #13 Goskatalog ---------------------------------------------------------------

def test_goskatalog_value_rule():
    accepts = regex_accepts("ru/ru_gov.yaml", "rugoskatalogregnumvalue")
    assert all(accepts(v) for v in ["1968551", "9881829", "10170632", "24245806"])
    assert not any(accepts(v) for v in ["КП 296809/249", "0123456", "123456", "123456789"])


def test_goskatalog_rules_need_the_field_name():
    value = rule("ru/ru_gov.yaml", "rugoskatalogregnumvalue")
    field = rule("ru/ru_gov.yaml", "rugoskatalogregnumfield")
    assert value["fieldrulematch"] == "text"
    assert "goskatalognumber" in value["fieldrule"].split(",")
    assert value["fieldrule"] == field["rule"]


# --- #14 surname with initials, author ---------------------------------------------

def test_initials_surname_rule():
    accepts = regex_accepts("ru/ru_persons.yaml", "rusinitialssurname")
    positives = ["И.И. Иванов", "И.И.Иванов", "Иванов И.И.", "П.Сидоров",
                 "Айвазовский И.К.", "Бринцева А.", "Билибин И.Я.", "Салтыков-Щедрин М.Е."]
    assert [v for v in positives if not accepts(v)] == []
    negatives = ["Иванов Иван Иванович", "Пабло Пикассо", "Нет", "ИВАНОВ И.И.", "I.I. Ivanov"]
    assert [v for v in negatives if accepts(v)] == []


def test_author_field_is_a_creator():
    spec = rule("common/dublincore.yaml", "authorfield")
    assert spec["key"] == "dc_creator"
    assert {"author", "автор"} <= set(spec["rule"].split(","))


# --- #15 locale -------------------------------------------------------------------

def test_language_tag_rules_name_locales():
    field = rule("common/intcodes.yaml", "languagetagfield")
    value = rule("common/intcodes.yaml", "languagetag")
    assert {"locale", "locales", "lang"} <= set(field["rule"].split(","))
    assert value["fieldrulematch"] == "text"
    assert {"locale", "locales", "lang"} <= set(value["fieldrule"].split(","))
    assert "imprecise" not in value
    codes = set(value["rule"].split(","))
    assert {"ru", "en", "es", "de", "fr", "ja", "zh", "it"} <= codes


# --- registry#135 slug, #137 object dimensions -----------------------------------

def test_slug_rule():
    accepts = regex_accepts("common/commonurl.yaml", "slugvalue")
    assert all(accepts(v) for v in ["model-gruzovogo-parohoda-donec", "kochedyk-10", "oil-on-canvas"])
    assert not any(accepts(v) for v in ["Model Donec", "model--donec", "-donec", "donec-"])
    assert rule("common/commonurl.yaml", "slugvalue")["fieldrule"] == rule("common/commonurl.yaml", "slugfield")["rule"]


def test_object_dimensions_rule():
    accepts = regex_accepts("common/culture.yaml", "objectdimensionsvalue")
    positives = ["30х40 см", "25х20.5 см", "68 x 82 cm", "10 x 15 x 2 cm", "40x30 cm", "20,3x20 см", "92×73 cm"]
    assert [v for v in positives if not accepts(v)] == []
    assert not any(accepts(v) for v in ["1920x1080", "30 см", "65х81", "canvas, oil"])


# --- registry#138 historical dating -----------------------------------------------

@pytest.mark.parametrize("value", [
    "XIX век", "Конец XVIII века", "конец XIX - начало XX века", "XVIII-XIX вв.", "ХХ век",
    "XIX в.", "Вторая половина XIX века", "первая четверть XX в.", "1950-е гг.", "1940-е годы",
    "конец 1930-х годов", "1930-1940-е гг.", "40-е годы XX века", "III тыс. до н.э.", "I в. до н.э.",
    "20 век", "XVII век - первая треть XVIII века", "Конец ХIХ века начало ХХ века",
])
def test_ru_historical_dating_accepts(value):
    assert is_ru_historical_dating(value)


@pytest.mark.parametrize("value", [
    "1895", "12.05.1895", "1895 г.", "Холст, масло", "Россия", "XIX", "век", "Иванов И.И.", "",
])
def test_ru_historical_dating_rejects(value):
    assert not is_ru_historical_dating(value)


@pytest.mark.parametrize("value", [
    "19th century", "early 20th century", "Late 19th century", "the second half of the 19th century",
    "late XIX - early XX centuries", "1st century BC", "5th century BC - 5th century AD",
    "Late 19th century – early 20th century", "1950s", "1920-1930s", "the mid-19th century",
])
def test_historical_dating_accepts(value):
    assert is_historical_dating(value)


@pytest.mark.parametrize("value", ["1895", "oil on canvas", "century", "19th", "Pablo Picasso", "1950", ""])
def test_historical_dating_rejects(value):
    assert not is_historical_dating(value)


# --- function rules import ---------------------------------------------------------

@pytest.mark.parametrize("relpath", [
    "common/commonurl.yaml", "common/culture.yaml", "en/dateandtime.yaml", "ru/ru_datetime.yaml",
])
def test_function_rules_import(relpath):
    data = yaml.safe_load((RULES / relpath).read_text(encoding="utf-8"))
    for spec in data["rules"].values():
        for name in [spec["rule"]] if spec["match"] == "func" else []:
            if not name.startswith("metacrafterext."):
                continue
            module, func = name.rsplit(".", 1)
            assert callable(getattr(importlib.import_module(module), func))
