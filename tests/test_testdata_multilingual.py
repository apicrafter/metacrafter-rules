"""Rules added or fixed after the multilingual metacrafter-testdata scan (#52).

Field rules are matched as metacrafter matches them: text rules by lower-cased membership,
regex rules with ``fullmatch`` on the name and the lower-cased name. Value rules with a field
guard only apply to fields whose lower-cased name is in the guard.
"""
import pathlib
import re

import pytest
import yaml

from metacrafterext.rules.common.identifiers import validate_cl_rut, validate_fi_ytunnus
from metacrafterext.rules.es.validators import validate_es_cif

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


# --- field names found in the testdata files -----------------------------------------

@pytest.mark.parametrize("path,rule_id,key,names", [
    ("jp/jp_geo.yaml", "jplatitudeknown", "latitude", ["緯度"]),
    ("jp/jp_geo.yaml", "jplongitudeknown", "longitude", ["経度"]),
    ("jp/jp_geo.yaml", "jplgcodeknown", "jp_lg_code", ["全国地方公共団体コード", "市区町村コード"]),
    ("jp/jp_geo.yaml", "jpmoneyknown", "money", ["予定価格", "落札金額", "最低制限価格"]),
    ("ko/ko_common.yaml", "kolatitudeknown", "latitude", ["위도"]),
    ("ko/ko_common.yaml", "kolongitudeknown", "longitude", ["경도"]),
    ("it/it_geo.yaml", "itlatitudeknown", "latitude", ["latitudine"]),
    ("it/it_geo.yaml", "itlongitudeknown", "longitude", ["longitudine"]),
    ("common/geo.yaml", "eastingbyfield", "easting",
     ["Easting", "UTMRechtswert", "X-UTM32N", "utm_x", "coordx_origine", "Souřadnice Y"]),
    ("common/geo.yaml", "northingbyfield", "northing",
     ["Northing", "UTMHochwert", "Y-UTM32N", "utm_y", "coordy_origine", "Souřadnice X"]),
    ("common/geo.yaml", "postindexbyfield", "postindex",
     ["Supplier Post Code", "station zip code", "address.postal-code", "mailing_zipcode"]),
    ("common/geo.yaml", "streetaddressbyfield", "street_address",
     ["5. STREET ADDRESS", "company_address_1", "Address Line 2", "registered_address"]),
    ("common/values.yaml", "moneyamountbyfield", "money",
     ["Amount", "Net Amount", "IMPORTE ADJUDICACION IVA INC.", "MONTO_DEFINITIVO", "montant",
      "Bedrag (x1000)", "importo_euro"]),
    ("de/de_geo.yaml", "depostcodeknown", "postindex", ["PLZ", "Postleitzahl"]),
    ("de/de_geo.yaml", "deagsknown", "de_ags", ["Gemeindeschluessel", "gemeinde_schluessel", "AGS"]),
    ("de/de_geo.yaml", "dearsknown", "de_ars", ["Amtlicher Regionalschlüssel"]),
    ("de/de_geo.yaml", "dekreisknown", "de_kreisschluessel", ["kreis_schluessel"]),
    ("at/at_geo.yaml", "atgkzknown", "at_gkz", ["GKZ", "STATAUSTRIA_GEM_CODE"]),
    ("ch/ch_geo.yaml", "chbfsgemeindeknown", "ch_bfs_gemeinde", ["bfsnr", "BFS_NR"]),
    ("cz/cz_geo.yaml", "czpostcodeknown", "postindex", ["PSČ"]),
    ("cz/cz_geo.yaml", "czmunicipalityknown", "cz_municipality_code", ["Kód obce"]),
    ("cz/cz_geo.yaml", "czstreetknown", "street", ["Název ulice"]),
    ("fr/fr_geo.yaml", "frpostcodeknown", "postindex", ["Code_postal"]),
    ("fr/fr_geo.yaml", "frcodgeoknown", "inseecode", ["CODGEO", "code_commune", "DEPCOM"]),
    ("es/es_geo.yaml", "esstreetknown", "street", ["CALLE"]),
    ("es/es_geo.yaml", "espostcodespelledknown", "espostcode", ["COD. POSTAL", "Código postal"]),
    ("eu/eu_procurement.yaml", "nutslevelbyfield", "nutsregion", ["NUTS1", "nuts_3_code", "NUTS3"]),
    ("gb/gb_geo.yaml", "ukgsscodebyfield", "ukgsscode",
     ["LSOA (code)", "ParliamentaryConstituency (code)", "LSOA21CD", "LAD23CD"]),
    ("ie/ie_geo.yaml", "ieeircodeknown", "ie_postcode", ["eircode"]),
    ("se/se_finances.yaml", "seorgnumberknownname", "seorgnumber", ["PeOrgNr", "orgnr"]),
    ("fi/fi_companies.yaml", "fiytunnusknown", "fi_ytunnus", ["Y-tunnus", "ytunnus"]),
    ("cl/cl_finances.yaml", "clrutknown", "cl_rut", ["rut_empresa"]),
])
def test_field_names_from_testdata(path, rule_id, key, names):
    assert load(path, rule_id)["key"] == key
    for name in names:
        assert field_matches(path, rule_id, name), name


