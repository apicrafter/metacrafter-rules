"""Rules for the RDA-UNR files of metacrafter-testdata (Repositorio de Datos Académicos of the
Universidad Nacional de Rosario, Argentina; Dataverse snapshot of April 2024): part-of-speech
tags, rating-scale answers, academic disciplines, age bands in an age column, Excel serial
dates with a time, date ranges and fatty acid shorthand; a height column of words (tall, short)
is no height.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.common.chemistry import validate_lipid_number, validate_lipid_number_any
from metacrafterext.rules.common.dateandtime import validate_date_range, validate_excel_serial_datetime
from metacrafterext.rules.common.fieldwork import validate_length_value
from metacrafterext.rules.common.linguistics import validate_pos_tag
from metacrafterext.rules.common.survey import (
    validate_age_band,
    validate_age_range_value,
    validate_discipline_name,
    validate_likert_response,
)
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (validate_pos_tag, ["nom", "det", "prep", "v", "cl", "coma", "npr", "S/E", "comill", "descon", "NOUN", "PROPN", "NN",
                        "VBZ", "PRP$", "NCMS000", "VMIP3S0", "SPS00", "DA0MS0", "Fc", "Zm"],
     ["G", "D", "x", "1", "Total", "nombre", "Biología", "LA", "I", "W", "NCMS0000000000"]),
    (validate_likert_response, ["Totalmente de acuerdo", "Algo  de acuerdo", "Moderadamente  en desacuerdo", "No sé",
                                "Neutral", "Extremadamente probable", "Altamente improbable", "Sí, muy interesada/o",
                                "Me interesa poco", "Nunca", "A veces", "Strongly disagree", "Neither agree nor disagree",
                                "Stimme eher zu", "Plutôt d'accord"],
     ["Sí", "No", "4", "Yes", "Datos observacionales", "Universidad Nacional de Rosario (UNR)", ""]),
    (validate_discipline_name, ["Biología", "Ciencias de la Tierra", "Veterinaria y Esp. Pecuarias", "Computer science"],
     ["0101", "3.1", "Sí", "no", "Otro", ""]),
    (validate_age_band, ["45-54", "25 a 34", "65 o más", "Menor a 25", "65+", "18 - 24", "<18", "70 und älter", "Más de 80"],
     ["3", "45", "Entre 15 y 24 años", "adult", ""]),
    (validate_age_range_value, ["65 o más", "Menor a 25", "45-54", "3"], ["Entre 15 y 24 años", "-1"]),
    (validate_excel_serial_datetime, ["45175.42585648148", "31911.416666666668", "44927.5", 45168.38967592592],
     ["45175", "45175.0", "1234.5", "2.5", "2023-09-06 10:13:14"]),
    (validate_date_range, ["10-2-00/9-3-00", "5-4-02 al 27-5-02", "18-9-15 al  22-10-15", "2020-01-01/2020-03-31",
                           "01.03.2020 - 31.03.2020", "del 1/3/2020 al 31/3/2020"],
     ["16-9-9/24/10-09", "27-2-02/22-1-02", "2019-2020", "12/05/2020", "31-2-02/1-3-02", "08:00-22:00"]),
    (validate_lipid_number, ["iC14:0", "aC15:0", "nC16:0", "C18:2", "C18:1n-9", "C20:5n3", "iso-C15:0", "C18:2(9Z,12Z)"],
     ["16:00", "3:1", "18:2", "C40:1", "C2:1", "C16:9", "Total"]),
    (validate_lipid_number_any, ["18:2 n-6", "16:0", "C18:1"], ["2:1", "16:00", "abc"]),
    (validate_length_value, ["175", "3.2 m", "12,5 cm", "1080 px", "5'"], ["tall", "short", "-", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("common/science.yaml", "postagbyname", ["ETIQUETA_1", "ETIQUETA_CORRECTA", "ETIQUETA_ANTERIOR", "pos", "upos", "xpos",
                                             "pos_tag", "POS tag", "postag", "part_of_speech", "categoría gramatical", "Wortart"],
     ["position", "posted", "positive", "tag", "tags", "label", "deposit"]),
    ("common/science.yaml", "academicdisciplinebyname", ["disciplina", "disciplinaotro", "discipline", "academic_discipline",
                                                         "field_of_research", "research_area", "área de conocimiento",
                                                         "Fachgebiet", "disciplina_principal"],
     ["disciplinary_action", "area", "field", "disciplined", "research", "disciplinas_deportivas_club"]),
    ("common/science.yaml", "lipidnumberbyname", ["fatty_acid", "Fatty acids", "FAME", "ácido graso", "lipid_number",
                                                  "fa_name"],
     ["fat", "fatty", "lipids_mg", "acid"]),
    ("pii/pii.yaml", "agerangebyagename", ["edad", "age", "Alter", "EDAD", "age_years", "edad años"],
     ["edades", "agency", "age_group_code"]),
    ("common/dateandtime.yaml", "excelserialdatetimebyname", ["datecreated", "datemodified", "Fecha y Hora", "created_at",
                                                              "date", "start_time", "timestamp", "Fecha"],
     ["id", "amount", "Caudal Liquido [m3/s]", "update"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("common/science.yaml", "lipidnumbervalue", ["iC14:0", "aC15:0", "C18:1n-9"], ["18:2", "16:00", "3:1"]),
    ("common/survey.yaml", "likertresponsevalue", ["Totalmente de acuerdo", "Algo probable", "A veces"], ["Sí", "4"]),
    ("common/dateandtime.yaml", "daterangevalue", ["5-4-02 al 27-5-02", "22-1-02/27-2-02"], ["2019-2020", "5-4-02"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def test_new_field_rules_need_values():
    for path, rule_id, _, _ in FIELDS:
        assert load(path, rule_id).get("needs_values") is True, rule_id


def test_height_needs_a_length():
    spec = load("common/common.yaml", "heightmeasurementbyknown")
    assert spec["validator"] == "metacrafterext.rules.common.fieldwork.validate_length_value"
