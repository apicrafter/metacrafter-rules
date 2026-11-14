"""Rules for the data.gov.au files of metacrafter-testdata (a snapshot of the Australian national open
data portal): IP Australia numbers and IPC symbols of IPGOD, ANZSIC and ANZSCO codes of the ATO
taxation statistics, ABS geography (SA2, LGA, GCCSA, Remoteness Areas, federal electoral divisions),
ORIC, ASIC, Standards Australia and PBS codes, financial years, months and quarters with their year,
money ranges; and rules for the registry types Australian state codes, suburbs, ACN, CAS Registry
Numbers, PCT / WO numbers and UPOV codes, which had none.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.au.codes import (
    validate_au_abn,
    validate_au_abn_or_acn,
    validate_au_acn,
    validate_au_anzsco_code,
    validate_au_anzsco_titled,
    validate_au_anzsic_code,
    validate_au_asic_licence_number,
    validate_au_federal_electoral_division,
    validate_au_gccsa_code,
    validate_au_icn,
    validate_au_lga_code,
    validate_au_lga_name,
    validate_au_lga_name_plain,
    validate_au_patent_application_number,
    validate_au_pbr_application_number,
    validate_au_pbs_item_code,
    validate_au_postcode,
    validate_au_remoteness_area,
    validate_au_sa2_code,
    validate_au_standard_designation,
    validate_au_state_code,
    validate_au_trademark_number,
)
from metacrafterext.rules.common.chemistry import validate_casrn
from metacrafterext.rules.common.software import validate_datasize_value
from metacrafterext.rules.common.periods import (
    validate_fiscal_year,
    validate_fiscal_year_short,
    validate_ipc_code,
    validate_ipc_group,
    validate_money_range,
    validate_not_yearmonth,
    validate_pct_application_number,
    validate_upov_code,
    validate_wo_publication_number,
    validate_year_quarter,
    validate_yearmonth_english,
)
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (validate_fiscal_year, ["2014-15", "2010–11", "1999-00", "2014/15", "2014-2015", "2010/2011", "FY201213", "FY2014-15"],
     ["2014-16", "2014-12", "2014", "2019-2021", "15-16", "2014-Q1"]),
    (validate_fiscal_year_short, ["2014-15", "1999-00", "FY201213", "FY 2014-15"], ["2014-2015", "2010/2011", "2014"]),
    (validate_yearmonth_english, ["Sep-17", "Aug-2011", "June 2014", "Jan 1841", "Sept-17"],
     ["17-Sep", "2017-09", "September", "Sep 2017 to Dec 2017"]),
    (validate_not_yearmonth, ["7", "07", "July", "Juli", "Июль"], ["Jul-19", "2019-07", "July 2019", "Aug-2011"]),
    (validate_year_quarter, ["2021Q04", "2022Q03", "2021-Q4", "2021 Q4", "Q4 2021"], ["2021Q5", "Q4", "4", "2021-04"]),
    (validate_money_range, ["$100K - $5m", "< $100K", "> $2.5m", "$100K - < $5m", "b. $18,201 to $37,000",
                            "a. 10,000 to less than 50,000", "$0-$49999", "Equal to or greater than $25,001",
                            "e. Refund between $2,000 and $3,999", "Loss/nil", "a. Less than $0", "Up to $185,000"],
     ["0", "25", "$5,000", "18-24", "5-24", "Micro", "1,234", "593244"]),
    (validate_ipc_code, ["A47G  23/02", "A47G23/02", "G06Q 90/00", "F21M    3/04", "H04L"], ["I01B 1/00", "A47G 23", "A4", "47"]),
    (validate_ipc_group, ["A47G  23/02", "B29C  51/16"], ["H04L", "A47G"]),
    (validate_pct_application_number, ["PCT/AU1980/000001", "PCT/AU80/00001", "PCT/US95/03744"], ["PCT/AU1980/1", "AU1980/000001"]),
    (validate_wo_publication_number, ["WO1980/002164", "WO80/02164", "WO 2004/012345 A1"], ["WO", "1980/002164"]),
    (validate_casrn, ["75-07-0", "64-19-7", "67-64-1", "7732-18-5"], ["75-07-1", "0075-07-0", "75070"]),
    (validate_upov_code, ["SOLAN_LYC", "LILIU", "PRUNU_PER_NUC", "OCIMU_BAS"], ["Lilium", "LIL", "solan_lyc"]),
    (validate_au_patent_application_number, ["2005249605", "1980059801", "59801/80", "1997PP7450", "AU 2005249605",
                                             "2002100537.0"],
     ["200524960", "3005249605", "1998/163", "PP7450"]),
    (validate_au_trademark_number, ["1", "268967", "1153388"], ["0", "12345678", "TM1"]),
    (validate_au_pbr_application_number, ["1998/163", "2019/226", "2002/091"], ["98/163", "59801/80", "1998/1630"]),
    (validate_au_anzsic_code, ["011", "0111", "01110", "A", "011 Nursery and Floriculture Production",
                               "A.Agriculture, Forestry and Fishing", "01110 Nursery Production (Under Cover)"],
     ["T", "1", "Agriculture", "011.1"]),
    (validate_au_anzsco_code, ["1111", "111111", "1111 Chief Executives and Managing Directors"], ["9100", "12345", "Teacher"]),
    (validate_au_anzsco_titled, ["1111 Chief Executives and Managing Directors",
                                 "111111 Chief executive or managing director",
                                 "1100 Chief Executives, General Managers and Legislators - type not specified"],
     ["1111", "Managers", "9100 Something"]),
    (validate_au_sa2_code, ["107031142", "120021388", "11001"], ["007031142", "1070311", "SA2"]),
    (validate_au_lga_code, ["10050", "24600", "16900"], ["357", "01005", "100500"]),
    (validate_au_lga_name, ["Albury (C)", "Kangaroo Island (DC)", "Kingston (C) (Vic.)", "The Hills Shire (A)"],
     ["Golden Plains Shire", "Albury", "Maroondah (C); Knox (C)"]),
    (validate_au_lga_name_plain, ["Albury (C)", "Gympie", "Norwood Payneham St Peters"], ["10050", "Division 1", "1"]),
    (validate_au_gccsa_code, ["1GSYD", "1RNSW", "8ACTE", "9OTER", "7gdar"], ["9GSYD", "1GSY", "ACT"]),
    (validate_au_remoteness_area, ["Major Cities of Australia", "Inner Regional Australia", "Very Remote", "Major_cities",
                                   "Outer_regional"],
     ["Regional", "Rural", "Major City"]),
    (validate_au_federal_electoral_division, ["Banks", "Kingsford Smith", "Eden-Monaro", "O'Connor", "O’Connor", "Macnamara"],
     ["Division 1", "Total", "Unknown", "Sydney City"]),
    (validate_au_icn, ["2", "1700", "9999"], ["0", "170200", "ICN"]),
    (validate_au_asic_licence_number, ["218600", "AFSL 218600", "ACL 389328"], ["21860", "2186001", "AR 13843"]),
    (validate_au_standard_designation, ["AS/NZS 4847.1:2010", "AS 1056.1", "NZS 4606.1-1989", "AS/NZS 2040.1:2005/Amdt 3:2010",
                                        "AS/NZS 4692.1:2005 + A1", "AS/NZS ISO 9001:2016"],
     ["ISO 9001:2015", "JIS B 8615-1", "AS", "N/A"]),
    (validate_au_pbs_item_code, ["01002R", "1001Q", "11124L", "48M"], ["23", "1001", "AB12"]),
    (validate_au_state_code, ["NSW", "Qld", "vic", "ACT", "WA"], ["CA", "New South Wales", "NY", "N/A"]),
    (validate_datasize_value, ["2048", "1.5", "100 MB", "5.2GB"], ["Large", "Medium", "Not Sized"]),
    (validate_au_acn, ["004085616", "008984049", "2399653", "103234448"], ["123456789", "0", "ABC"]),
    (validate_au_abn, ["51824753556", "51 824 753 556", "85007186003", "45449518275"], ["12345678901", "004085616", "05007186003"]),
    (validate_au_abn_or_acn, ["85007186003", "004085616"], ["12345678901", "ABC"]),
    (validate_au_postcode, ["2000", "0871", "871", "6517"], ["12", "10000", "ABCD", "0100"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("common/periods.yaml", "fiscalyearbyname",
     ["Financial Year", "Financial_Year", "financial_year", "Income year", "Water Year", "Financial Year Start", "FY",
      "first_reporting_year", "report_year"],
     ["Year", "Calendar Year", "year_of_act", "school_year"]),
    ("common/legal.yaml", "ipccodebyname",
     ["ipc_mark_value", "edited_ipc_mark_value", "primary_ipc_mark", "ipc", "ipc_code", "primary_ipc"],
     ["ipc_class_version_date", "ipc_mark_type_code", "class_code"]),
    ("common/chemistry.yaml", "casrnbyfieldname", ["cas_registry_numbers", "CAS number", "cas_rn", "casrn", "CAS"],
     ["case_number", "cash", "castle"]),
    ("common/science.yaml", "upovcodebyname", ["upov_code", "upov"], ["upov_name", "code"]),
    ("common/values.yaml", "moneyrangebyname",
     ["Taxable income range - tax brackets", "Total income or loss range", "Taxable or net income range",
      "Total Income 2019/20", "Total Assets 2021/22", "Total Income", "turnover", "Debtor Income", "Unsecured Debts",
      "Value of Assets", "Grant Value", "Total income ranges"],
     ["Income year", "Taxable status", "Number of individuals", "Industry"]),
    ("au/au_geo.yaml", "austatecodebyname",
     ["State", "State/Territory", "Jurisdiction", "AFS_LIC_ADD_STATE", "StateOrTerritory", "state_abb", "Head Office State",
      "state_or_territory", "address_state_code", "State/Territory of rental property", "jurisdiction_code"],
     ["Statement", "Status", "estate"]),
    ("au/au_geo.yaml", "ausuburbbyname",
     ["Suburb", "SUBURB", "suburb_name", "Suburb/Town", "B_Suburb", "supplier_suburb", "AFS_LIC_ADD_LOCAL", "Town/City",
      "Street Suburb"],
     ["Suburbs count", "Locality code", "town"]),
    ("au/au_geo.yaml", "ausa2codebyname", ["sa2_code", "sa2_main11", "SA2_5digitcode_2011", "SA2_MAINCODE_2016"],
     ["sa2_name", "sa2_name11", "SA2"]),
    ("au/au_geo.yaml", "aulgacodebyname", ["lga_code", "LGA_Code_2020", "LGA_Code_2018", "PR_LGAC"], ["lga_name", "LGA"]),
    ("au/au_geo.yaml", "aulganamebyname",
     ["lga_name", "LGA_NAME_2020", "LGA_name_2018", "lga11_name", "National LGA Name 2021", "LGA"],
     ["lga_code", "LGA_Code_2020"]),
    ("au/au_geo.yaml", "augccsacodebyname", ["gcc_code11", "GCCSA Code of Debtor", "gccsa_code"], ["gcc_name11", "GCCSA of Debtor"]),
    ("au/au_geo.yaml", "auremotenessbyname",
     ["Remoteness area", "National Remoteness Areas", "regional_area", "Remoteness"], ["Region", "asgs_code"]),
    ("au/au_geo.yaml", "aufederalelectoraldivisionbyname",
     ["elect_div", "ced_name_2013", "commonwealth_electoral_divisio00", "Electoral Division", "Electorate"],
     ["ced_code", "Division", "elections"]),
    ("common/geo.yaml", "suburbbyname", ["Suburb", "SUBURB", "suburb_name", "Street Suburb", "Head Office Suburb"],
     ["Suburb/Town", "suburbanisation"]),
    ("common/geo.yaml", "towncitybyname", ["TOWN/CITY", "Town/City", "Suburb/Town"], ["town", "city"]),
    ("au/au_finances.yaml", "auacnbyname", ["acn", "ACN", "company_acn", "AFS_LIC_ABN_ACN", "CRED_REP_ABN_ACN"],
     ["acnc_registered", "ACNC Registered"]),
    ("au/au_finances.yaml", "auabnacnbyname", ["AFS_LIC_ABN_ACN", "CRED_REP_ABN_ACN", "Supplier ABN", "abn"], ["abnormal", "cabn"]),
    ("au/au_geo.yaml", "aupostcodebyname", ["Post Code", "AFS_LIC_ADD_PCODE", "CRED_REP_PCODE", "postal_code", "postcode"],
     ["post", "code", "pcode_name"]),
    ("au/au_finances.yaml", "auasiclicencebyname", ["AFS_LIC_NUM", "CRED_LIC_NUM", "AFSL number", "afsl"],
     ["CRED_REP_NUM", "licence_number"]),
    ("au/au_finances.yaml", "auicnbyname", ["ICN", "icn"], ["icon", "acn"]),
    ("au/au_legal.yaml", "aupatentapplicationbyname",
     ["australian_appl_no", "application_number", "conv_to_appl_number", "old_patent_appl_no", "conv_from_appl_number",
      "old_conv_from_appl_number", "PATENT_PUBLICATION_NUMBER", "earliest_patent", "latest_patent"],
     ["wipo_appl_no", "pct_appl_no", "application_id"]),
    ("au/au_legal.yaml", "aupbrapplicationbyname", ["application_number", "appl_number", "pbr_app"], ["application_id"]),
    ("au/au_legal.yaml", "autrademarknumberbyname", ["tm_number", "trade_mark_number", "TRADEMARK_APP"], ["tm_name"]),
    ("au/au_industry.yaml", "auanzsicbyname",
     ["primary_anzsic_class_code", "anzsic_code", "Fine industry", "Finer industry", "Finer  industry", "Broad industry",
      "broad_industry3"],
     ["Industry", "industry_sector"]),
    ("au/au_industry.yaml", "auanzscobyname",
     ["Occupation", "anzsco_code", "Debtor Occupation Code (ANZSCO)", "anzsco_unit_group"], ["occupational_group_name"]),
    ("au/au_industry.yaml", "austandarddesignationbyname",
     ["N-Standard", "N-Standard_MEPS", "What test standard was used"], ["standard_deviation_value"]),
    ("au/au_medical.yaml", "aupbsitemcodebyname", ["item_code", "Item_number", "pbs_item"], ["item_name", "items"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("common/periods.yaml", "fiscalyearvalue", ["2014-15", "2010–11", "FY201213"], ["2014-2015", "2014"]),
    ("common/periods.yaml", "yearmonthenglishvalue", ["Sep-17", "Aug-2011"], ["17-Sep", "2017-09"]),
    ("common/periods.yaml", "yearquartervalue", ["2021Q04", "2021 Q4"], ["2021Q5", "Q4"]),
    ("common/legal.yaml", "ipccodevalue", ["A47G  23/02", "A47G23/02"], ["H04L"]),
    ("common/legal.yaml", "pctapplicationnumbervalue", ["PCT/AU1980/000001"], ["PCT/AU1980/1"]),
    ("common/legal.yaml", "wopublicationnumbervalue", ["WO1980/002164"], ["WO"]),
    ("au/au_geo.yaml", "aulganamevalue", ["Albury (C)"], ["Albury"]),
    ("au/au_geo.yaml", "augccsacodevalue", ["1GSYD"], ["1GSY"]),
    ("au/au_geo.yaml", "auremotenessvalue", ["Inner Regional Australia"], ["Regional"]),
    ("au/au_industry.yaml", "austandarddesignationvalue", ["AS/NZS 4847.1:2010"], ["ISO 9001:2015"]),
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
        assert spec.get("validator"), rule_id
        assert spec.get("needs_values") is True, rule_id


def test_month_rules_refuse_months_with_years():
    for rule_id in ("monthknown", "monthknownpat"):
        assert load("common/dateandtime.yaml", rule_id)["validator"].endswith("validate_not_yearmonth"), rule_id
