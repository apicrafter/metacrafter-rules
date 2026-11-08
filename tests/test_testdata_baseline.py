"""Rules from the metacrafter-testdata baseline (#55, #56, #57, #58).

Rules are matched as metacrafter matches them: text rules by lower-cased membership, regex
rules with ``fullmatch`` on the name and the lower-cased name; a value matches a regex rule
with ``fullmatch`` within minlen/maxlen, and its validator must accept it. A field guard
(``fieldrule``, text) lists the lower-cased names a value rule applies to.
"""
import importlib
import pathlib
import re

import pyparsing
import pytest
import yaml

from metacrafterext.rules.common.generic import (
    has_legal_form,
    has_letters,
    validate_bic_country,
    validate_dmy_date,
    validate_eea_station_code,
)
from metacrafterext.rules.fr.validators import validate_fr_siret

RULES = pathlib.Path(__file__).resolve().parent.parent / "rules"


def load(path, rule_id):
    return yaml.safe_load((RULES / path).read_text(encoding="utf-8"))["rules"][rule_id]


def field_matches(path, rule_id, name):
    spec = load(path, rule_id)
    assert spec["type"] == "field"
    if spec["match"] == "text":
        return name.lower() in {k.strip().lower() for k in spec["rule"].split(",")}
    pattern = re.compile(spec["rule"])
    return bool(pattern.fullmatch(name) or pattern.fullmatch(name.lower()))


def guarded_by(path, rule_id, name):
    spec = load(path, rule_id)
    assert spec["type"] == "data" and spec["fieldrulematch"] == "text"
    return name.lower() in {k.strip().lower() for k in spec["fieldrule"].split(",")}


def value_matches(path, rule_id, value):
    spec = load(path, rule_id)
    assert spec["type"] == "data"
    if not int(spec.get("minlen", 0)) <= len(value) <= int(spec.get("maxlen", 10**6)):
        return False
    if spec["match"] == "regex":
        ok = re.fullmatch(spec["rule"], value) is not None
    elif spec["match"] == "text":
        ok = value.lower() in {k.strip().lower() for k in spec["rule"].split(",")}
    elif spec["match"] == "ppr":
        namespace = {name: getattr(pyparsing, name) for name in (
            "Word", "Literal", "CaselessLiteral", "Optional", "ZeroOrMore", "oneOf", "nums", "alphas",
            "alphanums", "hexnums", "printables")}
        parser = pyparsing.lineStart + eval(spec["rule"], {"__builtins__": {}}, namespace) + pyparsing.lineEnd
        try:
            parser.parse_string(value)
            ok = True
        except pyparsing.ParseException:
            ok = False
    elif spec["match"] == "func":
        module, name = spec["rule"].rsplit(".", 1)
        ok = bool(getattr(importlib.import_module(module), name)(value))
    else:
        raise AssertionError(spec["match"])
    if ok and "validator" in spec:
        module, name = spec["validator"].rsplit(".", 1)
        ok = bool(getattr(importlib.import_module(module), name)(value))
    return ok


