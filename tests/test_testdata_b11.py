"""Rules for the files of metacrafter-testdata from 2024 snapshots of open data portals and data
repositories (Dateno sources cdi00001098, the Lithuanian Data Archive LiDA; cdi00001115, data.gov.mk;
cdi00001123, the National University of Mongolia; cdi00001190, the IISH Dataverse; cdi00001211, DataverseNO;
cdi00001241 and cdi00001243, data.govt.nz and the Biological Heritage repository of New Zealand; cdi00001247
to cdi00001264, the environment data portals of the Pacific, SPREP; cdi00001288, the Polish National
Institute of Public Health): attributes of the World Database on Protected Areas, Red List population
trends, IBTrACS basins and storm natures, c-squares codes, HISCO and ISCO-88 codes, seasons, case
classifications, Amsterdamse codes, references of the Supreme Court of Norway, Polish voivodeships, regions
of New Zealand, municipalities of North Macedonia and Mongolian days of the week, with the Polish,
Macedonian and Mongolian field names of sex, age group, year, month, phone and name.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.be.codes import validate_be_statistical_sector
from metacrafterext.rules.common import conservation as cons
from metacrafterext.rules.common.epidemiology import validate_case_classification, validate_case_classification_or_none
from metacrafterext.rules.common.periods import validate_season_name
from metacrafterext.rules.common.statcodes import validate_hisco, validate_isco_code
from metacrafterext.rules.common.taxa import validate_higher_taxon_name_any_case
from metacrafterext.rules.es.validators import validate_es_nif
from metacrafterext.rules.mk import codes as mk
from metacrafterext.rules.mn import codes as mn
from metacrafterext.rules.nl.validators import validate_nl_amco
from metacrafterext.rules.no.codes import validate_no_supreme_court_reference
from metacrafterext.rules.nz.codes import validate_nz_region
from metacrafterext.rules.pl import codes as pl
from tests.test_testdata_baseline import field_matches, load

VALIDATORS = [
    (cons.validate_wdpa_governance_type,
     ["Federal or national ministry or agency", "Indigenous peoples", "Collaborative governance", "Not Reported",
      "Non-profit organizations", "local communities"], ["State", "National", "Government", ""]),
    (cons.validate_wdpa_ownership_type, ["State", "Communal", "Joint ownership", "Multiple ownership", "Not Reported"],
     ["Joint governance", "Private", "Indigenous peoples", ""]),
    (cons.validate_wdpa_designation_type, ["National", "International", "Regional", "Not Applicable"],
     ["Marine Sanctuary", "Ramsar Site, Wetland of International Importance", "Local", ""]),
    (cons.validate_wdpa_no_take, ["All", "Part", "None", "Not Reported", "Not Applicable"], ["Yes", "No", "0", ""]),
    (cons.validate_wdpa_verification, ["State Verified", "Expert Verified", "Not Reported"], ["Designated", "Verified", ""]),
    (cons.validate_wdpa_id, ["902678", "555555577", "315565", "18608.0"], ["555624810_1", "0", "COK", "-1", ""]),
    (cons.validate_iucn_population_trend, ["Decreasing", "Increasing", "Stable", "Unknown", "decreasing"],
     ["Vulnerable", "Declining", "Least Concern", ""]),
    (cons.validate_ibtracs_basin, ["SP", "SI", "NA", "EP", "WP", "NI", "SA", "MM"], ["EA", "WA", "sp", "Ashley", "Mataura", ""]),
    (cons.validate_ibtracs_nature, ["TS", "ET", "NR", "DS", "SS", "MX"], ["HU", "TD", "Nature reserve", ""]),
    (cons.validate_csquares_code, ["3112", "3112:3", "3112:360", "3112:360:4", "1212:121:2", "1000:100:100:1", "7817:499"],
     ["2112:360", "3112:560", "3918", "3112:36", "1212-121-2", ""]),
    (cons.validate_csquares_code_fine, ["3112:3", "1212:121:2", "3013:141:4"], ["3112", "2019", "12:30", ""]),
    (validate_hisco, ["41025", "62490", "02120", "2000", "58320.0", "99999"], ["-1", "-105.0", "641", "141", "NA", "123456", ""]),
    (validate_isco_code, ["7245", "2145", "0", "66666", "9998", "110", "3231.0"], ["724501", "A", "72.45", ""]),
    (validate_higher_taxon_name_any_case, ["ANIMALIA", "CHORDATA", "ACTINOPTERYGII", "PERCIFORMES", "CARANGIDAE", "Fabaceae", "PLANTAE"],
     ["SMITH", "Caranx", "Lederman", "DIERCKX", ""]),
    (validate_season_name, ["Summer", "winter", "Autumn", "FALL", "Spring"], ["1986/87", "1897", "Year", "wet", "2004_summer", ""]),
    (validate_case_classification,
     ["potwierdzony", "Prawdopodobny", "MOŻLIWY", "Przypadek potwierdzony", "przypadek możliwy", "confirmed", "Probable", "suspected"],
     ["BD", "niesklasyfikowany", "ogniska", "hospitalised", ""]),
    (validate_case_classification_or_none, ["potwierdzony", "BD", "ND", "niesklasyfikowany", "nie spełnia definicji przypadku"],
     ["ogniska", "tak", "A", ""]),
    (validate_nl_amco, ["10002", "11434", "10357", "11228.0"], ["0363", "12001", "1002", "136", "20002", ""]),
    (validate_no_supreme_court_reference, ["HR-2019-2420-A", "HR-2019-1910-U", "HR-2018-389-A", "Rt-2015-353", "Rt-2008-1071"],
     ["HR-2019-2420", "LB-2019-2420", "HR-19-2420-A", "Rt 2015 s. 353", ""]),
    (pl.validate_pl_voivodeship,
     ["mazowieckie", "Warmińsko-mazurskie", "ŚLĄSKIE", "łódzkie", "KUJAWSKO-POMORSKIE", "Świętokrzyskie", "zachodniopomorskie"],
     ["warszawskie", "POLSKA", "M. st. Warszawa", "WSSE Katowice", "Mazowsze", ""]),
    (pl.validate_pl_voivodeship_column, ["mazowieckie", "POLSKA", "BD", "WSSE Katowice", "ŚLĄSKIE"],
     ["Białystok miasto", "Kraków", "1465", ""]),
    (pl.validate_pl_sex, ["M", "K", "Kobieta", "Mężczyzna", "mężczyzna", "k", "brak danych"], ["F", "Male", "1", "chłopiec", ""]),
    (pl.validate_pl_age_group, ["20-29", "40--49", "70+", "70 plus", "70plus", "≥70", "0", "4", "5-9", "BD", "brak danych"],
     ["dorośli", "2017", "20-29-39", "M", ""]),
    (pl.validate_pl_month, ["1", "6", "12", "07", "styczeń", "Grudzień"], ["13", "0", "January", "2017", ""]),
    (pl.validate_pl_yes_no, ["tak", "nie", "TAK", "Nie"], ["brak danych", "t", "yes", ""]),
    (pl.validate_pl_residence, ["miasto", "Wieś", "wieś", "Miasto 20-49 tys.", "Miasto >= 100 tys.", "BD", "bezdomny"],
     ["Warszawa", "gmina", "urban", ""]),
    (mk.validate_mk_municipality,
     ["Крушево", "КРУШЕВО", "Демир Хисар", "Карпош", "Чучер Сандево", "Чучер-Сандево", "Кисела вода", "Општина Карпош",
      "Маврово и Ростуша", "Ѓорче Петров"],
     ["Скопје", "Демир Хисар   Сопотница", "с. Бучин", "Македонија", ""]),
    (mk.validate_mk_phone,
     ["070235790", "047275166", "075/423-125", "02/3071-657", "+389075396926", "70673427", "3061922", "277577", "022035540"],
     ["ул. Борис Трајковски 5", "бб", "2014", "12", ""]),
    (mk.validate_mk_month, ["1", "12", "02", "јануари", "Декември"], ["13", "2015", "January", ""]),
    (mk.validate_decimal_degrees, ["41.22472", "21,5403", "-8.985", "41.2239129"], ["41.279.567", "21090710", "41", "999.25", ""]),
    (mn.validate_mn_dayofweek, ["Даваа", "Мягмар", "Лхагва", "Пүрэв", "Баасан", "Бямба", "Ням", "лхагва"],
     ["Намрын улирал", "Monday", "понедельник", ""]),
    (mn.validate_mn_sex, ["Эрэгтэй", "Эмэгтэй", "эмэгтэй"], ["Male", "Доктор", ""]),
    (validate_nz_region,
     ["Canterbury", "Bay of Plenty", "Hawke's Bay", "Hawkes Bay", "Manawatū-Whanganui", "Manawatu-Wanganui", "Otago Region",
      "Southland", "West Coast"],
     ["Christchurch", "RestSthIsland", "South Island", "New Zealand", "East Midlands", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value
    assert not func(None)


def test_object_types_of_kazakh_topographic_maps_are_no_nif_and_no_statistical_sector():
    # type of the layers of map.gov.kz: eight digits and l, m or f (line, area, point)
    for value in ["71150000m", "55100000m", "51631000l", "71162000l", "43211000f"]:
        assert not validate_es_nif(value), value
        assert not validate_be_statistical_sector(value), value
    assert validate_es_nif("12345678Z")
    assert validate_es_nif("12345678-Z")
    for value in ["21004A00-", "62063A012", "61072F3MN"]:
        assert validate_be_statistical_sector(value), value


FIELDS = [
    ("common/conservation.yaml", "wdpagovernancetypebyname", ["GOV_TYPE", "gov_type", "governance_type", "govtype"],
     ["government", "gov_type_1-4", "type"]),
    ("common/conservation.yaml", "wdpaownershiptypebyname", ["OWN_TYPE", "own_type", "ownership_type"], ["owner", "ownership", "type"]),
    ("common/conservation.yaml", "wdpadesignationtypebyname", ["DESIG_TYPE", "desig_type", "designation_type"],
     ["desig", "desig_eng", "design"]),
    ("common/conservation.yaml", "wdpanotakebyname", ["NO_TAKE", "no_take", "notake"], ["no_tk_area", "take"]),
    ("common/conservation.yaml", "wdpaverificationbyname", ["VERIF", "verif", "verification"], ["verified_by", "version"]),
    ("common/conservation.yaml", "wdpaidbyname", ["WDPAID", "wdpaid", "wdpa_id", "WDPA ID"], ["WDPA_PID", "wdpa", "metadataid"]),
    ("common/conservation.yaml", "ibtracsbasinbyname", ["BASIN", "basin"], ["subbasin", "basin_name", "river_basin"]),
    ("common/conservation.yaml", "ibtracsnaturebyname", ["NATURE", "nature"], ["nature_reserve", "signature"]),
    ("common/conservation.yaml", "csquarescodebyname", ["C-Square Code", "c-square code", "csquarecode", "c_square", "csquares", "CSquareCode"],
     ["square", "code", "csq"]),
    ("common/redlist.yaml", "iucnpopulationtrendbyname", ["populationTrend", "populationtrend", "population_trend", "pop_trend"],
     ["trend", "population", "populationsize"]),
    ("common/redlist.yaml", "iucnredlistcriteriabyname", ["redlistCriteria", "redlistcriteria", "criteria", "iucn_criteria", "critério"],
     ["criteriaversion", "category"]),
    ("common/occupations.yaml", "hiscobyname", ["hisco", "HISCO", "occupation_hisco_1", "hiscocode1", "hisco_code", "hiscocode2"],
     ["[occuphisco]", "hisclass", "hiscam"]),
    ("common/occupations.yaml", "isco88byname", ["isco88", "spisco88", "ISCO_88", "isco88com", "iscoco", "iscocop"],
     ["isco08", "isco", "k27isco", "disco88x"]),
    ("common/occupations.yaml", "isco08surveybyname", ["isco08", "spisco08", "isco08p", "ISCO_08"], ["isco88", "isco", "iscoco"]),
    ("common/periods.yaml", "seasonbyname", ["season", "Season", "seasons", "season_name", "sampling_season"],
     ["yearseason", "seasonal_index", "reason"]),
    ("common/medical.yaml", "caseclassificationbyname",
     ["klasyfikacja", "Klasyfikacja", "klasyfikacja przypadku", "klasyfikacja wg def", "klasyfikacja wg definicji",
      "klasyfikacja (potwierdzony, prawdopodobny, możliwy)", "klas. przyp.", "case_classification", "case status"],
     ["klasyfikacja budżetowa x", "classification", "status"]),
    ("common/science.yaml", "taxonranknamebyfield", ["kingdomName", "phylumName", "className", "orderName", "familyName", "family_name"],
     ["speciesName", "genusName", "lastname", "name"]),
    ("common/science.yaml", "taxongenusnamebyfield", ["genusName", "genus_name"], ["genus", "familyName"]),
    ("nl/nl_geo.yaml", "nlamcobyname", ["amco", "AMCO", "acode", "amsterdamse_code", "amsterdam_code", "Amsterdamse code"],
     ["cbsnr", "code", "amount"]),
    ("nz/nz_geo.yaml", "nzregionbyname", ["region", "Region", "regiongrp", "region_name", "regional_council", "nz_region"],
     ["regio", "subregion", "religion"]),
    ("pl/pl_statistics.yaml", "plvoivodeshipbyname",
     ["województwo", "Województwo", "województwo (nazwa)", "województwo zgłoszenia", "województwo zamieszkania", "wojewodztwo", "woj."],
     ["powiat", "wojsko", "gmina"]),
    ("pl/pl_statistics.yaml", "plsexbyname", ["płeć", "Płeć", "płeć (M, K)", "płeć m/k", "plec"], ["płeć dziecka x", "sex", "wiek"]),
    ("pl/pl_statistics.yaml", "plagegroupbyname", ["grupa wieku", "grupy wieku", "grupa wiekowa", "grupy wiekowe", "Grupa wieku"],
     ["wiek", "grupa", "grupa gis"]),
    ("pl/pl_statistics.yaml", "plyearbyname",
     ["rok zgłoszenia", "Rok zgłoszenia", "rok rejestracji", "rok rozpoznania", "rok (wykazania)", "rok (rejestracji)", "rok zgloszenia"],
     ["rok", "krok", "rok szkolny"]),
    ("pl/pl_statistics.yaml", "plmonthbyname", ["miesiąc", "miesiąc zachorowania", "miesiac zgłoszenia", "Miesiąc"],
     ["miesięcznie", "rok", "kwartał"]),
    ("pl/pl_statistics.yaml", "plresidencebyname",
     ["środowisko zamieszkania", "Środowisko zamieszkania", "środowisko zamieszkania (miasto, wieś)", "środowisko", "miasto/wieś"],
     ["zamieszkanie", "miasto", "ochrona środowiska x"]),
    ("pl/pl_statistics.yaml", "pldiseasebyname", ["jednostka chorobowa", "Jednostka chorobowa", "jednostka chororobowa", "choroba", "rozpoznanie"],
     ["jednostka", "postać choroby 1", "rok rozpoznania"]),
    ("mk/mk_common.yaml", "mkmunicipalitybyname", ["општина", "Општина", "ОПШТИНА", "општини"],
     ["одделениево општината", "услуги на општина лозово", "учество на општината"]),
    ("mk/mk_common.yaml", "mkfirstnamebyname", ["име", "Име", "име на контакт лице"], ["име на акт", "презиме", "назив"]),
    ("mk/mk_common.yaml", "mksurnamebyname", ["презиме", "Презиме", "презиме на контакт лице"], ["име", "име и презиме"]),
    ("mk/mk_common.yaml", "mkphonebyname",
     ["телефон", "Телефон", "контакт телефон", "контакт телефон 2", "тел.", "тел", "телефонски број", "контакт-телефон", "телефон 1",
      "телефон за контакт", "контакт телефонски број", "контакт", "контакт1", "контакт2"],
     ["телекомуникации", "контакт лице", "контакт информации", "телефон од претседателот на комисијата"]),
    ("mk/mk_common.yaml", "mkyearbyname", ["година", "Година"], ["годишен", "година на изградба x", "месец"]),
    ("mk/mk_common.yaml", "mkmonthbyname", ["месец", "Месец"], ["месечно", "година"]),
    ("mk/mk_common.yaml", "mklatitudebyname",
     ["географска ширина (latitude)", "географски координати (latitude)", "географска ширина"],
     ["географска должина (longitude)", "географски координати", "latitude"]),
    ("mk/mk_common.yaml", "mklongitudebyname",
     ["географска должина (longitude)", "географски координати (longitude)", "географска должина",
      "Географски координати (longitute)"],
     ["географска ширина (latitude)", "географски координати"]),
    ("mk/mk_common.yaml", "mknamebyname", ["назив", "Назив", "назив на објект", "назив на училиште", "назив на раздел"],
     ["називи", "опис"]),
    ("mk/mk_common.yaml", "mkcommentbyname", ["забелешка", "Забелешка", "забелешки", "коментар", "Дополнителни забелешки"], ["опис", "белешка x"]),
    ("mk/mk_common.yaml", "mkcitybyname", ["населено место", "Населено место", "град"], ["место", "градба", "населба"]),
    ("mn/mn_common.yaml", "mnsexbyname", ["хүйс", "элсэгчийн_хүйс", "Хүйс"], ["хүйсээр", "нэр"]),
    ("mn/mn_common.yaml", "mnschoolyearbyname", ["хичээлийн_жил", "хичээлийн жил"], ["жил", "хичээлийн_нэр"]),
    ("mn/mn_common.yaml", "mnyearbyname", ["он", "хөтөлбөр_батлагдсан_он"], ["огноо", "тодорхойлсон_огноо", "оноо"]),
    ("mn/mn_common.yaml", "mnnamebyname", ["нэр", "хичээлийн_нэр", "хөтөлбөрийн_нэр", "монгол_нэр", "тэнхимийн нэр"],
     ["хичээлийн_дугаар", "нэрс"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_names(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUE_RULES = [
    ("common/conservation.yaml", "csquarescodevalue", "csquares_code"),
    ("pl/pl_statistics.yaml", "plvoivodeshipvalue", "pl_voivodeship"),
    ("pl/pl_statistics.yaml", "plbooleanvalue", "boolean"),
    ("mn/mn_common.yaml", "mndayofweekvalue", "mn_dayofweek"),
    ("no/no_legal.yaml", "nosupremecourtreferencevalue", "no_supreme_court_reference"),
]


@pytest.mark.parametrize("path,rule_id,key", VALUE_RULES, ids=[v[1] for v in VALUE_RULES])
def test_value_rules(path, rule_id, key):
    spec = load(path, rule_id)
    assert spec["key"] == key
    assert spec["type"] == "data" and spec["match"] == "func"
    assert spec["minlen"] <= spec["maxlen"]
