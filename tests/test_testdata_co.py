"""Rules for the Colombian files of metacrafter-testdata (a May 2024 snapshot of Datos Abiertos Colombia,
www.datos.gov.co, Dateno source cdi00000385, which also lists the tables of the Cundinamarca map portal, the
ICDE, the CAR, the city of Cali and Postdata): departments by name and DIVIPOLA code, municipality codes,
comunas, corregimientos and veredas, the socioeconomic stratum, vehicle plates, the matrícula inmobiliaria and
the national parcel number, Sisbén IV groups, identity document types, health insurance regimes, CIIU classes,
DANE school codes and the NIT; and the small vocabularies of registers: school shifts, hazard and risk levels,
the medium of a record, languages by Spanish name and budget years.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.co.codes import (
    validate_co_ciiu,
    validate_co_ciiu_titled,
    validate_co_comuna,
    validate_co_comuna_name,
    validate_co_department,
    validate_co_department_code,
    validate_co_divipola,
    validate_co_estrato,
    validate_co_health_regime,
    validate_co_identity_document_type,
    validate_co_matricula_inmobiliaria,
    validate_co_nit,
    validate_co_place_name,
    validate_co_predial_number,
    validate_co_school_dane_code,
    validate_co_sisben_group,
    validate_co_vehicle_plate,
)
from metacrafterext.rules.common.directories import validate_attendance_mode
from metacrafterext.rules.common.generic import validate_place_name
from metacrafterext.rules.common.registers import (
    validate_budget_year,
    validate_language_name_es,
    validate_record_medium,
    validate_risk_level,
    validate_school_shift,
)
from tests.test_testdata_baseline import field_matches, load

VALIDATORS = [
    (validate_co_department, ["ANTIOQUIA", "Valle del Cauca", "Bogotá, D.C.", "BOGOTÁ D.C.", "Bogotá D.C", "Nariño", "QUINDIO",
                              "Norte de Santander", "San Andrés", "Boyaca", "LA GUAJIRA"],
     ["Medellín", "ARMENIA", "SIN DEPTO", "25", "Buenos Aires", "La Paz", ""]),
    (validate_co_department_code, ["05", "5", "25", "76", "99", "25.0", "11", "88"], ["12", "0", "100", "05001", "99999", "AN", ""]),
    (validate_co_divipola, ["05001", "5001", "76001", "25488", "11001", "66170", "76001.0", "5480"],
     ["12001", "095", "25000", "17380000", "1", "743", ""]),
    (validate_co_comuna, ["4", "21", "22", "21.0", "Comuna 5", "COMUNA 11", "17. MUTIS", "01. NORTE", "SEIS", "Comuna No. 3"],
     ["0", "62", "23", "110332", "482.9", "FUERA DE CALI", "Atardeceres", "ALTO DEL NUDO", ""]),
    (validate_co_place_name, ["El Diamante", "CHORRO CLARO", "Popoa Sur", "La Habana", "Zanjón Hondo", "LA UNION2"],
     ["45", "80", "No aplica", "N/A", "25-001", ""]),
    (validate_co_estrato, ["1", "6", "3.0", "ESTRATO 2", "Estrato 3", "ESTRATO 1.0"], ["0", "7", "8", "99", "Rural", "01-02", ""]),
    (validate_co_vehicle_plate, ["EYY-710", "AGH260", "MRM02C", "VBN90", "636ADX", "636adx", "nww41a", "AB1234", "R12345", "CAN 732"],
     ["SIN DATO", "AB12CD", "12345", "ABCD123", "EYY-7100", ""]),
    (validate_co_matricula_inmobiliaria, ["001-948136", "294-25763", "440-58428", "060-26027", "001 - 1207172"],
     ["948136", "NO TIENE", "01-02-0218-0001-000", "119559", "2021-05", ""]),
    (validate_co_predial_number, ["700010101000006900002000000000", "760010100021100220001500000001", "70001010100690002000"],
     ["000100010005000", "120010101000006900002000000000", "7000101010000069000020000000", "01-02-0218-0001-000", ""]),
    (validate_co_sisben_group, ["A1", "A5", "B4", "B7", "C18", "D21", "b3"], ["A6", "B8", "C19", "D22", "E1", "45.3", "Nivel 1", ""]),
    (validate_co_identity_document_type, ["CC", "TI", "RC", "CE", "C.C.", "T.I", "T.I.", "NIT", "NI", "PEP", "PPT", "CN", "Cédula de ciudadanía",
                                          "Tarjeta de identidad", "REGISTRO CIVIL", "Certificado de Nacido Vivo",
                                          "CERTIFICADO NACIDO VIVO"],
     ["DNI", "LE", "1", "Escritura Publica", "Resolución", "Libro", "CD", "DVD", ""]),
    (validate_co_comuna_name, ["Comuna 5", "COMUNA 11", "Comuna No. 3", "comuna 22"], ["5", "Comuna 23", "Comuna Norte", "COMUNA", ""]),
    (validate_co_health_regime, ["CONTRIBUTIVO", "Subsidiado", "EXCEPCIÓN", "Especial", "VINCULADO", "NO ASEGURADO", "PARTICULAR", "Otro"],
     ["Ley 756 8% variable", "Ley 141 20%", "SOAT-ECAT", "NUEVA EPS", "Común", ""]),
    (validate_co_ciiu, ["4711", "0112", "G4512", "A0112", "A0112 ** Cultivo de arroz", "G4512 ** Comercio de vehiculos automotores usados",
                        "4711.0"],
     ["G45", "47", "12345", "A. AGRICULTURA, GANADERÍA, CAZA", "Comercio", ""]),
    (validate_co_ciiu_titled, ["F4111 ** Construccion de edificios residenciales", "G4512 ** Comercio de vehiculos automotores usados"],
     ["4111", "F4111", "F4111 - Construccion", "A. AGRICULTURA", ""]),
    (validate_co_school_dane_code, ["176001004973", "266170000803", "205579800021", "276001022232", "108558000088"],
     ["076001004973", "512001000001", "112001000001", "0", "17600100497", "1760010049731", ""]),
    (validate_co_nit, ["890201725", "9014071116", "901603677-2", "890.201.725-4", "823004006", "830122566.0"],
     ["0", "NO APLICA", "315 5455973", "12345", "8", ""]),
    (validate_school_shift, ["DIURNA", "Nocturna", "Mañana", "TARDE", "Fin de semana", "COMPLETA", "DIURNA - NOCTURA", "MIXTA", "Única",
                             "Jornada Mañana", "Noturno", "Matutino", "Morning", "Otra"],
     ["8", "Presencial", "Lunes a viernes de 8 a 12", "PREGRADO", ""]),
    (validate_risk_level, ["Alta", "MEDIA", "Baja", "Muy Alta", "Muy Bajo", "Medio", "Alto", "Vulnerabilidad Media", "Amenaza Baja",
                           "Amenaza  Media", "Media - Alta", "Low", "Moderate", "Very high", "Sin amenaza"],
     ["0.5625", "3", "Sin Erosión", "Laminar", "Zona Residencial", "No apta", ""]),
    (validate_record_medium, ["Físico", "ELECTRONICO", "Digital", "Físico / Electrónico", "Físico/Digital", "Digital-Electrónico",
                              "Análogo", "Papel", "PAPEL Y DIGITAL", "Papel(Digital)", "FISICO/ELECTRONICO", "Internet", "Paper"],
     ["Carpetas - servidor", "PDF", "X", "Excel - servidor", "Documentos de Archivo-Electronicos", ""]),
    (validate_language_name_es, ["Español", "ESPAÑOL", "Castellano", "Inglés", "Español - Ingles", "Español  y Lenguaje de Señas (LSC)",
                                 "Español/Inglés", "N/A"],
     ["PDF", "Colombia", "3", "Documento de texto", ""]),
    (validate_budget_year, ["2021", "2019", "2019.0", "1998"], ["0", "2019-1", "2023-12-29T00:00:00.000", "No Aplica", "20210", ""]),
    # a comuna numbered before its name is not the name of a city
    (validate_place_name, ["Bucaramanga", "San José de Cúcuta", "La Dorada"], ["17. MUTIS", "01. NORTE", "Comuna 5", "CO"]),
    # the Universidad del Quindío writes DISTANCIA TRADICIONAL beside DISTANCIA VIRTUAL
    (validate_attendance_mode, ["DISTANCIA TRADICIONAL", "DISTANCIA VIRTUAL", "PRESENCIAL"], ["TRADICIONAL", "PREGRADO"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ + str(i) for i, v in enumerate(VALIDATORS)])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("co/co_geo.yaml", "codepartmentbyname", ["DEPARTAMENTO", "Departamento", "DEPARTAMEN", "depto", "DESC_DEPARTAMENTO", "Depa_Resi",
                                             "Departamento de residencia", "Departamento del hecho DANE", "nombre_departamento",
                                             "DEPA_PRO_COLEGIO"],
     ["COD_DEPTO", "ID_DEPARTAMENTO", "Código departamento", "Dependencia", "deporte"]),
    ("co/co_geo.yaml", "codepartmentcodebyname", ["Código departamento", "Código Departamento", "COD_DEPTO", "COD_DEPART", "Cod_Depto",
                                                 "CodigoDaneDepartamento", "ID_DEPARTAMENTO", "depa_codigo", "cod_dane_departamento"],
     ["DEPARTAMENTO", "Código Dependencia", "DESC_DEPARTAMENTO", "COD_MUNI"]),
    ("co/co_geo.yaml", "codivipolabyname", ["Cod_Municipio", "Código municipio", "CodigoDaneMunicipio", "ID_MUNICIPIO", "muni_codigo", "CODDANE",
                                           "COD_MUNI", "codigo_mun", "Código DANE de Municipio", "CODIGO_DANE", "divipola", "cod_mpio"],
     ["MUNICIPIO", "DESC_MUNICIPIO", "CodigoDane_EE", "COD_DEPTO", "CODIGO_DANE_SEDE"]),
    ("co/co_geo.yaml", "cocomunabyname", ["comuna", "COMUNA", "Comuna", "Comuna/Corregimiento", "identificador comuna o corregimiento",
                                         "COMUNA O CORREGIMIENTO", "nombre_comuna"],
     ["comunidad", "comunicado", "Corregimiento"]),
    ("co/co_geo.yaml", "cocorregimientobyname", ["Corregimiento", "CORREGIMIENTO", "Nombre Corregimiento", "nombre_corregimiento"],
     ["Código Corregimiento", "Comuna/Corregimiento", "corregidor"]),
    ("co/co_geo.yaml", "coveredabyname", ["VEREDA", "vereda", "nombre_vereda", "NOM_VEREDA", "veredas"], ["idveredas", "Código Vereda", "VEREDA/MUNICIPIO"]),
    ("co/co_codes.yaml", "coestratobyname", ["ESTRATO", "Estrato", "estrato", "ESTRATO_ALCALDIA", "estrato_socioeconomico", "ESTU_ESTRATO",
                                            "ACUEDUCTO-ESTRATO"],
     ["TIPO_ESTRATIFICACION", "estratificacion", "sustrato"]),
    ("co/co_codes.yaml", "cosisbengroupbyname", ["SISBEN", "sisben", "grupo_sisben", "Clasificación Sisbén", "Sisbén IV", "nivel_sisben"],
     ["puntaje_sisben", "ficha_sisben"]),
    ("co/co_codes.yaml", "coidentitydocumenttypebyname", ["TIPODOC", "tipo_doc", "Tipo de identificación", "TIPO IDENTIFICACIÓN",
                                                         "TIPO DE IDENTIFICACIÓN PERSONA VALORADA", "tipo_documento", "TIPO ID", "TIP_DOC",
                                                         "Tipo Documento"],
     ["Tipo documental", "numero_documento", "TIPO"]),
    ("co/co_codes.yaml", "cohealthregimebyname", ["REGIMEN", "Régimen", "Regimen", "Regimen Seguridad Social", "tipo_regimen", "RÉGIMEN DE SALUD"],
     ["Regimen Reg", "RegimenReg", "regimen_tributario"]),
    ("co/co_codes.yaml", "covehicleplatebyname", ["PLACA", "Placa", "placa", "placa_vehiculo", "Placa de la Moto", "numero_placa", "placas"],
     ["num_plaqueta", "placa_inventario", "Plancha"]),
    ("co/co_codes.yaml", "comatriculainmobiliariabyname", ["Matricula Inmobiliaria", "matricula inmobiliaria", "MATRICULA", "folio_matricula",
                                                          "Folio de Matrícula Inmobiliaria", "FMI"],
     ["EST-MATRICULA", "fecha matricula", "matriculados"]),
    ("co/co_codes.yaml", "copredialnumberbyname", ["NPN", "NPN_INFO_PRED_CAT", "numero_predial", "Número Predial Nacional", "Cedula Catastral",
                                                  "codigo_predial", "ficha catastral"],
     ["numero_del_predio", "PREDIAL_UTILIZADO", "DESTINO_PREDIAL", "DIRECCION_CATASTRAL"]),
    ("co/co_codes.yaml", "cociiubyname", ["CIIU", "ciiu", "CIIU-1", "CIIU-4", "Cod_CIIU Rev 4", "CLASIFICACION CIIU", "codigo_ciiu", "ciiu_principal"],
     ["ciudad", "ACTIVIDAD ECONÓMICA Y CIIU DETALLADO", "descripcion_ciiu_texto_largo_de_actividad"]),
    ("co/co_codes.yaml", "conitbyname", ["NIT", "Nit", "nit", "NIT ENTIDAD", "nit_proveedor", "ACUEDUCTO-NIT", "N.I.T.", "NIT ENTIDAD AUTORIZADO"],
     ["unit", "UNITS", "nitrato", "ACUEDUCTO-DV"]),
    ("co/co_codes.yaml", "coschooldanecodebyname", ["CODIGO_DANE_SEDE", "CodigoDane_EE", "CodigoSede_EE", "codigo_dane", "Código DANE", "codigo",
                                                   "Código", "dane_sede"],
     ["CodigoDaneMunicipio", "CodigoSecretaria", "Sede_ID", "codigo_habilitacion"]),
    ("common/registers.yaml", "schoolshiftbyname", ["jornada", "JORNADA", "Jornada", "jornada_academica", "turno", "school_shift", "EST_JORNADA"],
     ["jornadas_trabajadas_total", "jornal", "turnover"]),
    ("common/registers.yaml", "risklevelbyname", ["AMENAZA", "Amenaza", "RIESGO", "Riesgo", "VULNERABILIDAD", "Vulnerabil", "TORRENCIAL",
                                                 "CAT_VULNER", "Cat_F_Soci", "CAT_F_TOTA", "CAT_FRA_FI", "CAT_RESILI", "Amenaza_to", "IND_VULNER",
                                                 "hazard_level", "risk_level", "Riesgo_Tor"],
     ["CAT_PEND", "CAT_COMP", "CATEGORIA", "Confidencialidad", "FID_Amenaz"]),
    ("common/registers.yaml", "recordmediumbyname", ["Medio de conservación y/o soporte", "MEDIO DE CONSERVACION O SOPORTE", "Medio de conservación",
                                                    "medio_soporte", "Soporte", "Medio de conservación y/o soporte:",
                                                    "Documento(Papel o Digital)", "record_medium"],
     ["Formato", "Medio", "soporte_tecnico_telefono"]),
    ("common/registers.yaml", "languagenamebyspanishname", ["Idioma", "IDIOMA", "idioma", "idiomas", "idioma_original", "lengua"],
     ["NGIdioma_cod", "idiomas_count"]),
    ("common/registers.yaml", "budgetyearbyname", ["VIGENCIA", "Vigencia", "vigencia", "vigencia_fiscal", "año_vigencia"],
     ["vigencia_actual_acuerdo_pu", "fecha_vigencia", "vigente"]),
    ("common/directories.yaml", "attendancemodebyname", ["METODOLOGIA", "Metodología", "modalidad"], ["metodo", "Metodología de cálculo"]),
    ("common/directories.yaml", "educationlevelbyname", ["FORMACION_ACADEMICA", "Formación Académica", "Escolaridad", "NIVEL DE FORMACION"],
     ["FORMACION", "formacion_continua"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_names(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


def test_guarded_value_rules():
    """A plate has the shape of many short codes: the value rule runs only in fields named for plates. The
    30-digit parcel number that starts with a municipality code needs no guard."""
    assert load("co/co_codes.yaml", "covehicleplatevalue")["fieldregex"]
    assert load("co/co_geo.yaml", "cocomunavalue")["fieldregex"]
    spec = load("co/co_codes.yaml", "copredialnumbervalue")
    assert spec["minlen"] == spec["maxlen"] == 30 and "fieldregex" not in spec
