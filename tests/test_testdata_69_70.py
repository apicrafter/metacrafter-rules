"""Wrong labels (#69) and missed types (#70) of the fully annotated metacrafter-testdata, and the
rules for the registry datatypes unixtime_ms and ietf_rfc (metacrafter-registry#182). The second
pass of #69: US county names, and the wrong labels of the earlier baseline. The third pass:
Unix milliseconds in date fields (the ``fieldregex`` guard) and higher taxa by value.

Matched as tests/test_testdata_baseline.py matches them. A field rule's ``validator`` checks the
values of the field: metacrafter keeps the name match when at least half of them pass.
"""
import importlib
import re

import pytest

from metacrafterext.rules.common.common import _validate_email, _validate_filename
from metacrafterext.rules.common.dateandtime import validate_unixtime_ms
from metacrafterext.rules.common.generic import (
    validate_category_value,
    validate_date_value,
    validate_german_long_date,
    validate_gss_code,
    validate_iata_airline_code,
    validate_icao_airline_code,
    validate_id_value,
    validate_lonlat_number,
    validate_name_not_street,
    validate_name_text,
    validate_oid,
    validate_person_name_part,
    validate_species_name,
    validate_version_value,
    validate_year_value,
)
from metacrafterext.rules.common.identifiers import validate_iban, validate_no_orgnr
from metacrafterext.rules.common.internet import (
    validate_ietf_rfc,
    validate_ipv4_subnet,
    validate_ipv6_subnet,
    validate_mac_digits,
)
from metacrafterext.rules.common.placeholders import is_missing_text
from metacrafterext.rules.common.taxa import validate_higher_taxon_name
from metacrafterext.rules.mx.validators import validate_mx_rfc
from metacrafterext.rules.us.validators import validate_us_county_fips, validate_us_county_name
from tests.test_testdata_baseline import field_matches, guarded_by, load, value_matches


def validator_of(path, rule_id):
    module, name = load(path, rule_id)["validator"].rsplit(".", 1)
    return getattr(importlib.import_module(module), name)