# --- #58: rules for the datatypes of registry #154-#158 --------------------------------
# rule file, rule id, key, values from the registry examples and the test data, refused values,
# a field name of the guard (None: no guard).
NEW_TYPES = [
    ("common/transport.yaml", "gtfslocationtypevalue", "gtfs_location_type", ["0", "1", "4"], ["5"], "location_type"),
    ("common/transport.yaml", "gtfswheelchairboardingvalue", "gtfs_wheelchair_boarding",
     ["0", "1", "2", "1" + " " * 250], ["3"], "wheelchair_boarding"),
    ("common/transport.yaml", "ifoptstopidvalue", "ifopt_stop_id",
     ["de:05966:24128", "de:05966:24128:1:1"], ["05966:24128", "12:30:00"], None),
    ("gb/gb_transport.yaml", "gbnaptanatcovalue", "gb_naptan_atco",
     ["2580AUD0009", "069000010180", "1800NB01241"], ["AUD0009", "2580AUD00091234"], "stop_code"),
    ("es/es_transport.yaml", "esadifstationvalue", "es_adif_station_code", ["60000", "71801"], ["1003"], "codigo_estacion"),
    ("kr/kr_geo.yaml", "krbusstoparsvalue", "kr_bus_stop_ars", ["01001"], ["1001"], "arsno"),
    ("kr/kr_geo.yaml", "kradmindongcodevalue", "kr_admin_dong_code", ["1111051500"], ["11110515"], "행정기관코드"),
    ("jp/jp_datetime.yaml", "jpdateeravalue", "date_jp_era",
     ["平成 9. 4.27", "令和7.7.20", "令和元年5月1日"], ["2019年5月1日"], None),
    ("jp/jp_datetime.yaml", "jpyeareravalue", "year_jp_era", ["平成4年", "昭58", "平５", "令元"], ["1992年"], None),
    ("jp/jp_datetime.yaml", "jpestattimecodevalue", "jp_estat_time_code", ["1992001010"], ["1992"], "時間軸コード"),
    ("tw/tw_datetime.yaml", "twrocdatevalue", "date_roc", ["1081223", "1140101", "0991231"], ["1081323"], "最近異動日期"),
    ("tw/tw_datetime.yaml", "twrocyearmonthvalue", "yearmonth_roc", ["10506", "11412"], ["10513"], "statistic_yyymm"),
    ("common/dateandtime.yaml", "datedmonyyvalue", "date_dmony", ["06NOV26", "31DEC99"], ["06NOV2026", "6NOV26"], None),
    ("co/co_geo.yaml", "codivipolavalue", "co_divipola", ["05001", "91001"], ["5001"], "municipio_prestador"),
    ("br/br_geo.yaml", "brsiafimunicipalityvalue", "br_siafi_municipality_code", ["0643", "7107"], ["3550308"], "cod_mun"),
    ("mx/mx_geo.yaml", "mxinegimunicipalityvalue", "mx_inegi_municipality_code", ["09015", "015"], ["9015"], "cve_mun"),
    ("at/at_geo.yaml", "atbezirkvalue", "at_bezirkskennziffer", ["901", "911"], ["90101"], "stataustria_bez_code"),
    ("ch/ch_geo.yaml", "chbfsbezirkvalue", "ch_bfs_bezirk", ["101", "110"], ["12"], "bezkid"),
    ("nl/nl_geo.yaml", "nlcoropvalue", "nl_corop", ["07", "40", "CR23"], ["41"], "coropgebied code"),
    ("nl/nl_geo.yaml", "nlcbsregionyearvalue", "nl_cbs_region_code_year", ["2024GM0034", "2024WK003401"], ["GM0034"], None),
    ("fi/fi_geo.yaml", "fiwellbeingcountyvalue", "fi_wellbeing_services_county", ["01", "90"], ["1"], "hyvinvointialue"),
    ("cl/cl_geo.yaml", "clregionvalue", "cl_region_code", ["13", "5"], ["17"], "region tributaria"),
    ("ca/ca_geo.yaml", "caqcmunicipalitycodevalue", "ca_qc_municipality_code", ["46005"], ["4600"], "mcode"),
    ("pt/pt_geo.yaml", "ptinegeocodevalue", "pt_ine_geocode", ["1D11108"], ["1108"], "geocod"),
    ("gb/gb_education.yaml", "gbdfelacodevalue", "gb_dfe_la_code", ["202", "208"], ["E09000007"], "la (code)"),
    ("us/us_geo.yaml", "uscensussumlevvalue", "us_census_sumlev", ["040", "050"], ["40"], "sumlev"),
    ("us/us_geo.yaml", "uscensusregionvalue", "us_census_region", ["1", "4"], ["5"], "region"),
    ("us/us_geo.yaml", "uscensusdivisionvalue", "us_census_division", ["1", "9"], ["10"], "division"),
    ("us/us_geo.yaml", "uscensuslsadvalue", "us_census_lsad", ["06", "25"], ["6"], "lsad"),
    ("us/us_geo.yaml", "usnycbblvalue", "us_nyc_bbl", ["1000010010", "3001280001.00000000000"], ["0.00000000000", "6000010010"], "bbl"),
    ("us/us_geo.yaml", "usnycbinvalue", "us_nyc_bin", ["1086341", "4268835.00000000000"], ["6086341"], "bin"),
    ("us/us_geo.yaml", "usnycntavalue", "us_nyc_nta", ["MN17", "QN31", "BK0101"], ["NY17"], "ntacode"),
    ("ru/ru_codes.yaml", "ruifnscodevalue", "ru_ifns_code", ["7707", "0107"], ["107"], "tax_office"),
    ("ua/ua_govfinances.yaml", "uakpkvkvalue", "ua_kpkvk", ["1021", "6014"], ["102"], "cod_cons_mb_pk"),
    ("ua/ua_govfinances.yaml", "uafkvkvalue", "ua_fkvk", ["0810", "1040"], ["810"], "cod_cons_mb_fk"),
    ("ua/ua_govfinances.yaml", "uakekvvalue", "ua_kekv", ["2111", "2240"], ["211"], "cod_cons_ek"),
    ("ua/ua_govfinances.yaml", "uabudgetcodevalue", "ua_budget_code", ["26000000000"], ["2600000000"], "cod_budget"),
    ("fr/fr_common.yaml", "frmuseofilevalue", "fr_museofile", ["M1128", "M0003"], ["1128"], "identifiant"),
    ("fr/fr_common.yaml", "frmerimeevalue", "fr_merimee",
     ["PA00084643", "IA67009579", "SPR4400043", "SPR4400043;SPR4400044", "PA00085184;SPR4400040"], ["PA0008464"], None),
    ("fr/fr_common.yaml", "frpdlvalue", "fr_pdl", ["50076628911092"], ["5007662891109"], "num_pdl"),
    ("fr/fr_transport.yaml", "frirveidvalue", "fr_irve_id",
     ["FRS56PLMBT3H1YW1BIVW", "FRS56EPWRK1", "FR*S56*EPWRK1"], ["FRS56XPWRK1"], None),
    ("co/co_medical.yaml", "corepscodevalue", "co_reps_code", ["9100100019", "910010001901"], ["91001000"], "codigoprestador"),
    ("br/br_industry.yaml", "branpauthorizationvalue", "br_anp_authorization", ["PR/AC0167611"], ["AC0167611"], None),
    ("lv/lv_common.yaml", "lvbisregistervalue", "lv_bis_register_number", ["11239-R", "10593-R"], ["11239"], None),
    ("lv/lv_common.yaml", "lvmedicinenumbervalue", "lv_medicine_number", ["00-0003-01"], ["00000301"], "product_id"),
    ("lv/lv_common.yaml", "lvregistrationnumbervalue", "lv_registration_number", ["40003245752"], ["4000324575"],
     "registracijas_numurs_mitnes_valsti"),
    ("pl/pl_gov.yaml", "pladevalue", "pl_ade", ["AE:PL-55546-38867-UJDEW-16"], ["PL-55546-38867-UJDEW-16"], None),
    ("pl/pl_gov.yaml", "plexcisenumbervalue", "pl_excise_number", ["PL34100039204"], ["PL341000392"], "numer_akcyzowy"),
    ("nl/nl_education.yaml", "nlbrinvestigingvalue", "nl_brin_vestiging", ["32JK00", "16PK00"], ["32JK"], "vestigingscode"),
    ("nl/nl_education.yaml", "nlbevoegdgezagvalue", "nl_bevoegd_gezag", ["41676", "20091"], ["4167"], "bevoegd gezag nummer"),
    ("se/se_education.yaml", "seskolenhetskodvalue", "se_skolenhetskod", ["73048821"], ["7304882"], "skolenhetskod"),
    ("de/de_education.yaml", "deschulnummervalue", "de_schulnummer", ["100010"], ["10001"], "schulnummer"),
    ("us/us_medical.yaml", "uscmsccnvalue", "us_cms_ccn", ["010001", "05T001"], ["10001"], "facility id"),
    ("qa/qa_companies.yaml", "qabusinessactivityvalue", "qa_business_activity_code", ["0910001"], ["910001"],
     "رمز النشاط التجاري"),
    ("common/environment.yaml", "eeaeoistationcodevalue", "eea_eoi_station_code",
     ["DEBB003", "BETR891", "BELHB23"], ["DEBB03", "USAB123", "debb003"], "ab_eoi_code"),
    ("common/science.yaml", "dwcbasisofrecordvalue", "dwc_basis_of_record",
     ["PreservedSpecimen", "HumanObservation", "PRESERVED_SPECIMEN"], ["Specimen"], None),
    ("common/software.yaml", "sharepointcontenttypeidvalue", "sharepoint_content_type_id",
     ["0x", "0x01", "0x0101", "0x01000F389E14C9CE4CE486270B9D4713A5D6"], ["0x012", "01"], "stringid"),
    ("uy/uy_geo.yaml", "uyiso3166compactvalue", "iso3166code_compact", ["UYAR", "UYMO"], ["UY-AR"], "depto"),
]


