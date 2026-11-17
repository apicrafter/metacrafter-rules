"""Rules for the files of metacrafter-testdata from 2024 snapshots of 60 data catalogues (Dateno sources
temp00000210 to temp00005298): geoportals of Mongolia, Portugal, Sweden, Poland, the United Kingdom and the
Pacific, Open Data NI and other CKAN portals. Mongolian provinces, soums and bags with their codes;
Portuguese civil parishes; Healthcare Resource Groups; Northern Ireland wards, Super Output Areas and
district councils of 1992; UK road numbers; AddressBase classes; FACC feature codes.

Matched as tests/test_testdata_baseline.py matches them.
"""
import re

import pytest

from metacrafterext.rules.common import b14 as common
from metacrafterext.rules.gb import b14 as gb
from metacrafterext.rules.mn import geo as mn
from metacrafterext.rules.pt import codes as pt
from tests.test_testdata_baseline import field_matches, load

VALIDATORS = [
    (mn.validate_mn_aimag, ["Дорнод", "Баян-Өлгий", "Дархан Уул", "Улаанбаатар", "Khovd", "Bayan-Ölgii", "Govi-Altai"],
     ["Хан-Уул", "Монгол", "Dornod aimag", "5-р баг", ""]),
    (mn.validate_mn_aimag_code, ["011", "021", "084", "048", "067"], ["012", "11", "047", "0111", ""]),
    (mn.validate_mn_soum_code, ["01122", "02101", "06401", "08301"], ["01201", "0112", "011220", ""]),
    (mn.validate_mn_bag_code, ["0211353", "0640151", "0830175"], ["02113", "0121353", "02113531", ""]),
    (mn.validate_mn_soum, ["Хэрлэн", "Баянзүрх", "Хан-Уул", "Баян Овоо"], ["5-р баг", "Kherlen", "3", ""]),
    (mn.validate_mn_bag, ["5-р баг", "3-р хороо", "20-хороо", "04-р баг", "1-р баг Өндөрхошуу", "1-р баг, Цагаан дэрст"],
     ["Номгон-1", "Хан-Уул", "баг", "5", "20-р хороо, Баруун уулын үерийн далангийн баруун талын амралт зугаалгын талбай", ""]),
    (pt.validate_pt_freguesia, ["Valongo do Vouga", "UF Águeda e Borralha", "Santa Marinha e São Pedro da Afurada", "Belém",
                                "Santa Maria Maior (Lisboa)", "ARROIOS"],
     ["0", "-- Não conhecido --", "Não conhecido", "3750-100", "12 Rua", ""]),
    (gb.validate_gb_hrg_code, ["AA22G", "AA26H", "WA14Z"], ["AA2G", "aa22g", "AA222", ""]),
    (gb.validate_gb_ni_ward_1992_code, ["95AA01", "95ZZ16"], ["95AB01", "96AA01", "95AA1", ""]),
    (gb.validate_gb_ni_soa_code, ["95AA01S1", "95AA02W1"], ["95AA01", "95AA01X1", "95AB01S1", ""]),
    (gb.validate_gb_ni_lgd_1992_code, ["95AA", "95ZZ"], ["95AB", "95A", "N09000001", ""]),
    (gb.validate_gb_road_number, ["A2", "M1", "B101", "A1(M)", "a26"], ["C/UC", "D121", "A12345", "Medieval Mystery Trail", ""]),
    (gb.validate_gb_addressbase_classification, ["RD02", "RI01", "PP", "CR08", "R"], ["12", "RD2", "AD02", "Residential", ""]),
    (common.validate_facc_code, ["AL020", "AQ125", "BH502", "GB055"], ["AL20", "PPL", "HA020", "al020", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value
    assert not func(None)


def test_the_province_codes():
    assert len(mn.AIMAG_CODES) == 22


FIELDS = [
    ("mn/mn_geo.yaml", "mnaimagbyname", ["AU1_NAME", "au1_name", "aimag", "Aimag_name", "аймаг", "аймгийн нэр"], ["au1", "aimag_code", "name"]),
    ("mn/mn_geo.yaml", "mnaimagcodebyname", ["AU1", "au1", "aimag_code", "аймгийн код"], ["au1_name", "aimag", "au2"]),
    ("mn/mn_geo.yaml", "mnsoumbyname", ["AU2_NAME", "soum", "soum_name", "сум", "дүүрэг"], ["sum", "au2", "summa"]),
    ("mn/mn_geo.yaml", "mnsoumcodebyname", ["AU2", "soum_code", "сумын код"], ["au2_name", "soum", "sum_code"]),
    ("mn/mn_geo.yaml", "mnbagbyname", ["AU3_NAME", "bag", "khoroo", "хороо", "баг"], ["au3", "bags", "bag_code"]),
    ("mn/mn_geo.yaml", "mnbagcodebyname", ["AU3", "bag_code", "багийн код"], ["au3_name", "bag", "au2"]),
    ("pt/pt_parish.yaml", "ptfreguesiabyname", ["freguesia", "FREGUESIA", "Freguesias", "nome_freguesia", "freg", "freguesia_2"],
     ["fregues", "concelho", "freguesia_codigo"]),
    ("gb/gb_b14.yaml", "gbhrgcodebyname", ["HRG", "hrg_code", "HRG4", "Healthcare Resource Group Code"], ["HRG Label", "hr", "hrg_desc"]),
    ("gb/gb_b14.yaml", "gbroadnumberbyname", ["Route", "road_number", "ROAD_NO", "road", "rd_no", "road_ref"], ["router", "roadside", "route_name"]),
    ("gb/gb_b14.yaml", "gbaddressbaseclassbyname", ["BLPU_CLASS", "blpu_classification", "CLASSIFICATION_CODE", "abp_class"],
     ["class", "class_code", "blpu_state"]),
    ("common/feature_codes.yaml", "facccodebyname", ["F_CODE", "f_code", "FCODE", "facc", "FACC_CODE"], ["code", "fid", "f_codedesc"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    spec = load(path, rule_id)
    assert spec["key"]
    assert spec["validator"].startswith("metacrafterext.rules.") and spec["needs_values"] is True
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("gb/gb_b14.yaml", "gbniward1992value", ["95AA01", "95ZZ16"], ["95AB01", "95aa01"]),
    ("gb/gb_b14.yaml", "gbnisoavalue", ["95AA01S1", "95AA02W1"], ["95AA01X1", "95AB01S1"]),
    ("gb/gb_b14.yaml", "gbnilgd1992value", ["95AA", "95ZZ"], ["95AB", "95aa"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    spec = load(path, rule_id)
    pattern = re.compile(spec["rule"])
    for value in good:
        assert pattern.fullmatch(value), value
        assert spec["minlen"] <= len(value) <= spec["maxlen"]
    for value in bad:
        assert not pattern.fullmatch(value), value
