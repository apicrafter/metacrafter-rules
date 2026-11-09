"""Rules for the datatypes of metacrafter-registry #171-#174, from the third metacrafter-testdata
pass (#66).

Matched as tests/test_testdata_baseline.py matches them. A field rule's ``validator`` checks the
values of the field (metacrafter keeps the name match when at least half of them pass).
"""
import importlib

import pytest

from metacrafterext.rules.common.formats import (
    validate_file_formats,
    validate_gml_poslist,
    validate_json_text,
    validate_wkb,
    validate_xml_text,
)
from tests.test_testdata_baseline import field_matches, guarded_by, load, value_matches


def validator_accepts(path, rule_id, value):
    module, name = load(path, rule_id)["validator"].rsplit(".", 1)
    return bool(getattr(importlib.import_module(module), name)(value))


# Value rules: rule file, rule id, key, values (registry examples, test data), refused values,
# a field name of the guard (None: no guard).
VALUE_RULES = [
    ("lt/lt_common.yaml", "ltlegalformcodevalue", "lt_legal_form_code", ["310", "520", "960"], ["31", "UAB", "031"],
     "form_kodas"),
    ("common/orgs.yaml", "gleifentitycategoryvalue", "gleif_entity_category", ["GENERAL", "FUND", "SOLE_PROPRIETOR"],
     ["COMPANY"], "category"),
    ("us/us_orgs.yaml", "usirssubsectionvalue", "us_irs_subsection_code", ["03", "05", "07"], ["3", "003"],
     "SUBSECTION"),
    ("us/us_orgs.yaml", "usirsfoundationvalue", "us_irs_foundation_code", ["00", "04", "10", "15", "21"],
     ["30", "01", "5"], "FOUNDATION"),
    ("us/us_orgs.yaml", "usirsgroupexemptionvalue", "us_irs_group_exemption_number", ["0928", "3741", "0000"],
     ["928", "09280"], "GROUP"),
    ("us/us_orgs.yaml", "usirsactivityvalue", "us_irs_activity_code", ["031150120", "602000000"],
     ["031 150 120", "03115012"], "ACTIVITY"),
    ("ca/ca_orgs.yaml", "cacracharitycategoryvalue", "ca_cra_charity_category", ["0001", "0160", "0210"],
     ["140", "1140"], "Category"),
    ("eu/eu_funding.yaml", "euorganisationactivitytypevalue", "eu_organisation_activity_type",
     ["HES", "REC", "PRC", "PUB", "OTH"], ["SME"], "activityType"),
    ("common/software.yaml", "jsontextbyvalue", "json_text",
     ['[{"id": "BEL-469", "displayName": "S Mini"}]', '{"a": 1, "b": [2, 3]}'],
     ["{'a': 1}", "[30.5, 50.4]", '{"type": "Point", "coordinates": [30, 10]}', "{}"], None),
    ("common/software.yaml", "xmltextbyvalue", "xml_text",
     ['<ContentType ID="0x" Name="Системный" Group="_Hidden"><Fields /></ContentType>', '<item id="1"/>'],
     ['<ContentType ID="0x">', "<p>Opening <b>hours</b></p>", "<br>", '<!DOCTYPE x [<!ENTITY a "b">]><x>&a;</x>'],
     None),
    ("common/geo.yaml", "wkbbyvalue", "wkb",
     ["0101000000000000000000F03F000000000000F03F", "0101000020E6100000000000000000F03F000000000000F03F"],
     ["POINT (1 1)", "0101000000000000000000F03F", "d41d8cd98f00b204e9800998ecf8427e"], None),
]


@pytest.mark.parametrize("path,rule_id,key,good,bad,guard", VALUE_RULES, ids=[t[1] for t in VALUE_RULES])
def test_value_rules_for_new_types(path, rule_id, key, good, bad, guard):
    spec = load(path, rule_id)
    assert spec["key"] == key and spec["type"] == "data"
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value
    if guard is None:
        assert "fieldrule" not in spec
    else:
        assert guarded_by(path, rule_id, guard), guard
        assert not guarded_by(path, rule_id, "name"), "guard too broad"