@pytest.mark.parametrize("path,rule_id,names", [
    ("common/geo.yaml", "eastingbyfield", ["east", "x", "coorx", "beast"]),
    ("common/geo.yaml", "postindexbyfield", ["code", "post", "zip", "zipper_code"]),
    ("common/values.yaml", "moneyamountbyfield", ["amounts_count", "montante", "betragen", "quantity"]),
    ("gb/gb_geo.yaml", "ukgsscodebyfield", ["county code", "code", "lsoa_name"]),
    ("es/es_geo.yaml", "esstreetknown", ["via"]),
    ("cl/cl_finances.yaml", "clrutknown", ["run", "rut"]),
])
def test_names_that_must_not_match(path, rule_id, names):
    for name in names:
        assert not field_matches(path, rule_id, name), name


def test_generic_names_are_name_evidence_only():
    # rut is also the Uruguayan tax number; district code exists in every country.
    assert load("cl/cl_finances.yaml", "clrutsharedname")["priority"] == 3
    assert load("gb/gb_geo.yaml", "ukdistrictcodegenericfield")["priority"] == 3
    assert "district code" not in load("gb/gb_geo.yaml", "ukdistrictcodefield")["rule"].split(",")


# --- value rules of other countries need their field names ---------------------------

@pytest.mark.parametrize("path,rule_id,allowed,refused", [
    ("id/id_persons.yaml", "idpassportvalue", "passport_number", "lsoa (code)"),
    ("pii/id/id_pii.yaml", "id_pii_idpassportvalue", "paspor", "msoa (code)"),
    ("ch/ch_persons.yaml", "chpassportvalue", "reisepass", "lsoa (code)"),
    ("pii/ch/ch_pii.yaml", "ch_pii_chpassportvalue", "swiss_passport", "lsoa (code)"),
    ("kr/kr_persons.yaml", "krpassportvalue", "여권번호", "lsoa (code)"),
    ("pii/kr/kr_pii.yaml", "kr_pii_krpassportvalue", "passport", "lsoa (code)"),
    ("vn/vn_persons.yaml", "vn_persons_vnpassportvalue", "so_ho_chieu", "lsoa (code)"),
    ("pii/vn/vn_pii.yaml", "vnpassportvalue", "ho_chieu", "lsoa (code)"),
    ("es/es_tax.yaml", "escifvalue", "cif", "lsoa (code)"),
    ("ru/ru_orgs.yaml", "rukpp", "кпп", "gemeindeverband_schluessel"),
    ("sa/sa_persons.yaml", "sa_persons_saiqamavalue", "iqama_number", "peorgnr"),
    ("pii/sa/sa_pii.yaml", "saiqamavalue", "iqama", "peorgnr"),
    ("de/de_transport.yaml", "devehicleplatevalue", "kennzeichen", "id_pdc_local"),
])
def test_value_rules_are_guarded_by_field_names(path, rule_id, allowed, refused):
    spec = load(path, rule_id)
    assert spec["type"] == "data" and spec["fieldrulematch"] == "text"
    names = {k.strip().lower() for k in spec["fieldrule"].split(",")}
    assert allowed in names and refused not in names


def test_cif_and_nie_values_have_validators():
    assert load("es/es_tax.yaml", "escifvalue")["validator"].endswith("validate_es_cif")
    assert load("pii/es/es_pii.yaml", "es_pii_esnievalue")["validator"].endswith("validate_es_nie")


# --- validators ----------------------------------------------------------------------

@pytest.mark.parametrize("value,expected", [
    ("0112038-9", True), ("01120389", True), ("0112038-8", False), ("1111111-1", False),
    ("0000000-0", False), ("112038-9", False), ("", False), (None, False),
])
def test_validate_fi_ytunnus(value, expected):
    assert validate_fi_ytunnus(value) is expected


@pytest.mark.parametrize("value,expected", [
    ("78325576-6", True), ("78.325.576-6", True), ("78325555-3", True), ("78325576-5", False),
    ("95566826K", True), ("95.566.826-K", True), ("676347704", True),
    ("11.111.111-1", False), ("78325576", False), ("", False), (None, False),
])
def test_validate_cl_rut(value, expected):
    assert validate_cl_rut(value) is expected


def test_validate_cl_rut_check_letter_k():
    # 10 as the check value is written K: take the first body above 12345670 that has it.
    def check(body):
        return 11 - sum(int(d) * (2 + i % 6) for i, d in enumerate(reversed(body))) % 11

    body = next(str(n) for n in range(12345670, 12345800) if check(str(n)) == 10)
    assert validate_cl_rut(body + "-K") and validate_cl_rut(body + "-k")
    assert not validate_cl_rut(body + "-0")


@pytest.mark.parametrize("value,expected", [
    ("A28015865", True), ("A28015864", False), ("A2801586E", False), ("B1234567X", False),
    ("Q2826000H", True), ("Q28260008", False), ("28015865A", False), ("", False), (None, False),
])
def test_validate_es_cif(value, expected):
    assert validate_es_cif(value) is expected
