"""Rules for the files of metacrafter-testdata from 2024 snapshots of 43 data catalogues (Dateno sources
cdi00001606, ASARECA; cdi00001690, Harvard Dataverse; cdi00001862, NYC Open Data; cdi00002002, Subak;
cdi00002019, OpenUp; cdi00002091, Data Atlas Fontium; cdi00002093, GIAP; cdi00002171, Comune di Parma;
cdi00002343, Ho Chi Minh City; cdi00002408, Geoweba; cdi00004174, Ajman; cdi00004215, datos.gov.py;
cdi00004220, HealthData.gov; cdi00004270, opendata.ps; cdi00004515, Lounaistieto): New York City school
codes, boroughs, community districts and parks property numbers; US congressional districts, Congress
numbers and party identification; Gleditsch-Ward codes, Correlates of War abbreviations, Polity scores,
FAOSTAT codes and epidemiological weeks; Polish BDOT10k codes, PRNG identifiers, cadastral units, case
references and TERC codes; Algerian provinces; Paraguayan departments and procurement calls; Peruvian UBIGEO
codes; Palestinian governorates and postal codes; Makani numbers; South African Surveyor-General codes,
medicine registration numbers and schedules, small areas; ISTAT codes of states; Vietnamese certificate and
document numbers; Finnish drainage basins; ecological status classes; GMPP identifiers.

Matched as tests/test_testdata_baseline.py matches them.
"""
import re

import pytest

from metacrafterext.rules.ae import b13 as ae
from metacrafterext.rules.common import b13 as common
from metacrafterext.rules.dz import geo as dz
from metacrafterext.rules.eu import water as eu
from metacrafterext.rules.fi import b13 as fi
from metacrafterext.rules.gb import b13 as gb
from metacrafterext.rules.it import b13 as it
from metacrafterext.rules.pe import geo as pe
from metacrafterext.rules.pl import b13 as pl
from metacrafterext.rules.ps import geo as ps
from metacrafterext.rules.py import geo as py
from metacrafterext.rules.us import b13 as us
from metacrafterext.rules.vn import b13 as vn
from metacrafterext.rules.za import b13 as za
from tests.test_testdata_baseline import field_matches, load

