"""Rules for the United Kingdom and French files of metacrafter-testdata that come from 2024 snapshots of
UK open data portals (Dateno sources cdi00000763 to cdi00000799: data.gov.uk, Cambridgeshire Insight,
Calderdale Data Works, Open Leicester, London Datastore, Open Data Glasgow) and of French ones (cdi00000700 to
cdi00000747: Opendatasoft portals of ministries, communes and RTE, Paris Data, Open Data Corse and research
data repositories): names of LSOAs, MSOAs, local authorities and constituencies, USRNs, the phrases of
brownfield land registers, council tax bands, ProClass and SIC codes, CRS station codes, service URIs of the
Local Government Service List, 360Giving identifiers, school names, the departments and units of spend
files, amounts written with a currency sign; the codes of the French register of electricity installations,
PACAGE numbers, EUNIS habitat codes, the section and the side of a local budget line; and the fixes they
needed: an LSOA or MSOA column of names is no column of codes, GSS codes under a bare code column, Annex I
habitat codes, Natura 2000 site codes and Sandre river codes by field name.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.fr.portals import (
    validate_eu_habitat_type_code,
    validate_eu_natura2000_site,
    validate_eunis_habitat_code,
    validate_fr_budget_section,
    validate_fr_budget_sens,
    validate_fr_elec_code,
    validate_fr_elec_filiere_code,
    validate_fr_pacage,
)
from metacrafterext.rules.gb.portals import (
    validate_gb_360giving_id,
    validate_gb_area_name,
    validate_gb_brownfield_ownership_status,
    validate_gb_brownfield_permission_type,
    validate_gb_brownfield_planning_status,
    validate_gb_council_tax_band,
    validate_gb_crs_code,
    validate_gb_esd_service_uri,
    validate_gb_lsoa_name,
    validate_gb_msoa_name,
    validate_gb_proclass_code,
    validate_gb_sic_code,
    validate_gb_spend_body,
    validate_gb_usrn,
    validate_org_id_or_360g,
    validate_school_name,
    validate_symbol_amount,
)
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (validate_gb_lsoa_name, ["Cambridge 001A", "City of London 001C", "Kingston upon Hull, City of 001A",
                             "King's Lynn and West Norfolk 012B", "Calderdale 019E"],
     ["Leicester 003", "PE 004A-Barnack", "E01000001", "Lenzie North - 07", "cambridge 001A", ""]),
    (validate_gb_msoa_name, ["Leicester 003", "Barking and Dagenham 001", "City of London 001"],
     ["Cambridge 001A", "Brighouse", "Belgrave South", "E02000001", ""]),
    (validate_gb_area_name, ["Calderdale", "Barking and Dagenham", "Hampshire County Council", "Holborn and St Pancras", "FOYLE",
                             "Glasgow City", "Ynys Môn"],
     ["E14000614", "E06000001", "CMK", "37", "302", "Total", "England", "99.99", ""]),
    (validate_gb_usrn, ["44100754", "20001350", 44100754], ["20006", "441007540", "04410075", "E0500002", ""]),
    (validate_school_name, ["Abbey Park Academy", "St Malachy's Catholic Primary School", "BEYA", "Akiva School"],
     ["5406", "Yes", "1", "school", "101251", ""]),
    (validate_gb_brownfield_planning_status, ["permissioned", "Not Permissioned", "Pending decision", "not permissioned"],
     ["Expired", "Permission granted", "FUL", "Permisioned", ""]),
    (validate_gb_brownfield_ownership_status, ["not owned by a public authority", "Owned by a public authority.", "Mixed ownership",
                                               "unknown ownership", "Not Owned by a Public Authority"],
     ["Mixed", "Private", "owned", ""]),
    (validate_gb_brownfield_permission_type, ["full planning permission", "Reserved matters approval", "other", "permission in principle",
                                              "Outline planning permission"],
     ["Full Planning", "N/A", "Prior Approval", "Outline permission", ""]),
    (validate_gb_council_tax_band, ["A", "H", "I", "Band D", "d"], ["1", "2", "J", "rep", "AB", ""]),
    (validate_gb_proclass_code, ["271501", "271501-Information Communication Technology : Services",
                                 "321000  Social Community Care Supplies & Services", 389999],
     ["SOCIAL CARE SERVICES : Adult", "27150", "2715011", "271501 2", "071501", ""]),
    (validate_gb_sic_code, ["62020", "74990 - Non-trading company", "25.62", "74.90/9", "4525 - Other special trades", "62020,\n70229",
                            "9999 - Dormant company", "01110"],
     ["None Supplied", "Manufacturing", "123", "620200", "E38000025", ""]),
    (validate_gb_crs_code, ["HFX", "BHM", "PAD"], ["16107", "Hfx", "HFXX", "HF", ""]),
    (validate_gb_esd_service_uri, ["http://id.esd.org.uk/service/646", "https://id.esd.org.uk/service/1601"],
     ["http://opendatacommunities.org/def/concept/finance", "132A", "http://standards.esd.org.uk/?uri=service%2F579",
      "http://id.esd.org.uk/list/services", ""]),
    (validate_gb_360giving_id, ["360G-indigotrust:IND296", "360G-dulverton-006D000000MJrGZ", "360G-BarnetCouncil-ORG:137",
                                "360G-xyztrust-123_ABC"],
     ["GB-CHC-1131948", "360G", "360G-", "Transparency Aug 01", ""]),
    (validate_org_id_or_360g, ["GB-CHC-1131948", "GB-LAE-BNE", "360G-indigotrust", "GB-COH-01234567"], ["1131948", "Indigo Trust", ""]),
    (validate_gb_spend_body, ["Department for Transport", "DFID", "MoJ HQ", "Communities & Local Government", "HM Treasury"],
     ["T1", "T10", "1", "37", "True", "False", ""]),
    (validate_symbol_amount, ["£37,350.00", "-£1,917.95", "£0", "(£250.00)", "€ 1,200", "$15.5m", "£0.00", "£167,711,343.64", "£-250"],
     ["37,350.00", "£145,000 - £149,999", "£", "Nil Return", "£1,2", "1,200 €", ""]),
    (validate_fr_elec_filiere_code, ["SOLAI", "HYDLQ", "EOLIE", "THERM", "NUCLE", "BIOEN"], ["Solaire", "GAZ", "SOLAIR", "solai", ""]),
    (validate_fr_elec_code, ["GAZ", "FIOUL", "D.MEN", "PHOTV", "FIL.E", "LAC", "FIOUL,GAZ", "COG.V", "D.IND,GAZ"],
     ["Gaz", "Photovoltaïque", "G", "F.", "1", ""]),
    (validate_fr_pacage, ["02B003120", "02A000444", "014001234", "974000123", 14001234],
     ["2B003120", "02C003120", "0020031200", "000003120", "099", ""]),
    (validate_eunis_habitat_code, ["A5.535", "A3.23", "A5.5352", "G1.A1", "B1", "X09", "A1.44"],
     ["Pas de correspondance", "1170", "A", "K1.1", "a5.535", "III.6.1.", ""]),
    (validate_eu_habitat_type_code, ["1170", "91E0", "8330", "1120*", "91e0"], ["1170-13", "A5.535", "Pas de correspondance", "0170", ""]),
    (validate_eu_natura2000_site, ["FR9400570", "DE7820341", "DK00FX005"], ["BG1", "H", "UK11007", "fr9400570", "XX9400570", ""]),
    (validate_fr_budget_section, ["Fonctionnement", "INVESTISSEMENT", "investissement", "F", "I"], ["ANGLAIS", "Section 52", "A", "Recettes", ""]),
    (validate_fr_budget_sens, ["Dépenses", "dépense", "Recettes", "recette", "DEPENSES", "D", "R"],
     ["Double sens", "E-O", "1", "Fonctionnement", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ + str(i) for i, v in enumerate(VALIDATORS)])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("gb/gb_geo.yaml", "gblsoanamebyname", ["LSOA name", "LSOA11NM", "lsoa_name", "LSOA name (2011)", "2011 LSOA name",
                                            "Calderdale LSOA name (2021)", "lsoa01nm", "LSOA 2011 name", "lsoa", "lsoa_name_2011"],
     ["lsoa code", "LSOA11CD", "msoa name", "lsoa population"]),
    ("gb/gb_geo.yaml", "gbmsoanamebyname", ["MSOA name", "MSOA11NM", "msoa_name", "msoa21nm", "msoa"],
     ["msoa code", "MSOA11CD", "msoa11hclnm", "lsoa name"]),
    ("gb/gb_geo.yaml", "gblocalauthoritynamebyname", ["Local authority", "local_authority", "Local authority name", "LA name", "laname",
                                                      "LAD11NM", "lad20nm", "Local authority district"],
     ["authority", "local authority code", "LAD11CD", "la code", "planning authority"]),
    ("gb/gb_geo.yaml", "gbparliamentaryconstituencybyname", ["Parliamentary constituency", "UK constituency", "PCON17NM",
                                                             "parliamentary constituency name", "Westminster constituency"],
     ["constituency", "EU constituency", "PCON17CD", "constituency code"]),
    ("gb/gb_geo.yaml", "gbusrnbyname", ["USRN", "usrn", "street_usrn"], ["uprn", "usrn_description", "street"]),
    ("gb/gb_geo.yaml", "ukgsscodeundercode", ["Code", "area_code", "Area code", "geography_code", "gss_code", "geocode",
                                              "areacode", "LSOA code (2021)", "2011 LSOA"],
     ["postcode", "ward name", "area", "code description", "site code", "ONS code", "LA code"]),
    ("gb/gb_realestate.yaml", "gbbrownfieldplanningstatusbyname", ["PlanningStatus", "planning_status", "Planning status"],
     ["PlanningHistory", "status", "OwnershipStatus"]),
    ("gb/gb_realestate.yaml", "gbbrownfieldownershipstatusbyname", ["OwnershipStatus", "ownership_status", "Ownership status"],
     ["ownership", "PlanningStatus"]),
    ("gb/gb_realestate.yaml", "gbbrownfieldpermissiontypebyname", ["PermissionType", "permission_type", "Permission type"],
     ["PermissionDate", "type"]),
    ("gb/gb_realestate.yaml", "gbcounciltaxbandbyname", ["Council Tax Band", "council_tax_band", "CouncilTaxBand", "CT band"],
     ["band", "salary band", "% dwellings in council tax bands a or b"]),
    ("gb/gb_finances.yaml", "gbproclasscodebyname", ["Pro Class", "ProcurementClassification:ProClassCode",
                                                    "ProcrementClassification:ProClassCode", "proclass", "ProClass Category",
                                                    "Procurement category (ProClass)"],
     ["class", "procurement category", "process used"]),
    ("gb/gb_finances.yaml", "gb360givingorgidbyname", ["Recipient Org:Identifier", "Funding Org:Identifier", "RECORGIDENTIFIER", "FUNDINGORGIDENTIFIER"],
     ["Identifier", "Recipient Org:Name", "Recipient Org:Charity Number"]),
    ("gb/gb_finances.yaml", "gbspendbodybyname", ["Department family", "Departmental Family", "Entity", "department_family"],
     ["Department", "Entity type", "family", "Expense area"]),
    ("gb/gb_finances.yaml", "gbspendexpenseareabyname", ["Expense area", "expense_area", "Expenses Area"],
     ["Expense type", "area", "Expense area code"]),
    ("gb/gb_orgs.yaml", "gbsiccodebyname", ["SIC code", "SIC", "siccodes", "SICCode.SicText_1", "2007 SIC code(s)", "SIC 2007", "uk sic code"],
     ["SIC code title", "sic description", "sicbl", "basic", "music"]),
    ("gb/gb_transport.yaml", "gbcrscodebyname", ["TLC", "CRS", "CRS code", "three letter code", "station_crs", "3 alpha code"],
     ["station name", "NLC", "crs purpose code", "stationcode"]),
    ("common/education.yaml", "schoolnamebyname", ["School", "School name", "school_name", "SchoolName", "Name of school"],
     ["school type", "schools", "school code", "school year", "pschoolname1"]),
    ("fr/fr_environment.yaml", "frelecfilierecodebyname", ["codeFiliere", "code_filiere", "codefiliere", "code_filiere_de_production"],
     ["filiere", "libelle_filiere", "codecombustible"]),
    ("fr/fr_environment.yaml", "freleccombustiblecodebyname", ["codeCombustible", "codescombustiblessecondaires", "code_combustible"],
     ["combustible", "combustiblessecondaires", "codefiliere"]),
    ("fr/fr_environment.yaml", "frelectechnologiecodebyname", ["codeTechnologie", "code_technologie"], ["technologie", "codefiliere"]),
    ("fr/fr_environment.yaml", "frpacagebyname", ["pacage", "PACAGE", "num_pacage", "numero_pacage", "n_pacage"], ["cheptel", "ilot", "pacages"]),
    ("fr/fr_environment.yaml", "frsandrecourseaubyhydroname", ["code_hydro", "codehydro", "cgenelin", "code_h", "codhydro"],
     ["toponyme", "code", "hydro"]),
    # the keys of the budgets of the City of Paris
    ("fr/fr_budget.yaml", "frbudgetchapitrecodebyname", ["chapitre_budgetaire_cle"], ["chapitre_budgetaire_texte"]),
    ("fr/fr_budget.yaml", "frbudgetnaturecodebyname", ["nature_budgetaire_cle"], ["nature_budgetaire_texte"]),
    ("fr/fr_budget.yaml", "frbudgetfonctioncodebyname", ["fonction_cle"], ["fonction_texte"]),
    ("fr/fr_budget.yaml", "frbudgetsectionbyname", ["section", "BGT_SECTION", "section_budgetaire", "section_budgetaire_i_f"],
     ["section_cnu", "c_sec", "sections"]),
    ("fr/fr_budget.yaml", "frbudgetsensbyname", ["sens", "BGT_CODRD", "sens_depense_recette", "depense_recette", "Dépenses/Recettes"],
     ["sens_circulation", "recettes", "depenses"]),
    ("eu/eu_geo.yaml", "eunishabitatcodebyname", ["cod_eunis", "code_eunis", "eunis", "EUNIS code", "cod_eunis2", "eunis1"],
     ["lib_eunis", "lib_eunis2", "eunis_name"]),
    ("eu/eu_geo.yaml", "euhabitattypecodebyname", ["cod_eur27", "code_eur28", "eur27", "code_natura2000", "cod_eur"],
     ["lib_eur27", "cod_eunis", "eur", "cod_ch2004"]),
    ("eu/eu_geo.yaml", "eunatura2000sitebyname", ["cod_site", "sitecode", "site_code", "code_site", "SITECODE", "code_n2000"],
     ["site", "nom_site", "site_name", "code"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_names(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("gb/gb_geo.yaml", "gblsoanamevalue", ["Cambridge 001A", "Barking and Dagenham 001B"], ["Leicester 003", "E01000001", "12 High Street"]),
    ("gb/gb_realestate.yaml", "gbbrownfieldownershipstatusvalue", ["not owned by a public authority", "Mixed ownership"],
     ["Mixed", "owned by the council"]),
    ("gb/gb_finances.yaml", "gb360givingidvalue", ["360G-indigotrust:IND296", "360G-xyztrust-123"], ["GB-CHC-1131948", "360G"]),
    ("gb/gb_orgs.yaml", "gbesdserviceurivalue", ["http://id.esd.org.uk/service/646"], ["http://id.esd.org.uk/list/services",
                                                                                     "http://opendatacommunities.org/def/concept/finance"]),
    ("common/values.yaml", "moneywithsignvalue", ["£37,350.00", "-£1,917.95", "£0"], ["37,350.00", "£145,000 - £149,999", "Nil Return"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def test_lsoa_and_msoa_code_rules_need_gss_codes():
    """An LSOA or MSOA column of names (Cambridge 001A, Leicester 003) is no column of codes."""
    for rule_id in ("uksloafield", "ukmsoafield"):
        spec = load("gb/gb_geo.yaml", rule_id)
        assert spec["validator"].endswith("validate_gss_code") and spec["needs_values"]
        assert not [name for name in spec["rule"].split(",") if "name" in name]
