"""Rules for the Costa Rican files of metacrafter-testdata (an April 2024 snapshot of Datos Abiertos INEC,
datosabiertos.inec.cr, Dateno source cdi00000393: the procurement reports the Instituto Nacional de Estadística y
Censos exports from SICOP, its budgets and budget execution reports): SICOP procedure and contract numbers and
catalogue codes, the codes of the classifications by object of expenditure and of income; and the universal
rules they needed: procurement statuses, the Costa Rican procedure types, suppliers and people in charge by
Spanish field name, an estado of procurement statuses that is not a state, a NIK that does not start with 0.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.common.generic import validate_state_not_status
from metacrafterext.rules.common.identifiers import validate_id_nik
from metacrafterext.rules.common.procurement import (
    validate_procurement_method,
    validate_procurement_status,
    validate_procurement_status_code,
)
from metacrafterext.rules.cr.codes import (
    validate_cr_budget_income_code,
    validate_cr_budget_object_code,
    validate_cr_sicop_contract_number,
    validate_cr_sicop_goods_code,
    validate_cr_sicop_procedure_number,
)
from tests.test_testdata_baseline import field_matches, load

VALIDATORS = [
    (validate_cr_sicop_procedure_number, ["2022CD-000001-0014400001", "2023LD-000013-0014400001", "2021LN-000001-0014400001",
                                          "2023PX-000054-0014400001", "2022CD-000013-0006400001", " 2016CD-000001-0014400001 "],
     ["2022CD-000001", "452-0001-LPU17", "2022cd-000001-0014400001", "2022CD-00001-0014400001", "0432023010900006",
      "9999CD-000001-0014400001", ""]),
    (validate_cr_sicop_contract_number, ["0432023010900006", "0432022010900001", "0432023010900090-00", "432016010900002.00",
                                         "432020010900069", "432018010900120.0"],
     ["3201010101900001", "0431995010900006", "043202301090000", "45-2023", "CT-001", "2023LD-000001-0014400001", ""]),
    (validate_cr_sicop_goods_code, ["4010160492001000", "3910160592074333", "4010160492001000.00", "8610180892012640.0",
                                    "391016059207433300000001"],
     ["39101605", "0010160492001000", "9910160492001000", "401016049200100", "40101604-92001000", ""]),
    (validate_cr_budget_object_code, ["0", "1", "5", "0.01", "1.04", "0.01.01", "1.04.04", "1.04.99", "9.02.01", " 1.03.07 "],
     ["1.4.4", "1..04.99", "1.04.04.01", "10.04", "1.3.1.2.09.09.0.0.000", "REMUNERACIONES", "0.0 1", ""]),
    (validate_cr_budget_income_code, ["1.3.1.2.09.09.0.0.000", "1.0.0.0.00.00.0.0.000", "1.4.1.1.00.00.0.0.000",
                                      "3.0.0.0.00.00.0.0.000", "1.3.1.2.9.9.0.0.0", "   1.3.0.0.0.0.0.0.0"],
     ["4.0.0.0.00.00.0.0.000", "1.04.04", "1.3.1.2", "1.3.1.2.09.09.0.0", "1.0.0.00.00.0.0.0.000", "1.2.840.113549.1.1.11", ""]),
    (validate_procurement_status, ["Contrato", "Adjudicación en firme", "Desierto/Infructuoso", "Sin efecto", "En evaluación",
                                   "En recepción de ofertas", "En apertura", "Apelación o Revocación", "Contrato notificado",
                                   "Infructuoso", "ADJUDICADO", "Desierta"],
     ["Vigente", "Finalizado", "En proceso", "Jalisco", "Licitación Abreviada", "2023", "1",
      "El contrato fue adjudicado a la empresa que presentó la oferta de menor precio", ""]),
    (validate_procurement_status_code, ["active", "unsuccessful", "complete", "terminated", "Cancelled"], ["Contrato", "open", ""]),
    # the procedure types of the Costa Rican procurement laws, as SICOP names them
    (validate_procurement_method, ["Licitación Reducida", "Licitacion Menor", "Licitación Mayor", "Escasa cuantía",
                                   "Procedimiento por Excepción", "Licitación Abreviada", "Licitación Publica Nacional",
                                   "Contratación Directa"],
     ["Contrato", "Desierto/Infructuoso", "Excepción"]),
    # an estado of procurement statuses is not a state
    (validate_state_not_status, ["Jalisco", "SP", "Rio de Janeiro"],
     ["Contrato", "Adjudicación en firme", "Apelación o Revocación", "Desierto/Infructuoso", "Sin efecto", "En evaluación"]),
    # province codes of a NIK start at 11: a SICOP contract number is not one
    (validate_id_nik, ["3201010101900001"], ["0432023010900006", "0432022010900001"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ + str(i) for i, v in enumerate(VALIDATORS)])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("cr/cr_codes.yaml", "crsicopcontractnumberbyname", ["NUMERO_CONTRATO", "Número de contrato", "nro_contrato", "No. Contrato",
                                                        "Numero del contrato", "contrato_numero"],
     ["NUMERO_PROCEDIMIENTO", "contrato", "tipo_contrato", "OBJETO_CONTRACTUAL", "monto_contrato"]),
    ("cr/cr_codes.yaml", "crsicopgoodscodebyname", ["COD_BIEN_SERVICIO", "Código del bien o servicio", "codigo_bien", "cod_sicop",
                                                   "Código de bienes y servicios"],
     ["OBJETO_CONTRACTUAL", "LINEA", "bien", "COD_PROVEEDOR", "descripcion_bien"]),
    ("cr/cr_codes.yaml", "crbudgetobjectcodebyname", ["SUBPARTIDA", "Subpartida", "SUBP.", "SUBP\\.", "PART./ SUBP.", "PART\\./ SUBP\\.",
                                                     "PARTIDA", "partida_presupuestaria", "Código por OBG", "objeto_gasto"],
     ["DESCRIPCION", "Código por CE", "PROGRAMA 03", "contrapartida", "PRESUPUESTO ORDINARIO"]),
    ("common/procurement.yaml", "procurementstatusbyname", ["ESTADO", "estado", "estado_procedimiento", "Estado del concurso",
                                                           "Estado de la contratación", "situacion", "tender_status"],
     ["ESTADO_CIVIL", "estado_id", "TIPO_PROCEDIMIENTO", "status_code", "estado de salud"]),
    ("common/procurement.yaml", "procurementstatusocds", ["tender.status", "awards.status", "releases.contracts.status", "contracts.status"],
     ["status", "tender.statusDetails", "parties.status", "tender.procurementMethod"]),
    ("common/procurement.yaml", "suppliernamebyname", ["PROVEEDOR_ADJUDICADO", "PROVEEDOR_ADJU", "proveedor", "Proveedor", "contratista",
                                                      "nombre_proveedor", "nombre del contratista", "proveedores"],
     ["nit_proveedor", "rut_proveedor", "proveedor_id", "COD_PROVEEDOR", "ENCARGADO_PROVEDURIA", "tipo_proveedor"]),
    ("es/es_persons.yaml", "esinchargefullnamebyname", ["ENCARGADO_PROVEDURIA", "ENCARGADO_ESTUDIOS_TECNICOS", "ENCARGADO_RECOM_ADJUD",
                                                       "ENCARGADO_SOLICITUD_ADJUD", "ADMINISTRADOR_CONTRATACION", "encargado",
                                                       "Encargada", "administrador del contrato"],
     ["SOLICITUD_ESTUDIOS_TECNICOS", "administracion", "administrador", "cargo", "encargo"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_names(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


def test_guarded_value_rules():
    """Sixteen digits are also an Indonesian NIK, fifteen an IMSI, and 1.04.04 a date: the value rules of the
    contract number and of the object of expenditure run only in fields named for them, where they outrank the
    unnamed ones. A procedure number and an income code have a shape of their own and need no guard."""
    assert load("cr/cr_codes.yaml", "crsicopcontractnumbervalue")["fieldregex"]
    assert load("cr/cr_codes.yaml", "crbudgetobjectcodevalue")["fieldregex"]
    for rule_id in ("crsicopprocedurenumbervalue", "crbudgetincomecodevalue"):
        assert "fieldregex" not in load("cr/cr_codes.yaml", rule_id)
