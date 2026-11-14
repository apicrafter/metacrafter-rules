"""Rules for the datos.cultura.gob.ar files of metacrafter-testdata (an April 2024 snapshot of the open
data portal of the Argentine culture ministry): the cultural directories of the Mapa Cultural (radio
stations, cinemas, festivals, national monuments, university degrees, UNESCO sites) and the national
survey of cultural consumption (ENCC). Broadcast frequencies, geocoding precision, public or private
management, attendance mode, periodicity, levels of education, socioeconomic levels, legal acts,
Argentine regions, heritage categories and CONABIP numbers; Spanish names of years, months, phones,
addresses, floors, genders and survey weights; Spanish yes / no.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest
import yaml

from metacrafterext.rules.ar_country.codes import (
    validate_ar_conabip_number,
    validate_ar_heritage_category,
    validate_ar_region,
)
from metacrafterext.rules.common.directories import (
    validate_attendance_mode,
    validate_degree_title,
    validate_education_level,
    validate_es_month,
    validate_floor,
    validate_gender_word,
    validate_geocoding_precision,
    validate_geocoding_precision_strong,
    validate_legislation_number,
    validate_legislation_type,
    validate_ownership_type,
    validate_periodicity,
    validate_phone_digits,
    validate_radio_frequency,
    validate_radio_frequency_marked,
    validate_socioeconomic_level,
    validate_street_address,
)
from metacrafterext.rules.common.survey import validate_age_band, validate_age_range_value
from tests.test_testdata_baseline import RULES, field_matches, load, value_matches

VALIDATORS = [
    (validate_radio_frequency, ["88.3", "FM 104.1", "97.9 FM", "1410KHZ", "800 KHz", "AM 870", "98,5"],
     ["FM", "90", "150", "88.7/CANAL 3", "FM on line", "2000", "870"]),
    (validate_radio_frequency_marked, ["FM 104.1", "97.9 FM", "1410KHZ"], ["88.3", "FM", "FM 150"]),
    (validate_geocoding_precision, ["Localización precisa", "Centroide de la localidad", "centroide localidad",
                                    "Localización aproximada", "Exacta", "Precisa", "Localidad", "Centroide por proximidad",
                                    "localización por localidad", "ROOFTOP", "GEOMETRIC_CENTER", "Localizacón aproximada"],
     ["Codigo en La Matanza", "15", "Buenos Aires", "Store"]),
    (validate_geocoding_precision_strong, ["Centroide", "Localización Precisa ", "Localización Aproximada", "RANGE_INTERPOLATED"],
     ["Localidad", "Localización", "Calle"]),
    (validate_ownership_type, ["Público", "Privado", "Mixto", "Pública", "Estatal", "Público Municipal", "Municipal", "Privada",
                               "Comunal", "public", "Privé"],
     ["Sociedad Anónima", "2015-2019", "Sin fines de lucro", "Cine", "Púbico"]),
    (validate_attendance_mode, ["Presencial", "presencial", "Virtual", "Bimodal", "Mixta", "A distancia", "A Distancia", "online",
                                "OnlineEventAttendanceMode", "in person"],
     ["Licitación pública", "Contratación directa", "A Distincia"]),
    (validate_periodicity, ["Anual", "Bianual", "Mensual", "monthly", "ANNUAL", "ANNUAL_2", "IRREG", "Semanal"],
     ["Otro", "12", "A veces", "Nunca", "Siempre"]),
    (validate_education_level, ["Grado", "Pregrado", "Posgrado", "GRADO", "Secundario completo", "Universitario incompleto",
                                "SECUNDARIOS INCOMPLETOS", "upper secondary", "Bachelor's or equivalent"],
     ["3", "Vigente", "Medicina", "Alto"]),
    (validate_socioeconomic_level, ["ABC1", "C2", "C3", "D1", "D2E", "C2+C3", "D1+D2+E", "AB", "E", "C+", "A/B", "C1a",
                                    "Medio bajo", "Alto"],
     ["44", "C4", "Z", "X1", "1", "SD"]),
    (validate_legislation_type, ["Decreto", "Ley", "Resolución SC", "DNU", "Decreto de Necesidad y Urgencia", "Ordenanza"],
     ["Museo", "Monumento", "Lugar Histórico", "s/d"]),
    (validate_legislation_number, ["325", "24.262", "1172/2003", "Ley 27.103", "Decreto 325/1989", "N° 2043"],
     ["0", "Decreto", "abc", "1234567"]),
    (validate_gender_word, ["Mujer", "Varón", "VARON", "No binaria", "Varón trans", "Otras identidades", "otras_identidades",
                            "Mujer trans", "F", "M", "Masculino"],
     ["Poesía", "Rock", "Novela", "Cuentos", "1"]),
    (validate_es_month, ["Octubre", "febrero", "FEBRERO", "setiembre", "Febrero "], ["lunes", "s/d", "13", "Mayo 25"]),
    (validate_street_address, ["Sarmiento 450", "Av. Corrientes 1543", "Calle 9 entre 29 Y 30", "Rivadavia S/N", "Plaza Brown"],
     ["NE", "Dirección Nacional de Vialidad", "s/d", "N", "www.cine.com.ar"]),
    (validate_floor, ["1", "1°", "2º B", "P.B.", "PA", "Planta Baja", "Piso 3", "Subsuelo", "Loc. 1", "9 A", "3ro B"],
     ["Av. Corrientes 1543", "Timbre 4", "abc def ghi"]),
    (validate_phone_digits, ["4326 3396", "011-4372-8383", "3874212884", "42,164,821", "43716978 Int. 131", "426701"],
     ["0", "s/d", "1234", "Pedir turno"]),
    (validate_degree_title, ["Licenciado en Comunicación Social", "Profesor de Música", "Técnico en Sonido", "Arquitecto",
                             "Diseñador Gráfico", "Licenciado/a en Letras", "Bachelor of Arts"],
     ["Cien años de soledad", "El Aleph", "Medios"]),
    (validate_ar_region, ["NOA", "PATAGONIA", "CUYO", "NEA", "CENTRO", "GBA", "CABA", "C.A.B.A", "BUENOS AIRES", "Pampeana",
                          "GRAN BS.AS.", "COMAHUE", "GBA NORTE"],
     ["Neuquén", "Córdoba", "Salta", "Dublin"]),
    (validate_ar_heritage_category, ["Monumento Histórico", "Lugar Histórico", "Sepulcro", "Bien de Interés Histórico y Artístico",
                                     "Bien de interés histórico-artístico", "Árbol Histórico", "Lugar Històrico Nacional",
                                     "\xa0Bien de Interés Histórico Nacional", "Área de Amortiguación Visual"],
     ["Museo", "Iglesia", "s/d"]),
    (validate_ar_conabip_number, ["938", "1", "4398"], ["0", "12345", "abc"]),
    (validate_age_range_value, ["18 A 29 ANIOS", "65 ANIOS Y MAS", "65 años y más"], ["ANIOS"]),
    (validate_age_band, ["13 A 17 ANIOS", "65 ANIOS Y MAS"], ["2", "VARON"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("common/directories.yaml", "radiofrequencybyname", ["frecuencia", "frequency", "frecuencia_fm", "freq_mhz"],
     ["frecuenciaacceso", "frecuencia_de_uso", "freq"]),
    ("common/directories.yaml", "geocodingprecisionbyname",
     ["tipo_latitud_longitud", "TipoLatitudLongitud", "Tipo_latitudlongitud", "detalle_georreferencia", "location_type",
      "geocoding_precision", "tipo_georreferenciacion"],
     ["latitud", "Nota", "tipo"]),
    ("common/directories.yaml", "ownershiptypebyname",
     ["tipo_gestion", "tipo_de_gestion", "Tipo de gestion", "Tipo de gestión", "tipo_gest", "jurisdiccion", "dependencia",
      "statut_public_prive", "ownership"],
     ["Tipo de gestión privado", "NOMBRE_JURISDICCION", "jurisdiccion _declaratoria", "sector"]),
    ("common/directories.yaml", "attendancemodebyname", ["Modalidad", "modalidad_de_cursada", "attendance_mode", "course_mode"],
     ["modalidades", "modo"]),
    ("common/directories.yaml", "periodicitybyname", ["Periodicidad", "periodicity", "frecuencia_de_actualizacion", "accrual_periodicity"],
     ["frecuencia", "periodo"]),
    ("common/directories.yaml", "educationlevelbyname", ["Nivel", "nivel_educativo", "nivel de estudios", "education_level"],
     ["niveles", "nivel_agua"]),
    ("common/directories.yaml", "socioeconomiclevelbyname", ["NSE_3", "NSEcat1", "NSE_SOCIOE", "niv_socioe", "nse", "nivel_socioeconomico",
                                                            "social_grade"],
     ["NSEpuntaje", "nse_puntaje", "nivel"]),
    ("common/directories.yaml", "legislationtypebyname", ["decreto_o_ley", "tipo_norma", "tipo de norma", "instrumento_legal"],
     ["numero_de_decreto_o_ley", "decreto"]),
    ("common/directories.yaml", "legislationnumberbyname",
     ["numero_de_decreto_o_ley", "nro_decreto", "numero_ley", "número de resolución", "decreto_numero", "law_number"],
     ["decreto_o_ley", "numero", "norma_id"]),
    ("common/directories.yaml", "degreetitlebyname", ["Título", "titulo", "titulo_otorgado", "degree"], ["titulos_publicados", "title"]),
    ("ar_country/ar_geo.yaml", "arregionbyname", ["region", "REGION", "region_nombre", "nombre_region"], ["IdRegion", "regional"]),
    ("ar_country/ar_common.yaml", "arconabipnumberbyname", ["nro_conabip", "numero_conabip", "conabip"], ["conabip_nombre"]),
    ("es/es_common.yaml", "esphonebyname", ["Teléfono", "Telefóno", "tel", "telefono_2", "celular", "teléfono de contacto"],
     ["telefonia", "tele", "cod_tel"]),
    ("es/es_geo.yaml", "esstreetaddressbyname", ["direccion", "Dirección", "domicilio", "direccion_descripcion", "domicilio_de_planta"],
     ["direccion_nacional", "direcciones"]),
    ("es/es_geo.yaml", "esfloorbyname", ["piso", "Piso", "piso_dpto"], ["departamento", "pisos", "DEPTO", "dpto"]),
    ("pii/pii.yaml", "genderbyspanishname", ["identidad_genero", "identidad_de_genero", "identidad de género"],
     ["genero", "genero_area_principal_editorial", "identidades"]),
    ("pii/pii.yaml", "agerangebyname", ["franja_etaria", "grupos_edad", "rango etario", "franja de edad"], ["franja", "edad"]),
    ("common/survey.yaml", "surveyweightbyname", ["ponderador", "pondera_dem", "expansor", "EXPANSOR", "factor_expansion"],
     ["peso", "pondera_puntaje_kg"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("common/directories.yaml", "radiofrequencyvalue", ["FM 104.1", "1410KHZ"], ["88.3", "FM"]),
    ("common/directories.yaml", "geocodingprecisionvalue", ["Centroide", "Localización Precisa "], ["Localidad"]),
    ("ar_country/ar_common.yaml", "arheritagecategoryvalue", ["Monumento Histórico Nacional", "Sepulcro"], ["Museo"]),
    ("es/es_datetime.yaml", "esmonthnamevalue", ["Octubre", "FEBRERO"], ["Oct", "lunes"]),
    ("common/boolean.yaml", "booleansino", ["Sí", "SI", "no"], ["sí señor", "tal vez"]),
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
        assert spec.get("needs_values") is True, rule_id
        assert spec.get("validator"), rule_id


def test_spanish_year_names_guard_the_year_rule():
    import re

    spec = load("es/es_datetime.yaml", "esyearbydatafiltered")
    guard = re.compile(spec["fieldregex"], re.IGNORECASE)
    for name in ("año_inauguracion", "Año de inicio", "último año de actividad", "declaracion_año", "anio_actualizacion",
                 "ano_actualizacion", "Año_primera_edicion", "año_act", "inicio_actividad", "inicio_act"):
        assert guard.search(name), name
    for name in ("años", "Duracion (años)", "mano_de_obra", "inicio", "anios_experiencia"):
        assert not guard.search(name), name


def test_spanish_gender_and_birth_year_rules_keep_their_keys():
    rules = yaml.safe_load((RULES / "pii/es/es_pii.yaml").read_text(encoding="utf-8"))["rules"]
    assert rules["esgenderknown"]["key"] == "gender"
    assert rules["esbirthdayknown"]["key"] == "birthday"
    assert rules["esbirthyearknown"]["key"] == "birth_year"
    assert rules["esbirthyearknown"]["type"] == "field"