# Field rules with a value check: rule file, rule id, key, names, other names, values that fit,
# values that do not.
FIELD_RULES = [
    ("common/orgs.yaml", "legalformbyfield", "legal_form",
     ["Codigo de sociedad", "form_pavadinimas", "ΝΟΜΙΚΗ ΜΟΡΦΗ", "attributes.entity.legalForm.other",
      "properties.teisine_forma_pavadinimas", "Rechtsform", "forme_juridique", "Организационно-правовая форма"],
     ["attributes.entity.legalForm.id", "legal_form_code", "form_kodas", "Forma"],
     ["SpA", "EIRL", "Uždaroji akcinė bendrovė", "ΝΠΔΔ", "Mutual Fund", "310 - Uždaroji akcinė bendrovė"],
     ["K09K", "8888", "310", "https://example.org/form"]),
    ("es/es_common.yaml", "esaplicacionpresupuestariabyfield", "es_aplicacion_presupuestaria",
     ["APLICACION PRESUPUESTARIA", "Aplicación presupuestaria", "aplicaciones_presupuestarias"],
     ["partida", "presupuesto"],
     ["2026 001130 - 33210 - 62999", "2026 001120 - 13610 - 22104 \n2027 001120 - 13610 - 22104 ",
      "2026 800708 -  -  1.815,00\n2027 800708 -  -  1.815,00"],
     ["33210", "Sin aplicación"]),
    ("it/it_geo.yaml", "itistatprovincebyfield", "it_istat_province_code",
     ["Codice Provincia (Storico)(1)", "codice_provincia", "COD_PROV", "cod_provincia_istat"],
     ["Sigla automobilistica", "Denominazione della provincia"], ["001", "015", "058", "111"], ["TO", "1", "0001", "000"]),
    ("hu/hu_common.yaml", "hucountycodebyfield", "hu_county_code", ["Megye", "megye_kod", "Megyekód"],
     ["Megye megnevezése", "county"], ["01", "05", "20"], ["21", "5", "Baranya"]),
    ("hu/hu_common.yaml", "huneakspecialtybyfield", "hu_neak_specialty_code", ["Szakmakód", "szakma_kod"],
     ["Szakma megnevezése"], ["2200", "0200", "010C"], ["100", "Belgyógyászat"]),
    ("ro/ro_common.yaml", "rocountycodebyfield", "ro_county_code", ["JUD", "cod_judet", "Cod județ"],
     ["Judecătoria", "SIRUTA"], ["1", "2", "40", "52"], ["45", "0", "Alba"]),
    ("cz/cz_geo.yaml", "czruiancastobcebyfield", "cz_ruian_cast_obce_code", ["Kód části obce", "kod_casti_obce"],
     ["Název části obce", "Kód obce"], ["22969", "229851"], ["2296", "Latrán"]),
    ("de/de_geo.yaml", "debundestagwahlkreisbyfield", "de_bundestag_wahlkreis",
     ["Wahlkreis", "Wahlkreisnummer", "Bundestagswahlkreis", "WKR_NR"], ["Wahlkreisname", "Wahlbezirk"],
     ["5 - Kiel", "1 - Flensburg - Schleswig", "299"], ["300", "Kiel", "0"]),
    ("common/telecom.yaml", "phoneareacodebyfield", "phone_area_code",
     ["Telefonvorwahl", "Vorwahl", "area_code", "phone_area_code", "Prefisso"], ["Telefon", "area", "phone"],
     ["0221", "0211", "02151", "212"], ["0221 123456", "01", "123", "E09000001"]),
    ("common/science.yaml", "oastatusbyfield", "oa_status", ["open_access.oa_status", "oa_status", "OA status"],
     ["open_access.is_oa", "status"], ["gold", "green", "hybrid", "bronze", "closed", "diamond"], ["open", "true"]),
    ("common/science.yaml", "taxonnamebyfield", "taxon_name", ["kingdom", "family", "genus", "phylum"],
     ["species", "scientificName", "familyName"], ["Animalia", "Formicidae", "Tetramorium", "Arthropoda"],
     ["Solenopsis geminata", "smith", "Ab"]),
    ("common/science.yaml", "taxonclassorderbyfield", "taxon_name", ["class", "order"], ["classification"],
     ["Insecta", "Hymenoptera", "Mammalia", "Aves", "Passeriformes", "Asparagales"],
     ["Economy", "Standard", "First", "1A"]),
    ("common/science.yaml", "dwcinstitutioncodebyfield", "dwc_institution_code", ["institutionCode"],
     ["institution_code", "institution"], ["APQA", "MVZ", "NHMUK"], ["12345", "Museum of Zoology"]),
    ("common/dateandtime.yaml", "schoolyearbyfield", "school_year",
     ["properties.annoscolas", "anno_scolastico", "school_year", "Schuljahr", "Учебный год"],
     ["year", "anno"], ["202526", "2025/26", "2025-2026"], ["2025", "2025/27", "202527"]),
    ("common/internet.yaml", "wifissidbyfield", "wifi_ssid", ["ssid", "SSID", "wifi_ssid"], ["sid", "wifi"],
     ["LinkNYC Free Wi-Fi", "GuestWiFi"], ["https://example.org/wifi", "x" * 33]),
    ("common/software.yaml", "fileformatbyfield", "file_format", ["Форматы", "format", "file_format", "Formats"],
     ["formation", "format_date"], ["XML", "HTML,CSV,XLS,XML", "GeoJSON", "xlsx; csv"], ["text/csv", "A4", "Hardcover"]),
    ("common/geo.yaml", "gmlposlistbyfield", "gml_poslist",
     ["properties.geom.geom.Point.pos", "gml:posList", "posList"], ["position", "pos_code"],
     ["1680488.064 4846572.711", "123629.78 379674.57 123700.0 379674.57", "1 2 3"],
     ["1680488.064,4846572.711", "12", "POS 12"]),
]


