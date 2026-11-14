"""Rules for the ARSAT files of metacrafter-testdata (an April 2024 snapshot of the open data portal of
ARSAT, the Argentine state satellite and telecommunications company): KML coordinates written as text,
procurement methods in many languages, Argentine province names, Spanish gender words and
organizational units; and the fix of bank accounts on budget account lines named cuenta.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest
import yaml

from metacrafterext.rules.ar_country.codes import (
    validate_ar_bank_account_number,
    validate_ar_province,
    validate_ar_province_by_value,
)
from metacrafterext.rules.common.generic import (
    validate_es_gender_value,
    validate_es_gender_word,
    validate_es_orgunit_name,
    validate_kml_coordinates,
    validate_orgunit_text,
)
from metacrafterext.rules.common.procurement import (
    validate_procurement_method,
    validate_procurement_method_or_code,
)
from tests.test_testdata_baseline import RULES, field_matches, load, value_matches

VALIDATORS = [
    (validate_kml_coordinates,
     ["-68.96836853027344,-81.1478500366211,0.0 -72.55793762207031,-79.67288208007812,0.0",
      "-3.7038,40.4168 -3.7040,40.4170", " -58.4,-34.6,0 -58.5,-34.7,0\n-58.6,-34.8,0 "],
     ["220,220,220", "-58.4,-34.6", "1,2 3,4", "123629.78 379674.57 123700.0 379674.57", "200.5,10.1 1.0,1.0",
      "-58.4;-34.6 -58.5;-34.7", "12,5 13,7"]),
    (validate_procurement_method,
     ["Compras Menores", "Contratacion directa - Inciso F", "Licitacion Publica Nacional", "Licitación Pública BAC",
      "Licitación Privada", "Negociado sin publicidad", "Abierto simplificado", "Adjudicación directa",
      "Invitación a cuando menos tres personas", "Procédure adaptée", "Appel d'offres ouvert",
      "Marché public négocié sans publicité ni mise en concurrence préalable", "Dialogue compétitif",
      "Pregão Eletrônico", "Dispensa de Licitação", "Procedura negoziata", "Offenes Verfahren",
      "Öffentliche Ausschreibung", "Open procedure", "Request for Quotations", "Avatud hankemenetlus", "Lihthange",
      "Väikehange", "Электронный аукцион", "Запрос котировок в электронной форме", "指名競争入札", "一般競争入札",
      "随意契約"],
     ["Licitación Pública N° 12/2020 para la compra de 300 antenas", "Convenio", "Donación", "Abierto", "open",
      "Cerrado", "Pesos", "Gerencia Comercial", "Concursos de belleza", "Procedimiento", "452-0001-LPU17", ""]),
    (validate_procurement_method_or_code,
     ["open", "oth-single", "neg-wo-call", "comp-dial", "selective", "Abierto", "Negociado sin publicidad"],
     ["closed", "1", "LPU", "Gerencia Comercial"]),
    (validate_ar_province,
     ["Buenos Aires", "BUENOS AIRES", "Córdoba", "CORDOBA", "Entre Rios", "Sgo Del Estero", "Provincia del Neuquén",
      "CABA", "C.A.B.A.", "Capital Federal", "Tierra del Fuego, Antártida e Islas del Atlántico Sur", "Tucumán"],
     ["Totales", "N/A", "Rosario", "Madrid", "Neuquén Capital", "06", "Partido de La Matanza", ""]),
    (validate_ar_province_by_value, ["Buenos Aires", "Provincia de Santa Fe", "TUCUMAN"],
     ["Ciudad Autónoma de Buenos Aires", "CABA", "Capital Federal", "Totales"]),
    (validate_ar_bank_account_number,
     ["0012-3456/7", "2850590940090418135201", "123-004567/8", "CA 1234567-8"],
     ["Ingresos de Operación", "TOTAL INGRESOS CORRIENTES", "123", "A", "1.3.1", ""]),
    (validate_es_gender_word, ["Mujeres", "Hombres", "Femenino", "MASCULINO", "Varón", "varones", "No binario"],
     ["Total", "F", "Drama", "Comedia", "Novela"]),
    (validate_es_gender_value, ["Mujeres", "F", "M", "X", "Total", "Masculino"], ["Drama", "Novela", "Rock", "Poesía"]),
    (validate_es_orgunit_name,
     ["Presidencia", "Directorio", "Gerencia General", "Gerencia de Operaciones Terrestres", "Subgerencia de RRHH ",
      "Unidad de Auditoría Interna", "Secretaría General", "Jefatura de Gabinete de Asesores de Directorio"],
     ["CEATSA", "Total", "Departamento Capital", "Dirección Nacional de Vialidad", "Buenos Aires", "Gerente"]),
    (validate_orgunit_text, ["Subgerencia de RRHH", "Finance Department", "Ventas"], ["12", "", "A1", "001-002"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("common/procurement.yaml", "procurementmethodbyname",
     ["Tipocompra", "TIPO_PROCEDIMIENTO", "Tipo de procedimiento (catálogo)", "PROCEDIMIENTO DE ADJUDICACION",
      "procedimiento_tipo", "procedure", "procurementMethod", "tender.procurementMethodDetails",
      "TenderingProcess.ProcedureCode.#text", "modalidad_contratacion", "modalidade_de_licitacao", "tipo_procedura",
      "scelta_contraente", "Vergabeart", "契約方法"],
     ["procedimiento_numero", "procedure_date", "tipo", "modalidades", "procurement"]),
    ("ar_country/ar_geo.yaml", "arprovincebyname",
     ["PROVINCIA", "Provincia", "provincia_nombre", "nombre_provincia", "jurisdiccion", "prov"],
     ["provincia_id", "cod_prov", "provincias", "departamento"]),
    ("pii/es/es_pii.yaml", "esgenderbyname", ["Género", "genero", "GENERO", "genero_declarado", "sexo genero"],
     ["Género por Gerencia", "generos", "genero_literario_x_y"]),
    ("common/orgs.yaml", "orgunitbyname",
     ["Gerencia", "gerencia_solicitante", "Subgerencia", "dependencia", "Unidad organizativa", "org_unit",
      "Organizational unit", "business_unit", "repartición"],
     ["gerente", "Género por Gerencia", "unidad", "area"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("common/geo_text.yaml", "kmlcoordinatestext", ["-68.968,-81.147,0.0 -72.557,-79.672,0.0"], ["220,220,220"]),
    ("common/procurement.yaml", "procurementmethodvalue", ["Contratacion directa - Inciso F", "指名競争入札"],
     ["open", "Convenio"]),
    ("ar_country/ar_geo.yaml", "arprovincevalue", ["BUENOS AIRES", "Sgo Del Estero"], ["Totales", "Rosario", "CABA"]),
    ("pii/es/es_pii.yaml", "esgenderknown", ["Mujeres", "Masculino"], ["Total", "F"]),
    ("common/orgs.yaml", "orgunitesvalue", ["Gerencia Comercial", "Unidad de Auditoría Interna"], ["CEATSA", "Total"]),
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


def test_cuenta_needs_account_numbers():
    for path, rule_id in (("ar/ar_finances.yaml", "arbankaccountknown"),
                          ("ar_country/ar_finances.yaml", "ar_finances_arbankaccountknown")):
        spec = load(path, rule_id)
        assert "cuenta" in spec["rule"].split(",")
        assert spec["validator"].endswith("validate_ar_bank_account_number") and spec["needs_values"] is True


class _Keys(yaml.SafeLoader):
    """A loader that refuses a mapping key given twice, which PyYAML keeps silently (last wins)."""


def _no_duplicates(loader, node, deep=False):
    keys = [loader.construct_object(k, deep=deep) for k, _ in node.value]
    duplicated = {k for k in keys if keys.count(k) > 1}
    if duplicated:
        raise AssertionError(f"duplicate keys {sorted(duplicated)} at line {node.start_mark.line + 1}")
    return loader.construct_mapping(node, deep=deep)


_Keys.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_duplicates)


def test_spanish_gender_rule_is_not_shadowed():
    # The birthday rule of es_pii.yaml had the key of the gender rule, so the gender rule was lost.
    rules = yaml.load((RULES / "pii/es/es_pii.yaml").read_text(encoding="utf-8"), Loader=_Keys)["rules"]
    assert rules["esgenderknown"]["key"] == "gender"
    assert rules["esbirthdayknown"]["key"] == "birthday"


def test_fecha_is_a_date():
    spec = load("es/es_datetime.yaml", "esdatetimename")
    assert spec["key"] == "date" and field_matches("es/es_datetime.yaml", "esdatetimename", "Fecha")
