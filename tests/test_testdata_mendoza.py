"""Rules for the Mendoza files of metacrafter-testdata (a 2024 snapshot of datosabiertos.mendoza.gov.ar,
the open data portal of the province of Mendoza, Argentina): districts of the departments, school numbers,
the classifiers of the provincial budget (economic classification, financing sources, resource accounts,
accounting units), administrative files before GDE, electricity distributors, categories of hazardous
waste; tourist accommodation types and star ratings, interest rates, urban or rural classes, durations in
Spanish words, and new field names of existing types.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.ar_country.codes import validate_ar_gde_number_known_ecosystem
from metacrafterext.rules.ar_country.mendoza import (
    validate_ar_electricity_distributor,
    validate_ar_electricity_distributor_name,
    validate_ar_hazardous_waste_categories,
    validate_ar_mendoza_cuc,
    validate_ar_mendoza_district,
    validate_ar_mendoza_economic_classification,
    validate_ar_mendoza_economic_classification_value,
    validate_ar_mendoza_expediente_number,
    validate_ar_mendoza_expediente_number_with_office,
    validate_ar_mendoza_financing_source,
    validate_ar_mendoza_resource_account,
    validate_ar_mendoza_school_number,
)
from metacrafterext.rules.common.directories import validate_periodicity
from metacrafterext.rules.common.rates import (
    validate_es_amount,
    validate_interest_rate,
    validate_interest_rate_reference,
    validate_marked_amount,
)
from metacrafterext.rules.common.tourism import validate_accommodation_star_rating, validate_accommodation_type
from metacrafterext.rules.common.urban import validate_building_number, validate_urban_rural_class
from metacrafterext.rules.es.periods import validate_es_duration_words
from metacrafterext.rules.za.finances import validate_za_economic_classification_value
from tests.test_testdata_baseline import field_matches, value_matches

VALIDATORS = [
    (validate_ar_mendoza_district, ["Rodeo de la Cruz", "EL PLUMERILLO", "Va. Hipódromo", "San José (G)", "Medrano (R)",
                                    "Ciudad de San Martín", "Ciudad de Gral Alvear", "Segunda Sección", "SEGUNDA SECCION",
                                    "2° Sección", "Decima Sección", "4ª Sección Área Fundacional", "Gdor. Benegas",
                                    "Kilómetro 11", "el pastal", "Uspallata", "CIUDAD", "Las Heras"],
     ["Palermo", "Total", "1", "DISTRITO 6", "R2a II", "Philips-La Central-12 de octub", "Recoleta", ""]),
    (validate_ar_mendoza_school_number, ["4-013", "1-123", "P-131", "PS-046", "P113", "1152", "J023", "9-030"],
     ["5000035", "12-345", "Nº", "--", "A-1234", "1-12"]),
    (validate_ar_electricity_distributor, ["EDEMSA", "E.D.E.M.S.A.", "Edeste", "EDESTESA", "EDENOR", "Coop. Godoy Cruz",
                                           "Cooperativa Eléctrica de Godoy Cruz", "Coop. C.E.C.S.A.G.A.L.", "Coop. Sud Río Tunuyan"],
     ["CAMMESA", "Total", "GODOY CRUZ", "ALTO VERDE", "Cooperativa", "YPF"]),
    (validate_ar_electricity_distributor_name, ["GODOY CRUZ", "ALTO VERDE", "SUD RIO TUNUYAN", "MONTE COMAN", "EDEMSA"],
     ["Total", "Mendoza", "CAMMESA", "1"]),
    (validate_ar_mendoza_economic_classification, ["41101 PERSONAL PERMANENTE", "41100 - PERSONAL", "51101 BIENES DE CAPITAL",
                                                   "74102 AMORTIZACION DEUDA ACREEDORES VARIOS", "52401 - INVERSION FIDUCIARIA"],
     ["1110100000-IMPUESTO SOBRE LAS ACTIVIDADES", "41101", "0 Rentas Generales", "31101 PERSONAL"]),
    (validate_ar_mendoza_economic_classification_value, ["41201 BIENES CORRIENTES", "43200 - TRANSF.P/FINANCIAR EROGACIONES",
                                                         "51201 TRABAJOS PUBLICOS"],
     ["12345 MAIN STREET", "61234 GODOY CRUZ", "54321 Avenida Mitre"]),
    (validate_ar_mendoza_financing_source, ["0 Rentas Generales", "000 - Rentas Generales", "21 Tasa de Justicia",
                                            "999 No controla cuota", "186 Impuesto p/I.Brutos afec.a Bib.Popul"],
     ["2019/01", "H20001", "Rentas Generales", "0", "1000 Rentas"]),
    (validate_ar_mendoza_resource_account, ["1110100000-IMPUESTO SOBRE LAS ACTIVIDADES", "1120202000 - INT. GANADOS PRESTAMOS",
                                            "90604 1110101000-Impuesto sobre los ingresos brutos", "1000000000-RECURSOS CORRIENTES"],
     ["1110100000", "41101 PERSONAL PERMANENTE", "4110100000-Gastos", "11101000-IMPUESTO"]),
    (validate_ar_mendoza_cuc, ["906-Administración Central", "259-Hospital Central", "906", "504.0"],
     ["0 Rentas Generales", "9060", "Administración Central"]),
    (validate_ar_mendoza_expediente_number, ["4259-D-2015-03834", "1310/G/07/03834", "203-D-2014-18007", "3451-N-1943",
                                             "1373/G/02/30091 acum. Nº 1219/G/00/03834", "782/J/2006/03834"],
     ["EX-2018-01621874-GDEMZA-DPA#SAYOT", "2018-01-01", "-", "12/05/2019", "A-1234"]),
    (validate_ar_mendoza_expediente_number_with_office, ["4259-D-2015-03834", "1310/G/07/03834"],
     ["3451-N-1943", "4259-D-2015", "12-A-34-56"]),
    (validate_ar_hazardous_waste_categories, ["Y48", "Y8-Y9-Y48", "Y8, Y9, Y11", "Y8 / Y9 / Y48", "Y8, Y9, R9",
                                              "Y8-Y9-Y12-Y29- Y31-Y34", "Y8/Y9/Y11/Y18/Y35"],
     ["Y46", "Y49", "R9", "Decantación y Filtrado: Y8", "Y1 2020", ""]),
    (validate_accommodation_type, ["HOTEL", "APART-HOTEL", "CABAÑAS", "Hostería", "HOSTERIA RURAL", "Bed & Breakfast", "camping",
                                   "chambre d'hôtes", "Ferienwohnung", "VIV.USO TCO.", "COL.VACAC.", "REFUGIO"],
     ["RESTAURANTE", "DISPONIBLE", "PAT", "Hotel Sheraton", "BAR", ""]),
    (validate_accommodation_star_rating, ["3 ESTRELLAS", "1 ESTRELLA", "4 étoiles", "4 Sterne Superior", "5 stars", "3*", "****",
                                          "★★★", "SIN CATEGORIZAR"],
     ["4.5", "3", "HOSPEDAJE", "Clase 5", ""]),
    (validate_interest_rate, ["6,00%", "11.41 %", "Libor + 3,70%", "Badlar + 2", "BADLAR Bancos Privados", "CER + 0,1%",
                              "tasa fija anual del 21%", "30 % de la TNA del BNA", "15% / BADLAR Bancos Privados",
                              "Badlar Públicos + 2%"],
     ["Semestral", "12", "Pesos", "Monthly", "Coparticipación Federal de Impuestos"]),
    (validate_interest_rate_reference, ["Badlar + 2%", "Libor + 3,70%", "CER + 0,1%", "BADLAR Bancos Privados", "EURIBOR 6M + 0.5%",
                                        "UVA + 2%"],
     ["6,00%", "Uva", "CER", "Prime", "tasa fija anual del 21%"]),
    (validate_urban_rural_class, ["Urbano", "Urbano marginal", "Marginal", "Rural", "URBANO MARGINAL", "rural disperso",
                                  "(England/Wales) Urban major conurbation", "(England/Wales) Rural town and fringe",
                                  "Urban: Nearer to a major town or city", "städtisches Gebiet", "ländlich", "périurbain"],
     ["Urbanización La Esperanza", "1", "Centro", "U", "Zona Norte", ""]),
    (validate_es_duration_words, ["1 días, 13 horas, 20 minutos", "0 horas, 3 minutos", "272 días, 9 horas, 49 minutos",
                                  "2 años y 3 meses", "45 minutos"],
     ["13:20", "2019", "Nunca se derivó", "horas", "El ticket no está en estado ASIGNADO"]),
    (validate_periodicity, ["Mensual", "Semestral", "Trimestral", "Monthly", "Semi annual", "Quarterly"], ["Pesos", "semi", "88.3"]),
    (validate_building_number, ["1124", "S/N", "KM10", "KM.7,5", "KM 32", "km1059"], ["KM", "N/T", "5", "KM.12345"]),
    (validate_ar_gde_number_known_ecosystem, ["EX-2023-00006308- -GDEMZA-FTYC", "EX-2018-01621874-GDEMZA-DPA#SAYOT",
                                              "EX 2018-00345266-GDEMZA-DPA#SAYOT (Expte. 1234-D-2017-03834)"],
     ["EX-2018-1-XYZ", "4259-D-2015-03834"]),
    (validate_es_amount, ["6.613.703,03", "0,00", "0", "-136.786,75", "$ 298.278.261,30", "-"], ["2018/01", "abc", "4,509,343.45"]),
    (validate_marked_amount, ["$ 298.278.261,30", "ARS 3.662,50", "USD 44,59", "1.234,50 €", "$ 0,00"], ["$5", "USD", "298.278.261,30", "Pesos"]),
    (validate_za_economic_classification_value, ["Goods and services", "Compensation of employees"], ["CAPITAL", "Capital", "Current"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("ar_country/ar_mendoza.yaml", "armendozadistrictbyname", ["distrito", "DISTRITO", "distrito_nombre", "guia_domicilio_distrito",
                                                               "distrito_punto_wi_fi", "oficina_domicilio_ distrito_o_localidad"],
     ["distrital", "id_distrit"]),
    ("ar_country/ar_mendoza.yaml", "armendozaschoolnumberbyname", ["ESC", "esc", "numero_escuela", "numero_establecimiento",
                                                                   "Nº de escuela", "escuela_numero"],
     ["numero", "escuela_nombre", "NUMERO"]),
    ("ar_country/ar_mendoza.yaml", "armendozaeconomicbyname", ["Clasificación Económica", "clasificacion_economica",
                                                               "clasificacion-economica", "ejecucion presupuesto_partida gasto",
                                                               "ejecucion_presupuesto_partida_gasto"],
     ["clasificacion_economica_principal", "clasificacion"]),
    ("ar_country/ar_mendoza.yaml", "armendozafinancingbyname", ["Financiamiento", "financiamiento",
                                                                "ejecucion presupuesto_ nomenclador financiamiento",
                                                                "ejecucio_ presupuesto_ nomenclador_financiamiento", "fuente_de_financiamiento"],
     ["financiamientos", "linea de credito_objeto de financiamiento"]),
    ("ar_country/ar_mendoza.yaml", "armendozaresourcebyname", ["Cuenta Contable Nivel 4", "cuenta_contable_nivel_1", "cuenta_contable_nivel _3",
                                                               "plan_cuentas", "Plan de cuentas", "plan_de_cuentas", "presupuesto_partidas"],
     ["cuenta", "cuenta_banco_numero"]),
    ("ar_country/ar_mendoza.yaml", "armendozacucbyname", ["CUC", "cuc", "id_cuc"], ["cuco", "cuc_id_x"]),
    ("ar_country/ar_mendoza.yaml", "armendozaexpedientebyname", ["expediente_numero", "numero_expediente", "expediente_operatoria",
                                                                 "expediente_mina", "expediente", "expediente_número"],
     ["expedientado", "numero"]),
    ("ar_country/ar_mendoza.yaml", "arhazardouswastebyname", ["categorias de control autorizadas", "categorías_de_control_autorizadas",
                                                              "categorias_gestion_atorizadas", "corrientes_autorizadas", "categorias"],
     ["categoria_agencia", "corriente"]),
    ("ar_country/ar_energy.yaml", "arelectricitydistributorbyname", ["distribuidora", "Distribuidora", "DISTRIBUIDORA",
                                                                     "distribuidora_nombre", "id_distribuidora", "distribuidora_id"],
     ["distribucion", "distribuidoras_de_gas_x"]),
    ("common/tourism.yaml", "accommodationtypebyname", ["clase", "CLASE", "RUBRO", "tipo_alojamiento", "accommodation_type",
                                                        "type d'hébergement"],
     ["clases", "rubros_x", "personal_clase"]),
    ("common/tourism.yaml", "accommodationstarsbyname", ["categoria", "CATEGORIA", "categoría", "estrellas", "star_rating", "classement"],
     ["categorias", "categoria_agencia"]),
    ("common/rates.yaml", "interestratebyname", ["tasa", "Tasa", "tasa_interes", "tasa de interés", "linea de credito_tasa",
                                                 "Operatoria Bonificacion de tasa_tasa final", "Cupón/Cupon", "Cupón / Cupon",
                                                 "coupon", "interest_rate", "taux"],
     ["tasas_de_desempleo_x", "tasar"]),
    ("common/geo.yaml", "urbanruralbyname", ["ambito", "ámbito", "AMBITO", "urban_rural", "UrbanRural (name)", "station setting name"],
     ["ambitos", "urbano"]),
    ("common/geo.yaml", "compasspointbyname", ["hi_dir", "wind_dir", "winddirection"], ["dir", "hi"]),
    ("common/periods.yaml", "yearmonthbyname", ["Ejercicio/Mes", "ejercicio_mes", "id_ejercicio_mes", "ejercicio-mes"], ["ejercicio"]),
    ("common/directories.yaml", "periodicitybyname", ["Frecuencia / Frequency", "frecuencia_de_pago", "payment_frequency"],
     ["frecuencia", "Frequency"]),
    ("common/directories.yaml", "legislationnumberbyname", ["resolucion", "RESOL.", "RES.", "reolucion", "numero_resolucion",
                                                            "resolucion_inscripcion_agencia", "numero_resolucion_inscripción",
                                                            "decreto_provincial_numero", "resolucion_epas_numero"],
     ["resoluciones_x", "resolver", "resolucion_epas_anio", "decreto_provincial_anio"]),
    ("es/es_common.yaml", "esphonebyname", ["telefono_agencia", "telefono_de_contacto_fijo_profesional_turismo", "oficina_telefono",
                                           "contacto_telefono_numero_fijo_abonado", "telefono_escuela", "telefono_destacamento_policial"],
     ["telefonista", "cod_tel"]),
    ("ar_country/ar_geo.yaml", "arpostcodebyname", ["C_POSTAL", "c_postal", "codigo_postal_solicitante"], ["postal", "c_post"]),
    ("ar_country/ar_census.yaml", "ardepartmentnamebyname", ["departamento_centro_de_salud", "domicilio_departamento",
                                                             "oficina_domicilio_departamento", "departamento_domicilio_agencia",
                                                             "C_DEPTO", "Departamen", "id_departamento", "domicilio_legal_depto"],
     ["departamento_id", "Tipo de Vivienda Departamento", "cod_departamento", "departamento_cod"]),
    ("ar_country/ar_caba.yaml", "arcuebyname", ["cue_escuela", "escuela_cue"], ["cuenta"]),
    ("es/es_geo.yaml", "esstreetbycompoundname", ["domicilio_calle_escuela", "oficina_domicilio_calle", "delegacion_calle",
                                                  "direccion_calle", "domicilio_calle_local_gastronomico"],
     ["calle", "calles"]),
    ("es/es_geo.yaml", "esbuildingnumberbycompoundname", ["numero_domicilio_agencia", "oficina_domicilio_numero", "delegacion_numero",
                                                          "numeracion_domicilio_local_gastronomico", "direccion_numero_bodega",
                                                          "numero_direccion_bodega_enoturismo", "numero_contacto"],
     ["numero", "numero_de_solicitud"]),
    ("es/es_geo.yaml", "esfloorbycompoundname", ["domicilio_piso", "piso_domicilio_agencia", "oficina_domicilio_piso", "delegacion_piso",
                                                 "piso_domicilio_local_gastronomico"],
     ["piso", "pisos"]),
    ("es/es_budget.yaml", "esbudgetstageamountbyname", ["votado", "presupuesto_devengado", "ejecucion presupuesto_autorizado",
                                                       "presupuesto_mandado a pagar", "credito_vigente", "calculado_ingresos",
                                                       "sancion_total_impuesta", "acreditado_usuarios", "en_procesos_acreditacion_usuarios",
                                                       "acreditado_cuenta_ acumulacion"],
     ["ingresos", "votacion", "saldo_inicial_x"]),
    ("es/es_budget.yaml", "esejercicioyearbyname", ["ejercicio", "id_ejercicio", "ejercicio_fiscal"], ["ejercicio_mes", "ejercicios"]),
    ("common/values.yaml", "temperaturebyname", ["hi_temp", "low_temp", "temo_out", "dew_point", "in_dew", "wind_chill", "heat_index",
                                                 "thw_index", "in_temp", "temperatura_grados_centigrados_momento_medicion"],
     ["heat", "dew", "temp"]),
    ("es/es_datetime.yaml", "esdurationwordsbyname", ["demora_desde_solicitud_tickets", "horas_demora_desde_solicitud", "duracion",
                                                     "Horas de demora desde que se asignó"],
     ["demoras_x1", "hora"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("ar_country/ar_mendoza.yaml", "armendozaeconomicvalue", ["41101 PERSONAL PERMANENTE", "41300 - SERVICIOS"], ["12345 MAIN ST"]),
    ("ar_country/ar_mendoza.yaml", "armendozaresourcevalue", ["1110100000-IMPUESTO SOBRE LAS ACTIVIDADES"], ["1110100000"]),
    ("ar_country/ar_mendoza.yaml", "armendozaexpedientevalue", ["4259-D-2015-03834", "1310/G/07/03834"], ["3451-N-1943"]),
    ("ar_country/ar_mendoza.yaml", "arhazardouswastevalue", ["Y8-Y9-Y48", "Y8, Y9, Y11"], ["Y46", "R9"]),
    ("ar_country/ar_energy.yaml", "arelectricitydistributorvalue", ["EDEMSA", "Coop. Godoy Cruz"], ["GODOY CRUZ"]),
    ("common/tourism.yaml", "accommodationtypevalue", ["APART-HOTEL", "Hostería"], ["RESTAURANTE"]),
    ("common/tourism.yaml", "accommodationstarsvalue", ["3 ESTRELLAS", "4 étoiles"], ["3"]),
    ("common/rates.yaml", "interestratereferencevalue", ["Badlar + 2%", "Libor + 3,70%"], ["6,00%", "Uva"]),
    ("common/geo.yaml", "urbanruralvalue", ["Urbano marginal", "städtisches Gebiet"], ["Centro"]),
    ("es/es_datetime.yaml", "esdurationwordsvalue", ["1 días, 13 horas, 20 minutos"], ["13:20"]),
    ("es/es_budget.yaml", "esmarkedamountvalue", ["$ 298.278.261,30", "ARS 3.662,50"], ["298.278.261,30"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value