@pytest.mark.parametrize("path,rule_id,key,names,others,fit,unfit", FIELD_RULES, ids=[t[1] for t in FIELD_RULES])
def test_field_rules_with_value_checks(path, rule_id, key, names, others, fit, unfit):
    assert load(path, rule_id)["key"] == key
    for name in names:
        assert field_matches(path, rule_id, name), name
    for name in others:
        assert not field_matches(path, rule_id, name), name
    for value in fit:
        assert validator_accepts(path, rule_id, value), value
    for value in unfit:
        assert not validator_accepts(path, rule_id, value), value


# Field rules by standard terms (Darwin Core, GTFS) and the extended unit-of-measure names.
NAME_RULES = [
    ("common/science.yaml", "dwcoccurrenceidbyfield", "dwc_occurrence_id", ["occurrenceID", "dwc:occurrenceID"],
     ["occurrence", "id"]),
    ("common/science.yaml", "dwccatalognumberbyfield", "dwc_catalog_number", ["catalogNumber"], ["catalog", "number"]),
    ("common/transport.yaml", "gtfsstopidbyfield", "gtfs_stop_id", ["stop_id", "parent_station"], ["stop_name", "id"]),
    ("common/transport.yaml", "gtfszoneidbyfield", "gtfs_zone_id", ["zone_id"], ["zone", "time_zone"]),
    ("common/trade.yaml", "unitofmeasurebyfield", "unit_of_measure",
     ["単位", "Единица", "Einheit", "unit_of_measure", "UoM"], ["unit_price", "Verwaltungseinheit"]),
]


@pytest.mark.parametrize("path,rule_id,key,names,others", NAME_RULES, ids=[t[1] for t in NAME_RULES])
def test_name_rules_for_new_types(path, rule_id, key, names, others):
    assert load(path, rule_id)["key"] == key
    for name in names:
        assert field_matches(path, rule_id, name), name
    for name in others:
        assert not field_matches(path, rule_id, name), name


def test_russian_units_by_field_name():
    assert guarded_by("ru/ru_codes.yaml", "ruokeisymbolbyfield", "Единица")
    assert value_matches("ru/ru_codes.yaml", "ruokeisymbolbyfield", "мкг/м3")


def test_wkb_bytes_of_geoparquet():
    # GeoParquet keeps the geometry as bytes; metacrafter passes their text form.
    point = bytes.fromhex("0101000000000000000000F03F000000000000F03F")
    assert validate_wkb(point)
    assert validate_wkb(str(point))
    polygon_header = bytes.fromhex("01030000000100000005000000") + bytes(80)
    assert validate_wkb(str(polygon_header))
    assert not validate_wkb(str(b"\x02\x03\x00\x00\x00"))


def test_format_helpers():
    assert validate_json_text('[{"id": 1}, {"id": 2}]')
    assert not validate_json_text("[1, 2, 3]")
    assert not validate_xml_text("<div><p>x</p></div>")
    assert validate_gml_poslist("1 2 3 4 5 6")
    assert not validate_gml_poslist("1 2 3 4 5")
    assert validate_file_formats("CSV")
    assert not validate_file_formats("")
