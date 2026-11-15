"""Rules for the Brazilian files of metacrafter-testdata (2024 snapshots of five CKAN portals of the Dateno
catalogue: the Banco Central do Brasil, the BNDES, CAPES, the Jardim Botânico do Rio de Janeiro and Governo
Aberto SP): CNPJ numbers and roots, ISPB and COMPE codes, CNAE and NCM codes, the size class of companies,
federative units, regions, IBGE municipality codes, CEP and phone numbers, NUP protocol numbers, TCU
processes and rulings, CAPES programme and institution codes, e-MEC codes, CAPES evaluation areas and
grades, biomes, IUCN Red List categories and criteria, country and language names in Portuguese and
taxonomy in Portuguese.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.br.codes import (
    validate_br_biome,
    validate_br_capes_evaluation_area,
    validate_br_capes_grade,
    validate_br_capes_institution_code,
    validate_br_capes_program_code,
    validate_br_cnae,
    validate_br_cnpj_root,
    validate_br_company_size,
    validate_br_compe_code,
    validate_br_emec_institution_code,
    validate_br_ispb,
    validate_br_municipality_code,
    validate_br_nup,
    validate_br_nup_number,
    validate_br_phone_formatted,
    validate_br_phone_national,
    validate_br_postcode,
    validate_br_postcode_formatted,
    validate_br_region,
    validate_br_state,
    validate_br_state_code,
    validate_br_tcu_process_number,
    validate_br_tcu_process_number_tc,
    validate_br_tcu_ruling,
    validate_cnpj,
    validate_cnpj_formatted,
    validate_mercosur_ncm,
)
from metacrafterext.rules.common.taxa import validate_iucn_red_list_category, validate_iucn_red_list_criteria
from metacrafterext.rules.pt.countries import validate_pt_country_name
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (validate_cnpj, ["12.917.918/0001-89", "60.701.190.0001-04", "00000000000191", "60746948000112", "5463212000129",
                     "31.599.545/0001-90", "12.ABC.345/01DE-35"],
     ["00.000.000.0000-00", "12.917.918/0001-88", "11111111111111", "Não se aplica", "**.*70.727/0001-**", "----------",
      "23862762", ""]),
    (validate_cnpj_formatted, ["12.917.918/0001-89", "60.701.190.0001-04"], ["12917918000189", "12.917.918/0001-88"]),
    (validate_br_cnpj_root, ["23862762", "02658435", "00000000", "60.701.190"], ["2386276", "60701190000104", "ABCDEFGH", ""]),
    (validate_br_ispb, ["00000000", "00360305", "360305"], ["001", "123456789", "n/a", ""]),
    (validate_br_compe_code, ["001", "070", "237", "1"], ["0", "000", "1234", "n/a", ""]),
    (validate_br_cnae, ["C1011200", "O8411600", "D3511584", "A0119900", "4711-3/02", "47.11-3", "47113", "4711302", "F42", "47.1"],
     ["47", "Z1011200", "C3511584", "4711", "12345678", "F41 e F43", "INDUSTRIA DE TRANSFORMAÇÃO", ""]),
    (validate_mercosur_ncm, ["84328000", "8432.80.00", "73090090", "04090000"], ["77000000", "98000000", "8432800", "00000000", ""]),
    (validate_br_company_size, ["GRANDE", "MÉDIA", "PEQUENA", "MICRO", "EPP", "ME", "Microempresa", "Demais"],
     ["Pequeno 1", "Pequeno 2", "Metrópole", "Médio", "Grande porte", ""]),
    (validate_br_state_code, ["SP", "RJ", "DF", " SP", "ba"], ["BR", "XX", "SPA", ""]),
    (validate_br_state, ["São Paulo", "MINAS GERAIS", "Ceara", "Espirito Santo", "AMAZONAS", "Distrito Federal"],
     ["Sao", "Lisboa", "Campinas", "SP", ""]),
    (validate_br_region, ["SUDESTE", "Centro-Oeste", "Região Sul", "Nordeste", "Norte"],
     ["Leste", "Oeste", "Região Administrativa de Campinas", "Bragança Paulista", ""]),
    (validate_br_municipality_code, ["3550308", "5300108", "3304557", "4314902", "2201919", "3550308.0"],
     ["9999999", "0", "3550309", "9950308", "355030", ""]),
    (validate_br_postcode, ["01310-100", "89041002", "01.310-100", "13469-070"], ["00000-000", "1310-100", "8904100", ""]),
    (validate_br_postcode_formatted, ["01310-100", "13469-070"], ["89041002", "00000-000", "12345-6789"]),
    (validate_br_phone_national, ["(19) 3472-9700", "(11) 98765-4321", "19 3472 9700", "+55 61 3414-1414", "(11) 4652-7000"],
     ["(10) 3472-9700", "(19) 1472-9700", "3472-9700", "(11) 88765-4321", "02253534622", "0913353055", "02252.299.777", ""]),
    (validate_br_phone_formatted, ["(19) 3472-9700", "(11) 98765-4321", "(61) 3414 1414"], ["19 3472 9700", "1934729700", "(19)34729700"]),
    (validate_br_nup, ["99903000615201603", "99903.000615/2016-03"], ["99903000615201604", "12345678901234567", "99903.000615/16-03", ""]),
    (validate_br_nup_number, ["99903000615201603", "029358/2019-39"], ["029358/19-39", "TC 005.291/2021-6", ""]),
    (validate_br_tcu_process_number, ["TC 005.291/2021-6", "TC-036.817/2018-0", "005.291/2021-6"], ["TC 005.291/2021", "5.291/2021-6", ""]),
    (validate_br_tcu_process_number_tc, ["TC 005.291/2021-6", "TC-036.817/2018-0"], ["005.291/2021-6", "TC 005.291/2021"]),
    (validate_br_tcu_ruling, ["2726/2023-Plenário", "13262/2023-1ª Câmara", "10384/2023-2ª Câmara", "Acórdão 1234/2020 - TCU - Plenário"],
     ["2726/2023", "Plenário", "TC 005.291/2021-6", ""]),
    (validate_br_capes_program_code, ["33003017040P8", "10001018016P2"], ["33003017040P", "3300301704P8", "63003017040P8", ""]),
    (validate_br_capes_institution_code, ["33003017", "10001018", "40001016", "33003017.0"], ["699", "63003017", "3300301", ""]),
    (validate_br_emec_institution_code, ["699", "1", "23412"], ["0", "NI", "1234567", ""]),
    (validate_br_capes_evaluation_area, ["ENGENHARIAS III", "CIÊNCIAS BIOLÓGICAS I", "ASTRONOMIA / FÍSICA", "ASTRONOMIA/FÍSICA",
                                         "Interdisciplinar", "LETRAS / LINGUÍSTICA"],
     ["CIÊNCIAS HUMANAS", "ENGENHARIAS V", "MULTIDISCIPLINAR", ""]),
    (validate_br_capes_grade, ["1", "5", "7", "A", "4.0"], ["0", "8", "B", ""]),
    (validate_br_biome, ["Mata Atlântica", "Amazônia, Mata Atlântica, Cerrado", "CERRADO", "Caatinga; Pantanal"],
     ["Floresta", "Mata", "Floresta Ombrófila", ""]),
    (validate_iucn_red_list_category, ["CR", "en", "VU", "LR/nt", "CR(PEX)", "DD"], ["XX", "Vulnerable", "C", ""]),
    (validate_iucn_red_list_criteria, ["B1ab(iii)", "B2(iii,v)", "B1ab(i,iii)+2ab(ii,iii)", "D2", "A4cd; B2ab(ii,iii)", "C2a(i)"],
     ["E", "ABC", "B3", "12", "Brasil", "DD", ""]),
    (validate_pt_country_name, ["Brasil", "ESTADOS UNIDOS", "EQUADOR", "REPUBLICA DOMINICANA", "França", "FRANCA", "Japão", "Holanda"],
     ["Perú", "Japón", "España", "Lisboa", "NÃO INFORMADO", "Germany", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("br/br_codes.yaml", "brcnpjbyname", ["cnpj", "cnpj_do_exportador", "cnpj_fabricante", "cnpj_do_agente_financeiro",
                                          "cnpj_da_instituicao_financeira_credenciada", "CNPJ IF", "cpf_cnpj"],
     ["cnpjs", "nr_cnpjota", "razao_social"]),
    ("br/br_codes.yaml", "brispbbyname", ["ISPB", "ispb", "cod_ispb", "ispb_participante"], ["ispbx", "isp"]),
    ("br/br_codes.yaml", "brcompecodebyname", ["Número_Código", "codigo_banco", "cod_banco", "compe", "codigo_compe", "numero_banco"],
     ["banco", "nome_banco", "codigo"]),
    ("br/br_codes.yaml", "brcnaebyname", ["cnae", "subsetor_cnae_codigo", "cnae_fiscal", "cd_cnae", "codigo_cnae_ibge"], ["cnaes", "canae"]),
    ("br/br_codes.yaml", "mercosurncmbyname", ["ncm", "co_ncm", "cd_ncm", "codigo_ncm", "ncm_desc"], ["ncms", "ancm"]),
    ("br/br_codes.yaml", "brcompanysizebyname", ["porte", "porte_do_cliente", "porte_do_exportador", "Porte", "porte_empresa"],
     ["aporte", "transporte", "suporte"]),
    ("br/br_geo.yaml", "brstatecodebyname", ["uf", "UF", "sg_uf", "SG_UF_PROGRAMA", "uf_sede_agente", "UNIDADE_FEDERACAO", "estado",
                                             "SG_UF_IES_ESTUDO"],
     ["ufc", "uffa", "estados_civis"]),
    ("br/br_geo.yaml", "brstatebyname", ["estado", "stateProvince", "nm_uf", "nome_estado", "unidade_federativa"], ["estadio", "state"]),
    ("br/br_geo.yaml", "brregionbyname", ["regiao", "NM_REGIAO", "NM_REGIAO_IES_ESTUDO", "região", "Região Administrativa"], ["regional"]),
    ("br/br_geo.yaml", "brmunicipalitycodebyname", ["municipio_codigo", "cod_municipio", "codigo_ibge", "cd_mun", "co_municipio",
                                                    "id_municipio", "cod_ibge", "geocodigo"],
     ["municipio", "nome_municipio"]),
    ("br/br_geo.yaml", "brcepbyname", ["cep", "cep_sede_agente", "CEP do Arquivo Público", "nr_cep"], ["recepcao", "cepas"]),
    ("br/br_geo.yaml", "brphonebyname", ["telefone", "Telefone do Arquivo Público", "fone", "tel", "celular"], ["telefonia_movel_pct", "hotel"]),
    ("br/br_government.yaml", "brnupbyname", ["ped_nu_ptcol", "nup", "Número de Protocolo (NUP)", "protocolo", "numero_protocolo"],
     ["protocolar", "nupcial"]),
    ("br/br_government.yaml", "brtcuprocessbyname", ["processo", "processo_n_o", "numero_processo", "Processo"], ["processamento"]),
    ("br/br_education.yaml", "brcapesinstitutioncodebyname", ["CD_ENTIDADE_CAPES", "CD_IES_ESTUDO", "cd_ies", "codigo_ies_capes"],
     ["CD_ENTIDADE_EMEC", "SG_IES_ESTUDO"]),
    ("br/br_education.yaml", "bremecinstitutioncodebyname", ["CD_ENTIDADE_EMEC", "CO_IES", "codigo_emec", "cod_ies_e_mec"],
     ["CD_ENTIDADE_CAPES", "NO_IES"]),
    ("br/br_education.yaml", "brcapesevaluationareabyname", ["NM_AREA_AVALIACAO", "NM_AREA_AVALIACAO_ATUAL", "NM_AREA_AVALIACAO_ANO",
                                                             "área de avaliação"],
     ["CD_AREA_AVALIACAO", "NM_AREA_CONHECIMENTO"]),
    ("br/br_education.yaml", "brcapesgradebyname", ["CD_CONCEITO_PROGRAMA", "CONCEITO_ANO", "conceito", "nota_capes"], ["conceitos_basicos"]),
    ("br/br_ecology.yaml", "brbiomebyname", ["bioma", "biomas", "Dom. Fitogeográfico", "Dom\\. Fitogeográfico", "dominio_fitogeografico"],
     ["biomassa", "dominio"]),
    ("common/redlist.yaml", "iucnredlistcategorybyname", ["categoria", "Categoria de ameaça", "categoria_ameaca", "iucn_category",
                                                          "red_list_category", "threat_status", "Categoria de ameaça da espécie"],
     ["subcategoria", "categoria_id"]),
    ("common/redlist.yaml", "iucnredlistcriteriabyname", ["critério", "Critério", "criterio", "criteria", "iucn_criteria"], ["criterion_id"]),
    ("pt/pt_geo.yaml", "ptcountrynamebyname", ["pais", "país", "NM_PAIS", "NM_PAIS_ORIGEM", "pais_destino_das_exportacoes", "pais_de_origem"],
     ["pais_solicitante", "pais_residencia_solicitante", "pais_desc", "pais_edicion_id", "NM_CIDADE_PAIS"]),
    ("pt/pt_taxa.yaml", "pttaxonnamebyfield", ["Família", "familia aceita", "Gênero", "Genêros", "FAMÍLIA", "Ordem"],
     ["Espécie", "familiar", "genero", "Genero"]),
    ("pt/pt_taxa.yaml", "ptspeciesbyfield", ["Nome científico", "nome aceito", "Espécies", "Espécie sem autor", "Táxon",
                                             "Táxon completo (segundo a Flora do Brasil 2020)", "NOME CIENTÍFICO"],
     ["Espécie botânica", "autor"]),
    ("pt/pt_taxa.yaml", "ptauthorshipbyfield", ["Autor", "autor", "autor do táxon"], ["Autoria", "autores", "autor_1"]),
    ("pt/pt_taxa.yaml", "ptvernacularnamebyfield", ["NOME POPULAR", "nome popular", "nomes populares", "nome vulgar", "nome comum"],
     ["Nomes Vernaculares", "nome"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("br/br_codes.yaml", "brcnpjformattedvalue", ["12.917.918/0001-89"], ["12917918000189", "12.917.918/0001-88"]),
    ("br/br_geo.yaml", "brstatevalue", ["AMAZONAS", "São Paulo"], ["Sao", "Lisboa do Sul e Norte dos Campos"]),
    ("br/br_geo.yaml", "brcepvalue", ["13469-070"], ["89041002"]),
    ("br/br_geo.yaml", "brphonevalue", ["(19) 3472-9700"], ["19 3472 9700"]),
    ("br/br_government.yaml", "brnupvalue", ["99903.000615/2016-03"], ["99903000615201603", "99903.000615/2016-04"]),
    ("br/br_government.yaml", "brnupdigitsvalue", ["99903000615201603"], ["99903000615201604"]),
    ("br/br_government.yaml", "brtcuprocessvalue", ["TC 005.291/2021-6"], ["005.291/2021-6"]),
    ("br/br_government.yaml", "brtcurulingvalue", ["2726/2023-Plenário", "13262/2023-1ª Câmara"], ["2726/2023"]),
    ("br/br_education.yaml", "brcapesprogramcodevalue", ["33003017040P8"], ["33003017040"]),
    ("br/br_education.yaml", "brcapesinstitutioncodevalue", ["33003017", "10001018"], ["699"]),
    ("common/redlist.yaml", "iucnredlistcriteriavalue", ["B1ab(iii)", "B1ab(i,iii)+2ab(ii,iii)"], ["D2", "Brasil"]),
    ("pt/pt_taxa.yaml", "pttaxonrankvalue", ["Família", "ESPECIE", "sub_especie", "Variedade"], ["Nome aceito", "family"]),
    ("pt/pt_taxa.yaml", "pttaxonomicstatusvalue", ["Nome aceito", "Sinônimo", "NOME_ACEITO"], ["accepted", "Família"]),
    ("pt/pt_common.yaml", "ptlanguagenamevalue", ["INGLES", "Português", "espanhol"], ["english", "Brasil"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def test_guards():
    """Value rules whose values alone are ambiguous read only fields named for them, and the state names
    only fields that are no cities."""
    assert load("br/br_government.yaml", "brnupdigitsvalue")["fieldregex"]
    assert load("br/br_education.yaml", "brcapesinstitutioncodevalue")["fieldregex"]
    import re
    guard = re.compile(load("br/br_geo.yaml", "brstatevalue")["fieldregex"])
    assert guard.search("column_2") and guard.search("estado")
    for name in ("Cidade", "municipio_sede_agente", "Município", "Endereço do Arquivo Público"):
        assert not guard.search(name), name
