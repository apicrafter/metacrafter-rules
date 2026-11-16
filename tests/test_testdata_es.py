"""Rules for the Spanish files of metacrafter-testdata (2024 snapshots of Spanish open data portals, Dateno
sources cdi00000546 to cdi00000588: Generalitat Valenciana, Arganda del Rey, Diputació de Castelló, Las Palmas
de Gran Canaria, Región de Murcia, Datos Abiertos de Canarias, Observa Gijón, UniversiDATA and València, and
cdi00000504, sprogteknologi.dk): INE codes, school codes, RUCT codes, street type abbreviations, budget
classifications, vehicle plates, masked identity documents, BDNS codes, air quality stations, DIR3 codes,
Erasmus institution codes, SDMX codes and identifiers of the Danish Central Word Register.

Matched as tests/test_testdata_baseline.py matches them.
"""
import re

import pytest

from metacrafterext.rules.es import codes
from tests.test_testdata_baseline import field_matches, load

VALIDATORS = [
    (codes.validate_es_ine_province_code, ["03", "28", "46", "3", "52", "3.0"], ["00", "53", "030", "Alicante", ""]),
    (codes.validate_es_ine_municipio_code, ["28079", "03014", "3014", "12028", "28079.0"], ["030", "99001", "280796", "28000", "Madrid", ""]),
    (codes.validate_es_ccaa_code, ["13", "07", "7", "19"], ["0", "20", "Madrid", ""]),
    (codes.validate_es_ine_country_code, ["108", "110", "340", "501"], ["724", "032", "99", "España", ""]),
    (codes.validate_es_centro_docente_code, ["03013698", "28051581", "12000091", "3013698"], ["2012", "99013698", "IES", ""]),
    (codes.validate_es_ruct_universidad_code, ["056", "019", "010"], ["56", "E MADRID03", "URJC", ""]),
    (codes.validate_es_ruct_titulo_code, ["2500089", "4310001", "2500089.0"], ["8", "250008", "Grado", ""]),
    (codes.validate_erasmus_code, ["E  MADRID03", "PL WARSZAW02", "I MILANO03", "F STRASBO48", "IRLDUBLIN01", "A  ST-POLT03",
                                  "D  BAD-HON01", "I  ROMA16"],
     ["017", "MADRID", "Universidad de Valladolid", "E MADRID", ""]),
    (codes.validate_erasmus_code_by_value, ["E  MADRID03", "PL WARSZAW02", "I MILANO03", "IRLDUBLIN01"],
     ["ROMA0101", "ABCDEF12", "SKP P001", "MADRID03", ""]),
    (codes.validate_es_tipo_via, ["CL", "AV", "PZ", "PS", "cl", "CM", "CR", "RD"], ["CALLE", "C/", "C", "12", ""]),
    (codes.validate_es_budget_economic_code, ["1", "10", "100", "10000", "100.00", "22103"], ["1000", "011A", "0", "Gastos de personal", ""]),
    (codes.validate_es_budget_program_code, ["1", "13", "132", "1521", "91200", "0"], ["5210", "A0010", "111A", "Seguridad", ""]),
    (codes.validate_es_vehicle_plate, ["3499 CDB", "7202JGL", "0360-JDX", "1315 gtz"], ["M4617YU", "1234 ABC", "3499", "(BAJA) 8570GDF", ""]),
    (codes.validate_es_dni_masked, ["***4567**", "****4567*"], ["*********", "12345678X", "053***8***", ""]),
    (codes.validate_es_bdns_code, ["604968", "302000", "103"], ["BDNS604968", "2022/15", "12", ""]),
    (codes.validate_es_air_station_code, ["03009003", "28079008", "4066003"], ["03009", "AL31", "99009003", ""]),
    (codes.validate_es_dir3, ["L05120007", "E04921901", "EA0008567", "l05120007"], ["L0512", "05120007", "Ayuntamiento", ""]),
    (codes.validate_unm49_region, ["150", "039", "419", "39", "019", "19"], ["724", "1500", "Europa", ""]),
    (codes.validate_countrycode_num, ["724", "380", "032", "56", "056"], ["7240", "ES", "España", "1", ""]),
    (codes.validate_sdmx_obs_status, ["A", "E", "P", "M", "_U"], ["C", "AB", "a", "Provisional", ""]),
    (codes.validate_sdmx_age, ["Y15T24", "Y_GE65", "Y_LT5", "Y16", "_T", "Y15"], ["Y15-24", "15T24", "Total", ""]),
    (codes.validate_sdmx_age_band, ["Y15T24", "Y45T64"], ["Y_GE65", "Y15", "_T", ""]),
    (codes.validate_sdmx_reporting_period, ["2018-Q1", "2008-M03", "2020-S2", "2021-W07", "2019-A1"], ["2018", "2018Q1", "03/2008", "2008-M13", ""]),
    (codes.validate_sdmx_reporting_month, ["2008-M03", "2024-M12"], ["2008-03", "2008M03", "2018-Q1", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value
    assert not func(None)


FIELDS = [
    ("es/es_codes.yaml", "esineprovincecodebyname", ["COD_PROV", "cod_provincia", "cod_provincia_residencia", "provincia_cod", "prov_codigo",
                                                    "codigo_provincia", "cod_provincia_centro_sec"],
     ["provincia", "NOM_PROV", "des_provincia_residencia", "cod_postal"]),
    ("es/es_codes.yaml", "esinemunicipiocodebyname", ["COD_MUN", "cod_municipio", "codmun", "codmunsub", "ine", "codigo_mun",
                                                     "cod_municipio_residencia", "municipio_cod", "muni_codigo", "cod_ine", "codigo_municipio"],
     ["municipio", "NOM_MUN", "linea", "cod_mancomunidad"]),
    ("es/es_codes.yaml", "esccaacodebyname", ["cod_comunidad_residencia", "cod_comunidad_destino", "codigo_de_ca", "cod_autonomia", "cod_ccaa",
                                             "cod_comunidad"],
     ["des_comunidad_residencia", "comunidad_autonoma", "cod_caja_fija"]),
    ("es/es_codes.yaml", "esinecountrycodebyname", ["Código Nacionalidad", "Codigo Nacionalidad", "codigo_nacionalidad"],
     ["nacionalidad", "cod_pais_nacionalidad"]),
    ("es/es_codes.yaml", "escentrodocentecodebyname", ["COD_CENTRO", "cod_centro", "codigo_centro", "cod_conser", "cod_eoi", "cod_fpa",
                                                      "cod_unidad_responsable", "código del centro"],
     ["NOM_CENTRO", "cod_centro_gestor", "centro", "cod_tipo_centro"]),
    ("es/es_codes.yaml", "esructuniversidadcodebyname", ["cod_universidad", "cod_universidad_mat", "cod_universidad_doctorado"],
     ["des_universidad", "universidad"]),
    ("es/es_codes.yaml", "esructtitulocodebyname", ["cod_titulacion", "cod_titulacion_origen", "codigo_titulacion"],
     ["des_titulacion", "cod_titulacion_exigida", "titulacion"]),
    ("es/es_codes.yaml", "estipoviabyname", ["TipoVia", "tipo_via", "Tipo vía", "Tipo via", "VIAL", "codtipovia", "Cod. Tipo Via", "sigla"],
     ["NombreVia", "via", "tipo_viajero_code", "codvia"]),
    ("es/es_codes.yaml", "esbudgeteconomiccodebyname", ["cod_capitulo", "cod_articulo", "cod_concepto", "cod_subconcepto", "cod_economico",
                                                       "COD_ECONOMICA", "economica"],
     ["capitulo", "des_capitulo", "concepto", "cod_partida"]),
    ("es/es_codes.yaml", "esbudgetprogramcodebyname", ["cod_programa", "cod_funcional", "cod_areas_de_gasto", "funcional"],
     ["programa", "areas_de_gasto", "cod_organico"]),
    ("es/es_codes.yaml", "esvehicleplatebyname", ["MATRICULA", "Matrícula", "matricula_vehiculo"],
     ["total_matriculaciones", "matriculados", "tipo_matricula_code"]),
    ("es/es_codes.yaml", "esbdnscodebyname", ["Código BDNS", "codigo_bdns", "bdns", "id_bdns", "BDNS ID"], ["Enlace", "codigo"]),
    ("es/es_codes.yaml", "esairstationcodebyname", ["COD_ESTACION", "codigo_estacion", "codigo_nacional", "cod_nacional_estacion"],
     ["NOM_ESTACION", "estacion", "codest"]),
    ("es/es_codes.yaml", "esdir3byname", ["dir3", "DIR3", "codigo_dir3", "dir3_organo"], ["dir", "direccion"]),
    ("es/es_codes.yaml", "escountrycodenumbyname", ["cod_pais_nacionalidad", "cod_pais_residencia", "cod_pais_univ_destino", "cod_pais"],
     ["des_pais_nacionalidad", "pais", "lat_pais_nacionalidad"]),
    ("es/es_codes.yaml", "esunm49byname", ["cod_continente_nacionalidad", "cod_agregacion_paises_nacionalidad", "cod_continente",
                                          "cod_agregacion_paises_univ_destino"],
     ["des_continente_nacionalidad", "continente"]),
    ("es/es_codes.yaml", "escpvcodebyname", ["CPV_CODIGO", "codigo_cpv", "cpvcodigo"], ["CPV_DESCRIPCION", "cpvdescripcion"]),
    ("es/es_codes.yaml", "escifbyrolename", ["ADJUDICATARIO_CIF", "cif_adjudicatario", "cd_nif", "cif_asociacion", "nif_proveedor",
                                            "adjudicatariocif"],
     ["ADJUDICATARIO_DESCRIPCION", "codigo", "unifamilia"]),
    ("es/es_codes.yaml", "esnutsbyname", ["codnut1", "codnut2", "codnut3"], ["nut", "codnucleo"]),
    ("common/sdmx.yaml", "sdmxobsstatusbyname", ["OBS_STATUS", "ESTADO_OBSERVACION_CODE", "observation_status"],
     ["ESTADO_OBSERVACION", "CONFIDENCIALIDAD_OBSERVACION_CODE", "status"]),
    ("common/sdmx.yaml", "sdmxagebyname", ["EDAD_CODE", "AGE_CODE", "GRUPO_EDAD_CODE", "ALCOHOL_CONSUMO_EDAD_INICIO_CODE"],
     ["EDAD", "SEXO_CODE", "age"]),
    ("common/sdmx.yaml", "sdmxreportingperiodbyname", ["TIME_PERIOD_CODE", "TIME_PERIOD", "time_period"], ["periodos_id", "time", "period"]),
    ("common/sdmx.yaml", "erasmuscodebyname", ["erasmus_code", "codigo_erasmus", "Erasmus code", "cod_universidad_procedencia",
                                              "cod_universidad_destino"],
     ["cod_universidad", "des_universidad_destino", "erasmus_plus_grant"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    spec = load(path, rule_id)
    assert spec["key"]
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("es/es_codes.yaml", "esvehicleplatevalue", ["3499 CDB", "7202JGL"], ["3499 CDA", "M4617YU", "123 BCD"]),
    ("es/es_codes.yaml", "esdnimaskedvalue", ["***4567**", "****4567*"], ["*********", "12345678X"]),
    ("dk/dk_texts.yaml", "dkcoridvalue", ["COR.72642", "COR.99892.122.01", "COR.EXT.100002.300.01", "COR.SEM.1000001.01", "COR.EXT.137129"],
     ["COR.7264", "COR", "COR.EXT", "ABC.12345"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    spec = load(path, rule_id)
    pattern = re.compile(spec["rule"])
    for value in good:
        assert pattern.fullmatch(value), value
    for value in bad:
        assert not pattern.fullmatch(value), value