VALIDATORS = [
    (us.validate_us_nyc_dbn, ["01M015", "24Q600", "02M630", "31R080", "10X141"], ["01A015", "1M015", "01M15", "M015", ""]),
    (us.validate_us_nyc_borough, ["Manhattan", "BROOKLYN", "Staten Island", "Bronx", "The Bronx", "Queens", "K", "X"],
     ["Harlem", "Camden", "New York", "4", ""]),
    (us.validate_us_nyc_borough_code, ["1", "5", "3.0"], ["0", "6", "12", "M", ""]),
    (us.validate_us_nyc_community_district, ["310", "101", "164", "503", "11", "7", "08"], ["319", "601", "19", "0", "BK10", ""]),
    (us.validate_us_nyc_parks_property_id, ["B028", "Q012", "X010A", "M042-ZN01", "X010A-02", "B166D", "B073-ZN15"],
     ["A028", "28", "Central Park", ""]),
    (us.validate_us_congressional_district, ["NY10", "CA-12", "WY-AL", "TN01", "ak01"], ["XX10", "NY99", "10", "NY", ""]),
    (us.validate_us_congress_number, ["96", "111", "111.0", "117th", "1"], ["0", "1995", "130", "dem", ""]),
    (us.validate_us_party_identification, ["1", "7", "3.0", "Democrat", "Strong Republican", "Not sure", "Independent"],
     ["Labour", "0", "10", "999", ""]),
    (common.validate_gw_country_code, ["2", "200", "710", "540.0"], ["0", "USA", "1000", ""]),
    (common.validate_cow_country_abbreviation, ["USA", "UKG", "GMY"], ["US", "usa", "Germany", ""]),
    (common.validate_polity_score, ["10", "-7", "0", "-88", "9.0", "-10"], ["11", "0.5", "-11", "NA", ""]),
    (common.validate_faostat_area_code, ["114", "231", "5000"], ["KEN", "0", "50000", ""]),
    (common.validate_faostat_item_code, ["15", "56", "3010"], ["0111", "wheat", ""]),
    (common.validate_faostat_element_code, ["5510", "5312", "551"], ["55", "production", ""]),
    (common.validate_epi_week, ["1", "01", "29", "53", "16.0"], ["0", "54", "2020", ""]),
    (pl.validate_pl_bdot10k_code, ["BUBD11", "ADMS14", "ADMS14_h", "BUIN03"], ["BUBD", "bubd11", "BUBD111", ""]),
    (pl.validate_pl_prng_id, ["134542", "4438", "99"], ["0", "12345678", "Wiczlino", ""]),
    (pl.validate_pl_jednostka_ewidencyjna, ["186101_1", "180902_5"], ["186101", "186101_7", "18610_1", ""]),
    (pl.validate_pl_znak_sprawy, ["6730.26.2016", "6730.2.2016", "AB.6730.26.2016", "WGN.6840.1.12.2020.MK"],
     ["6730/26/2016", "26.2016", "2016", ""]),
    (pl.validate_pl_teryt_terc, ["0225011", "1408052", "3063011", "0809035", "02", "1408"], ["0125011", "06230", "0600042x", "34", ""]),
    (dz.validate_dz_wilaya, ["Alger", "ALGER", "Bejaia", "Béjaïa", "TIZI OUZOU", "Oum El Bouaghi", "M'Sila", "Timimoun"],
     ["Kouba", "Algérie", "Rabat", ""]),
    (dz.validate_dz_wilaya_code, ["16", "6", "06", "58", "31.0"], ["0", "59", "Alger", ""]),
    (py.validate_py_department, ["Alto Paraná", "CONCEPCION", "PDTE. HAYES", "Asunción", "Capital", "Ñeembucu", "Guaira"],
     ["Total", "Santa Cruz", "Antioquia", "Ciudad del Este", ""]),
    (py.validate_py_department_code, ["0", "11", "07", "17", "2.0"], ["18", "99", "Central", ""]),
    (py.validate_py_dncp_licitacion_id, ["187326", "156600"], ["18732", "1873260", "LPN", ""]),
    (pe.validate_pe_ubigeo, ["150101", "010101", "10101", "250401"], ["260101", "000101", "1501", "Lima", ""]),
    (ps.validate_ps_governorate,
     ["Hebron", "Ramallah and Al-Bireh", "Tubas & Northern Valleys", "Jericho and Al Aghwar", "Qalqilia", "Khan Yunis",
      "الخليل", "رام الله والبيرة", "رام الله و البيرة", "محافظة رام الله والبيرة", "أريحا والأغوار"],
     ["Cairo", "West Bank", "Amman", "القاهرة", ""]),
    (ps.validate_ps_postcode, ["P3920463", "P6100154", "P392 0463"], ["6100154", "P610015", "Px", ""]),
    (ae.validate_ae_makani_number, ["42642 10565", "5009209779"], ["426421056", "NULL", "42642-10565", ""]),
    (za.validate_za_sg_code, ["C03700050000652000000", "C05300370000000100000", "T0JR00000000012300000"],
     ["C0370005000065200000", "A03700050000652000000", ""]),
    (za.validate_za_medicine_registration_number,
     ["29/20.1.1/0163", "37/30.2/0252", "R/3.1/71", "D/24/208", "B675 (OM)", "E875 (Act 101/1965)", "B1041 Act 101 of 1965"],
     ["29-20.1.1-0163", "2016/123456/07", "0163", ""]),
    (za.validate_za_medicine_schedule, ["S4", "S0", "Schedule 6", "s3"], ["S9", "4", "Medicine Schedule", ""]),
    (za.validate_za_small_area_code, ["2610024", "2610045"], ["261002", "26100245", "R 15 000", ""]),
    (it.validate_it_istat_country_code, ["100", "443", "305", "201.0"], ["44", "ALBANIA", "1000", "010", ""]),
    (vn.validate_vn_cchn_number, ["000019/HCM-CCHN", "000017/BYT-CCHN", "000058/ĐL-CCHN", "0000778/HCM-CCHN", "000001/CTHO- CCHN"],
     ["000019/HCM", "HCM-CCHN", "000019", ""]),
    (vn.validate_vn_document_number, ["1753/QĐ-GDĐT-TC", "2279/GDĐT-TC", "04211/SYT-GPHĐ", "30/2020/NĐ-CP"],
     ["1753", "QĐ-GDĐT", "04/01/2022", ""]),
    (fi.validate_fi_vesistoalue, ["35.141", "24.061", "82.047", "4.1"], ["35.1411", "135.14", "35", "Kokemäenjoki", ""]),
    (eu.validate_eu_wfd_ecological_status, ["High", "Good", "Moderate", "POOR", "bad", "Hyvä"], ["Excellent", "Sufficient", "1", ""]),
    (gb.validate_gb_gmpp_id, ["MOD_0101_1516-Q1", "BEIS_0001_1617-Q2", "DfT_0012_1213-Q1"], ["MOD_0101", "MOD_0101_1516-Q5", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value
    assert not func(None)


def test_a_case_reference_is_no_version():
    from metacrafterext.rules.common.software import validate_semver

    assert not validate_semver("6730.26.2016") and not validate_semver("6730.2.2016")
    assert validate_semver("1.2.3") and validate_semver("2016.1.0")


def test_the_lists_of_names():
    assert len(dz.WILAYAS) == len(set(dz.WILAYAS)) == 58
    assert len(py.DEPARTMENTS) == len(set(py.DEPARTMENTS)) == 17
    assert len(us.BOROUGHS) == 5


FIELDS = [
    ("us/us_nyc.yaml", "usnycdbnbyname", ["DBN", "dbn", "School DBN", "ATS System Code"], ["db", "dbname", "school"]),
    ("us/us_nyc.yaml", "usnycboroughbyname", ["Borough", "BOROUGH", "boro", "BoroName", "borough_name"], ["borocode", "BoroCD", "neighborhood"]),
    ("us/us_nyc.yaml", "usnycboroughcodebyname", ["BoroCode", "borocode", "boro_code", "Borough Code"], ["borough", "BoroCD", "code"]),
    ("us/us_nyc.yaml", "usnyccommunitydistrictbyname", ["Community Board", "communityboard", "Community District", "BoroCD", "community_board"],
     ["community", "cd", "council_district", "Community Council"]),
    ("us/us_nyc.yaml", "usnycparkspropertybyname", ["GISPROPNUM", "gispropnum", "OMPPROPID"], ["propnum", "property", "gis"]),
    ("us/us_politics.yaml", "uscongressionaldistrictbyname", ["congress_district", "cong_dist", "congdist", "cd_code", "Congressional District"],
     ["cd", "district", "congress"]),
    ("us/us_politics.yaml", "uscongressnumberbyname", ["congress", "Congress", "cong", "congress_number"], ["congressman", "cong_dist", "conglome"]),
    ("us/us_politics.yaml", "uspartyidentificationbyname", ["pid3", "pid7", "pid7_legacy", "PID3", "party_id7"], ["pid", "party", "pid10x"]),
    ("common/research_codes.yaml", "gwcountrycodebyname", ["gwno", "GWNo", "gwcode", "gwno_a", "gwno_loc", "opponent_gwno"], ["gw", "gwp", "cowcode"]),
    ("common/research_codes.yaml", "cowcountryabbreviationbyname", ["stateabb", "StateAbb", "stateabb1", "cowabb"], ["state", "stateabbr", "abb"]),
    ("common/research_codes.yaml", "polityscorebyname", ["polity", "polity2", "Polity IV", "polity_score", "e_polity2", "polity4"],
     ["policy", "politycode", "polity2_lag"]),
    ("common/research_codes.yaml", "faostatelementcodebyname", ["Element Code", "element_code", "ElementCode"], ["Element", "Item Code", "code"]),
    ("common/research_codes.yaml", "faostatareacodebyname", ["Area Code (FAO)", "area_code_fao"], ["Area Code", "Area Code (M49)", "Area"]),
    ("common/research_codes.yaml", "faostatitemcodebyname", ["Item Code (FAO)", "item_code_fao"], ["Item Code", "Item Code (CPC)", "Item"]),
    ("common/research_codes.yaml", "epiweekbyname", ["MMWR Week", "mmwr_week", "MMWRweek", "epi_week", "epiweek", "Epidemiological Week"],
     ["week", "MMWR Year", "week_ending_date"]),
    ("pl/pl_topo.yaml", "plbdot10kcodebyname", ["x_kod", "X_KOD", "kod_o", "kod obiektu", "kod_bdot10k"], ["kod", "kod_pocztowy", "x_katIstnienia"]),
    ("pl/pl_topo.yaml", "plprngidbyname", ["id_prng", "idPRNG", "ID_PRNG", "identyfikator PRNG"], ["id", "prng", "id_osady"]),
    ("pl/pl_topo.yaml", "plznaksprawybyname", ["znak sprawy", "Znak_sprawy", "numer decyzji", "decyzje_numerdecyzji", "nr_sprawy", "sygnatura", "numer wniosku"],
     ["numer", "decyzja", "data decyzji", "nr_dzialki"]),
    ("pl/pl_topo.yaml", "plteryttercbyname", ["teryt", "TERYT", "JPT_KOD_JE", "kod_teryt", "terc", "kodTERC"], ["idteryt", "kod", "teryt_nazwa"]),
    ("dz/dz_geo.yaml", "dzwilayabyname", ["wilaya", "Wilaya", "WILAYA", "nom_wilaya", "wilaya_name"], ["code_wilaya", "commune", "wilaya_agence"]),
    ("dz/dz_geo.yaml", "dzwilayacodebyname", ["code_wil", "code_wilaya", "CODE_WILAYA", "wilaya_code", "wilaya_agence", "wilaya"],
     ["code", "commune_agence", "nom_wilaya"]),
    ("py/py_geo.yaml", "pydepartmentbyname", ["departamento", "Departamento", "DEPARTAMENTO", "dpto", "depdes", "nombre_departamento"],
     ["dep", "departamento y distrito de residencia", "distrito"]),
    ("py/py_geo.yaml", "pydepartmentcodebyname", ["dep", "DEP", "dptov"], ["depdes", "departamento", "dpto", "dis"]),
    ("py/py_geo.yaml", "pydncplicitacionidbyname", ["id_llamado", "ID Llamado", "id_licitacion", "nro_licitacion", "id licitación"],
     ["llamado", "nombre_licitacion", "id"]),
    ("pe/pe_geo.yaml", "peubigeobyname", ["ubigeo", "UBIGEO", "cod_ubigeo", "ubigeo_inei", "ubigeo2010", "codigo_ubigeo"],
     ["ubigeo_total_obs", "ubicacion", "geo"]),
    ("ps/ps_geo.yaml", "psgovernoratebyname", ["Governorate", "governorate", "governorate_a", "Governorate_E", "المحافظة", "محافظة"],
     ["government", "governance_type", "المدينة"]),
    ("ps/ps_geo.yaml", "pspostcodebyname", ["postcode", "PostCode", "postal_code", "Postal Code", "zip"], ["post", "code", "po_box"]),
    ("ae/ae_makani.yaml", "aemakaninumberbyname", ["makaninumber", "MakaniNumber", "makani_no", "Makani"], ["makan", "number", "licensenumber"]),
    ("za/za_codes.yaml", "zamedicineregistrationbyname", ["MCC medicine reg no", "mcc_medicine_reg_no", "registration number", "Reg No.", "reg_no"],
     ["registration date", "medicine", "region"]),
    ("za/za_codes.yaml", "zamedicineschedulebyname", ["medicine schedule", "Medicine Schedule", "schedule", "medicine_schedule"],
     ["scheduled", "schedule_date", "medicine"]),
    ("za/za_codes.yaml", "zasmallareacodebyname", ["sal", "SAL", "sal_code", "SAL_CODE", "small area code", "sal2011"], ["salary", "sale", "small area"]),
    ("it/it_istat.yaml", "itistatcountrycodebyname", ["cittad", "CITTAD", "cittadinanza", "cod_cittadinanza", "codice stato estero", "stato_estero"],
     ["citta", "stato", "cittadini"]),
    ("vn/vn_documents.yaml", "vndocumentnumberbyname", ["quyetdinhso", "QuyetDinhSo", "số quyết định", "sogiayphep", "Số giấy phép", "số hiệu", "so_ky_hieu"],
     ["loaiquyetdinh", "ngaycap", "so", "sochungchi"]),
    ("fi/fi_environment.yaml", "fivesistoaluebyname", ["vesalnro", "VesalNro", "vesistöalue", "vesistoalue_nro", "valuma-alueen tunnus"],
     ["vesisto", "nro", "alue"]),
    ("eu/eu_environment.yaml", "euwfdecologicalstatusbyname", ["eco_status", "Ecological status", "ecological_status_class", "ekologinen tila", "ekol_tila"],
     ["status", "economic_status", "chem_status"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    spec = load(path, rule_id)
    assert spec["key"]
    assert spec["validator"].startswith("metacrafterext.rules.") and spec["needs_values"] is True
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("us/us_nyc.yaml", "usnycdbnvalue", ["01M015", "24Q600"], ["01A015", "1M015", "01m015"]),
    ("pl/pl_topo.yaml", "pljednostkaewidencyjnavalue", ["186101_1", "180902_5"], ["186101_7", "186101-1"]),
    ("za/za_codes.yaml", "zasgcodevalue", ["C03700050000652000000", "T0JR00000000012300000"], ["A03700050000652000000", "c03700050000652000000"]),
    ("vn/vn_documents.yaml", "vncchnnumbervalue", ["000019/HCM-CCHN", "000058/ĐL-CCHN", "0000778/HCM-CCHN"], ["000019/HCM", "19/HCM-CCHN"]),
    ("ps/ps_geo.yaml", "pspostcodevalue", ["P3920463", "P610 0154"], ["6100154", "P610015", "p3920463"]),
    ("gb/gb_gov.yaml", "gbgmppidvalue", ["MOD_0101_1516-Q1", "BEIS_0001_1617-Q2"], ["MOD_0101_1516", "MOD_0101_1516-Q5"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    spec = load(path, rule_id)
    pattern = re.compile(spec["rule"])
    for value in good:
        assert pattern.fullmatch(value), value
        assert spec["minlen"] <= len(value) <= spec["maxlen"]
    for value in bad:
        assert not pattern.fullmatch(value), value
