"""Rules for the tables of the WDC Web Tables Corpus 2015 (tables of HTML pages that Web Data Commons extracted from
the Common Crawl of July 2015; 4 963 794 relational tables of 2 571 606 pages on 98 249 hosts in six segments) and
the files of metacrafter-testdata taken from it: class standings, game results and win-loss records, athletics and
swimming events, clothing sizes, stock availability and condition of items, academic terms, data types, priorities,
screen resolutions, currency pairs, Unix file modes, ordinal numbers, HTTP header names and DNS record types.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.common import webtables as wt
from tests.test_testdata_baseline import field_matches, load

VALIDATORS = [
    (wt.validate_class_standing, ["Fr.", "SO", "R-Fr.", "Redshirt Junior", "Fr. (RS)", "Sr", "Gr.", "RS-So."],
     ["Jr. Varsity", "2015", "A", ""]),
    (wt.validate_class_standing_value, ["Freshman", "So.", "RS-So.", "Fr.", "R-Sr."],
     ["Jr.", "Sr", "Junior", "Senior", "FR", "SO", "fr", ""]),
    (wt.validate_clothing_size, ["XS", "S", "M", "XXL", "3XL", "2X", "X-Large", "X-Small", "One Size", "S/M", "XLT",
                                 "XS (150/76A)"], ["32", "10-12", "72.72 KB", "Size", "Small", "Medium", "Large",
                                                   "Not Sized", ""]),
    (wt.validate_clothing_size_value, ["XS", "XL", "X-Large", "One Size", "S/M", "2XL"], ["S", "M", "L", "Small", "Large", ""]),
    (wt.validate_game_result, ["W 31-28", "L, 10-0", "W, 3-2 (OT)", "Won, 3-2", "Loss 104-111", "T 1-1",
                               "W 4-3 (10 inn.)", "W 31-28, OT", "W, 3-0 (25-20, 25-18, 25-15)", "L 9 - 1"],
     ["3-2", "W", "Postponed", "2015-16", ""]),
    (wt.validate_win_loss_record, ["20-5", "9-3-0", "(10-0)", "3-0-0-0", "16-3-0 (W-L-T)", "11-8-13"],
     ["W 3-2", "20", "2015-2016", "2015-16", "5-6-7-8-9", ""]),
    (wt.validate_data_type, ["int", "String", "boolean", "void", "VARCHAR(64)", "bigint(20) unsigned", "Decimal(39,0)",
                             "List<String>", "java.lang.Integer", "xs:date", "int[]", "uint32", "INT(10)†",
                             "Short Integer", "Text"], ["Name", "255", "Required", "List", "Article", "Resource", ""]),
    (wt.validate_data_type_value, ["int", "String", "boolean", "VARCHAR(64)", "uint32", "String[]"],
     ["Text", "Date", "Number", "Long", "Double", "Object", ""]),
    (wt.validate_academic_term_value, ["Fall 2015", "Spring Semester 2016", "Summer Term 2015", "Fall ’10",
                                       "2013 Fall Semester", "Fall II 2014", "Michaelmas Term 2014",
                                       "2nd Semester 2014-15", "FALL 2013"],
     ["Fall", "SU19", "Spring Break", "2015", "2004 Summer", ""]),
    (wt.validate_academic_term, ["Fall 2015", "FA14", "Sp 2011", "2013 Fall", "Spring", "Semester 2", "1st Semester",
                                 "Winter Quarter 2014"],
     ["2015", "Week 3", "Finals", "First Quarter", "Quarter 2", "1st Quarter 2015", ""]),
    (wt.validate_priority_level, ["High", "Medium", "Low", "Normal", "Urgent", "Critical", "Blocker", "Trivial", "P1",
                                  "Highest", "High Priority", "2 - High", "Must Have", "nice-to-have"],
     ["3", "Open", "Bug", ""]),
    (wt.validate_screen_resolution, ["1920x1080", "1024 × 768", "320 × 480 px", "3648x2736", "1280x720p",
                                     "1920x1080 (Full HD)", "704 x 576"], ["15 X 6", "94.2 x 55.0", "1920", ""]),
    (wt.validate_screen_resolution_value, ["1920x1080", "1366x768", "1024 x 768", "640 × 960 px", "3840x2160"],
     ["210x277", "3648x2736", "100x100", ""]),
    (wt.validate_item_availability, ["In Stock", "Out of Stock", "Sold Out", "Pre-order", "Backordered", "Only 2 left!",
                                     "6 copies available", "Available", "Discontinued", "Special Order", "Auf Lager",
                                     "En stock", "Temporarily out of stock", "On Order"],
     ["12", "$9.99", "Add to Cart", ""]),
    (wt.validate_item_availability_value, ["In Stock", "Out of Stock", "Sold Out", "Pre-order", "Only 3 left",
                                           "Auf Lager"], ["Available", "Unavailable", "Discontinued", ""]),
    (wt.validate_item_condition, ["New", "Used", "Refurbished", "Like New", "Pre-Owned", "Open Box", "NOS",
                                  "Used - Good", "For parts or not working", "Gebraucht", "Occasion", "PRE-OWNED"],
     ["Good", "Fair", "Poor", "In Stock", "2007", ""]),
    (wt.validate_item_condition_value, ["Used", "Refurbished", "Pre-Owned", "Like New", "Open Box", "Gebraucht"],
     ["New", "Demo", "Mint", ""]),
    (wt.validate_currency_pair_value, ["EUR/USD", "USD/JPY", "GBP-USD", "eur/chf"],
     ["EUR", "EURUSD", "ABC/DEF", "USD/USD", ""]),
    (wt.validate_currency_pair, ["EUR/USD", "EURUSD", "USDJPY=X"], ["EUR", "EURO", ""]),
    (wt.validate_unix_file_mode_value, ["-rw-r--r--", "drwxr-xr-x", "lrwxrwxrwx", "-rwsr-xr-x", "d---------",
                                        "-rw-r--r--@"], ["rw-r--r--", "-rw-r--r-x-", "755", ""]),
    (wt.validate_unix_file_mode, ["-rw-r--r--", "0644", "755", "4755"], ["8", "999", "rw", ""]),
    (wt.validate_ordinal_number, ["1st", "2nd", "3rd", "4th", "11th", "22nd", "103rd", "4TH", "T-3rd", "1st Place",
                                  "112th"], ["1", "2th", "11st", "1º", "1er", "12nd", ""]),
    (wt.validate_athletics_event, ["100m", "200 Meter Dash", "110m Hurdles", "4x400m Relay", "Long Jump", "Shot Put",
                                   "Javelin Throw", "Decathlon", "Marathon", "3000m Steeplechase", "Men's 100m", "5K",
                                   "Mile", "800 m", "Boys 100 Meter Dash", "4x100"],
     ["100 Free", "Saturday", "10.34", ""]),
    (wt.validate_athletics_event_value, ["100 Meter Dash", "110m Hurdles", "4x400 Relay", "Long Jump", "Shot Put",
                                         "Marathon", "Pole Vault"], ["100m", "5K", "Mile", "100 m", ""]),
    (wt.validate_swimming_event, ["50 Free", "100 Freestyle", "200 IM", "400 Individual Medley", "100 Back",
                                  "200 Breaststroke", "100 Fly", "200 Medley Relay", "400 Free Relay",
                                  "Women 50 Yard Freestyle", "100 SCY Free", "200 Free Relay"],
     ["Freestyle", "100m", "Long Jump", ""]),
    (wt.validate_http_header_name, ["Content-Type", "Cache-Control", "X-Powered-By", "Transfer-Encoding", "Server",
                                    "Date", "Vary", "ETag", "set-cookie", "X-Varnish"],
     ["Content-Type: text/html", "Header", "nginx", "X-01", "X-07", ""]),
    (wt.validate_http_header_name_value, ["Content-Type", "Cache-Control", "X-Powered-By", "Last-Modified", "ETag",
                                          "Set-Cookie"], ["Date", "Server", "Location", "Vary", ""]),
    (wt.validate_dns_record_type, ["MX", "NS", "SOA", "TXT", "CNAME", "AAAA", "PTR", "SRV", "SPF", "CAA"],
     ["A", "mx", "MAIL", "Type", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value
    assert not func(None)


def test_a_roster_column_of_class_standings_is_half_specific():
    roster = ["Fr.", "So.", "Jr.", "Sr.", "Fr.", "So.", "Jr.", "Sr."]
    assert all(map(wt.validate_class_standing, roster))
    assert sum(map(wt.validate_class_standing_value, roster)) / len(roster) == 0.5
    countries = ["FR", "FR", "SO", "FR"]
    assert all(map(wt.validate_class_standing, countries))
    assert not any(map(wt.validate_class_standing_value, countries))
    suffixes = ["Jr.", "Sr.", "III", "II", "Jr."]
    assert not any(map(wt.validate_class_standing_value, suffixes))


def test_a_column_of_results_is_no_clothing_size_by_value():
    for column in (["W", "L", "L", "W"], ["M", "F", "M", "F"], ["N", "S", "E", "W"]):
        assert not any(map(wt.validate_clothing_size_value, column))


def test_a_column_of_dns_records_passes_without_a():
    records = ["A", "NS", "NS", "MX", "MX", "TXT", "SOA"]
    assert sum(map(wt.validate_dns_record_type, records)) * 2 >= len(records)
    grades = ["A", "B", "A", "C"]
    assert not any(map(wt.validate_dns_record_type, grades))


FIELDS = [
    ("common/education.yaml", "classstandingbyname", ["Yr", "Yr.", "Cl.", "CL", "Class", "Year", "Class Year",
                                                     "Eligibility", "Elig.", "Yr/Exp", "Academic Standing"],
     ["class name", "years in college"]),
    ("common/education.yaml", "academictermbyname", ["term", "Semester", "Academic Term", "Year & Term", "TERM",
                                                    "Session", "Eff. Date", "term offered", "semestre"],
     ["terms of use", "term length", "quarter", "Quarter"]),
    ("common/sports.yaml", "winlossrecordbyname", ["Record", "Overall", "Conf", "W-L", "W-L-T", "Home", "Away",
                                                  "H W-L-T", "Conf. Record", "Road"], ["records retrieved", "score"]),
    ("common/sports.yaml", "athleticseventbyname", ["Event", "Events", "Discipline", "Disziplin", "Épreuve", "prueba",
                                                   "race"], ["event date", "eventual"]),
    ("common/ecommerce.yaml", "clothingsizebyname", ["Size", "Sizes", "SIZE", "Taglia", "Größe", "Talla", "taille",
                                                    "General Hat Size", "Size Category", "INT Size", "Options"],
     ["size (sq.ft.)", "sock size chart pdf"]),
    ("common/ecommerce.yaml", "itemavailabilitybyname", ["Availability", "Stock", "Stock Status", "Inventory",
                                                        "Onhand", "Dispo.", "Disponibilité", "Lieferbarkeit"],
     ["stock#", "stock price"]),
    ("common/ecommerce.yaml", "itemconditionbyname", ["Condition", "New/Used", "New or Used", "Item Condition",
                                                     "Zustand", "état", "New"], ["conditions of use", "air condition"]),
    ("common/software.yaml", "datatypebyname", ["Type", "Data Type", "Datatype", "Modifier and Type", "Return Type",
                                               "value type", "Java Type", "Typ"],
     ["type of service", "datatypes list"]),
    ("common/software.yaml", "unixfilemodebyname", ["Mode", "Permissions", "perms", "chmod", "File Mode",
                                                   "Prawa dostępu", "drwxr-xr-x"], ["mode of transport", "permit"]),
    ("common/internet.yaml", "httpheadernamebyname", ["Header Key", "Header Name", "Header", "Response Header",
                                                     "HTTP Header", "Header Field Name"], ["header value", "headers sent"]),
    ("common/internet.yaml", "dnsrecordtypebyname", ["Type", "Record Type", "RR Type", "qtype", "DNS Type",
                                                    "Record"], ["type of record", "record date"]),
    ("common/internet.yaml", "screenresolutionbyname", ["Resolution", "Screen Resolution", "Display Resolution",
                                                       "Auflösung", "Résolution", "Risoluzione", "Resolutie", "Pixels",
                                                       "Size (w×h)", "RAW", "JPEG"][:9],
     ["resolution date", "resolved"]),
    ("common/trade.yaml", "currencypairbyname", ["Currency pair", "Pair", "Symbol", "Instrument", "Cross",
                                                "Paire de devise", "Pasangan mata uang", "Währungspaar"],
     ["currency", "pairing"]),
    ("common/common.yaml", "prioritylevelbyname", ["Priority", "Prio", "Importance", "Urgency", "Priorität",
                                                  "priorité", "Task Priority", "priority level"],
     ["prior", "priority date"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    spec = load(path, rule_id)
    assert spec["key"]
    assert spec["validator"].startswith("metacrafterext.rules.common.webtables.") and spec["needs_values"] is True
    module, _, name = spec["validator"].rpartition(".")
    assert callable(getattr(wt, name))
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUE_RULES = [
    ("common/education.yaml", "classstandingvalue"), ("common/education.yaml", "academictermvalue"),
    ("common/sports.yaml", "gameresultvalue"), ("common/sports.yaml", "athleticseventvalue"),
    ("common/sports.yaml", "swimmingeventvalue"), ("common/ecommerce.yaml", "clothingsizevalue"),
    ("common/ecommerce.yaml", "itemavailabilityvalue"), ("common/ecommerce.yaml", "itemconditionvalue"),
    ("common/software.yaml", "datatypevalue"), ("common/software.yaml", "unixfilemodevalue"),
    ("common/internet.yaml", "httpheadernamevalue"), ("common/internet.yaml", "screenresolutionvalue"),
    ("common/trade.yaml", "currencypairvalue"), ("common/values.yaml", "ordinalnumbervalue"),
]


@pytest.mark.parametrize("path,rule_id", VALUE_RULES, ids=[r[1] for r in VALUE_RULES])
def test_value_rules(path, rule_id):
    spec = load(path, rule_id)
    assert spec["type"] == "data" and spec["match"] == "func"
    module, _, name = spec["rule"].rpartition(".")
    assert module == "metacrafterext.rules.common.webtables" and callable(getattr(wt, name))
    assert 0 < spec["minlen"] <= spec["maxlen"]
