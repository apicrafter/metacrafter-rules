"""Rules for the files of the statistics office of Córdoba, Argentina (DGEyC,
datosestadistica.cba.gov.ar) in metacrafter-testdata (an April 2024 snapshot): INDEC census
radius and fraction codes, radius types, the department, locality and local government parts
of the INDEC codes in columns of their own, department names, locality names of the radius
lists, and dot-grouped thousands that are no semantic versions.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.ar_country.census import (
    DEPARTMENT_CODES,
    DEPARTMENT_NAMES,
    validate_ar_department_name,
    validate_ar_indec_census_fraction_code,
    validate_ar_indec_census_radius_code,
    validate_ar_indec_census_radius_link,
    validate_ar_indec_census_radius_type,
    validate_ar_indec_department_part,
    validate_ar_indec_local_government_part,
    validate_ar_indec_locality_part,
)
from metacrafterext.rules.common.software import validate_semver
from tests.test_testdata_baseline import field_matches, load

VALIDATORS = [
    (validate_ar_indec_census_radius_link, ["140070101", "140980807", "020010101", "20010101", 140070102],
     ["140070001", "140070100", "040070101", "149990101", "14007010", "1400701010", "05"]),
    (validate_ar_indec_census_radius_code, ["140070101", "01", "05", "7", "99"],
     ["00", "100", "01 Parte", "01 al 03", "040070101", "RADIO"]),
    (validate_ar_indec_census_fraction_code, ["1400701", "01", "27", "001", "9"],
     ["1400700", "0400701", "1000", "FRACCION", ""]),
    (validate_ar_indec_census_radius_type, ["U", "R", "M", "u", "Mixto", "URBANO"], ["X", "UR", "Urbana", ""]),
    (validate_ar_indec_department_part, ["098", "007", "7", "014", "182", "14098", "6014", "02105"],
     ["000", "999", "008x", "14999", "CAPITAL", "UYAR"]),
    (validate_ar_indec_locality_part, ["050", "010", "000", "025"], ["50", "0500", "BERROTARAN", ""]),
    (validate_ar_indec_local_government_part, ["0196", "2630", "7", "140196", "60441"], ["0", "0000", "1234567", "EMBALSE"]),
    (validate_ar_department_name, ["Calamuchita", "RIO CUARTO", "Río Cuarto", "Gral. San Martín", "Pte. Roque S. Peña",
                                   "PTE. ROQUE SAENZ PEÑA", "Departamento Capital", "Comuna 1", "12 de Octubre",
                                   "Adolfo Gonzales Chaves", "UNION"],
     ["Total Provincia", "TOTAL PROVINCIAL", "PROVINCIA CORDOBA", "098", "Antioquia", "Montevideo", "Casa", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


def test_department_list():
    # 529 of georef and 17 older codes (comunas 02001 to 02015, two of them also georef codes; 94007, 94014)
    assert len(DEPARTMENT_CODES) == 529 + 17 - 2
    assert {"14007", "14182", "06014", "02105", "02001", "94014"} <= DEPARTMENT_CODES
    assert {"calamuchita", "rio cuarto", "presidente roque saenz pena", "comuna 15"} <= DEPARTMENT_NAMES


FIELDS = [
    ("ar_country/ar_census.yaml", "arindeccensusradiuscodebyname",
     ["RADIO", "RADIO2008", "radio_censal", "cod_radio", "Radio Censal", "id_radio", "radio_censal_id"],
     ["radios", "radio_km", "radiodifusion", "Emisora", "TIPO_RAD"]),
    ("ar_country/ar_census.yaml", "arindeccensusradiuslinkbyname", ["CODIGO", "Código", "cod", "LINK", "link"],
     ["codigo_postal", "cod_loc", "CODDEPTO"]),
    ("ar_country/ar_census.yaml", "arindeccensusfractioncodebyname",
     ["FRAC", "FRACCION", "FRAC2008", "fraccion_censal", "Fracción", "cod_frac", "fraccion_id"],
     ["fracciones", "fraccionamiento", "fractal"]),
    ("ar_country/ar_census.yaml", "arindeccensusradiustypebyname", ["TIPO_RAD", "TIPO_RAD08", "tipo_radio", "tipo de radio"],
     ["tipo", "tipo_rama", "RADIO"]),
    ("ar_country/ar_census.yaml", "arindecprovincecodebarename", ["PROV", "prov", "PROV2008"], ["provincia", "province", "provider"]),
    ("ar_country/ar_census.yaml", "arindecdepartmentpartbyname",
     ["CODDEPTO", "DEPTO", "Cod - D", "cod_dpto", "DPTO", "codigo departamento"], ["departamento", "dep", "deposit"]),
    ("ar_country/ar_census.yaml", "arindeclocalitypartbyname", ["CODLOC", "cod_loc", "codigo_localidad"], ["localidad", "nomloc"]),
    ("ar_country/ar_census.yaml", "arindeclocalgovernmentpartbyname", ["COD_MUNI", "Cod-M", "cod_municipio", "COD_MUNI2"],
     ["municipio", "NOM_MUNI"]),
    ("ar_country/ar_census.yaml", "ardepartmentnamebyname",
     ["Departamento", "NOMDEPTO", "Dpto. Residencia", "departamento_nombre", "DEPARTAMENTO DE RESIDENCIA",
      "Departamento de residencia de la madre", "Departamento  de residencia", "nombre_departamento", "Partido", "DEPTO"],
     ["departamento_id", "Cod - D", "CODDEPTO", "Tipo de Vivienda Departamento"]),
    ("ar_country/ar_census.yaml", "arlocalitynamebyname", ["NOMLOC", "NOM_MUNI", "NOM_MUNI1", "nom_localidad"], ["nombre", "CODLOC"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


def test_code_rules_need_values():
    for path, rule_id, _, _ in FIELDS:
        spec = load(path, rule_id)
        assert spec.get("validator"), rule_id
        if rule_id != "arlocalitynamebyname":
            assert spec.get("needs_values") is True, rule_id


def test_semver_refuses_dot_grouped_thousands():
    for value in ("1.003.522", "3.413.530", "12.345.678", "1.446.201"):
        assert not validate_semver(value), value
    for value in ("1.2.3", "10.20.30", "1.100.2", "2.0.0-beta.1"):
        assert validate_semver(value), value
