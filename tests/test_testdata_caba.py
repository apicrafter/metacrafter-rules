"""Rules for the Buenos Aires files of metacrafter-testdata (a 2024 snapshot of data.buenosaires.gob.ar,
the open data portal of the City of Buenos Aires): comunas and barrios, cadastral designations
(sección-manzana-parcela) and property tax accounts, school codes (CUE, CUE-Anexo) and school districts,
Subte lines and stations, districts of the planning code, CUIL numbers, identity document types and
vehicle plates; Spanish days of the week, quarters, opening hours, marital status and surnames; periods
of a year and a month, SAS datetimes, street intersections, house numbers, Plus Codes and OCDS ids.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.ar_country.caba import (
    validate_ar_caba_barrio,
    validate_ar_caba_cadastral_block,
    validate_ar_caba_comuna,
    validate_ar_caba_comuna_name,
    validate_ar_caba_partida,
    validate_ar_caba_school_district,
    validate_ar_caba_school_district_name,
    validate_ar_caba_smp,
    validate_ar_caba_subte_line,
    validate_ar_caba_subte_station,
    validate_ar_caba_zoning_district,
    validate_ar_cue,
    validate_ar_cue_anexo,
    validate_ar_cuil,
    validate_ar_identity_document_type,
    validate_ar_vehicle_plate,
)
from metacrafterext.rules.ar_country.census import validate_ar_department_name
from metacrafterext.rules.common.generic import validate_place_name, validate_state_not_status
from metacrafterext.rules.common.urban import (
    validate_building_number,
    validate_calendar_year,
    validate_plus_code,
    validate_sas_datetime,
    validate_street_intersection,
    validate_street_name,
    validate_street_number_large,
    validate_yearmonth,
    validate_youtube_video_id,
)
from metacrafterext.rules.es.periods import (
    validate_es_dayofweek,
    validate_es_quarter,
    validate_es_year_quarter,
    validate_marital_status,
    validate_opening_hours,
    validate_time_ampm_dotted,
    validate_time_of_day,
)
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (validate_ar_caba_comuna, ["1", "15", "14.0", "15.00000000000", "Comuna 14", "COMUNA 04", "COMUNA 1", "C14", "Comuna N° 3"],
     ["0", "16", "Total", "Total Ciudad", "Recoleta", "Providencia", "1, 2,3", "Comuna 16"]),
    (validate_ar_caba_comuna_name, ["Comuna 14", "COMUNA 04", "comuna 1"], ["14", "C14", "Comuna 16", "Comuna"]),
    (validate_ar_caba_barrio, ["PALERMO", "Villa Crespo", "NUÑEZ", "Nuñez", "Núñez", "VILLA GRAL. MITRE", "Villa General Mitre",
                               "BOCA", "La Boca", "PATERNAL", "Montserrat", "MONSERRAT", "Constitución", "San Nicolás",
                               "FLORESTA - MONTE CASTRO - VELEZ SARSFIELD", "BARRACAS - SAN TELMO - LA BOCA", "Villa del Parque"],
     ["Olivos", "Centro", "Comuna 1", "(Sin Especificar)", "CAPITAL FEDERAL", "Villa 31", "Avellaneda", "12", ""]),
    (validate_ar_caba_smp, ["067-041-003", "067-098-029a", "067-031A-017", "068-116B-000F", "13-060-0000", "42-074-016A",
                            "097-001Ñ-000", "001-025A-002"],
     ["067-041", "2014-01-15", "011-4372-8383", "003-SIN NOMENCLATURA", "20-25218726-0", "abc"]),
    (validate_ar_caba_cadastral_block, ["041-005", "064-094B", "001-046"], ["041-005-012", "11-031", "41-5", "2019-01"]),
    (validate_ar_caba_partida, ["223539", "211685", "98577", "1234567", "223539.0"], ["0", "352", "3.5.2", "30707492011", "abc"]),
    (validate_ar_cue, ["0201845", "201845", "1400123", "0612345", "201845.0"], ["9912345", "20184", "020184500", "abc", "0101845"]),
    (validate_ar_cue_anexo, ["020012301", "20012301", "060123400", "20298400"], ["0200123", "990012301", "2001230", "abc"]),
    (validate_ar_caba_school_district, ["1", "21", "9.000000000000000", "DISTRITO 6", "Distrito Escolar 9", "DE 14", "D.E. 9",
                                        "XIV", "Distrito Escolar XXI"],
     ["0", "22", "Total", "R2a II", "CABA"]),
    (validate_ar_caba_school_district_name, ["DISTRITO 6", "Distrito Escolar 21", "D.E. 14", "DE 9"], ["6", "DISTRITO 22", "UP", "C1"]),
    (validate_ar_caba_subte_line, ["A", "B", "H", "E", "P", "LINEA A", "Línea B", "LINEA_D", "PREMETRO", "Premetro", "Subte H"],
     ["F", "G", "101", "092", "F.C.G.B.M.", "Mitre", ""]),
    (validate_ar_caba_subte_station, ["PLAZA DE MAYO", "Facultad de Medicina", "CONGRESO DE TUCUMAN", "SAENZ PEÑA",
                                      "CALLAO - MAESTRO ALFREDO BRAVO", "PASTEUR - AMIA", "HUMBERTO 1°", "AGÜERO",
                                      "PTE. ILLIA (Lacarra)", "INTENDENTE SAGUIER", "Jose Maria Moreno", "R.SCALABRINI ORTIZ",
                                      "ENTRE RIOS - RODOLFO WALSH", "DE LOS INCAS -PQUE. CHAS"],
     ["Olivos", "Tigre", "Av. Rivadavia 1234", "Estación automática", "001 - Facultad de Derecho", ""]),
    (validate_ar_caba_zoning_district, ["R2a II", "R2aII", "C3 I", "E4 67", "APH 51", "APH  23", "U3 b", "U32", "UP", "UP/APH 2",
                                        "R1b I 4", "R2b III 1", "ARE", "NE", "C1", "P", "I1"],
     ["R5", "CABA", "DISTRITO 6", "CAPITAL FEDERAL", "A", "E5", "12"]),
    (validate_ar_cuil, ["20-25218726-0", "20-00000019-2", "27000000278", "23-00000033-7"],
     ["30-70783660-8", "20-25218726-1", "20252187260000", "abc"]),
    (validate_ar_identity_document_type, ["DNI", "DU", "LE", "LC", "CI", "PAS", "CUIT", "D.N.I.", "Libreta Cívica", "dni"],
     ["NIE", "Resolución", "13800691", "Otro"]),
    (validate_ar_vehicle_plate, ["EOI127", "DGT 763", "AB123CD", "AB 123 CD", "JWI 535 - MCL 595 - FML 627", "bvm203"],
     ["C0631201", "Resto de la Ciudad", "buenosaires.gob.ar", "1234", "ABCD123"]),
    (validate_es_dayofweek, ["lunes", "Miércoles", "MIERCOLES", "SABADO", "Sábado", "domingo"],
     ["enero", "Lunes a Viernes", "feriado", "HABIL", "Juves", "lun"]),
    (validate_es_quarter, ["1", "4", "2.0", "1er trimestre", "SEGUNDO", "PRIMER", "CUARTO", "III", "T4", "3er Trimestre", "Trim 2"],
     ["5", "0", "2019", "2015-01", "3 TRIMESTRE 2019", "semestre"]),
    (validate_es_year_quarter, ["primer_trimestre_2019", "cuarto_trimestre_2021", "3 TRIMESTRE 2019", "2006 - 4to. trim.",
                                "2007 - 1er. trim.", "1er trimestre de 2020", "2019 T3", "T3 2019"],
     ["2019", "2015-01", "trimestre", "SEGUNDO", "2021Q4", "primer semestre 2019"]),
    (validate_time_ampm_dotted, ["10:19:59 a.m.", "03:46:02 p.m.", "8:30 pm", "12:00 AM", "9:05 a. m."],
     ["10:19:59", "13:00 p.m.", "a.m.", "10 a.m."]),
    (validate_time_of_day, ["10:42:00", "8:30", "19.30", "20:00 hs", "03:46 p.m.", "00:00:00", "7h30"],
     ["lunes a viernes de 8 a 20", "24 Horas", "PERIODO", "17", "SALIDA ADELANTADA"]),
    (validate_opening_hours, ["lunes a viernes de 8 a 20", "Lun a vier de 10 a 13.30", "MIERCOLES A DOMINGOS 11:00 - 19:00",
                              "9:00 - 16:00", "24 Horas", "8 a 15 hs", "08:00 HS A 14:00 HS", "lunes a domingo mediodía y noche",
                              "19 A 21 HS", "Martes a Sábado de 11 a 19"],
     ["10:42:00", "SIN DATO", "17", "Mañana", "Consultar"]),
    (validate_marital_status, ["Soltero/a", "Casado/a", "Divorciado/a de matrimonio", "Viudo/a de unión o matrimonio", "Casado",
                               "Separado/a", "Unido/a", "single", "Married", "Widowed"],
     ["Activo", "Vigente", "1", "No corresponde", "Soltería"]),
    (validate_yearmonth, ["201909", "2019-09", "2019/09", "09/2019", "9-2019", "201801.0", "2018_01"],
     ["2019", "201913", "20190915", "2019-9-15", "ene-97", "202201x"]),
    (validate_sas_datetime, ["09DEC2005:00:00:00", "28JUL2022:00:00:00.000000", "31mar2020:23:59:59"],
     ["09DEC2005", "NA:00:00:00.000000", "32DEC2005:00:00:00", "2005-12-09 00:00:00"]),
    (validate_street_intersection, ["DEHEZA@PINTO", "CORDOBA AV. & JUNIN", "Av. San Juan y Chacabuco", "AV. MEXICO-AV. 9 DE JULIO",
                                    "Main St & 2nd Ave", "RUIZ HUIDOBRO@CRAMER", "paz, gral. av. & balbin, ricardo", "LIMA Y BRASIL",
                                    "Paraguay esq. Libertad"],
     ["Av. Córdoba 374", "RIVADAVIA", "info@example.org", "1234", "A&B", "Rojas 1201 entre Antezana y Apolinario Figueroa.",
      "Av. Brasil entre Lima y Salta", "CORRIENTES AV. 1234 y URUGUAY"]),
    (validate_street_name, ["RIVADAVIA AV.", "paz, gral. av.", "9 DE JULIO AV.", "JUSTO, JUAN B. AV.", "O'BRIEN"],
     ["DEHEZA@PINTO", "LIMA Y BRASIL", "CORDOBA AV. & JUNIN", "1234", "X"]),
    (validate_calendar_year, ["2016", "1991", "2016.0"], ["201601", "16", "2016-2017", "primer_trimestre_2019"]),
    (validate_building_number, ["2202", "380", "1550.0", "2100/2110", "S/N", "20"], ["0", "5", "12,5", "1.80", "abc", "123456"]),
    (validate_street_number_large, ["2202", "380", "100", "1550.0"], ["20", "99", "12.5", "S/N", "45000"]),
    (validate_plus_code, ["8FVC9G8F+6W", "48Q3CJ00+", "48Q39G00+", "8fvc9g8f+6w", "8FVC9G8F+"], ["9G8F+6W", "48Q3CJ00", "ABCDEFGH+IJ", "+"]),
    (validate_youtube_video_id, ["Jw7w1musWqs", "Iej0fF9KS-k", "_pVaF5n9efU", "s4q9VS4Dj_Y&feature=youtu.be"],
     ["https://www.youtube.com/watch?v=Jw7w1musWqs", "<iframe title=\\YouTube video player\\\"", "abc", "12345"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


def test_place_name_is_not_a_numbered_division():
    for value in ("Comuna 14", "COMUNA 04", "Distrito 6", "Zona 3", "Sector 12", "Ward 5", "District 9", "Comuna N° 3"):
        assert not validate_place_name(value), value
    for value in ("Palermo", "Villa 31", "San Nicolás", "Providencia", "25 de Mayo", "Colonia 25 de Mayo"):
        assert validate_place_name(value), value


def test_estado_of_statuses_is_no_state():
    for value in ("RENOVADO 2023", "INSCRIPCION VENCIDA", "VACANTE", "Normal", "CLAUSURADA", "Usado", "A estrenar", "1",
                  "Disponible", "COVID-19 - Paralizada - 2021", "LEY FIRME", "Proyectado", "INSTALADO"):
        assert not validate_state_not_status(value), value
    for value in ("SP", "Jalisco", "Rio de Janeiro", "Nuevo León", "Minas Gerais", "Baja California", "Baja California Sur"):
        assert validate_state_not_status(value), value


def test_apartment_letter_is_no_department():
    for value in ("A", "B", "C", "2"):
        assert not validate_ar_department_name(value), value
    for value in ("Calamuchita", "RIO CUARTO", "Pte. Roque S. Peña", "Comuna 1"):
        assert validate_ar_department_name(value), value


FIELDS = [
    ("ar_country/ar_caba.yaml", "arcabacomunabyname", ["comuna", "COMUNA", "Comuna", "comunas", "domicilio_comuna", "comuna_normalizada",
                                                      "domicilio_cgpc"],
     ["comunidad", "comunal", "id_comuna_x_y_z_w"]),
    ("ar_country/ar_caba.yaml", "arcababarriobyname", ["barrio", "BARRIO", "barrios", "domicilio_barrio", "barrio_normalizado", "zona",
                                                      "sector"],
     ["barrido", "zonas", "subsector"]),
    ("ar_country/ar_caba.yaml", "arcabasmpbyname", ["smp", "SMP", "smp1", "seccion_manzana_parcela", "nomenclatura"], ["sm", "smpx", "parcela"]),
    ("ar_country/ar_caba.yaml", "arcabacadastralblockbyname", ["sm", "SM", "codigo_man"], ["smp", "manzana"]),
    ("ar_country/ar_caba.yaml", "arcabapartidabyname", ["partida", "PARTIDA", "partida_matriz", "nro_partida"], ["partido", "partidas", "contrapartida"]),
    ("ar_country/ar_caba.yaml", "arcuebyname", ["cue", "CUE", "codigo_cue", "cue_id"], ["cueanexo", "cuenta", "cuerpo", "cui"]),
    ("ar_country/ar_caba.yaml", "arcueanexobyname", ["cueanexo", "CUEANEXO", "cue_anexo", "CUE_ANEXO"], ["cue", "anexo"]),
    ("ar_country/ar_caba.yaml", "arcabaschooldistrictbyname", ["de", "DE", "distrito_e", "distrito_escolar", "dist_esc"],
     ["distrito", "desde", "dep"]),
    ("ar_country/ar_caba.yaml", "arcabaschooldistrictbydistrito", ["distrito", "DISTRITO"], ["distrito_1", "distritos"]),
    ("ar_country/ar_caba.yaml", "arcabasubtelinebyname", ["linea", "LINEA", "lineasub", "lineas_de_", "fr1_linea", "linea_subte", "línea"],
     ["lineal", "linea_2x", "alineacion"]),
    ("ar_country/ar_caba.yaml", "arcabasubtestationbyname", ["estacion", "ESTACION", "nombre_estacion", "estación"],
     ["estacionamiento", "domicilio_estacion", "horario_estacion"]),
    ("ar_country/ar_caba.yaml", "arcabazoningdistrictbyname", ["distrito", "DISTRITO", "distrito_1", "DISTRITO_4", "distrito_c", "zonificacion"],
     ["distritos", "distrito_escolar", "dist_1_grp"]),
    ("ar_country/ar_caba.yaml", "arcuilbyname", ["cuil", "CUIL", "cuil_beneficiario", "nro_cuil"], ["cuit", "cuilx"]),
    ("ar_country/ar_caba.yaml", "aridentitydocumenttypebyname", ["tipo_documento", "tipo_doc", "TipoDoc", "tipo_de_documento"],
     ["tipo", "numero_documento", "documento"]),
    ("ar_country/ar_caba.yaml", "arvehicleplatebyname", ["dominio", "DOMINIO", "patente", "nro_dominio", "dominio_vehiculo"],
     ["predominio", "patentes_industriales_x"]),
    ("es/es_datetime.yaml", "esquarterbyname", ["trimestre", "TRIMESTRE", "trim", "trimestre_"], ["cuatrimestre", "semestre", "año_trimestre"]),
    ("es/es_datetime.yaml", "esopeninghoursbyname", ["horario", "horarios", "horario_de_atencion", "horario de atencion", "dias y horario",
                                                    "horario_at", "horario_cursada", "dia_hora"],
     ["hora", "horario_hasta", "horas"]),
    ("es/es_datetime.yaml", "eshorariotimebyname", ["horario", "HORARIO"], ["horarios", "hora"]),
    ("es/es_geo.yaml", "esstreetnamebyname", ["calle2", "calle_cruce", "cruce", "calle_1", "calles", "nomoficial", "entre_calle", "y_calle",
                                             "1_calle", "calle_normalizada"],
     ["calle", "calle_altura", "callejero"]),
    ("es/es_geo.yaml", "esbuildingnumberbyname", ["calle_altura", "domicilio_altura", "calle_nro", "numero_puerta"], ["altura", "altura_maxima"]),
    ("es/es_geo.yaml", "esalturabuildingnumber", ["altura", "ALTURA"], ["altura_maxima", "alturas"]),
    ("es/es_persons.yaml", "essurnamebyname", ["apellido", "APELLIDOS", "primer_apellido", "funcionario_apellido", "apellido_paterno"],
     ["apellido_y_nombre", "nombre_apellido", "nombre"]),
    ("es/es_persons.yaml", "esfullnamebyname", ["apellido_y_nombre", "nombre_y_apellido", "nombre y apellido", "ayn",
                                               "profesional_nombre_apellido", "apellidos_y_nombres"],
     ["apellido", "nombre"]),
    ("pii/pii.yaml", "maritalstatusbyname", ["estado_civil", "estado_civil_1", "marital_status", "situacion_conyugal", "ESTADO CIVIL"],
     ["estado", "civil"]),
    ("pii/pii.yaml", "nationalitybyspanishname", ["nacionalidad", "NACIONALIDAD", "madre_nacionalidad"], ["nacional", "nacion"]),
    ("common/periods.yaml", "yearmonthbyname", ["periodo", "PERIODO", "período", "anio_mes", "mes_anio", "year_month", "yyyymm"],
     ["periodicidad", "mes", "anio"]),
    ("common/periods.yaml", "yearbyperiodoname", ["periodo", "PERIODO", "período"], ["periodicidad", "periodo_fiscal"]),
    ("common/geo.yaml", "longitudebylongname", ["long", "LONG", "x_long", "long_x"], ["longitud_tramo", "longueur", "lon"]),
    ("common/geo.yaml", "streetintersectionbyname", ["cruce", "interseccion", "intersecci", "esquina", "intersection", "cross_streets",
                                                    "calle_cruce", "ubicacion", "Ubicación"],
     ["cruz", "sections"]),
    ("common/media.yaml", "youtubevideoidbyname", ["id_youtube", "youtube_id", "youtubeId", "id_video_youtube"], ["youtube", "id"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("ar_country/ar_caba.yaml", "arcabacomunavalue", ["Comuna 14", "COMUNA 04"], ["14", "Comuna 16"]),
    ("es/es_datetime.yaml", "esdayofweekvalue", ["lunes", "MIERCOLES", "Sábado"], ["enero", "lun"]),
    ("es/es_datetime.yaml", "esyearquartervalue", ["primer_trimestre_2019", "3 TRIMESTRE 2019"], ["2019", "SEGUNDO"]),
    ("es/es_datetime.yaml", "estimeampmvalue", ["10:19:59 a.m.", "03:46:02 p.m."], ["10:19:59"]),
    ("common/dateandtime.yaml", "sasdatetimevalue", ["09DEC2005:00:00:00", "28JUL2022:00:00:00.000000"], ["09DEC2005"]),
    ("common/geo.yaml", "pluscodevalue", ["8FVC9G8F+6W", "48Q3CJ00+"], ["9G8F+6W"]),
    ("common/procurement.yaml", "ocdsocidvalue", ["ocds-bulbcf-101-0014-CDI19-1", "ocds-213czf-000-00001"],
     ["ocds-bulbcf", "spr-101-0028-OCA18", "OCDS-BULBCF-101"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def test_new_field_rules_need_values():
    for path, rule_id, _, _ in FIELDS:
        spec = load(path, rule_id)
        assert spec.get("validator") and spec.get("needs_values") is True, rule_id


def test_horario_is_not_a_time_by_name_alone():
    # horario holds opening hours as often as a time: the Portuguese name list no longer has it.
    assert not field_matches("pt/pt_datetime.yaml", "pttimeknown", "horario")
    assert field_matches("pt/pt_datetime.yaml", "pttimeknown", "hora")
    # hora of hour numbers (HORA: 9) or of datetimes (31MAR2020:15:00:00) is no time of day
    spec = load("pt/pt_datetime.yaml", "pttimeknown")
    assert spec["validator"].endswith("validate_time_of_day") and spec["needs_values"] is True
    for value in ("9", "17", "31MAR2020:15:00:00"):
        assert not validate_time_of_day(value), value


def test_more_argentine_field_names():
    assert field_matches("ar_country/ar_geo.yaml", "arpostcodebyname", "codpost")
    assert field_matches("ar_country/ar_geo.yaml", "arpostcodebyname", "cod_postal")
    for name in ("direccion_normalizada", "DIRECCION_NORMALIZADA", "dom_norma", "DOM_GEO", "dom_edific", "dom_establ", "direccion_norm"):
        assert field_matches("es/es_geo.yaml", "esstreetaddressbyname", name), name
    assert not field_matches("es/es_geo.yaml", "esstreetaddressbyname", "dominio")
