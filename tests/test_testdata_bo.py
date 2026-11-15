"""Rules for the Bolivian files of metacrafter-testdata (2024 snapshots of the GeoNode of SIARH, the water information
system of the Ministry of Environment and Water, of the GeoNode of the Institute of Geography of UMSA and of
datos.gob.bo): departments, provinces, municipalities and communities by name and INE code, SISIN codes of public
investment projects, SIE codes of schools; Pfafstetter basin codes, oxygen demands and suspended solids of water
quality laboratories, Spanish names of water readings, UTM positions, elevations, areas and years; positions in
degrees, minutes and seconds; and the fixes of false positives these files showed (Argentine department parts,
Mendoza resource accounts, species names, states that are statuses).

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest
import yaml

from metacrafterext.rules.ar_country.census import validate_ar_indec_department_part
from metacrafterext.rules.ar_country.mendoza import validate_ar_mendoza_resource_account
from metacrafterext.rules.bo.codes import validate_bo_sie_code, validate_bo_sisin_code, validate_bo_sisin_code_by_value
from metacrafterext.rules.bo.geo import (
    MUNICIPALITIES,
    PROVINCES,
    validate_bo_community_code,
    validate_bo_department,
    validate_bo_department_code,
    validate_bo_municipality,
    validate_bo_municipality_code,
    validate_bo_municipality_code_known,
    validate_bo_province,
    validate_bo_province_code,
)
from metacrafterext.rules.common.fieldwork import validate_projected_coordinate
from metacrafterext.rules.common.generic import (
    validate_latitude_value,
    validate_longitude_dms,
    validate_longitude_value,
    validate_species_name,
    validate_state_not_status,
)
from metacrafterext.rules.common.hydrology import validate_pfafstetter_code, validate_pfafstetter_code_long
from metacrafterext.rules.common.waterquality import validate_oxygen_demand, validate_suspended_solids
from tests.test_testdata_baseline import RULES, field_matches, load, value_matches

VALIDATORS = [
    (validate_bo_department, ["La Paz", "LA PAZ", "Potosí", "POTOSI", "Potosi", "PotosÃ­", "Potos?", "Santa Cruz",
                              "CHUQUISACA", "El Beni", "09.PANDO", "Departamento de Oruro", "LPZ", "Cochabamba"],
     ["Murillo", "El Alto", "Bolivia", "Total", "Tupiza", "Soracaya", "", "02", "Catamarca", "Pot?"]),
    (validate_bo_department_code, ["01", "02", "9", "07", "5.0"], ["0", "00", "10", "001", "2a", ""]),
    (validate_bo_province, ["Murillo", "Pedro Domingo Murillo", "SUD YUNGAS", "Sur Yungas", "Andrés Ibáñez",
                            "Andres Iba?ez", "ZUDAÃ\x91EZ", "ZudÃ¡Ã±ez", "Muńecas", "MUÃ\x91ECAS", "Ñuflo De Chavez",
                            "?uflo De Ch?vez", "General Jose Balliv", "Gualberto Villarroe", "Provincia Cercado",
                            "Cercado", "Gral. José Manuel Pando", "Obispo Santisteban", "Abun?", "Esteban Arze"],
     ["El Alto", "Potosí", "Total", "Plan Agroforestal Chuquisaca", "Manejo Integral de Cuencas", "General", "", "0201"]),
    (validate_bo_province_code, ["0201", "201", "0715", "0905", "0110", "0316.0"],
     ["0221", "0617", "0720", "1001", "0001", "0200", "02011", "02", ""]),
    (validate_bo_municipality, ["El Alto", "SACABA", "Nuestra Señora de La Paz", "Nuestra Seï¿½ora de La Paz",
                                "Villa Tunari", "Soracachi (Paria)", "SORACACHI (PARIA)", 'Colcha "K"', "Muyupampa",
                                "Villa Vaca Guzmán", "Tiwanaku", "TIAWANACU", "Municipio de Sucre", "PotosÃ­",
                                "Villa montes", "SIPE SIPE", "CORO CORO", "ENTRE RIOS CBBA", "SAN RAMON BENI",
                                "Ascención de Guarayos", "AYOPAYA (V. DE INDEPENDENCIA)", "CIUDAD EL ALTO"],
     ["Murillo", "Oropeza", "Total", "Arroyo Grande", "Abierto", "", "020105", "Costa rica"]),
    (validate_bo_municipality_code, ["020105", "20105", "070101", "070101.0", "040302", "031304"],
     ["020109", "260101", "0201", "0201050", "000101", "021501a", ""]),
    (validate_bo_municipality_code_known, ["020105", "70101", "090503"], ["031304", "010104", "250101", "020109"]),
    (validate_bo_community_code, ["02010501001", "03020101001", "2010501001", "01010105005001", "02010501701"],
     ["020105", "00000000000", "02010500001", "02010501000", "26010501001", "4691333969-D", ""]),
    (validate_bo_sisin_code, ["0287-30477-00000", "086-60061-00000", "086-60063-0000", "2873912800000", "02873912800000"],
     ["s/s", "0287-30477", "2019-03-12", "287391280", "a287-30477-00000", ""]),
    (validate_bo_sisin_code_by_value, ["0287-30477-00000", "0086-60061-00000"], ["2873912800000", "0287-3047-00000"]),
    (validate_bo_sie_code, ["50710004", "80660071", "81980107", "61980032.0"], ["5071000", "05071000", "507100045", "SIE", ""]),
    (validate_pfafstetter_code, ["8", "46", "85899", "8589929", "01592", "85899 - Rio Guadalquivir", "4669.0"],
     ["12a", "-1", "Rio Guadalquivir", "", "1234567890123"]),
    (validate_pfafstetter_code_long, ["015", "0158", "01592", "85899 - Rio Guadalquivir"], ["0", "01", "Muy bajo", ""]),
    (validate_oxygen_demand, ["5", "18,6", "18.5", "250 mg/L", "<2", "< 0.5 mg/L", "0"], ["-1", "2022-03-16", "Alto", ""]),
    (validate_suspended_solids, ["25", "22,8", "0.5", "<5", "43 mg/L"], ["-3", "N/D", "12 NTU", ""]),
    (validate_longitude_dms, ['66° 53\' 41,622" W', "68°08'45\"O", "17 42 26.8 W", "65°30'01.6\"E"],
     ['18° 24\' 5,758" S', "-66.5", "66° 61' 10\" W", "1200 m", ""]),
    (validate_latitude_value, ['18° 24\' 5,758" S', "17°42'26.855\"S", "47.956011633", "-33.86"],
     ["120.5", "1", '66° 53\' 41,622" W', ""]),
    (validate_longitude_value, ['66° 53\' 41,622" W', "-121.67"], ["200.5", "12"]),
    (validate_projected_coordinate, ["576899.428379", "8172295.10953", "590583.09", "-98295.75"],
     ["350.5", "12000000", "576899.4283791234"]),
    (validate_species_name, ["Quercus robur L.", "Paratrechina longicornis (Latreille, 1802)"],
     ["Inventario de Presas 2010", "Proyecto de Riego 2015", "Plan del Agua 2012"]),
    (validate_state_not_status, ["Jalisco", "Rio de Janeiro", "SP", "Baja California Sur"],
     ["Existente y en operacion", "Existe y no operable", "F/Problemas", "DATOS ACTUALIZADOS", "VERIFICAR TRANSMISION",
      "ERROR NIVEL", "ENT DEFINITIVA", "EJEC NORMAL", "VALIDADA", "(*) PROPUESTA TECNICA", "EN FUNCIONAMIENTO"]),
    (validate_ar_indec_department_part, ["7", "098", "14098", "06014"], ["01", "02", "09"]),
    (validate_ar_mendoza_resource_account, ["1110100000-IMPUESTO SOBRE LAS ACTIVIDADES", "1120202000 - INT. GANADOS"],
     ["2838530907-D", "2818917271-D", "1110100000"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


def test_tables_of_the_ine():
    assert len(PROVINCES) == 112
    assert len(MUNICIPALITIES) == 339
    assert all(code[:4] in PROVINCES for code in MUNICIPALITIES)
    # Every municipality of the 2012 list passes, by its INE name and by its code.
    for code, names in MUNICIPALITIES.items():
        assert validate_bo_municipality_code(code) and validate_bo_municipality_code_known(code), code
        for name in names:
            assert validate_bo_municipality(name), name
    for names in PROVINCES.values():
        for name in names:
            assert validate_bo_province(name), name


FIELDS = [
    ("bo/bo_geo.yaml", "bodepartmentbyname", ["DEPARTAMEN", "DEPTO", "Depto", "departamento", "nombre_dep", "NOMDEPT", "DEP_",
                                              "NombreDepa", "DEPA", "DPTO", "nom_dep", "Departamento"],
     ["COD_DEPTO", "departamentos_id", "DEPARTAMENTO_ID", "depositos"]),
    ("bo/bo_geo.yaml", "bodepartmentcodebyname", ["COD_DEPTO", "cod_depto", "CODDEPTO", "codigo_dep", "CODDEP", "C_DEPTO",
                                                  "cod_departamento"],
     ["DEPTO", "departamento", "id_departamento", "id_departa"]),
    ("bo/bo_geo.yaml", "boprovincebyname", ["PROVINCIA", "Provincia", "NOM_PROV", "nombre_pro", "NombreProv", "prov"],
     ["COD_PROV", "codigo_pro", "proveedor"]),
    ("bo/bo_geo.yaml", "boprovincecodebyname", ["COD_PROV", "cod_prov", "codigo_pro", "C_PROV", "cod_provincia"],
     ["PROVINCIA", "NOM_PROV", "codpro"]),
    ("bo/bo_geo.yaml", "bomunicipalitybyname", ["MUNICIPIO", "Municipio", "MUNI", "MUN_", "NOM_MUN", "nombre_m_1", "NombreMuni",
                                                "nom_mun"],
     ["COD_MUN", "MUNICOD", "municipalidad_id", "comunidad"]),
    ("bo/bo_geo.yaml", "bomunicipalitycodebyname", ["COD_MUN", "cod_mun", "MUNICOD", "codigo_ine", "cod_municipio", "C_MUN"],
     ["MUNICIPIO", "codigo", "cod_com"]),
    ("bo/bo_geo.yaml", "bomunicipalitycodebycodename", ["CODIGO", "Codigo", "codigo", "COD", "code"], ["COD_MUN", "codigos"]),
    ("bo/bo_geo.yaml", "bocommunitycodebyname", ["COD_COM", "cod_com", "cod_comunidad", "cod_localidad", "COD_INE", "cod_loc"],
     ["COMUNIDAD", "cod_mun", "codigo"]),
    ("bo/bo_government.yaml", "bosisincodebyname", ["SISIN", "cod_sisin", "codigo_sisin", "sisin_web"], ["sisinf", "SISTEMA"]),
    ("bo/bo_government.yaml", "bosiecodebyname", ["cod_ue", "codigo_sie", "cod_sie", "rue", "sie", "codigo_ue"],
     ["des_ue_det", "series", "ruedas"]),
    ("common/geo.yaml", "eastingspanishbyname", ["ESTE", "Este", "UTM_ESTE", "utm_este", "coord_este", "coordenada_este", "Coord_X"],
     ["oeste", "estetica", "ESTADO"]),
    ("common/geo.yaml", "northingspanishbyname", ["NORTE", "Norte", "UTM_NORTE", "UTM_NOR", "coordenada_norte", "Coord_Y"],
     ["nortena", "noreste"]),
    ("common/geo.yaml", "utmzonespanishbyname", ["Zona_UTM", "zona_utm", "utm_zona", "huso", "huso_utm"], ["zona", "ZONA"]),
    ("common/geo.yaml", "longitudedmsbyname", ["LONG", "long", "long_dms", "longitud_gms"], ["longitud", "LONGITUD", "lon", "longitude"]),
    ("common/geo.yaml", "pfafstettercodebyname", ["COD_UH", "codigo_uh", "COD_SBC_N5", "pfafstetter", "PFAF_ID", "cod_pfaf",
                                                  "cobacia"],
     ["NIVEL_5", "cod_ue", "uh"]),
    ("common/geo.yaml", "pfafstetterlevelbyname", ["NIVEL_5", "NIVEL3", "nivel5_pfafstetter", "uh_nivel_4"], ["Nivel", "nivel_educativo"]),
    ("common/geo.yaml", "elevationspanishbyname", ["ALTITUD", "altitud", "altitud_msnm", "COTA_COR", "Cota", "msnm"],
     ["altura", "ALTURA_M", "cotas_x"]),
    ("common/observations.yaml", "conductivityspanishbyname", ["ce_us_cm", "conductividad", "conductividad_electrica", "CE (µS/cm)"],
     ["CE", "cedula"]),
    ("common/observations.yaml", "turbidityspanishbyname", ["turbidez", "turbiedad", "turbidez_ntu", "Turb_UNT"], ["turbina"]),
    ("common/observations.yaml", "dissolvedsolidsspanishbyname", ["SDT_mg_L", "solidos_disueltos_totales", "std_mg_l"],
     ["SDT", "std"]),
    ("common/observations.yaml", "suspendedsolidsbyname", ["SST_mg_L", "tss_mg_l", "total_suspended_solids", "solidos_suspendidos_totales"],
     ["SST", "TSS", "sst_c"]),
    ("common/observations.yaml", "biochemicaloxygendemandbyname", ["DBO5_mgO2", "dbo5", "DBO", "bod5", "BOD5_mg_L",
                                                                   "demanda_bioquimica_de_oxigeno"],
     ["dbox", "body"]),
    ("common/observations.yaml", "chemicaloxygendemandbyname", ["DQO_mgO2", "dqo", "cod_mg_l", "chemical_oxygen_demand"],
     ["cod", "COD", "codigo"]),
    ("common/environment.yaml", "dissolvedoxygenspanishbyname", ["oxigeno_disuelto", "OD_mg_L", "od_porc", "OD (%)"], ["od", "OD_"]),
    ("common/values.yaml", "areaspanishbyname", ["SUP_KM2", "Sup_km2", "SUP_HA", "area_has", "Hectares", "hectareas"],
     ["sup", "SUPERVISOR", "area"]),
    ("common/dateandtime.yaml", "yearbygestionname", ["GESTION", "gestion", "gestión", "gestion_fiscal", "año_gestion"],
     ["gestor", "tipo_gestion"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("bo/bo_government.yaml", "bosisincodevalue", ["0287-30477-00000", "086-60061-00000"], ["2873912800000", "0287-30477"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def test_name_rules_of_codes_need_values():
    for path, rule_id, _, _ in FIELDS:
        if rule_id == "areaspanishbyname":
            continue  # areas are told by the unit in the name, as areabyfield
        spec = load(path, rule_id)
        assert spec.get("validator") and spec.get("needs_values") is True, rule_id


def test_bolivian_rule_files_have_the_country():
    for rel in ("bo/bo_geo.yaml", "bo/bo_government.yaml"):
        assert yaml.safe_load((RULES / rel).read_text(encoding="utf-8"))["country_code"] == "bo"