@pytest.mark.parametrize("path,rule_id,key,good,bad,guard", NEW_TYPES, ids=[c[1] for c in NEW_TYPES])
def test_rules_of_new_datatypes(path, rule_id, key, good, bad, guard):
    spec = load(path, rule_id)
    assert spec["key"] == key
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value
    if guard is None:
        assert "fieldrule" not in spec
    else:
        assert guarded_by(path, rule_id, guard)


def test_new_rule_files_have_a_country():
    for rel, cc in (("tw/tw_datetime.yaml", "tw"), ("ua/ua_govfinances.yaml", "ua"), ("lv/lv_common.yaml", "lv"),
                    ("co/co_geo.yaml", "co"), ("qa/qa_companies.yaml", "qa"), ("uy/uy_geo.yaml", "uy")):
        assert yaml.safe_load((RULES / rel).read_text(encoding="utf-8"))["country_code"] == cc


@pytest.mark.parametrize("path,rule_id,key,names", [
    ("common/transport.yaml", "ifoptstopidknown", "ifopt_stop_id", ["Globale ID", "Steig Globale ID", "DHID"]),
    ("common/science.yaml", "dwcbasisofrecordknown", "dwc_basis_of_record", ["basisOfRecord"]),
    ("jp/jp_finances.yaml", "jpcnknown", "jp_cn", ["法人番号"]),
    ("hu/hu_legal.yaml", "hulegislationknown", "legislationname", ["jogszabály"]),
    ("common/values.yaml", "areabyfield", "area",
     ["FLAECHE", "Fläche km² ¹⁾", "ALAND", "AWATER", "msuperf", "Terület", "shape_area", "Shape__Area",
      "wijkenbuurten:oppervlakteTotaalInHa", "OppervlakteTotaal_116", "superficie_ha", "area_km2", "total_area"]),
])
def test_field_names(path, rule_id, key, names):
    assert load(path, rule_id)["key"] == key
    for name in names:
        assert field_matches(path, rule_id, name), name


