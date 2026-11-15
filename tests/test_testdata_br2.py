"""Rules for the Brazilian files of the second round of metacrafter-testdata (2024 snapshots of the Dateno
catalogue: dados.mg.gov.br, cdi00000221, dados.recife.pe.gov.br, cdi00000227, dados.rs.gov.br, cdi00000228,
and the Dataverse repositories Arca Dados of Fiocruz, cdi00000251, SciELO Data, cdi00000252, CIDACS,
cdi00000254, and FGV, cdi00000255): six-digit IBGE municipality codes, IBGE state codes, census tract
codes, INEP school codes, CNES numbers, ICD-10 codes as DATASUS writes them, ICD-10 chapters in Portuguese,
the race or colour categories of IBGE and Sim/Não.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.br.codes import (
    validate_br_census_tract_code,
    validate_br_cnes,
    validate_br_inep_school_code,
    validate_br_municipality_code,
    validate_br_municipality_code_6,
    validate_br_race_colour,
    validate_br_state_ibge_code,
    validate_icd10_datasus,
)
from metacrafterext.rules.common.classifications import validate_icd10_chapter, validate_icd10_chapter_or_other
from tests.test_testdata_baseline import field_matches, value_matches

VALIDATORS = [
    (validate_br_municipality_code_6, ["355030", "310620", "530010", "354990.0", "110001.0", "120001"],
     ["3550308", "999999", "995030", "35503", "Barbacena", "1.2E3", ""]),
    (validate_br_municipality_code, ["3550308.0", "1100015"], ["355030", "355030.0"]),
    (validate_br_state_ibge_code, ["11", "35", "53", "35.0", "29"], ["34", "99", "SP", "1", "350", ""]),
    (validate_br_census_tract_code, ["355030801000001", "3.55030801000001E14", "3.54100005000009E14", "3.55670105000001E14"],
     ["355030901000001", "35503080100000", "1.300110000000019E21", "3.55E14", "Codsetor", ""]),
    (validate_br_inep_school_code, ["26175347", "26121972", "26175347.0"], ["2617534", "99175347", "261753470", "384", ""]),
    (validate_br_cnes, ["2446480", "0000957", "957.0", "2446480.0", "6058116"], ["1", "2", "0000000", "24464800", "ESF", ""]),
    (validate_br_race_colour, ["Parda", "Branca", "Preta", "Amarela", "Indígena", "INDIGENA", "Ignorado", "Não informado", "PARDO"],
     ["1", "5", "Azul", "Nelore", "Masculino", ""]),
    (validate_icd10_datasus, ["C159", "W788", "C20", "I10X", "C15.9", "X954", "I209"],
     ["C1599", "159", "CC15", "ESOFAGO NE", "II. NEOPLASIAS (TUMORES)", "8.0", ""]),
    (validate_icd10_chapter, ["II. NEOPLASIAS (TUMORES)", "IV. DOENÇAS ENDÓCRINAS NUTRICIONAIS E METABÓLICAS",
                              "IX. Doenças do aparelho circulatório", "XX. Causas externas de morbidade e de mortalidade",
                              "XV. Gravidez, parto e puerpério", "Neoplasms"],
     ["Parto normal", "Doenças", "C159", "NEOPL MALIG DO ESOFAGO", "DOENÇAS INFECCIOSAS E PARASITÁRIAS", ""]),
    (validate_icd10_chapter_or_other, ["DOENÇAS INFECCIOSAS E PARASITÁRIAS", "Doenças do aparelho digestivo", "II. NEOPLASIAS (TUMORES)",
                                       "Capítulo IX - Doenças do aparelho circulatório"],
     ["CARDIOLOGIA", "NÃO SE APLICA", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ + str(i) for i, v in enumerate(VALIDATORS)])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("br/br_geo.yaml", "brmunicipalitycode6byname",
     ["municipio_cod", "cod_municipio", "codmun6", "Cod6d", "codmunres", "codmunocor", "CODMUNI", "CODIGOMUNICIPIODOOBITO", "IBGE",
      "Cód.IBGE"],
     ["comunidade", "COMUNAS", "cidade", "municipio", "nMunicRm", "codigo"]),
    ("br/br_geo.yaml", "brmunicipalitycodebyname", ["CODMUNI_A", "CODCIDADE", "codmunres", "municipio_cod", "Cód.IBGE", "cod_municipio"],
     ["comuna", "municipio", "nome_municipio"]),
    ("br/br_geo.yaml", "brstateibgecodebyname", ["uf", "UF_Cod", "coduf", "CDUF", "CODUF", "UF(cod)", "cod_uf", "codigo_estado"],
     ["uf_nascimento", "nome_da_uf", "estado", "ufs"]),
    ("br/br_geo.yaml", "brcensustractcodebyname", ["Codsetor", "cd_setor", "CD_GEOCODI", "setor_censitario", "cod_setor_censitario"],
     ["Situacaosetor", "Setorondetrabalha", "setor"]),
    ("br/br_education.yaml", "brinepschoolcodebyname", ["inep_escola", "co_entidade", "CO_ENTIDADE", "codigo_inep", "cod_inep", "inep"],
     ["CD_ENTIDADE_CAPES", "CD_ENTIDADE_EMEC", "codigo_escola"]),
    ("br/br_health.yaml", "brcnesbyname", ["CNES", "CNESFINAL", "CNESADESÃO", "NOVOCNES", "NovoCNES", "co_cnes"],
     ["CNEScontrat", "CNESCONTRATUALIZAÇÃO", "cnes_count"]),
    ("br/br_health.yaml", "bricd10byname", ["co_cid_causa_basica", "causabas", "causabaso", "CAUSABASICADO", "RASTREIOCID", "cid10", "CID"],
     ["cidade", "CIDADE", "nome_cidade", "causab", "causabas2"]),
    ("br/br_persons.yaml", "brracecolourbyname", ["tp_raca_cor", "CS_RACA", "CORRAÇA", "raça/cor", "racacor", "RAÇA_CO", "raca", "cor_raca"],
     ["cor", "Cor", "caracteristica", "racao"]),
    ("common/classifications.yaml", "icd10chapterbyname", ["capitulo_cid_causa_basica", "capitulo_cid10", "cid10_capitulo"],
     ["capitulo", "cid"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


def test_guarded_value_rules():
    """Codes whose digits fit other patterns (cz_ico, imsi) are read by value only in fields named for them."""
    from tests.test_testdata_baseline import load
    assert load("br/br_education.yaml", "brinepschoolcodevalue")["fieldregex"]
    assert load("br/br_geo.yaml", "brcensustractcodevalue")["fieldregex"]
    assert value_matches("br/br_education.yaml", "brinepschoolcodevalue", "26175347")
    assert value_matches("br/br_geo.yaml", "brcensustractcodevalue", "3.54100005000009E14")
    assert field_matches("br/br_geo.yaml", "brregionbyname", "NMREGIAO")


def test_boolean_sim_nao():
    for value in ("Sim", "SIM", "Não", "NAO", "nao"):
        assert value_matches("common/boolean.yaml", "booleansimnao", value), value
    for value in ("Talvez", "Ignorado", "S"):
        assert not value_matches("common/boolean.yaml", "booleansimnao", value), value
