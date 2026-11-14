"""Rules for the datos.gob.ar files of metacrafter-testdata (an April 2024 snapshot of the Argentine
national open data portal): INDEC geographic codes of the georef service, CUIT with a check digit,
CLAE activities, GDE document numbers, COMPR.AR / CONTRAT.AR / BAC process numbers, SAF and BAPIN
budget codes, oil and gas well designations and sedimentary basins, CAMMESA electricity market
codes, ANAC aerodrome designators, Argentine area and postal codes, NCM codes, GeoJSON written as
text and ISO 3166-2 codes; and fixes of person names on nombre_completo and of states on estado.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.ar_country.codes import (
    validate_ar_anac_airport_code,
    validate_ar_bapin_code,
    validate_ar_cammesa_agent_code,
    validate_ar_cammesa_generating_unit_code,
    validate_ar_cammesa_power_plant_code,
    validate_ar_clae,
    validate_ar_compras_procedure_number,
    validate_ar_cpa,
    validate_ar_cuit,
    validate_ar_gde_number,
    validate_ar_gde_number_known_ecosystem,
    validate_ar_hydrocarbon_well_code,
    validate_ar_indec_department_code,
    validate_ar_indec_local_government_code,
    validate_ar_indec_locality_code,
    validate_ar_indec_province_code,
    validate_ar_indec_street_code,
    validate_ar_ncm_code,
    validate_ar_phone_area_code,
    validate_ar_postcode,
    validate_ar_province_letter,
    validate_ar_saf_code,
    validate_ar_sedimentary_basin,
)
from metacrafterext.rules.common.generic import (
    validate_geojson_geometry_text,
    validate_iso3166_2_code,
    validate_person_fullname_not_place,
    validate_state_not_status,
)
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (validate_ar_indec_province_code, ["02", "06", "58", "94", "2", "6", 14], ["04", "152", "95", "06014", "", "AR-C"]),
    (validate_ar_indec_department_code, ["06014", "30015", "02007", "6014", "2004", 58035],
     ["03014", "3001", "601", "060140", "95001"]),
    (validate_ar_indec_local_government_code, ["060441", "140399", "908063", "60441"], ["003001", "05001", "7654321"]),
    (validate_ar_indec_locality_code, ["06007010", "02000010", "1401401002", "6441030", 58007010],
     ["8585", "10", "00101001", "9876543210123"]),
    (validate_ar_indec_street_code, ["0200701000000", "0665801099996", "200701000006"],
     ["02028010999360800726", "0300701000000", "0200701"]),
    (validate_ar_cuit, ["30-50014329-7", "30506726804", "30-65823369-2", "20121502934", "33-71180303-9"],
     ["30-50014329-8", "84X20AZ402006P", "11-12345678-9", "3050672680", "30-5001432-97"]),
    (validate_ar_clae, ["011111", "475230", "620100", "14211", "990000"], ["1", "46", "041111", "1234567", "A"]),
    (validate_ar_gde_number, ["IF-2019-68464597-APN-DNCOPRCYFC#JGM", "PLIEG-2017-1484136-APN-DCC#MEM",
                              "EX-2021-23967059-   -APN-GASNYA#CNEA", "RESOL-2017-232-APN#MD", "NO-2018-06919784-APN-JGM",
                              "EX-2022-20377022-   -GCABA-DGINYAR"],
     ["EE-10947", "450-9020-LPU16", "2021-15925129", "EXP-S04:0187701/2009", "RL-23-12-APN"]),
    (validate_ar_compras_procedure_number, ["452-0001-LPU17", "81-0009-OBR18", "14-1002-CON21", "14-549-SCO18",
                                            "10179-0125-LPU22"],
     ["452-0001-ABC17", "40/31-0001-OBR20", "OC-00010620", "PLIEG-2017-1484136-APN-DCC#MEM"]),
    (validate_ar_saf_code, ["105", "604", "325"], ["0105", "42", "1000", "abc"]),
    (validate_ar_bapin_code, ["0", "30025", "143014"], ["1234567", "SAF 315", ""]),
    (validate_ar_hydrocarbon_well_code, ["YPF.Nq.LLL-1218(d)", "PAE.Ch.Z.IA-1072", "YPF.Md.NSN.e-2", "CGC.SCA.CI-1021(d)",
                                         "Pp.Nq.Ce-1019"],
     ["T-49", "RA-59", "1.2.3-4", "YPF.Nq.LLL"]),
    (validate_ar_sedimentary_basin, ["NEUQUINA", "GOLFO SAN JORGE", "Golfo de San Jorge", "CAÑADON ASFALTO", "Austral",
                                     "NEU", "GSJ"],
     ["Neuquén", "Cuenca Baja Riachuelo", "NO", "Total Cuenca"]),
    (validate_ar_cammesa_agent_code, ["EPECORDG", "CCOSTANG", "CAPEX-QA", "14DEMP3N", "J&PSCAJN"],
     ["COST", "12345678", "EPEC GENERACION", "CTBROWNGG"]),
    (validate_ar_cammesa_power_plant_code, ["COST", "NPUE", "TUNAHI", "SNIC"], ["2019", "CO", "COSTTG08X", "cost"]),
    (validate_ar_cammesa_generating_unit_code, ["COSTTG08", "ANATDI01", "CEPUTG11", "SNICTV15"],
     ["COST", "NIDETV", "12345678", "COSTTG8"]),
    (validate_ar_anac_airport_code, ["AER", "CBA", "DOZ", "EZE", "MOR"], ["AEP", "COR", "MDZ", "SABE", "aer"]),
    (validate_ar_phone_area_code, ["11", "351", "2942", "0221", "3777"], ["4", "54911", "5", "123456"]),
    (validate_ar_postcode, ["C1038AAK", "X5187XAB", "1414", "8345"], ["0123", "28079", "C1038AA", "I1038AAK"]),
    (validate_ar_cpa, ["C1038AAK", "B1900AAA"], ["1414", "O1038AAK"]),
    (validate_ar_province_letter, ["B", "C", "X", "Q"], ["I", "O", "BA", "b"]),
    (validate_ar_ncm_code, ["010121", "0101.21", "01012100"], ["Caballos, reproductores de raza pura", "01", "A01"]),
    (validate_geojson_geometry_text, ['{"type":"Point","coordinates":[-58.6613,-34.480036]}',
                                      '{"type":"MultiLineString","coordinates":[[[-58.66,-34.48],[-58.67,-34.49]]]}',
                                      '{"coordinates":[-58.6613,-34.48],"type":"Point"}'],
     ['{"type":"Feature","geometry":{}}', "[-58.66, -34.48]", "POINT(-58.66 -34.48)", "0101000020E6100000"]),
    (validate_iso3166_2_code, ["AR-C", "AR-Q", "DE-BY", "FR-75C"], ["ARG", "06", "AR-", "ar-c"]),
    (validate_person_fullname_not_place, ["Luis Esteban Genoud", "Fernandez, Alberto Angel", "MARIA MANUELA LOPEZ MENENDEZ"],
     ["Provincia del Neuquén", "Partido de Adolfo Gonzales Chaves", "Departamento Capital", "Ciudad Autónoma de Buenos Aires",
      "GENOUD"]),
    (validate_state_not_status, ["SP", "Jalisco", "Rio de Janeiro", "N/I"],
     ["Finalizada", "En proceso", "Exploración Avanzada", "ANULADA", "Producción "]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


def test_gde_value_rule_takes_known_ecosystems_only():
    assert validate_ar_gde_number_known_ecosystem("PLIEG-2017-1484136-APN-DCC#MEM")
    assert validate_ar_gde_number_known_ecosystem("EX-2022-20377022-   -GCABA-DGINYAR")
    assert not validate_ar_gde_number_known_ecosystem("RS-2025-00124133-GLP-MCM")
    assert validate_ar_gde_number("RS-2025-00124133-GLP-MCM")


FIELDS = [
    ("ar_country/ar_geo.yaml", "arindecprovincecodebyname",
     ["provincia_id", "id_provincia_indec", "provincia_indec_id", "cod_prov", "ID_prov", "IdProvincia", "calle_provincia_id",
      "jurisdiccion_residencia_id", "cod_provincia"],
     ["provincia", "provincia_nombre", "jurisdiccion_id", "ubicacion_geografica_id"]),
    ("ar_country/ar_geo.yaml", "arindecdepartmentcodebyname",
     ["departamento_id", "iddepartamento", "id_depar", "cod_dep", "in_departamentos", "codigo_departamento_indec", "IdDepartamento"],
     ["departamento", "departamento_nombre", "department"]),
    ("ar_country/ar_geo.yaml", "arindeclocalgovernmentcodebyname", ["municipio_id", "id_municipio", "cod_municipio"],
     ["municipio", "municipio_nombre", "municipality_code"]),
    ("ar_country/ar_geo.yaml", "arindeclocalitycodebyname",
     ["localidad_censal_id", "cod_loc", "Cod_Loc", "localidad_id", "calle_localidad_censal_id", "id_localidad"],
     ["localidad", "localidad_nombre"]),
    ("ar_country/ar_geo.yaml", "arindecstreetcodebyname", ["calle_id", "calle_a_id", "calle_b_id"], ["calle", "calle_nombre"]),
    ("ar_country/ar_geo.yaml", "arcentroidlatitudebyname", ["centroide_lat", "centroide_latitud"], ["centroide_lon", "lat"]),
    ("ar_country/ar_geo.yaml", "arcentroidlongitudebyname", ["centroide_lon", "centroide_longitud"], ["centroide_lat"]),
    ("ar_country/ar_geo.yaml", "arprovinceletterbyname",
     ["letra_provincia_inscripcion_inicial", "letra_provincia_transferencia", "letra_provincia"], ["letra", "provincia"]),
    ("ar_country/ar_geo.yaml", "aranacairportbyname", ["Aeropuerto", "Origen / Destino", "origen/destino", "aerodromo"],
     ["Aeronave", "Aerolinea Nombre"]),
    ("ar_country/ar_geo.yaml", "arphoneareacodebyname", ["codigo_indicativo_telefono", "cod_tel", "cod_area", "característica"],
     ["telefono", "tel", "area"]),
    ("ar_country/ar_geo.yaml", "arpostcodebyname", ["cp", "CP", "codigo_postal", "cod_postal", "cpa"], ["cps", "postal"]),
    ("ar_country/ar_finances.yaml", "arcuitbyfieldname",
     ["Cuit Vendedor", "Cuit Comprador", "contratista_cuit", "cuit_cuil", "CUIT", "persona_juridica_cuit"],
     ["cuenta", "razon_social"]),
    ("ar_country/ar_finances.yaml", "arclaebyname", ["clae6", "clae", "clae_6", "codigo_clae"], ["clae2", "letra", "clae6_desc"]),
    ("ar_country/ar_finances.yaml", "arsafbyname", ["organismo_codigo_saf", "codigo_saf", "saf"], ["safety", "servicio_id"]),
    ("ar_country/ar_finances.yaml", "arbapinbyname", ["codigo_bapin_id", "bapin", "codigo_bapin"], ["codigo_bapin_desc"]),
    ("ar_country/ar_finances.yaml", "arncmbyname", ["cod_ncm_6d", "ncm", "codigo_ncm", "posicion_arancelaria"], ["ncm_desc"]),
    ("ar_country/ar_government.yaml", "argdenumberbyname",
     ["pliego_condiciones_generales_numero_gedo", "expediente_procedimiento_numero", "numero_gedo", "expediente"],
     ["procedimiento_numero", "numero_obra"]),
    ("ar_country/ar_government.yaml", "arcomprasnumberbyname",
     ["procedimiento_numero", "contrato_numero", "numero_obra", "solicitud_de_contratacion_numero"],
     ["procedimiento_nombre", "obra_nombre"]),
    ("ar_country/ar_energy.yaml", "arwellcodebyname", ["sigla", "sigla_pozo"], ["siglas", "pozo"]),
    ("ar_country/ar_energy.yaml", "arsedimentarybasinbyname", ["cuenca", "idcuenca", "basin"], ["subcuenca", "cuenca_hidrica"]),
    ("ar_country/ar_energy.yaml", "arcammesaagentbyname", ["agente_nemo", "nemo", "agente"], ["agente_descripcion", "tipo_agente"]),
    ("ar_country/ar_energy.yaml", "arcammesapowerplantbyname", ["central", "central_nemo"], ["centrales", "central_descripcion"]),
    ("ar_country/ar_energy.yaml", "arcammesagenerationunitbyname", ["maquina", "máquina", "maquina_nemo"], ["tipo_maquina"]),
    ("common/geo_text.yaml", "iso3166subdivisionbyname", ["iso_id", "iso_3166_2", "subdivision_code"], ["iso", "iso_nombre"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("ar_country/ar_finances.yaml", "arcuitdashedvalue", ["30-50014329-7", "30-69639421-7"], ["30-50014329-8", "30506726804"]),
    ("ar_country/ar_government.yaml", "argdenumbervalue", ["PLIEG-2017-1484136-APN-DCC#MEM"], ["RS-2025-00124133-GLP-MCM", "EE-10947"]),
    ("ar_country/ar_government.yaml", "arcomprasnumbervalue", ["452-0001-LPU17", "10179-0125-LPU22"], ["2021-15925129"]),
    ("ar_country/ar_energy.yaml", "arwellcodevalue", ["YPF.Nq.LLL-1218(d)"], ["T-49"]),
    ("ar_country/ar_energy.yaml", "arcammesagenerationunitvalue", ["COSTTG08"], ["COST"]),
    ("ar_country/ar_geo.yaml", "arcpavalue", ["C1038AAK"], ["1414"]),
    ("common/geo_text.yaml", "geojsongeometrytext", ['{"type":"Point","coordinates":[-58.6613,-34.480036]}'], ["[1, 2]"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def test_new_field_rules_need_values():
    for path, rule_id, _, _ in FIELDS:
        if rule_id == "arncmbyname":
            assert load(path, rule_id).get("validator")
        assert load(path, rule_id).get("needs_values") is True, rule_id


def test_person_and_state_rules_check_values():
    for path, rule_id in (("ar_country/ar_common.yaml", "ar_common_arpersonnameknown"), ("mx/mx_persons.yaml", "mxpersonnameknown")):
        assert load(path, rule_id)["validator"].endswith("validate_person_fullname_not_place"), rule_id
    for path, rule_id in (("pt/pt_geo.yaml", "ptstateknown"), ("br/br_geo.yaml", "brstateknown"), ("mx/mx_geo.yaml", "mxstateknown")):
        assert load(path, rule_id)["validator"].endswith("validate_state_not_status"), rule_id
