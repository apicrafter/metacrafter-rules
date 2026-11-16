"""Rules for the French and Finnish files of metacrafter-testdata (May 2024 snapshots of French open data
portals, Dateno sources cdi00000664 to cdi00000698: data.gouv.fr, the portals of the ministries of education
and of higher education and research, Île-de-France, Occitanie, Toulouse Métropole, SNCF; and of Finnish ones,
cdi00000621 to cdi00000633: the GeoServer of Statistics Finland, Avoindata.fi, Tampere): the codes of French
local budgets and State budget programmes, kinds of education units, RNSR numbers, CNU sections, BAAC accident
numbers, line codes and kilometre points of the national rail network, line identifiers of Île-de-France
Mobilités, road numbers, IDURBA identifiers, house number suffixes, Finnish municipality, region, sub-region
and electoral district codes, postal codes and grid cell codes; and the fixes they needed: the prefixed codes
of the higher education data (A01, R11, D075), IdRef identifiers by field name, dep that is no package, a CCAM
code of four letters and three digits.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.fi.codes import (
    validate_fi_kuntanumero,
    validate_fi_maakunta_code,
    validate_fi_postcode,
    validate_fi_seutukunta_code,
    validate_fi_vaalipiiri_code,
    validate_inspire_grid_cell_code,
)
from metacrafterext.rules.fr.codes import validate_fr_academie_code, validate_fr_department_code, validate_fr_region_code
from metacrafterext.rules.fr.portals import (
    validate_fr_baac_accident_number,
    validate_fr_budget_chapitre_code,
    validate_fr_budget_fonction_code,
    validate_fr_budget_nature_code,
    validate_fr_budget_nomenclature,
    validate_fr_cnu_section_code,
    validate_fr_idfm_line_id,
    validate_fr_idref_id,
    validate_fr_idurba,
    validate_fr_indice_repetition,
    validate_fr_lolf_programme_code,
    validate_fr_nature_uai_code,
    validate_fr_rail_pk,
    validate_fr_rfn_line_code,
    validate_fr_rnsr,
    validate_fr_road_number,
)
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (validate_fr_budget_nomenclature, ["M14", "M14V", "M57", "M49", "M43", "M52", "M22", "M4x", "M4", "M14B", "m57", "M71"],
     ["CNU", "SISE", "NAFRev2", "M1", "M140", "14", ""]),
    (validate_fr_budget_chapitre_code, ["011", "012", "65", "21", "040", "930", "C204", "011 - CHARGES A CARACTERE GENERAL",
                                        "21-IMMOBILISATIONS CORPORELLES", 65, 11.0],
     ["64111", "6574", "I", "II", "Engagement Sociétal", "1", "2020-01", ""]),
    (validate_fr_budget_nature_code, ["6574", "64111", "611", "60632", "2188", "657341", "60632 - FOURNITURES DE PETIT EQUIPEMENT", 6336],
     ["011", "65", "aide en numéraire", "à l'", "au", "COLLEGE", "8", "0611", ""]),
    (validate_fr_budget_fonction_code, ["020", "01", "822", "1", "5234", "020 - ADMINISTRATION GENERALE", 33],
     ["-", "Directeur", "82-2", "822000", "Maire adjoint", ""]),
    (validate_fr_lolf_programme_code, ["150", "172", "P172", "p150", "743", 217],
     ["Coopération", "ERC", "MSCA", "1720", "15", "015", "SP1", ""]),
    (validate_fr_nature_uai_code, ["101", "151", "340", "306", "600", 320], ["6574", "ELEMENTAIRE", "lycée polyvalent", "34", "051", ""]),
    (validate_fr_rnsr, ["200012199P", "201420835R", "199712638E", " 200510689B "],
     ["0750671X", "200012199", "200012199p", "180012199P", "2000121999", "210012199P", ""]),
    (validate_fr_cnu_section_code, ["27", "01", "60", "99", "00"], ["270", "Informatique", "7", "A1", ""]),
    (validate_fr_baac_accident_number, ["201800000138", "200500000001", "202100000044", 201900000003],
     ["20180000013", "200400000001", "199900000001", "2018000001380", "201800000138A", ""]),
    (validate_fr_rfn_line_code, ["830000", "420000", "005000", "752000", "1000", "5000", 990000], ["12", "A", "C01742", "1234", "87543207", ""]),
    (validate_fr_rail_pk, ["055+368", "000+000", "528+422", "-001+250"], ["55.368", "55+368", "055+36", "055 368", "+33612", ""]),
    (validate_fr_idfm_line_id, ["C01742", "IDFM:C01742", "C00179", "C01373,C01375,C01379"],
     ["A01840", "C1742", "c01742", "IDFM:22388", "C017420", "STIF:Line::C01742:", ""]),
    (validate_fr_road_number, ["D121", "A6", "N20", "D1083", "RD 1083", "D 910", "d18", "D906A", "M6"],
     ["907", "0", "E15", "13, 97", "Route de Paris", "D", "B190", ""]),
    (validate_fr_idurba, ["64024_PLU_20201024", "200067106_PLUi_20200222", "2A004_PLU_20190101", "64024_PLU_20201024_A", "75056_PSMV_20131218"],
     ["64024_PLU", "64024_PLU_2020", "64024-PLU-20201024", "64024_SCOT_20201024", "64024_PLU_20201324", ""]),
    (validate_fr_indice_repetition, ["bis", "BIS", "ter", "TER", "QUATER", "quinquies", "B", "a", "T", "QUA*"],
     ["0", "1", "12", "bis ter", "AB", "N°", ""]),
    (validate_fr_idref_id, ["068861281", "059861169", "02640470X", "26404702", 68861281], ["0688612810", "68861", "idref068861281", "A68861281", ""]),
    # the prefixed codes of the open data of higher education
    (validate_fr_academie_code, ["A01", "A25", "01", "9", "43"], ["A1", "B01", "A100", ""]),
    (validate_fr_region_code, ["R11", "R84", "11", "84"], ["R12", "R1", "D11", "R110"]),
    (validate_fr_department_code, ["D075", "D013", "D02A", "D974", "75", "2A", "028"], ["D75", "D0750", "R075", "D000", "D099"]),
    (validate_fi_kuntanumero, ["091", "837", "005", "91", "5", 410, 91.0], ["Kuhmo", "0910", "091 Helsinki", "FI091", ""]),
    (validate_fi_maakunta_code, ["01", "02", "06", "19", "21", "1", 17], ["03", "22", "00", "Uusimaa", "001", ""]),
    (validate_fi_seutukunta_code, ["011", "023", "211"], ["11", "0110", "Helsinki", ""]),
    (validate_fi_vaalipiiri_code, ["01", "07", "13", "12 Oulun vaalipiiri", "08 Kaakkois-Suomen vaalipiiri", "1"],
     ["16", "00", "Oulun vaalipiiri", "012", ""]),
    (validate_fi_postcode, ["00100", "33580", "920", "100", 33710], ["001000", "FI-00100", "00100 Helsinki", "12", ""]),
    (validate_inspire_grid_cell_code, ["1kmN2599E4695", "1kmN6638E0272", "5kmN1338E0017", "250mN66380E02720", "100mN26174E47435",
                                       "CRS3035RES1000mN2599000E4695000"],
     ["N6638E0272", "1kmN6638", "1km N6638 E0272", "kmN6638E0272", "1kmS6638E0272", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ + str(i) for i, v in enumerate(VALIDATORS)])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("fr/fr_budget.yaml", "frbudgetnomenclaturebyname", ["nomenclature", "nomenclature_comptable", "type_nomenclature", "Type nomenclature",
                                                        "instruction_budgetaire"],
     ["nomenclatureactiviteprincipaleetablissement", "nomenclature_actes", "code_chapitre"]),
    ("fr/fr_budget.yaml", "frbudgetchapitrecodebyname", ["chapitre", "code_chapitre", "chapitre_par_nature", "chapitre_code", "Chapitre",
                                                        "BGT_NATURE", "BGT_CONTNAT", "numero_chapitre"],
     ["libelle_chapitre", "BGT_CONTNAT_LABEL", "code_article", "chapitre_libelle"]),
    ("fr/fr_budget.yaml", "frbudgetnaturecodebyname", ["article", "code_article", "ARTICLE", "BGT_CONTNAT", "BGT_NATURE", "compte_nature",
                                                      "nature_comptable", "nature"],
     ["libelle_article", "BGT_NATURE_LABEL", "nature_uai", "code_nature", "nature_ap_epcp", "code_chapitre"]),
    ("fr/fr_budget.yaml", "frbudgetfonctioncodebyname", ["fonction", "code_fonction", "code_fonctionnel", "BGT_FONCTION", "Fonction",
                                                        "sous_fonction"],
     ["libelle_fonction", "BGT_FONCTION_LABEL", "fonction_role_auteur", "code_article"]),
    ("fr/fr_budget.yaml", "frlolfprogrammecodebyname", ["programme", "code_programme", "code_du_programme", "code_de_programme",
                                                       "identifiant_programme_lolf_chef_de_file", "numero_programme"],
     ["libelle_programme", "programme_name_en", "programme_lib", "entite_financiere_programme", "nombre_de_trains_programmes"]),
    ("fr/fr_education.yaml", "frnatureuaicodebyname", ["nature_uai", "code_nature", "code_nature_etab", "code_nature_uai", "Nature UAI"],
     ["nature_uai_libe", "libelle_nature", "nature", "code_nature_culture", "nature_u_1"]),
    ("fr/fr_education.yaml", "frrnsrbyfieldname", ["numero_national_de_structure", "rnsr", "unitesrecherche_rnsr", "numero_de_structure_parent",
                                                  "structure_de_recherche", "code_rnsr"],
     ["type_de_structure", "sigle_structure", "nom_structure", "code_de_type_de_structure"]),
    ("fr/fr_education.yaml", "frcnusectioncodebyname", ["code_section_cnu", "section_cnu", "Section CNU", "code_cnu"],
     ["groupe_cnu", "code_groupe_cnu", "secteur_cnu", "code_secteur_cnu"]),
    ("fr/fr_education.yaml", "fridrefidbyname", ["idref", "identifiant_idref", "id_idref", "IdRef"], ["lien_idref", "lien_notice_idref", "idrefliga"]),
    ("fr/fr_education.yaml", "fracademiecodebyname", ["code_academie", "code_acad", "etablissement_code_academie"], ["academie", "acad", "libelle_academie"]),
    ("fr/fr_transport.yaml", "frbaacaccidentnumberbyname", ["Num_Acc", "num_acc", "numero_accident", "id_accident"],
     ["num_veh", "accidents", "nb_accidents", "accident"]),
    ("fr/fr_transport.yaml", "frrfnlinecodebyname", ["code_ligne", "CODE_LIGNE", "code ligne", "code_de_la_ligne"],
     ["lib_ligne", "ligne", "nom_ligne", "idligne", "code_voie"]),
    ("fr/fr_transport.yaml", "fridfmlineidbyfieldname", ["id_line", "idrefligc", "route_id", "id_ligne", "ID_Line"],
     ["name_line", "idrefliga", "id_groupoflines", "shortname_line", "id_ref_zdc"]),
    ("fr/fr_transport.yaml", "frroadnumberbyname", ["RD", "rd", "route", "num_route", "numero_route", "ROUTE", "rn"],
     ["niveau_route", "infrastructure_type", "address_route", "pr_deb", "routes"]),
    ("fr/fr_geo.yaml", "frindicerepetitionbyname", ["rep", "rep_loc", "indice_de_repetition", "indice_rep", "suffixe"],
     ["num_loc", "comp_loc", "reponse", "repertoire", "rep_academique"]),
    ("fi/fi_geo.yaml", "fikuntanumerobyname", ["kunta", "kuntanumero", "Kuntanumero", "kunta_nro", "kuntanro", "Kuntakoodi", "kunnro2022",
                                               "KUNTA"],
     ["kunta_nimi", "maakunta", "seutukunta", "Kunnan nimi", "kuntayhtymä"]),
    ("fi/fi_geo.yaml", "fimaakuntacodebyname", ["maakunta", "Maakunta", "Maakuntanro", "maakuntakoodi"], ["maakunta_nimi", "kunta", "seutukunta"]),
    ("fi/fi_geo.yaml", "fiseutukuntacodebyname", ["seutukunta", "seutukuntakoodi"], ["seutukarttakoodi", "kunta", "maakunta"]),
    ("fi/fi_geo.yaml", "fivaalipiiricodebyname", ["vaalipiiri", "Vaalipiiri", "vaalipiirinro"], ["vaalit", "kunta", "vaalipiirin_nimi"]),
    ("fi/fi_geo.yaml", "fipostcodebyname", ["postinumero", "POSTINUMERO", "posti_alue", "postinumeroalue", "Toimittajan postinumero"],
     ["postitoimipaikka", "posti", "nimi", "postiosoite"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_names(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("fr/fr_education.yaml", "frrnsrvalue", ["200012199P", "199712638E"], ["0750671X", "200012199"]),
    ("fr/fr_transport.yaml", "frrailpkvalue", ["055+368", "000+000"], ["55.368", "0553680"]),
    ("fr/fr_transport.yaml", "fridfmlineidvalue", ["IDFM:C01742"], ["C01742", "IDFM:22388"]),
    ("fr/fr_geo.yaml", "fridurbavalue", ["64024_PLU_20201024", "200067106_PLUi_20200222"], ["64024_PLU", "64024_SCOT_20201024"]),
    ("common/geo.yaml", "inspiregridcellcodevalue", ["1kmN2599E4695", "250mN66380E02720"], ["N6638E0272", "1kmN6638"]),
    # a CCAM code is four letters and three digits, not the M14V of a budget instruction
    ("fr/fr_med.yaml", "frccamvalue", ["HBQK002", "ZBQK002"], ["M14V", "M57"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def test_dep_is_no_package():
    """dep is the department of French tables (75, 92), not a software dependency."""
    assert "dep" not in load("common/software.yaml", "packagebyknown")["rule"].split(",")
