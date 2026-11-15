"""Rules for the SICYTAR files of metacrafter-testdata (a 2024 snapshot of datasets.datos.mincyt.gob.ar,
the open data portal of the Argentine science ministry): ANPCyT and CONICET project codes, ANPCyT funds,
equipment codes of the Sistemas Nacionales, CONICET staff categories, BAHRA settlement codes, OECD FORD
codes, ISIC Rev. 4 codes, journal titles, volumes, quartiles and page numbers, keywords, abstracts,
publishers and the INDEC codes and Spanish country names of the institution addresses.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.ar_country.census import validate_ar_department_name
from metacrafterext.rules.ar_country.science import (
    validate_ar_anpcyt_project_code,
    validate_ar_bahra_code,
    validate_ar_bahra_department_part,
    validate_ar_conicet_category,
    validate_ar_conicet_category_name,
    validate_ar_conicet_project_code,
    validate_ar_cyt_project_code,
    validate_ar_mincyt_equipment_id,
)
from metacrafterext.rules.common.research import (
    validate_abstract_text,
    validate_grant_number,
    validate_isic_rev4,
    validate_journal_quartile,
    validate_journal_title,
    validate_journal_volume,
    validate_keyword_list,
    validate_oecd_ford_code,
    validate_page_number,
    validate_work_title,
)
from tests.test_testdata_baseline import field_matches, value_matches

ABSTRACT = ("El presente proyecto propone la realización de un estudio ecológico del Embalse Paso de las Piedras, "
            "integrado al desarrollo de modelos matemáticos.")

VALIDATORS = [
    (validate_ar_anpcyt_project_code, ["PICT-2015-1234", "PICT-2008-0100", "PICTO-2009-0012", "PID-2011-0002", "PICT- 201-0031",
                                       "ANR 600 NA093/08", "CF BA 001/07", "CRE+CO 0062/12", "EMP FONSOFT NA038/07", "FITAP 001 A03",
                                       "LEY 2011/047", "ARSET-I 0015", "ANR TEC 0001/15 C2", "ANR P+L 0034/13"],
     ["11220150100433CO", "PICT", "ANR", "ANR FONSOFT", "PNAPI-122002", "NA001", "R01GM123456", ""]),
    (validate_ar_conicet_project_code, ["11220150100433CO", "22920160100012CO", "11420080100426CO"],
     ["11220150100433", "1122015010043CO", "11218150100433CO", "PICT-2015-1234"]),
    (validate_ar_cyt_project_code, ["PICT-2015-1234", "11220150100433CO", "ANR 600 NA093/08"], ["PNAPI-122002", "2015", "abc"]),
    (validate_ar_mincyt_equipment_id, ["SNM-826", "SNCAD-483", "SNEM-512", "SINALA-1021", "SNB-7", "SNMAG-1203", "snrx-45"],
     ["SNX-12", "SNM826", "SNM-", "SNM-123456", "PICT-2015-1234"]),
    (validate_ar_conicet_category, ["Investigador asistente", "Investigador adjunto", "INVESTIGADORA PRINCIPAL", "Investigador superior",
                                    "Investigador superior emérito", "Investigador correspondiente", "Becario doctoral",
                                    "Personal de apoyo", "No pertenece a Conicet", "Gestión CyT"],
     ["PRINCIPAL", "Superior", "adjunto", "Profesor titular", "Técnico principal", "Investigador", "Director"]),
    (validate_ar_conicet_category_name, ["asistente", "Adjunto", "principal", "Investigador independiente"], ["Profesor titular", "1"]),
    (validate_ar_bahra_code, ["02000010000", "06441030015", "14014010000", "50007010001", "6441030015", "02000010000.0"],
     ["14014010", "1401401002", "99000010000", "0200001000A", "020000100001"]),
    (validate_ar_bahra_department_part, ["084", "000", "7", "14098"], ["999", "abc"]),
    (validate_ar_department_name, ["Capital Federal", "Ciudad Autónoma de Buenos Aires", "Diamante", "Tafí del Valle"], ["Resistencia", "A"]),
    (validate_oecd_ford_code, ["1", "6", "1.1", "1.7", "2.11", "5.9", "6.5", "1.0", "1.1.0", "1.1.1", "1.5.10", "3.1.10"],
     ["-1", "0", "7", "1.8", "2.12", "7.1", "1.1.1.1", "1.123", "SIN DATOS"]),
    (validate_journal_quartile, ["Q1", "Q2", "Q3", "Q4", "q1", "NO INDEXADO", "-", "not indexed"], ["Q5", "Q12", "Q0", "1", "A"]),
    (validate_journal_title, ["FOOD CHEMISTRY", "VETERINARY ANAESTHESIA AND ANALGESIA", "J. Biol. Chem.", "TEUKEN-BIDIKAY", "Nature"],
     ["1467-2987", "22158405", "Q1", "123", "https://example.org/journal", ""]),
    (validate_journal_volume, ["43", "190", "2015", "12A", "5 Suppl", "XXXV", "IX", "43.0"], ["0", "-", "195-198", "Q1", "abc", "123456"]),
    (validate_page_number, ["195", "1093", "1", "S12", "e0123", "xiv", "12345678", "195.0"], ["0", "195-198", "abc", "", "123456789"]),
    (validate_keyword_list, ["Maropitant|Morphine|Acepromacine", "Golfo San Jorge; Contaminantes", "CAPITAL SOCIAL|EMPRENDEDORES",
                             "oviducto", "teoría de aproximación"],
     ["", "123", "x" * 1001, ABSTRACT]),
    (validate_abstract_text, [ABSTRACT, "No publicable"], ["mmmmm", "Golfo San Jorge; Contaminantes", ""]),
    (validate_work_title, ["DOS GRANDES METROPOLIS LATINOAMERICANAS", "Water Stress in Biological, Chemical, Pharmaceutical and Food Systems"],
     ["1", "", "x" * 501]),
    (validate_grant_number, ["R01GM123456", "PICT-2015-1234", "101034427", "ANR 600 NA093/08"],
     ["", "Ministerio de Ciencia", "x1" * 25, "uno dos tres cuatro cinco seis 7"]),
    (validate_isic_rev4, ["A", "U", "01", "011", "0111", "4520", "99"], ["V", "04", "34", "01111", "1", "AB"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("ar_country/ar_science.yaml", "arconicetcategorybyname", ["categoria_conicet", "categoria_conicet_descripcion", "conicet_categoria",
                                                              "persona_categoria_conicet"],
     ["categoria", "conicet"]),
    ("ar_country/ar_geo.yaml", "arbahracodebyname", ["cod_bahra", "codigo_bahra", "bahra_id", "bahra", "cod_asentamiento_bahra"],
     ["bahrain", "cod_bah"]),
    ("ar_country/ar_geo.yaml", "arindecprovincecodebyname", ["dpt_codigo", "dpt_cod", "provincia_id", "cod_prov"], ["dpt_descripcion"]),
    ("ar_country/ar_geo.yaml", "arprovincebyname", ["dpt_descripcion", "provincia"], ["dpt_codigo"]),
    ("ar_country/ar_geo.yaml", "arbahradepartmentpartbyname", ["dpa__codigo", "dpa_codigo"], ["dpa_descripcion", "CODDEPTO"]),
    ("ar_country/ar_census.yaml", "arindeclocalitypartbyname", ["localidad_codigo", "CODLOC"], ["localidad_descripcion"]),
    ("ar_country/ar_census.yaml", "ardepartmentnamebyname", ["dpa_descripcion", "departamento"], ["dpa__codigo"]),
    ("ar_country/ar_census.yaml", "arlocalitynamebyname", ["localidad_descripcion", "NOMLOC"], ["localidad_codigo"]),
    ("common/research.yaml", "oecdfordcodebyname", ["area_codigo", "gran_area_codigo", "disciplina_codigo", "codigo_disciplina", "ford",
                                                   "fos_code"],
     ["area", "codigo_area", "area_descripcion"]),
    ("common/research.yaml", "journaltitlebyname", ["revista", "journal", "journal_title", "Journal Name", "source title", "nombre_revista",
                                                   "titulo_revista"],
     ["revista_sjr", "journal_id", "revistas_x"]),
    ("common/research.yaml", "journalvolumebyname", ["volumen", "volume", "vol", "Vol.", "journal_volume"], ["volumen_m3", "volumes", "tomo"]),
    ("common/research.yaml", "pagenumberbyname", ["pagina_inicial", "pagina_final", "start_page", "end_page", "first page", "spage",
                                                 "epage", "page_start", "pag_desde"],
     ["pagina", "page", "pages", "paginas_totales", "homepage"]),
    ("common/research.yaml", "keywordbyname", ["palabras_clave", "palabras clave", "keywords", "Key words", "mots-clés",
                                              "author_keywords", "Schlagwörter"],
     ["clave", "palabras", "key", "keyword_id_x_y"]),
    ("common/research.yaml", "abstractbyname", ["resumen", "abstract", "resumo", "résumé", "Zusammenfassung", "resumen_proyecto"],
     ["resumenes_x", "summary", "resumido"]),
    ("common/research.yaml", "worktitlebyname", ["titulo_libro", "titulo_del_proyecto", "título_artículo", "book_title", "article title"],
     ["titulo", "title", "titulo_grado", "job_title"]),
    ("common/research.yaml", "grantnumberbyname", ["grant_number", "award_number", "grant id", "funding_number", "numero_de_subsidio"],
     ["grant", "award", "grantor"]),
    ("common/research.yaml", "isicrev4byname", ["codigo_rev4", "ciiu", "ciiu_rev4", "isic", "isic_rev4", "cod_ciiu", "rev4"],
     ["cuci", "clae", "naics"]),
    ("common/dublincore.yaml", "publisherbyname", ["editorial", "publisher", "Publisher", "casa_editorial", "editora"],
     ["editoriales_x", "editor", "editorial_id_x"]),
    ("common/science.yaml", "academicdisciplinebyname", ["disciplina_descripcion", "area_descripcion", "gran_area_descripcion",
                                                        "disciplina"],
     ["area", "descripcion"]),
    ("es/es_geo.yaml", "esstreetnamebyname", ["direccion_calle", "dirección_calle", "calle2"], ["direccion", "calle"]),
    ("pii/pii.yaml", "genderbyname", ["sexo_director", "sexo_directora", "sexo_del_director", "sexo", "sex_code"], ["sexo_director_x"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f"{f[1]}-{i}" for i, f in enumerate(FIELDS)])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("ar_country/ar_science.yaml", "aranpcytprojectcodevalue", ["PICT-2015-1234", "CF BA 001/07"], ["11220150100433CO"]),
    ("ar_country/ar_science.yaml", "arconicetprojectcodevalue", ["11220150100433CO"], ["PICT-2015-1234"]),
    ("ar_country/ar_science.yaml", "aranpcytfundvalue", ["FONCYT", "FONTAR", "FONSOFT", "FONARSEC"], ["FONDECYT", "CONICET"]),
    ("ar_country/ar_science.yaml", "armincytequipmentidvalue", ["SNM-826", "SINALA-1021"], ["SNX-12"]),
    ("ar_country/ar_science.yaml", "arconicetcategoryvalue", ["Investigador adjunto", "Becario doctoral"], ["PRINCIPAL"]),
    ("common/research.yaml", "journalquartilevalue", ["Q1", "NO INDEXADO"], ["Q5"]),
    ("common/research.yaml", "oecdfordcodevalue", ["1.1.0", "2.11"], ["1.12", "-1"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value