# --- validators: values that fit, values that do not --------------------------------------
VALIDATORS = [
    (validate_lonlat_number, ["16.25362921", "-3.703660160446558", "0.0", "-179.5", "48"],
     ["570181.18", "6592327.82", "1680154.06915773", "", "abc", "nan"]),
    (validate_year_value, ["2024", "2024.0", "1802", "2019/20", "FY2020", "平成4年"], ["58", "21", "226", "0", "", "3001"]),
    (validate_date_value, ["2024-01-05", "05.01.2024", "20240105", "1689019752", "44927", "18. November 1827"],
     ["8", "113", "2024", "[2024]", "0", ""]),
    (validate_category_value, ["Adjudicación directa", "H", "Active", "1", "Limited company"],
     ["true", "False", "2019-11-27", "2016-12-01T00:00:00", "http://covid19faq.ru/l/ru/category/x",
      "/l/ru/category/sektq6cyzf-vaccination", ""]),
    (validate_version_value, ["1.2.3", "v2", "2024.01", "3b"], ["publishedVersion", "acceptedVersion", "", "1", "12"]),
    (validate_person_name_part, ["Абабкова", "Ольга", "Магомет-Башировна", "Ахмед оглы", "O'Neil"],
     ["Иванов Иван Иванович Петров", "ООО 123", "12", "", "a" * 41]),
    (validate_name_text, ["Федеральная налоговая служба", "Acme Ltd", "Café 58"],
     ["58c84c461752ab5b2544a566", "bcffc6c0-15fc-4a31-8913-6179db57d72c", "1", "https://x.org", "a@b.org"]),
    (validate_oid, ["1.2.840.113549", "2.5.4.3", "urn:oid:1.3.6.1"], ["353432", "3.1.2", "1", "1.02.3"]),
    (validate_gss_code, ["E09000001", "W05000001", "S12000033"], ["H", "J", "E0900000", "X09000001"]),
    (validate_iata_airline_code, ["EB", "6V", "U2"], ["PLM", "12", "e"]),
    (validate_icao_airline_code, ["PLM", "AXY"], ["EB", "LFPG", "pl1"]),
    (validate_german_long_date, ["18. November 1827", "7. März 1833", "2. Oktober 1902", "1.Mai 2000"],
     ["31. Februar 1900", "18 November 1827", "18. Novembre 1827"]),
    (validate_unixtime_ms, ["1689019752000", "-1019869200000", "936050400000", "1794571609018", "1689019752000.0"],
     ["1689019752", "4102444800000", "-2208988800001", "16890197520000", "abc"]),
    (validate_species_name, ["Paratrechina longicornis (Latreille, 1802)", "Solenopsis geminata (Fabricius, 1804)",
                             "Monomorium chinense Santschi, 1925", "Quercus robur L.", "Abies alba Mill."],
     ["Solenopsis geminata", "Main street Station", "New York City Hall", "Formicidae"]),
    (validate_ipv4_subnet, ["0.0.0.0/8", "100.64.0.0/10", "255.255.255.255/32"],
     ["192.0.0.0/24 [2]", "10.0.0.0/33", "300.0.0.0/8", "10.0.0.0"]),
    (validate_ipv6_subnet, ["2001:200::/23", "2002::/16", "::/0"], ["2001:200::/129", "2001:200::", "10.0.0.0/8"]),
    (validate_mac_digits, ["00405abf7503", "A4B1C2D3E4F6"], ["01405abf7503", "000000000000", "00405abf750", "00:40:5a:bf:75:03"]),
    (validate_ietf_rfc, ["[RFC 1918]", "[RFC 791, Section 3.2]", "[RFC 1122, Section 3.2.1.3]", "RFC 6598",
                         "[RFC 8190]; [RFC 919, Section 7]"],
     ["RFC", "[RFC 0]", "GODE561231GR8", "RFC-1918"]),
    (validate_no_orgnr, ["922727457", "914459265", "872417842", "974 760 673", "NO 974760673 MVA"],
     ["922727458", "123456785", "92272745", "999999999"]),
    (validate_mx_rfc, ["GODE561231GR8", "ABC010203XY1", "GODE-561231-GR8"], ["[RFC 1918]", "GODE561331GR8", "GODE56123GR8"]),
    (validate_us_county_fips, ["36001", "06037", "72001"], ["36", "001", "36000", "99001", "3600a"]),
    (_validate_email, ["anna@example.org", "Anna <anna@example.org>"],
     ["https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=51.17%2C4.34", "x@y", "no at sign"]),
    (_validate_filename, ["report 2020.pdf", "data.csv"],
     ["La versión pública fue aprobada: https://gobiernoabierto.example.mx/wp-content/uploads/ACTA.pdf",
      "https://example.org/a.pdf"]),
    (validate_iban, ["DE18 7500 0000 0075 0010 21", "DE89 3704 0044 0532 0130 00"],
     ["DE18 7500 0000 0075 0010 22"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    assert [v for v in good if not func(v)] == []
    assert [v for v in bad if func(v)] == []


# --- #69: field-name rules check their values -----------------------------------------------
# rule file, rule id, values of the field that fit, values that do not
FIELD_VALUE_CHECKS = [
    ("common/geo.yaml", "coordinategeobyknown", ["16.37", "48.21", "0.0"], ["570181.18", "6592327.82"]),
    ("common/geo.yaml", "countryknown", ["Norway", "US"], ["226"]),
    ("common/geo.yaml", "addressknown", ["Main St 1"], ["168"]),
    ("common/dateandtime.yaml", "yearknown", ["2024"], ["58"]),
    ("common/dateandtime.yaml", "dateknown", ["2024-01-05"], ["26", "2024"]),
    ("common/dateandtime.yaml", "datetimeknown", ["2024-01-05T10:00:00"], ["8"]),
    ("common/dateandtime.yaml", "modifieddatebyknown", ["2024-01-05T10:00:00"], ["113"]),
    ("pt/pt_datetime.yaml", "ptdateknown", ["05/01/2024"], ["26"]),
    ("common/culture.yaml", "artmediumfield", ["oil on canvas"], ["24"]),
    ("common/texts.yaml", "descriptionfield", ["A text"], ["89"]),
    ("en/en_common.yaml", "endescriptionknown", ["A text"], ["58"]),
    ("common/software.yaml", "versionbyknown", ["1.2.3"], ["publishedVersion"]),
    ("common/generic.yaml", "categorybyfield", ["Active"], ["true", "2019-11-27", "http://x.org/category/a"]),
    ("common/intcodes.yaml", "languagetagfield", ["fi", "sv-FI"], ["1", "2"]),
    ("common/objects.yaml", "oidfield", ["1.2.840.113549"], ["353432"]),
    ("common/dublincore.yaml", "authorfield", ["Leo Tolstoy"], ["1"]),
    ("mx/mx_persons.yaml", "mxrfcknown", ["GODE561231GR8"], ["[RFC 1918]"]),
    ("pii/mx/mx_pii.yaml", "mx_pii_mxrfcknown", ["GODE561231GR8"], ["[RFC 1918]"]),
    ("gb/gb_geo.yaml", "ukgsscodebyfield", ["E09000001"], ["H"]),
    ("common/generic.yaml", "orgnamebyfield", ["Acme Ltd"], ["58c84c461752ab5b2544a566"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELD_VALUE_CHECKS, ids=[c[1] for c in FIELD_VALUE_CHECKS])
def test_field_rules_check_values(path, rule_id, good, bad):
    spec = load(path, rule_id)
    assert spec["type"] == "field"
    check = validator_of(path, rule_id)
    assert all(check(v) for v in good)
    assert not any(check(v) for v in bad)


def test_id_attribute_of_an_xml_id_element_is_not_an_id():
    path = "common/generic.yaml"
    for name in ("ProcurementProjectLot.ID.#text", "ContractingParty.Party.PartyIdentification.ID.#text", "stop_id"):
        assert field_matches(path, "idbyfield", name), name
    for name in ("ID.@schemeName", "ProcurementProjectLot.ID.@schemeName",
                 "ContractingParty.Party.PartyIdentification.ID.@schemeName"):
        assert not field_matches(path, "idbyfield", name), name


def test_guarded_value_rules_need_their_field_names():
    # gridnode: ORG-0001 and LOT-0001 of eForms have the shape
    assert guarded_by("en/en_environment.yaml", "engridnodevalue", "grid_node")
    assert not guarded_by("en/en_environment.yaml", "engridnodevalue", "#text")
    # ArcGIS OBJECTID, not any object_id
    assert guarded_by("basic/identifiers.yaml", "arcgisobjectidvalue", "OBJECTID")
    assert not guarded_by("basic/identifiers.yaml", "arcgisobjectidvalue", "object_id")
    # Bank of Russia registration numbers, not any registration number
    assert guarded_by("ru/ru_finances.yaml", "rucbrregnumvalue", "@RegN")
    assert not guarded_by("ru/ru_finances.yaml", "rucbrregnumvalue", "Регистрационный номер")


def test_username_is_not_a_user_id():
    assert field_matches("pii/pii.yaml", "usernamebyknown", "username")
    assert not field_matches("pii/pii.yaml", "usernamebyknown", "user_id")
    assert not field_matches("pii/pii.yaml", "usernamebyknown", "userid")


def test_chilean_rut_without_separators_needs_a_rut_field():
    path = "cl/cl_finances.yaml"
    for value in ("78325576-6", "12.345.678-5", "76123451-K", "95566826K"):
        assert value_matches(path, "clrutvalue", value), value
    # A Norwegian organisation number passes the same check digit
    assert not value_matches(path, "clrutvalue", "922727457")
    assert value_matches(path, "clrutdigitsvalue", "783255766")
    assert guarded_by(path, "clrutdigitsvalue", "rut")
    assert not guarded_by(path, "clrutdigitsvalue", "organisasjonsnummer")


def test_norwegian_organisation_number():
    path = "no/no_orgs.yaml"
    assert field_matches(path, "noorgnrbyfield", "organisasjonsnummer")
    assert field_matches(path, "noorgnrbyfield", "overordnetEnhet")
    assert value_matches(path, "noorgnrvalue", "922727457")
    assert value_matches(path, "noorgnrvalue", "NO 974760673 MVA")
    assert not value_matches(path, "noorgnrvalue", "922727458")
    assert guarded_by(path, "noorgnrvalue", "organisasjonsnummer")


@pytest.mark.parametrize("path,rule_id,key,field,values", [
    ("common/intcodes.yaml", "iso3166alpha2bylocalname", "countrycode_alpha2", "landkode", ["NO", "SE"]),
    ("common/geo.yaml", "countrybylocalnamevalue", "country", "pays_de_deces", ["France", "Belgique", "Espagne"]),
    ("pl/pl_geo.yaml", "plpowiatvalue", "district", "Powiat siedziby", ["Katowice", "rycki"]),
    ("ru/ru_codes.yaml", "ruokogunamebyfieldvalue", "okoguname", "okoguName", ["Федеральная налоговая служба"]),
])
def test_guarded_rules_outweigh_unnamed_value_lists(path, rule_id, key, field, values):
    # metacrafter drops a value rule without name evidence (boolean no, encountryname, plcity,
    # orgname) when a guarded value rule matched at least as many values
    spec = load(path, rule_id)
    assert spec["key"] == key
    assert guarded_by(path, rule_id, field)
    assert not guarded_by(path, rule_id, "name")
    for value in values:
        assert value_matches(path, rule_id, value), value


def test_new_york_is_a_city_before_a_state():
    states = {v.strip() for v in load("us/us_geo.yaml", "usstatebyvalue")["rule"].split(",")}
    cities = {v.strip() for v in load("us/us_geo.yaml", "uscitybyvalue")["rule"].split(",")}
    assert "New York" in cities and "New York" not in states
    assert "California" in states


# --- #70: missed types ---------------------------------------------------------------------
@pytest.mark.parametrize("path,rule_id,key,good,bad,guard", [
    ("common/internet.yaml", "ipv4subnetvalue", "ipv4subnet", ["0.0.0.0/8", "100.64.0.0/10"], ["10.0.0.0"], None),
    ("common/internet.yaml", "ipv6subnetvalue", "ipv6subnet", ["2001:200::/23", "2002::/16"], ["2001:db8::"], None),
    ("common/internet.yaml", "ietfrfcvalue", "ietf_rfc", ["[RFC 1918]", "[RFC 791, Section 3.2]"], ["RFC"], None),
    ("common/internet.yaml", "macaddressdigitsvalue", "mac_address", ["00405abf7503"], ["00405abf750"], "bssid"),
    ("common/gs1.yaml", "ean13value", "ean", ["4056489789246", "0000020123031"], ["4056489789247"], "Barkod proizvoda"),
    ("de/de_datetime.yaml", "delongdatevalue", "date_german", ["18. November 1827", "7. März 1833"],
     ["18. November 18270"], None),
    ("common/dateandtime.yaml", "unixtimemsvalue", "unixtime_ms", ["1793960864568"], ["1793960864"], None),
    ("common/science.yaml", "speciesnamewithauthorshipvalue", "species",
     ["Paratrechina longicornis (Latreille, 1802)", "Monomorium chinense Santschi, 1925", "Quercus robur L."],
     ["Solenopsis geminata", "Main street Station", "Formicidae"], None),
])
def test_value_rules_for_missed_types(path, rule_id, key, good, bad, guard):
    spec = load(path, rule_id)
    assert spec["key"] == key and spec["type"] == "data"
    assert not spec.get("imprecise")
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value
    if guard:
        assert guarded_by(path, rule_id, guard)


@pytest.mark.parametrize("path,rule_id,key,names,other", [
    ("common/internet.yaml", "ietfrfcbyfield", "ietf_rfc", ["RFC", "reference"], ["rfc_mexico"]),
    ("pii/fr/fr_pii.yaml", "frdeathdayknown", "deathday", ["date_du_deces", "date de décès"], ["date"]),
    ("pii/de/de_pii.yaml", "de_pii_birthdayfield", "birthday", ["Geburtsdatum", "properties.Geburtsdatum"], ["Datum"]),
    ("pii/de/de_pii.yaml", "de_pii_deathdayfield", "deathday", ["Sterbedatum", "Todestag"], ["Datum"]),
    ("us/us_geo.yaml", "usfips64byname", "fips64", ["County FIPS", "fips"], ["State FIPS"]),
    ("common/transport.yaml", "icaoairlinecodebyname", "icaoairlinecode", ["ICAO"], ["icao24"]),
    ("common/transport.yaml", "iataairlinecodebyname", "iataairlinecode", ["IATA"], ["iata_airport"]),
    ("common/dateandtime.yaml", "yearbylocalname", "year", ["Tahun", "shnat_yitzur", "rok"], ["nam", "nefah_manoa"]),
    ("ru/ru_persons.yaml", "russurnamebycyrillicfield", "russurname", ["Фамилия"], ["surname"]),
    ("ru/ru_persons.yaml", "rusfirstnamebycyrillicfield", "rusfirstname", ["Имя"], ["name"]),
    ("ru/ru_persons.yaml", "rusmidnamebycyrillicfield", "rusmidname", ["Отчество"], ["middle_name"]),
])
def test_field_rules_for_missed_types(path, rule_id, key, names, other):
    spec = load(path, rule_id)
    assert spec["key"] == key and spec["priority"] == 1
    if spec["match"] == "regex":
        name_matches = lambda n: field_matches(path, rule_id, n)  # noqa: E731
    else:
        name_matches = lambda n: field_matches(path, rule_id, n.rsplit(".", 1)[-1])  # noqa: E731
    for name in names:
        assert name_matches(name), name
    for name in other:
        assert not name_matches(name), name


def test_field_rules_for_missed_types_check_values():
    assert validator_of("us/us_geo.yaml", "usfips64byname")("36001")
    assert not validator_of("us/us_geo.yaml", "usfips64byname")("36")
    assert validator_of("common/dateandtime.yaml", "yearbylocalname")("2014")
    assert not validator_of("common/dateandtime.yaml", "yearbylocalname")("1598.5")
    assert validator_of("ru/ru_persons.yaml", "rusmidnamebycyrillicfield")("Магомет-Башировна")


def test_nationality_list_has_the_demonyms_of_a_census():
    names = {v.strip().lower() for v in load("pii/pii.yaml", "ennationalitybyvalue")["rule"].split(",")}
    for value in ("Austrian", "Belgian", "Dutch", "Luxembourger", "Portuguese", "New Zealander", "Afghan"):
        assert value.lower() in names, value


def test_milliseconds_in_timestamp_fields_are_unixtime_ms():
    # the milliseconds rule has the timestamp field guard of the seconds rule
    rules = {rule_id: load("common/dateandtime.yaml", rule_id) for rule_id in ("unixtimevalue", "unixtimemsvalue")}
    for line in rules["unixtimevalue"]["fieldrule"].splitlines():
        if "oneOf" not in line:
            assert line in rules["unixtimemsvalue"]["fieldrule"]
    assert not value_matches("common/dateandtime.yaml", "unixtimevalue", "1793960864568")


def test_a_timestamp_field_of_milliseconds_is_not_unixtime():
    check = validator_of("common/dateandtime.yaml", "timestampknown")
    assert check("1471181882") and check("2024-01-05T10:00:00")
    assert not check("1793960864568")


@pytest.mark.parametrize("rule_id,name", [("ripemd160hash", "ripemd160"), ("blake2b256hash", "blake2b256"),
                                          ("blake2b512hash", "blake2b512"), ("keccak256hash", "keccak256"),
                                          ("keccak512hash", "keccak512")])
def test_digests_of_sha_lengths_need_their_names(rule_id, name):
    # an iCalendar UID of 40 hexadecimal digits is no RIPEMD-160 digest; sha1hash stays unguarded
    assert guarded_by("basic/crypto.yaml", rule_id, name)
    assert not guarded_by("basic/crypto.yaml", rule_id, "uid")
    assert "fieldrule" not in load("basic/crypto.yaml", "sha1hash")


# --- #69, second pass: US counties and the older wrong labels -------------------------------
@pytest.mark.parametrize("func,good,bad", [
    (validate_us_county_name,
     ["KENT", "PROVIDENCE", "Washington", "Kent County", "Orleans Parish", "Doña Ana County", "DONA ANA",
      "ST. LOUIS CITY", "Saint Louis", "Prince George's County", "DE KALB", "MIAMI-DADE", "Nome Census Area",
      "Juneau City and Borough", "Mayagüez Municipio", "Kent County, RI", "NEW HAVEN"],
     ["Nairobi", "Kiambu", "Zhambyl District", "West Sussex", "Buckinghamshire", "THE DISTRICT", "County",
      "123", ""]),
    (validate_id_value, ["123", "muoh02ndax", "GB", "abc-def", "58c84c461752ab5b2544a566", "А-1", "Non renseigné"],
     ["新北市板橋區", "新北市三重區", "Central Park", "б/н", ""]),
    (validate_name_not_street, ["Dupont", "Musée du Louvre", "Tour Eiffel - Pilier Est", "AC/DC", "Pont-Aven"],
     ["Bd Raspail / Varenne", "Saxe / Breteuil", "Place du Panthéon/ Clotaire", "Quai Branly", "19, Bd Poissonnière",
      "49 Av Montaigne", "Rue de Rivoli", "1"]),
    (is_missing_text, ["Non renseigné", "NON  RENSEIGNÉ", "n/a", "нет данных", "-"], ["Nairobi", "0", "", None]),
], ids=["validate_us_county_name", "validate_id_value", "validate_name_not_street", "is_missing_text"])
def test_validators_of_the_second_pass(func, good, bad):
    assert [v for v in good if not func(v)] == []
    assert [v for v in bad if func(v)] == []


def test_us_county_names_outweigh_the_city_list_in_county_fields():
    # KENT, PROVIDENCE and WASHINGTON of an EPA TRI 7. COUNTY column are counties, and also US
    # cities: the guarded county rule matches as many values, so metacrafter drops uscity
    path = "us/us_geo.yaml"
    assert load(path, "uscountynamevalue")["key"] == "uscounty"
    for name in ("7\\. COUNTY", "County Name", "County/Parish", "CTYNAME", "county_name"):
        assert guarded_by(path, "uscountynamevalue", name.rsplit(".", 1)[-1].strip()), name
    # GIAS County (name) holds English counties, Kenyan lists have Sub county: not guarded
    for name in ("County (name)", "Sub county", "NAME", "city"):
        assert not guarded_by(path, "uscountynamevalue", name), name
    for value in ("KENT", "PROVIDENCE", "WASHINGTON", "BRISTOL", "NEWPORT", "Autauga County"):
        assert value_matches(path, "uscountynamevalue", value), value
    for value in ("Nairobi", "Kiambu", "Homa Bay", "West Sussex"):
        assert not value_matches(path, "uscountynamevalue", value), value


@pytest.mark.parametrize("rule_id,names,other", [
    ("uscensusregionvalue", ["REGION", "census_region", "Census Region"], ["region", "Region", "region_code"]),
    ("uscensusdivisionvalue", ["DIVISION", "census_division"], ["division", "Division"]),
])
def test_census_region_and_division_need_census_field_names(rule_id, names, other):
    # an Armenian region of marz numbers (1-11, the first rows 1 and 2) is no census region
    for name in names:
        assert guarded_by("us/us_geo.yaml", rule_id, name), name
    for name in other:
        assert not guarded_by("us/us_geo.yaml", rule_id, name), name


def test_thai_provinces_by_value_need_a_province_field():
    path = "th/th_geo.yaml"
    for name in ("province", "PROVINCE_NAME", "changwat", "จังหวัด"):
        assert guarded_by(path, "thprovincevalue", name), name
    assert not guarded_by(path, "thprovincevalue", "city")
    assert value_matches(path, "thprovincevalue", "Bangkok")
    for town in ("Pattaya", "Hat Yai", "Hua Hin", "Cha-am"):
        assert not value_matches(path, "thprovincevalue", town), town


def test_russian_positions_by_value_need_a_russian_position_field():
    # Директор and Ректор are Ukrainian titles too (university_director_post)
    path = "ru/ru_persons.yaml"
    assert value_matches(path, "ruspersonworkpositions", "Директор")
    for name in ("Должность", "должность руководителя", "dolzhnost"):
        assert guarded_by(path, "ruspersonworkpositions", name), name
    for name in ("university_director_post", "position", "посада"):
        assert not guarded_by(path, "ruspersonworkpositions", name), name


def test_id_field_names_and_values():
    path = "common/generic.yaml"
    # the CKAN row number _id, nested or not, is no id
    for name in ("_id", "properties._id"):
        assert not field_matches(path, "idbyfield", name), name
    assert field_matches(path, "idbyfield", "site_id")
    check = validator_of(path, "idbyfield")
    assert check("FRS56PLMBT3H1YW1BIVW") and check("Non renseigné")
    assert not check("新北市板橋區")


def test_french_name_field_values_are_not_streets():
    check = validator_of("fr/fr_common.yaml", "frtitleknown")
    assert check("Musée du Louvre")
    assert not check("Bd Raspail / Varenne")


# --- third pass: milliseconds in date fields, higher taxa by value --------------------------
def _fieldregex(path, rule_id):
    return re.compile(load(path, rule_id)["fieldregex"], re.IGNORECASE)


def test_milliseconds_in_date_fields_are_unixtime_ms():
    path, rule_id = "common/dateandtime.yaml", "unixtimemsdatefieldvalue"
    spec = load(path, rule_id)
    assert spec["key"] == "unixtime_ms" and spec["type"] == "data"
    names = _fieldregex(path, rule_id)
    for name in ("TicketReportedOnDate", "Data założenia", "Data rozpoczęcia działalności", "feature_Age", "from",
                 "to", "updated", "created_at", "updatedAt", "DateCreated", "Datum der Benennung", "Дата регистрации"):
        assert names.search(name), name
    # codes of 12 and 13 digits in fields that name a code, and date inside another word
    for name in ("Regionalschlüssel", "OGRN", "ОГРН", "KLADR", "gemi_number", "date_id", "DateID", "data",
                 "validatedAs", "Kod daty", "update_date_code", "Origen"):
        assert not names.search(name), name
    # metacrafter versions without fieldregex use the fieldrule list as the guard
    assert guarded_by(path, rule_id, "from") and guarded_by(path, rule_id, "updated")
    assert not guarded_by(path, rule_id, "Regionalschlüssel")
    for value in ("1689019752000", "921452400000", "-578624400000", "1794571598835"):
        assert value_matches(path, rule_id, value), value
    for value in ("1689019752", "4102444800000", "16890197520000"):
        assert not value_matches(path, rule_id, value), value


def test_higher_taxon_names_by_value():
    for value in ("Eukaryota", "Animalia", "Arthropoda", "Hexapoda", "Insecta", "Hymenoptera", "Formicoidea",
                  "Formicidae", "Myrmicinae", "Poaceae", "Magnoliopsida", "Ascomycota", "Tracheophyta",
                  "Passeriformes", "Primates"):
        assert validate_higher_taxon_name(value), value
    for value in ("Tetramorium", "Solenopsis geminata", "Crematogastrini", "Municipales", "Rosales", "Wales",
                  "Informes", "Uniformes", "FORMICIDAE", "Eukaryota 2", None):
        assert not validate_higher_taxon_name(value), value
    path = "common/science.yaml"
    assert load(path, "highertaxonnamevalue")["key"] == "taxon_name"
    assert "fieldrule" not in load(path, "highertaxonnamevalue")
    assert value_matches(path, "highertaxonnamevalue", "Arthropoda")
