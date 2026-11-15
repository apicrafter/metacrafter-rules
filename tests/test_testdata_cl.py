"""Rules for the Chilean files of metacrafter-testdata (2024 snapshots of the Dateno catalogue: the research
data repositories of the Universidad de Chile, datos.uchile.cl, cdi00000365, and of the Universidad de
Concepción, datav.udec.cl, cdi00000364): the comunas and the indigenous peoples of Chile, country names in
Spanish, amino acids, codons, KEGG Orthology identifiers, p-values and log2 fold changes of expression tables,
earthquake magnitudes, the self-rated health, smoking status and employment status of survey respondents,
sports teams, and the option codes of survey forms (soltero_a, muy_de_acuerdo_5, educaci_n_media_completa).

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.cl.geo import CL_COMUNAS, validate_cl_comuna, validate_cl_comuna_or_none
from metacrafterext.rules.cl.persons import validate_cl_indigenous_people, validate_cl_indigenous_people_answer
from metacrafterext.rules.common.directories import validate_education_level
from metacrafterext.rules.common.formcodes import form_text
from metacrafterext.rules.common.generic import has_letters
from metacrafterext.rules.common.omics import (
    validate_amino_acid,
    validate_amino_acid_or_stop,
    validate_codon,
    validate_kegg_orthology_id,
    validate_log2_fold_change,
    validate_p_value,
    validate_standard_amino_acid,
)
from metacrafterext.rules.common.respondents import (
    validate_employment_status,
    validate_self_rated_health,
    validate_smoking_status,
)
from metacrafterext.rules.common.seismology import validate_earthquake_magnitude
from metacrafterext.rules.common.survey import validate_likert_response
from metacrafterext.rules.es.countries import validate_es_country_name
from metacrafterext.rules.es.periods import validate_marital_status
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (validate_cl_comuna, ["Lo Barnechea", "Til Til", "Til-Til", "Tiltil", "CONCEPCION", "Viña del Mar", "Chillán", "santiago",
                          "Puerto Saavedra", "Comuna de Maipú", "Ñuñoa", "O'Higgins", "Llay-Llay", "Coihaique", "Aisén"],
     ["Cachapoal", "Metropolitana", "13101", "Buenos Aires", "Comuna 14", "No sabe", ""]),
    (validate_cl_comuna_or_none, ["Paine", "Otra", "Sin información"], ["Lima", "DIA", ""]),
    (validate_cl_indigenous_people, ["Mapuche", "mapuche", "diaguitas", "quechua", "Aymara", "Rapa Nui", "Atacameño o Lickanantay",
                                     "Kawésqar", "Selk'nam", "Huilliche", "Pueblo Colla"],
     ["ninguna_no_sabe", "otro", "Guaraní", "Chilena", "3", ""]),
    (validate_cl_indigenous_people_answer, ["mapuche", "ninguna_no_sabe", "otro", "No pertenece a ningún pueblo indígena"],
     ["Guaraní", "si", ""]),
    (validate_es_country_name, ["Perú", "PERU", "Haiti", "Haití", "Brasil", "México", "Estados Unidos", "EE.UU.", "Países Bajos",
                                "Alemania", "Chile", "Reino Unido"],
     ["Germany", "United States", "Venezolana", "Brazil", "CL", "152", ""]),
    (validate_amino_acid, ["Ala", "Arg", "Leu", "Ser", "Gly", "ARG", "Sec", "Xaa"], ["Abc", "A", "Alanine", "Ter", ""]),
    (validate_standard_amino_acid, ["Ala", "Arg", "Trp", "SER"], ["Sec", "SEC", "Xaa", "PRI", ""]),
    (validate_amino_acid_or_stop, ["Arg", "Ter", "Stop", "End", "*"], ["Abc", "1", ""]),
    (validate_codon, ["GCG", "ATG", "TAA", "UAA", "AUG", "gcg"], ["GCX", "ATGC", "ATU", "AT", ""]),
    (validate_kegg_orthology_id, ["K00128", "K01689", "ko:K00134", "K00134,K10705"], ["k00128", "K0012", "K001289", "KO", ""]),
    (validate_p_value, ["0.023", "0.96", ".05", "3.2e-08", "0", "1", "1.0", "NA", "<0.001"], ["1.5", "-0.2", "15", "significant", ""]),
    (validate_log2_fold_change, ["-2.32", "1.35", "0.24", "-15", "15", "-1000000", "Inf", "-Inf", "NA"], ["up", "2015-09-17", ""]),
    (validate_earthquake_magnitude, ["4.46", "1.864", "8.8", "-0.3", "5", "Mw 6.1", "5.2 ML", "NaN"], ["25", "12.02", "1200", "strong", ""]),
    (validate_self_rated_health, ["Excellent", "Very good", "Good", "Fair", "Poor", "excelente", "muy_bueno", "bueno", "regular", "malo",
                                  "Very bad", "No sabe"],
     ["3", "Yes", "Diabetes", "si", ""]),
    (validate_smoking_status, ["Never smoker", "Former smoker", "Current smoker", "Ex-smoker", "Daily", "fumo_habitualmente",
                               "antes_fumaba__pero_lo_dej", "nunca_he_fumado", "fumo_espor_dicamente__menos_de_dos_veces", "Exfumador",
                               "No fumador"],
     ["Yes", "No", "si", "10", "Cigarettes", ""]),
    (validate_employment_status, ["Employed", "Unemployed", "Retired", "Self-employed", "Employed full-time", "Student", "Desempleado",
                                  "Jubilada", "Dueña de casa", "trabajo_tiempo_completo__dependiente_o_i",
                                  "trabajo_de_medio_tiempo__dependiente_o_i", "trabajo_dom_stico_no_remunerado__due_a_o",
                                  "desempleado__buscando_trabajo", "desocupado__no_busca_trabajo"],
     ["Yes", "40", "Engineer", "trabajo", ""]),
    # the option codes of a survey form
    (validate_likert_response, ["muy_de_acuerdo_5", "1_muy_en_desacuerdo", "5_muy_de_acuerdo", "muy_importante", "algo_importante",
                                "no_es_importante", "nada_importante", "casi_siempre", "a_veces", "ocasionalmente", "unas_pocas_veces",
                                "f_cil", "muy_f_cil", "dif_cil", "muy_dif_cil", "apropiado", "medianamente_apropiado",
                                "algo_preocupado_a", "para_nada_preocupado_a", "Totalmente de acuerdo", "Siempre"],
     ["4", "si", "vive_solo_a", "soltero_a", "supermercado", "no_aplica", ""]),
    (validate_marital_status, ["soltero_a", "casado_a", "viudo_a", "separado_a", "divorciado_a", "anulado_a",
                               "conviviente_civil__con_acuerdo_de_uni_n_", "conviviente_o_pareja_sin_acuerdo_de_uni_", "Soltero/a"],
     ["Activo", "si", "muy_bueno", ""]),
    (validate_education_level, ["educaci_n_media_completa__cient_fico_hum", "educaci_n_media_incompleta__cient_fico_h",
                                "educaci_n_superior_completa__t_cnica_sup", "educaci_n_superior_incompleta__t_cnica_s",
                                "8vo_b_sico_o_menor", "Secundario completo"],
     ["a_veces", "soltero_a", "muy_bueno", "fumo_habitualmente", ""]),
    # a uri of row numbers is no address
    (has_letters, ["https://datos.uchile.cl", "example.org/a"], ["1", "370", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ + str(i) for i, v in enumerate(VALIDATORS)])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


def test_comunas():
    assert len(CL_COMUNAS) == len(set(CL_COMUNAS)) == 346
    assert all(validate_cl_comuna(name) for name in CL_COMUNAS)
    assert all(validate_cl_comuna(name.upper()) for name in CL_COMUNAS)


def test_form_text():
    """Two pieces around a lost accented letter are one word when the whole is known."""
    known = frozenset(("educacion", "basico", "mas", "deje"))
    assert form_text("educaci_n_media_completa", known) == "educacion media completa"
    assert form_text("8vo_b_sico_o_menor", known) == "8vo basico o menor"
    assert form_text("m_s_de_5_a_os", known) == "mas de 5 a os"
    assert form_text("lo_dej", known) == "lo deje"
    assert form_text("Soltero/a") == "soltero a"


FIELDS = [
    ("cl/cl_geo.yaml", "clcomunabyname", ["Comuna", "comuna", "COMUNA", "nombre_comuna", "nom_comuna", "comuna_residencia", "glosa_comuna",
                                         "NOM_COM", "comuna_de_residencia", "comunas"],
     ["cod_comuna", "comuna_id", "codigo_comuna", "comunidad", "cut_comuna"]),
    ("cl/cl_persons.yaml", "clindigenouspeoplebyname", ["pueblo_originario", "pueblo_indigena", "pueblos originarios", "pertenencia_indigena",
                                                       "pertenencia_a_pueblo_originario", "04Ustedseconsideraperten"],
     ["pueblo", "etnia", "originario", "indigena_si_no_cod"]),
    ("common/geo.yaml", "escountrynamebyname", ["pais_origen", "pais_nacimiento", "país de nacimiento", "pais_residencia", "nombre_pais",
                                               "pais_desc", "pais_descripcion", "pais_destino"],
     ["pais", "país", "pais_origem", "nm_pais", "pais_id", "cod_pais", "country"]),
    ("common/science.yaml", "aminoacidbyname", ["AmAcid", "amino_acid", "aminoacid", "Amino Acid", "residue", "aa", "aa_code", "aminoácido"],
     ["acid", "amino_acid_count", "aa_position", "residues_total"]),
    ("common/science.yaml", "codonbyname", ["Codon", "codon", "codons", "ref_codon", "start_codon", "triplet", "anticodon"],
     ["codon_count", "codon_position", "Fraction"]),
    ("common/science.yaml", "keggorthologyidbyname", ["K0s", "KO", "ko", "KOs", "ko_id", "KEGG_ko", "kegg_orthology", "KEGG Orthology ID"],
     ["kegg_pathway", "kegg", "Path1", "ENZ", "koala"]),
    ("common/science.yaml", "pvaluebyname", ["p-value", "pvalue", "p.value", "p_value", "pval", "padj", "FDR", "q-value",
                                            "Differential Expression p-value", "adj.P.Val", "p_value_adjusted", "valor_p"],
     ["p", "value", "p_s", "price_value", "pv", "Differential Expression Log2 Ratio"]),
    ("common/science.yaml", "log2foldchangebyname", ["log2FoldChange", "logFC", "log2FC", "Log2 Ratio", "Differential Expression Log2 Ratio",
                                                    "log2_fold_change", "l2fc"],
     ["fold", "log", "ratio", "FC", "Differential Expression p-value", "logistic"]),
    ("common/observations.yaml", "earthquakemagnitudebyname", ["magnitude", "Magnitude", "mag", "magnitud", "magnitude(Mw)", "mag_ml",
                                                              "local_magnitude", "mw_mag", "event_magnitude", "MAGNITUDE (ML)"],
     ["ML", "Mw", "MA", "std_ML", "magType", "magnet", "image", "magazine", "depth(km)"]),
    ("common/survey.yaml", "selfratedhealthbyname", ["self_rated_health", "general_health", "Health_Status", "health_status",
                                                    "estado_de_salud", "salud_autopercibida", "45Engeneralcmoesuestadodesalud", "SRH"],
     ["health", "salud", "health_centre", "estado", "mental_health_score"]),
    ("common/survey.yaml", "smokingstatusbyname", ["smoking_status", "smoking", "smoker", "Smoking Status", "tobacco_use", "tabaquismo",
                                                  "fuma", "46Ustedfumatabaco", "current_smoker"],
     ["cigarettes_per_day", "smoke_free_area", "tabaco_precio", "smoking_years"]),
    ("common/survey.yaml", "employmentstatusbyname", ["employment_status", "Employment Status", "labour_force_status", "labor_force_status",
                                                     "work_status", "situacion_laboral", "situación laboral", "condicion_de_actividad",
                                                     "06Cmodefiniraacinlaboralactual", "empstat"],
     ["employment", "employer", "status", "laboral", "employment_rate", "job_title"]),
    ("common/generic.yaml", "sportsteambyname", ["homeTeam", "awayTeam", "home_team", "away_team", "away_team_name", "equipo_local",
                                                "equipo_visitante", "opponent_team"],
     ["team", "team_id", "home", "away", "teams", "team_size", "homeTeamScore"]),
    ("common/environment.yaml", "phbyname", ["pH", "sed_pH", "soil_ph", "water pH", "pH_H2O"], ["sed_EC", "graph", "phase"]),
    ("pii/pii.yaml", "maritalstatusbyname", ["estado_civil", "marital_status", "05Culessuestadocivil"], ["estado", "civil"]),
    ("common/directories.yaml", "educationlevelbyname", ["nivel_educativo", "education_level", "07Culfuesultducacionalalcanzado"],
     ["Education", "alcanzado"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_names(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


def test_value_rules():
    assert value_matches("cl/cl_geo.yaml", "clcomunavalue", "Lo Barnechea")
    assert not value_matches("cl/cl_geo.yaml", "clcomunavalue", "DIA")
    assert value_matches("common/science.yaml", "aminoacidvalue", "Arg")
    assert not value_matches("common/science.yaml", "aminoacidvalue", "SEC")
    assert not value_matches("common/science.yaml", "aminoacidvalue", "Arginine")
    assert value_matches("common/science.yaml", "codonvalue", "GCG")
    assert not value_matches("common/science.yaml", "codonvalue", "GCX")
    assert value_matches("common/science.yaml", "keggorthologyidvalue", "K00128")
    assert not value_matches("common/science.yaml", "keggorthologyidvalue", "K0012")


def test_guarded_value_rules():
    """Three letters of A, C, G and T are also initials, K and five digits a part number, a people's name a
    language (quechua): the value rules run only in fields named for them. A date as a spreadsheet day number
    is read in DateBirrth and DateAss, and a uri of row numbers is no URL."""
    import re
    for path, rule_id in (("common/science.yaml", "codonvalue"), ("common/science.yaml", "keggorthologyidvalue"),
                          ("cl/cl_persons.yaml", "clindigenouspeoplevalue"), ("cl/cl_geo.yaml", "clcomunavalue")):
        assert load(path, rule_id)["fieldregex"], rule_id
    # Maipú and San Rafael are departments of Mendoza, Constitución an act of a company register
    comuna = re.compile(load("cl/cl_geo.yaml", "clcomunavalue")["fieldregex"])
    assert all(comuna.search(name) for name in ("Comuna Social", "Comuna Tributaria", "comuna_establecimiento"))
    assert not any(comuna.search(name) for name in ("departamento", "Tipo de actuacion", "3a"))
    guard = re.compile(load("common/dateandtime.yaml", "excelserialdatevalue")["fieldregex"])
    assert all(guard.search(name) for name in ("DateBirrth", "DateAss", "date_of_birth", "fecha_nacimiento"))
    assert not any(guard.search(name) for name in ("update", "candidate", "date", "dated_2020_values"))
    assert load("common/internet.yaml", "websiteknown")["validator"].endswith("has_letters")
