"""Rules for the AUSSDA files of metacrafter-testdata (Austrian Social Science Data Archive,
Dataverse exports of 2024): survey weights, ages and age bands, coded sex, the Eurostat degree
of urbanisation, Correlates of War country codes, variable names of codebooks, ESS country
codes, and the checks that keep the V-Dem index v2x_gender off gender and the NTA consumption
column CF off the Italian tax number.

Matched as tests/test_testdata_baseline.py matches them.
"""
import re

import pytest

from metacrafterext.rules.common import survey
from metacrafterext.rules.common.identifiers import validate_it_taxid_shape
from tests.test_testdata_baseline import field_matches, guarded_by, load, value_matches

VALIDATORS = [
    (survey.validate_survey_weight, ["0.5977", "2.555830211799104", "1", "0", "1523.4", "7.9421225E-6", 0.92],
     ["-99", "-1", "abc", "", "1,000,000"]),
    (survey.validate_age_value, ["26", "22.0", "0", "90", "0.5", 42], ["-1", "131", "65+", "16-34", "x"]),
    (survey.validate_age_range_value, ["16-34", "65+", "<18", "20 bis 29 Jahre", "70 und älter", "18 - 24", "3", "1.0", 7],
     ["sixteen", "1.5", "-1", "100", "16-"]),
    (survey.validate_gender_code, ["1", "2", "0.0", "99", "M", "female", "Männlich", "W", "K"],
     ["0.912", "0.5", "1234", "10.75", ""]),
    (survey.validate_degurba, ["1", "2", "3", "1.0", 3], ["0", "4", "11", "urban", ""]),
    (survey.validate_cow_country_code, ["2", "20", "305", "900", "990", "260", "2.0", 365],
     ["040", "0", "1", "3", "1000", "AT", "999"]),
    (survey.validate_variable_name, ["f1", "SEX_2016", "Q28_1", "sugu#", "v2x_polyarchy", "doi", "W1_WEIGHTD", "Größe"],
     ["Wie zufrieden sind Sie?", "1", "12a", "Variable Label", ""]),
    (validate_it_taxid_shape, ["RSSMRA85T10A562S", "00743110157", "IT00743110157", "rssmra85t10a562s"],
     ["5616.664", "CF", "RSSMRA85T10A562", "0074311015"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


def test_cow_codes_are_the_state_system_list():
    assert len(survey.COW_COUNTRY_CODES) == 217
    assert {2, 20, 200, 255, 305, 365, 710, 900, 990} <= survey.COW_COUNTRY_CODES


FIELDS = [
    ("common/survey.yaml", "surveyweightbyname",
     ["dweight", "pspwght", "pweight", "anweight", "Gewicht_DES", "Gewicht_POS", "Gewicht_GES", "gew", "gew_roh",
      "gewichtung", "W1_WEIGHTD", "W1W10_WEIGHTD", "W2_WEIGHTP", "design_weight", "weight_final", "final weight",
      "wgt", "hh_wght", "perwt", "pwgtp", "weighting_factor", "hochrechnungsfaktor"],
     ["weight", "Gewicht", "Gewicht_kg", "gesamtgewicht", "weight_kg", "MolecularWeight", "wgt_kg", "height", "gewinn",
      "geworben"]),
    ("common/survey.yaml", "variablenamebyname",
     ["variable", "VARIABLENAME", "variable_name", "varname", "Variablenameindataset", "field_name", "Feldname",
      "column name"],
     ["value", "Label", "VARIABLELABEL", "variable_label", "variables_count", "var"]),
    ("common/survey.yaml", "cowcountrycodebyname", ["COWcode", "cowcode", "ccode", "ccode1", "ccode2", "cow_ccode", "statenum"],
     ["cow", "cows", "country_id", "countrycode", "code"]),
    ("pii/pii.yaml", "genderbyname",
     ["sex", "SEX", "SEX_2016", "SD_GENDER", "author_sex", "gender", "Geschlecht", "geschlecht", "GESCHLECHT",
      "sexo", "Sexo (catálogo)", "Gender (name)", "sugu", "kaaskoneleja_sugu", "sexe", "Code sexe", "пол", "v2x_gender"],
     ["sex_ratio", "intsex", "gendered", "geschlechter_verhaeltnis", "sussex"]),
    ("pii/pii.yaml", "agebyname",
     ["age", "AGE", "Alter", "ALTER", "edad", "vanus", "kaaskoneleja_vanus", "age_years", "patient_age", "âge", "ålder"],
     ["age_group", "SD_AGE_CAT", "alter_gr", "page", "image", "average", "stage", "age0", "age_zentr_1993", "Altersgruppen"]),
    ("pii/pii.yaml", "agerangebyname",
     ["age_group", "AGE_GROUP", "agegroup", "SD_AGE_CAT", "age_cat", "alter_gr", "Altersgruppen", "altersklasse",
      "age_range", "age band", "grupo de edad", "grupo_etario", "tranche_d_age", "Q1_age_group"],
     ["age", "Alter", "stage_group", "page_range", "agency"]),
    ("eu/eu_geo.yaml", "eudegurbabyname",
     ["degurba", "DEGURBA", "deg_urba", "urban", "xurb", "xurb12", "urbanisierung_ec", "urbanisation", "degree_of_urbanisation",
      "Grad der Urbanisierung", "DGURBA"],
     ["suburban", "urbanrural", "UrbanRural (code)", "rural", "urban_area_name"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


def test_variable_name_values_are_guarded():
    spec = load("common/survey.yaml", "variablenamevalue")
    for name in ("variable", "VARIABLENAME", "varname", "field_name"):
        assert re.search(spec["fieldregex"], name.rsplit(".", 1)[-1]), name
    for name in ("Label", "value", "id", "name"):
        assert not re.search(spec["fieldregex"], name), name
    for value in ("Q10", "M1", "SEX_2016", "doi"):
        assert value_matches("common/survey.yaml", "variablenamevalue", value), value
    assert not value_matches("common/survey.yaml", "variablenamevalue", "Variable Label")


def test_survey_country_names_take_iso_alpha2():
    for name in ("cntry", "ccode", "ctry"):
        assert guarded_by("common/intcodes.yaml", "iso3166alpha2bylocalname", name), name
    assert value_matches("common/intcodes.yaml", "iso3166alpha2bylocalname", "AT")


def test_italian_tax_names_check_values():
    assert load("it/it_finances.yaml", "ittaxidknown")["validator"].endswith("validate_it_taxid_shape")


def test_state_names_need_letters():
    # INFO-POW state is a 0/1 flag of state actors.
    for path, rule_id in (("au/au_geo.yaml", "austateknown"), ("in/in_geo.yaml", "instateknown")):
        assert load(path, rule_id)["validator"].endswith("survey.validate_not_flag"), rule_id
    for value in ("01", "06", "NSW", "Kerala", 6):
        assert survey.validate_not_flag(value), value
    for value in ("0", "1", "1.0", "yes", "False"):
        assert not survey.validate_not_flag(value), value
