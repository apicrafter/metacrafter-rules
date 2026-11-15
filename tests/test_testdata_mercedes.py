"""Rules for the Mercedes files of metacrafter-testdata (datosabiertos.mercedes.gob.ar, the open data portal
of the municipality of Mercedes, Buenos Aires: a 2024 snapshot and the portal of 2026): the school
designations of Buenos Aires Province (EP Nº 1, JARDÍN 901) and the DIPREGEP numbers of private schools,
municipal tender numbers (LPub Nº 03/2018), vehicle types and Spanish engine and chassis fields, medical
specialties, the common names of street trees; Spanish field names for heads in office, job titles,
makes, model years, budgets, landlines and departments.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.ar_country.pba import (
    validate_ar_licitacion_number,
    validate_ar_pba_dipregep_number,
    validate_ar_pba_school_service,
    validate_ar_pba_school_service_value,
)
from metacrafterext.rules.common.directories import validate_phone_digits
from metacrafterext.rules.common.vehicles import validate_engine_or_chassis_number, validate_vehicle_type
from metacrafterext.rules.es.vocab import validate_es_tree_name, validate_es_tree_name_value, validate_medical_specialty
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (validate_ar_pba_school_service,
     ["EP Nº 1", "EP Nº3", "E.S Nº1 MEDIANº1", "E.S Nº3 NACIONAL", "E.E.S Nº8", "E.S Nº9 (EPNº12)", "E.S nª14 (EPNº1)", "EET Nº1 ",
      "EESA Nº1", "CEPT Nº4", "CEA Nº9", "CFP Nº 401", "JIRMM Nº1", "JARDÍN 901", "CEC Nº801", "CEF N° 193", "EEE Nº503",
      "NORMAL ISFD Nº137", "I.S.F.D.YT. N° 7", "CATDI Nº1", "JARDIN DE INFANTES N° 905", "EP 12"],
     ["SAD", "JEF. REGIONAL", "CONSEJO ESCOLAR", "CFL", "EEE", "CONS. DE MÚSICA", "E de ARTE", "Escuela N° 12 D.E. 5", "EP 0",
      "EPA Nº 1", "Jardín", ""]),
    (validate_ar_pba_school_service_value, ["EP Nº 1", "E.S. N° 7", "CEF N° 193", "JARDÍN 901", "JIRMM Nº1"],
     ["EP 12", "ES 2019", "CFP 401", "Escuela N° 12"]),
    (validate_ar_pba_dipregep_number, ["1750", "374", "9003", "5052.0"], ["0", "604988", "S/N", "", "12345"]),
    (validate_ar_licitacion_number,
     ["LPub Nº 03/2018", "Lpriv Nº 29/2018", "Licitación Pública N° 12/2021", "LICITACION PRIVADA Nº 45/19",
      "Concurso de Precios N° 3/2019", "Contratación Directa N° 45/20", "LP 5/2020", "LPub Nº 14/2018"],
     ["452-0001-LPU17", "12/2021", "Licitación Pública", "LPub Nº 0/2018", "CP 7/1890", "Lpub 2018", "Expediente 1332/2018"]),
    (validate_vehicle_type, ["Automóvil", "Pick Up", "Camioneta", "Camión", "Motoniveladora", "Motonivelad.", "Tractor", "Truck",
                             "Motorcycle", "Retroexcavadora"],
     ["Rail", "Toyota Hilux", "Ferry", "DOD 711", "2011", "Motonivela", ""]),
    (validate_engine_or_chassis_number, ["10DXBA0003019", "2KD-5369584", "9BFFF25G6YD036053", "BF6L913            Serie 703481",
                                         "30627914.0", "160HB.Serie 31118"],
     ["2000", "123", "Diesel", "S/N", ""]),
    (validate_medical_specialty, ["CARDIOLOGÍA", "CLÍNICA MÉDICA", "Pediatría", "KINESIOLOGIA", "OFTALMOLOGÍA", "Cardiology"],
     ["LABORATORIO", "VACUNAS", "Técnico", "DRA. PITARO, ANA", "Bachiller", ""]),
    (validate_es_tree_name, ["Fresno Americano", "Plátano", "Pl�tano", "S�fora", "Ligustro Variegado", "Acacia Bola",
                             "Ciruelo de Jardin", "Paraíso", "Limpia Tubo", "Jacarandá"],
     ["Otros", "-------------", "tio", "t�o", "Fraxinus pennsylvanica", "Av. Rivadavia"]),
    (validate_es_tree_name_value, ["Fresno Americano", "Plátano", "Ligustro Variegado"], ["Paraíso", "Sauce", "Álamo", "Roble"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


def test_landlines_of_the_school_lists():
    for value in ("423384", "426044/430410", "02324-426288", "15415879"):
        assert validate_phone_digits(value), value


FIELDS = [
    ("ar_country/ar_pba.yaml", "arpbaschoolservicebyname", ["SERV. EDUC", "SERV\\. EDUC", "servicio_educativo", "Servicio educativo",
                                                         "escuela", "establecimiento", "nombre_escuela"],
     ["servicio", "educacion_fisica", "escuelas_cantidad"]),
    ("ar_country/ar_pba.yaml", "arpbadipregepbyname", ["N° Diepregep", "dipregep", "DIPREGEP", "nro_dipregep", "diegep", "numero diegep"],
     ["dipreg", "gep"]),
    ("ar_country/ar_pba.yaml", "arlicitacionnumberbyname", ["Licitación", "licitacion", "nro_licitacion", "numero_de_licitacion",
                                                         "licitacion_nro", "N° Licitación"],
     ["tipo_licitacion", "licitaciones_desiertas", "fecha_licitacion"]),
    ("common/vehicles.yaml", "vehicletypebyname", ["Vehículo", "vehiculo", "tipo_vehiculo", "tipo de vehículo", "vehicle_type",
                                                   "Vehicle Type", "VEHICLE TYPE CODE 1", "body_type", "clase_vehiculo"],
     ["vehiculos_cantidad", "patente_vehiculo", "vehicle_id"]),
    ("common/vehicles.yaml", "esenginenumberbyname", ["Motor Nro.", "Motor Nro\\.", "nro_motor", "numero_de_motor", "N° motor"],
     ["motor", "motorizacion"]),
    ("common/vehicles.yaml", "eschassisnumberbyname", ["Chasis Nro.", "Chasis Nro\\.", "nro_chasis", "numero_de_chasis", "chasis",
                                                       "bastidor"],
     ["chasis_tipo"]),
    ("es/es_med.yaml", "esmedicalspecialtybyname", ["especialidad", "ESPECIALIDAD", "especialidad_medica", "especialidades",
                                                   "specialty", "medical_specialty"],
     ["especial", "especialidad_x_y"]),
    ("es/es_common.yaml", "estreespeciesbyname", ["especie", "ESPECIE", "nombre_comun", "nombre común", "nombre_vulgar", "especie_arborea"],
     ["especies_cantidad", "nombre"]),
    ("es/es_common.yaml", "esphonebyname", ["TEL FIJO", "tel_fijo", "tel. fijo", "tel celular", "telefono_fijo", "Teléfono"],
     ["telar", "tele"]),
    ("es/es_common.yaml", "esbrandbyname", ["marca", "Marca", "MARCA", "marca_vehiculo", "marca comercial"], ["marcador", "marcas_x"]),
    ("es/es_common.yaml", "esmodelyearbyname", ["modelo", "Modelo", "año_modelo", "anio_modelo"], ["modelo_vehiculo", "modelado"]),
    ("es/es_persons.yaml", "esofficialfullnamebyname", ["DIRECTIVO", "directivo", "director", "Directora", "PROFESIONAL", "presidente",
                                                       "RESPONSABLE", "responsable", "coordinadora"],
     ["titular", "direccion", "profesionales_cantidad"]),
    ("es/es_persons.yaml", "esjobtitlebyname", ["Puesto", "puesto_de_trabajo", "puestos_solicitados", "cargo", "ocupación"],
     ["puestos_x", "cargos_fijos"]),
    ("common/values.yaml", "moneyamountbyfield", ["Presupuesto Oficial o adjudicado", "PRESUPUESTO TOTAL IVA INC.", "presupuesto",
                                                  "monto"],
     ["presupuestario"]),
    ("common/orgs.yaml", "orgunitbyname", ["SECRETARIAS", "secretaria", "Subsecretaría", "Area Solicitante", "área responsable"],
     ["secretario", "area"]),
    ("common/directories.yaml", "legislationnumberbyname", ["Decreto", "decreto", "Nº DECRETO", "nro_decreto"], ["decretado"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


def test_new_field_rules_need_values():
    for path, rule_id, _, _ in FIELDS:
        spec = load(path, rule_id)
        if rule_id == "moneyamountbyfield":
            continue  # an amount field of an older rule, without a validator
        assert spec.get("validator") and spec.get("needs_values") is True, rule_id


VALUES = [
    ("ar_country/ar_pba.yaml", "arpbaschoolservicevalue", ["EP Nº 1", "E.S. N° 7", "JARDÍN 901"], ["EP 12", "CFL"]),
    ("ar_country/ar_pba.yaml", "arlicitacionnumbervalue", ["LPub Nº 03/2018", "Licitación Pública N° 12/2021"], ["12/2021"]),
    ("es/es_med.yaml", "esmedicalspecialtyvalue", ["CARDIOLOGÍA", "Clínica Médica"], ["LABORATORIO", "Lunes"]),
    ("es/es_common.yaml", "estreespeciesvalue", ["Fresno Americano", "Plátano"], ["Paraíso", "Otros"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value