@pytest.mark.parametrize("path,rule_id,names", [
    ("common/values.yaml", "areabyfield", ["area", "area_name", "area_code", "Flächennutzung", "service_area"]),
])
def test_names_that_must_not_match(path, rule_id, names):
    for name in names:
        assert not field_matches(path, rule_id, name), name


# --- #57: generic types by multilingual field names -------------------------------------

GENERIC = "common/generic.yaml"


@pytest.mark.parametrize("rule_id,key,good,bad", [
    ("categorybyfield", "category",
     ["Expense Type", "company_status", "tipologia", "Вид на водата", "Състояние", "Είδος Μητρώου", "種別", "유형",
      "Komersanta_veids", "Aktualais_statuss", "Hospital Ownership", "AUSPICE", "type_code"],
     ["type", "geometry.type", "mainBusinessLine.type", "mime_type", "Content Type", "typeface"]),
    ("citybyfield", "city",
     ["municipality", "Gemeinde", "Název obce", "settlement", "POBLACIÓN", "市区町村名", "البلدية", "gemname",
      "nom_commune", "gemeentenaam", "Comuna Tributaria", "address.locality"],
     ["code_commune", "cod_comune", "Codice Comune formato numerico", "gemeinde_schluessel", "Name mit Ort", "kunta"]),
    ("orgnamebyfield", "orgname",
     ["Razon Social", "RAZAOSOCIAL", "Denominación", "Nosaukums", "BETREIBER", "Φορέας", "업체명", "公司名稱",
      "service_provider_english", "Facility Name", "Назва місцевого суду"],
     ["company_type", "company_status", "cd_entidade", "company_number", "company_address_1", "Назва"]),
    ("idbyfield", "id",
     ["id", "stop_id", "MA11_OBJEKT_ID", "BEVOEGD GEZAG NUMMER", "номер", "番号", "번호", "identifiant"],
     ["_id", "idea", "width", "Kód obce", "Kod pocztowy siedziby"]),
])
def test_generic_field_names(rule_id, key, good, bad):
    spec = load(GENERIC, rule_id)
    assert spec["key"] == key and spec["priority"] == 1
    for name in good:
        assert field_matches(GENERIC, rule_id, name), name
    for name in bad:
        assert not field_matches(GENERIC, rule_id, name), name


