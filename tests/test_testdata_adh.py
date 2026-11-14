"""Rules for the Africa Data Hub files of metacrafter-testdata (a 2024 snapshot of the CKAN portal
ckan.africadatahub.org): ISO country codes in fields named after ISO, IMF, WHO and Our World in Data
codes, Google place ids, EM-DAT and GLIDE disaster numbers, compact dates, South African province
codes, SARS-CoV-2 lineages and WHO labels, COVID-19 vaccine names and HXL hashtags.

Matched as tests/test_testdata_baseline.py matches them; fieldregex guards are searched in the short
field name without regard to case, as metacrafter does.
"""
import re

import pytest

from metacrafterext.rules.common.statcodes import (
    validate_date_ymd_compact,
    validate_emdat_disaster_number,
    validate_hxl_hashtag,
    validate_imf_country_code,
    validate_imf_indicator_code,
    validate_longitude_long_name,
    validate_who_gho_indicator_code,
)
from tests.test_testdata_baseline import field_matches, guarded_by, load, value_matches

VALIDATORS = [
    (validate_imf_country_code, ["111", "512", "914", "199", "612.0"], ["001", "USA", "1111", "11", "", "abc"]),
    (validate_imf_indicator_code,
     ["PCPI_IX", "PCPI_PC_CP_A_PT", "PCPIF_PC_PP_PT", "PCPIHO_PC_PP_PT", "NGDP_XDC", "ENDA_XDC_USD_RATE", "LUR_PT"],
     ["NY.GDP.MKTP.CD", "SI_POV_DAY1", "MALARIA_EST_DEATHS", "PCPIPCH", "pcpi_ix", "Consumer Price Index", ""]),
    (validate_who_gho_indicator_code,
     ["MALARIA_EST_DEATHS", "WHOSIS_000001", "MDG_0000000001", "NCD_BMI_30A", "M_Est_cig_curr", "SDGPM25"],
     ["malaria", "Estimated number of malaria deaths", "12345", "MALARIA EST", ""]),
    (validate_hxl_hashtag,
     ["#date", "#country+code", "#adm1+name", "#affected+infected", "#geo +lat", "#Org+Name"],
     ["#COVID19", "#tbt", "country+code", "#country code", "#", ""]),
    (validate_emdat_disaster_number, ["2020-0218", "1993-0500-CMR", " 2020-0022-BRA"], ["2020-218", "1993-0500-cmr", ""]),
    (validate_date_ymd_compact, ["20200305", " 20200524", "19991231", "20200305.0"],
     ["20201305", "20200230", "2020035", "18991231", "21000101", "2020-03-05", ""]),
    (validate_longitude_long_name, ["67.709953", "-63.6167", "1.6596", "-179.999"],
     ["12", "-71.0", "20.15", "181.123", "long", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("common/intcodes.yaml", "imfcountrycodebyname",
     ["WEO Country Code", "weo_country_code", "IMF Country Code", "imf_code", "IFS Code", "ifs_code"],
     ["Country Code", "country", "WEO Subject Code", "code"]),
    ("common/intcodes.yaml", "imfindicatorcodebyname",
     ["Indicator Code", "Indicator.Code", "indicator_code", "series_code", "IMF indicator"],
     ["IndicatorCode", "Indicator", "Indicator Name", "code"]),
    ("common/intcodes.yaml", "whoghoindicatorcodebyname", ["IndicatorCode", "GHO_CODE", "gho_indicator"],
     ["Indicator Code", "Indicator", "indicator_name"]),
    ("common/geo.yaml", "longitudebylongname", ["Long", "Long_", "long"], ["Longueur", "long_name", "Lat"]),
    ("common/environment.yaml", "emdatdisasternumberbyname", ["Dis No", "DisNo.", "disno", "emdat_id"],
     ["number", "dis", "no"]),
    ("common/dateandtime.yaml", "dateymdcompactbyname", ["YYYYMMDD", " YYYYMMDD".strip(), "date_yyyymmdd", "AAAAMMJJ"],
     ["date", "yyyy", "mm", "date_received"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


def test_field_rules_need_values():
    for path, rule_id, _, _ in FIELDS:
        spec = load(path, rule_id)
        assert spec.get("validator") and spec.get("needs_values") is True, rule_id


VALUES = [
    ("common/intcodes.yaml", "iso3166alpha3byisofield", ["DZA", "AGO", "SSD", "XKX", "cuw"], ["OWID_AFR", "EUR", "GHAN"]),
    ("common/intcodes.yaml", "iso3166alpha2byisofield", ["DZ", "AO", "XK", "ss"], ["UK", "EU", "DZA"]),
    ("common/intcodes.yaml", "imfweosubjectcodevalue", ["NGDP_R", "PCPIPCH", "LUR", "GGXWDG_NGDP"],
     ["PCPI_IX", "NY.GDP.MKTP.CD", "GDP"]),
    ("common/intcodes.yaml", "whoregioncodevalue", ["AFR", "AMR", "SEAR", "EUR", "EMR", "WPR"], ["AFRO", "EURO", "SA"]),
    ("common/intcodes.yaml", "owidentitycodevalue", ["OWID_AFR", "OWID_WRL", "OWID_KOS", "OWID_EUN"],
     ["AFG", "OWID_", "OWID_africa", "OWID_ABCDE"]),
    ("common/environment.yaml", "emdatdisasternumbervalue", ["2020-0218", "1993-0500-CMR", "2020-0022-BRA"],
     ["2020-218", "EQ-2010-000009-HTI", "2020-02-18"]),
    ("common/environment.yaml", "glidenumbervalue", ["EQ-2010-000009-HTI", "TC-2005-000144-USA", "FL-2016-000121----"],
     ["EQ-2010-9-HTI", "XX-2010-000009-HTI", "2020-0218"]),
    ("common/geo.yaml", "googleplaceidvalue", ["ChIJN1t_tDeuEmsRUsoyG83frY4", "ChIJvRKrsd9IXj4RpwoIwFYv0zM"],
     ["ChIJN1t_tDeuEmsRUsoy", "GhIJN1t_tDeuEmsRUsoyG83frY4", "ChIJN1t_tDeuEmsRUsoyG83frY4x"]),
    ("common/medical.yaml", "pangolineagevalue", ["B.1.1.7", "B.1.617.2", "P.1", "B.1.1.529", "BA.2.86", "XBB.1.5", "A", "B"],
     ["P1", "501Y.V2", "Variant 501.Y.V1 or B.1.1.7", "20I", "b.1.1.7"]),
    ("common/medical.yaml", "sarscov2variantlabelvalue", ["Alpha", "Delta", "Omicron", "omicron", "Mu"],
     ["Nu", "Xi", "Delta Plus", "B.1.1.7"]),
    ("common/medical.yaml", "covid19vaccinevalue",
     ["Pfizer-BioNTech", "Oxford-AstraZeneca", "Johnson & Johnson", "Sputnik V", "Covaxin", "Pfizer/BioNTech",
      "Sinopharm", "Nuvaxovid", "Vaxzevira", "ZF2001"],
     ["unknown", "BNT162 (3 LNP-mRNAs )", "Serum Institute of India", "Oxford-AstraZenec"]),
    ("common/texts.yaml", "hxlhashtagvalue", ["#country+code", "#affected+infected", "#date"], ["#COVID19", "country+code"]),
    ("za/za_geo.yaml", "zaprovincecodevalue", ["EC", "GP", "GT", "KZN", "wc"], ["NL", "NP", "ZA", "KZ"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def _regex_guard(path, rule_id, name):
    spec = load(path, rule_id)
    return re.search(spec["fieldregex"], name.rsplit(".", 1)[-1].strip(), re.IGNORECASE) is not None


GUARDS = [
    ("common/intcodes.yaml", "iso3166alpha3byisofield", guarded_by,
     ["iso_code", "ISO", "ISO_3", "iso3", "SpatialDimValueCode", "Geography", "adm0_a3"], ["code", "country_name", "isin"]),
    ("common/intcodes.yaml", "iso3166alpha2byisofield", guarded_by, ["ISO_2", "iso2", "iso_a2"], ["iso", "code"]),
    ("common/intcodes.yaml", "imfweosubjectcodevalue", _regex_guard, ["WEO Subject Code", "series", "Indicator"],
     ["code", "Scale", "Units"]),
    ("common/intcodes.yaml", "whoregioncodevalue", _regex_guard, ["ParentLocationCode", "WHO region", "who_region_code"],
     ["currency", "region", "ParentLocation"]),
    ("common/environment.yaml", "emdatdisasternumbervalue", _regex_guard, ["Dis No", "emdat_id", "disaster_number"],
     ["case_number", "id"]),
    ("common/medical.yaml", "pangolineagevalue", _regex_guard, ["pango_lineage", "lineage", "variant"], ["section", "version"]),
    ("common/medical.yaml", "sarscov2variantlabelvalue", _regex_guard, ["variant_name", "WHO label"], ["release", "stage"]),
    ("common/medical.yaml", "covid19vaccinevalue", _regex_guard, ["common_name", "vaccine", "vaccines", "manufacturer"],
     ["supplier_name", "company"]),
    ("za/za_geo.yaml", "zaprovincecodevalue", _regex_guard, ["Geography", "province", "prov_code", "region"],
     ["country", "code", "iso2"]),
]


@pytest.mark.parametrize("path,rule_id,check,good,bad", GUARDS, ids=[g[1] for g in GUARDS])
def test_guards(path, rule_id, check, good, bad):
    for name in good:
        assert check(path, rule_id, name), name
    for name in bad:
        assert not check(path, rule_id, name), name


def test_new_value_rules_without_guard_are_distinctive():
    # OWID codes, place ids, GLIDE numbers and HXL tags are read anywhere: their shapes are their own.
    for path, rule_id in (("common/intcodes.yaml", "owidentitycodevalue"), ("common/geo.yaml", "googleplaceidvalue"),
                          ("common/environment.yaml", "glidenumbervalue"), ("common/texts.yaml", "hxlhashtagvalue")):
        spec = load(path, rule_id)
        assert "fieldrule" not in spec and "fieldregex" not in spec, rule_id