@pytest.mark.parametrize("value,expected", [
    ("SIA Būvnieks", True), ("Vindobini GmbH", True), ("Adler-Apotheke e.K.", True), ("Telefónica S.A.", True),
    ("Banco do Brasil S/A", True), ("株式会社ほげ", True), ("㈜대한건설", True), ("台北有限公司", True),
    ("ООО Ромашка", True), ("Acme Ltd", True), ("Bygg AS", True),
    ("LTD", False), ("LTD - Private Company Limited by Shares", False), ("Lazkov G.A.", False),
    ("Kubentayev S.A. | Alibekov D.T.", False), ("che sia così", False), ("5 kg", False), ("as long as", False),
    ("Public Prosecution", False), ("12345", False), (None, False),
])
def test_has_legal_form(value, expected):
    assert has_legal_form(value) is expected


# --- #56: identifier rules that matched other codes -------------------------------------

@pytest.mark.parametrize("path,rule_id,refused", [
    ("common/telecom.yaml", "imeivalue", ["19974968000013", "05938540000134", "50076628911092"]),
    ("basic/identifiers.yaml", "mongodbidfield", ["9029172", "252", "1"]),
    ("common/objects.yaml", "objects_gtinfield", ["00-0003-01", "12345678"]),
    ("common/crossborder_finance.yaml", "bicvalue", ["STIMMBEZIRK", "BRIEFWAHLBEZIRK"]),
    ("en/en_common.yaml", "endescriptiondetails", ["4585/8", "24880"]),
    ("gb/gb_geo.yaml", "ukwardnamebyknown", ["3", "8"]),
    ("it/it_geo.yaml", "itpostcodeknown", ["0", "0.36"]),
    ("fr/fr_tax.yaml", "frsiretvalue", ["05938540000134", "50076628911092"]),
    ("de/de_geo.yaml", "deagsknown", ["130030000000"]),
])
def test_values_that_are_refused(path, rule_id, refused):
    for value in refused:
        assert not value_matches(path, rule_id, value), value


@pytest.mark.parametrize("path,rule_id,accepted", [
    ("common/telecom.yaml", "imeivalue", ["490154203237518"]),
    ("basic/identifiers.yaml", "mongodbidfield", ["6167df39d9af277471403f52"]),
    ("basic/identifiers.yaml", "arcgisobjectidvalue", ["9029172", "252", "89.0"]),
    ("common/objects.yaml", "objects_gtinfield", ["09506000134352"]),
    ("common/crossborder_finance.yaml", "bicvalue", ["DEUTDEFF", "NEDSZAJJXXX"]),
    ("en/en_common.yaml", "endescriptiondetails", ["Two-storey building"]),
    ("gb/gb_geo.yaml", "ukwardnamebyknown", ["Abbey"]),
    ("it/it_geo.yaml", "itpostcodeknown", ["50121"]),
    ("fr/fr_tax.yaml", "frsiretvalue", ["19974968000013", "49185036800011"]),
    ("de/de_geo.yaml", "deagsarsknown", ["130030000000"]),
    ("de/de_geo.yaml", "deagsknown", ["13003000"]),
])
def test_values_that_are_accepted(path, rule_id, accepted):
    for value in accepted:
        assert value_matches(path, rule_id, value), value


@pytest.mark.parametrize("path,rule_id,allowed,refused", [
    ("fr/fr_persons.yaml", "frcnivalue", "cni", "id"),
    ("pii/fr/fr_pii.yaml", "fr_pii_frcnivalue", "numero_cni", "id"),
    ("eg/eg_persons.yaml", "egnationalidvalue", "national_id", "siret"),
    ("pii/eg/eg_pii.yaml", "eg_pii_egnationalidvalue", "national_id", "cnpj"),
    ("en/en_environment.yaml", "enenergypointvalue", "plant_id", "nuts3"),
    ("basic/identifiers.yaml", "mongodbidfield", "_id", "id"),
    ("basic/identifiers.yaml", "arcgisobjectidvalue", "objectid", "_id"),
    ("common/objects.yaml", "objects_gtinfield", "product_id", "id"),
    ("pii/us/us_pii.yaml", "usnpivalue", "npi", "時間軸コード"),
    ("us/us_persons.yaml", "us_persons_usnpivalue", "national_provider_identifier", "phone"),
    ("us/us_persons.yaml", "ennpivalue", "npi_number", "id"),
])
def test_value_rules_need_their_field_names(path, rule_id, allowed, refused):
    assert guarded_by(path, rule_id, allowed) and not guarded_by(path, rule_id, refused)


def test_field_rules_that_fired_on_common_words():
    assert not field_matches("common/texts.yaml", "headlinefield", "title")
    assert field_matches("common/texts.yaml", "headlinefield", "article_title")
    assert not field_matches("it/it_persons.yaml", "itfirstnameknown", "nome")
    assert field_matches("it/it_geo.yaml", "itnomeknown", "nome")
    assert not field_matches("common/geo.yaml", "streetaddressbyfield", "company_address_4")
    assert field_matches("common/geo.yaml", "streetaddressbyfield", "company_address_1")
    # AKT_TIMESTAMP holds dates: a timestamp name is evidence, not a label on its own.
    assert load("common/dateandtime.yaml", "timestampknownpat")["priority"] == 2


def test_zip_code_names_give_postindex_without_a_country():
    spec = load("common/geo.yaml", "postindexzipvalue")
    assert spec["key"] == "postindex" and spec["fieldrule"] == load("us/us_geo.yaml", "uszipcodebyname")["fieldrule"]


# --- #55: dates and datetimes --------------------------------------------------------------

def test_date_names_and_patterns():
    assert load("fr/fr_datetime.yaml", "frdatetimename")["key"] == "date"
    assert not value_matches("nl/nl_datetime.yaml", "nldatetimepattern", "01-01-1920")
    assert value_matches("nl/nl_datetime.yaml", "nldatepattern", "01-01-1920")
    assert not value_matches("nl/nl_datetime.yaml", "nldatepattern", "31-02-2020")


@pytest.mark.parametrize("value,expected", [
    ("01-01-1920", True), ("31-12-2025", True), ("29-02-2024", True), ("29-02-2023", False),
    ("31-04-2020", False), ("01-13-2020", False), ("01-01-20", False), ("", False), (None, False),
])
def test_validate_dmy_date(value, expected):
    assert validate_dmy_date(value) is expected


# --- validators ---------------------------------------------------------------------------

def test_coordinates_of_a_point():
    assert value_matches("common/geo.yaml", "coordinategeobyknown", "[16.36984624, 48.20057929]")
    assert value_matches("common/geo.yaml", "coordinategeobyknown", "-3.70,40.41")
    assert not value_matches("common/geo.yaml", "coordinategeobyknown", "[[[16.36984624, 48.20057929], [16.37, 48.2]]]")


def test_small_validators():
    assert validate_eea_station_code("DEBB003") and not validate_eea_station_code("USAB123")
    assert validate_bic_country("DEUTDEFF") and not validate_bic_country("STIMMBEZ")
    assert has_letters("Centro") and not has_letters("17") and not has_letters(None)
    assert validate_fr_siret("19974968000013") and not validate_fr_siret("05938540000134")
