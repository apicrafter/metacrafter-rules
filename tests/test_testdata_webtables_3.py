"""Rules for seven more segments of the WDC Web Tables Corpus 2015 (tables of HTML pages that Web Data Commons
extracted from the Common Crawl of July 2015; 5 778 000 relational tables of 2 963 718 pages on 109 005 hosts) and
the files of metacrafter-testdata taken from them: seasons of sports leagues, types of dwellings, age groups of
youth sports, names of Dublin Core elements, keyboard shortcuts, Exif tags, branches of the armed forces, stock
market indexes, stock exchanges, betting odds, types of crimes and crops.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.common import webtables as wt
from tests.test_testdata_baseline import field_matches, load

VALIDATORS = [
    (wt.validate_sports_season, ["2013-14", "1999-00", "2014–15", "2013/2014", "2013/14", "2015", "2013-14*",
                                 "2013–14 (NHL)"], ["2013-15", "2015-14", "Summer", "13-14", "Career", ""]),
    (wt.validate_dwelling_type, ["Detached", "Semi-detached", "Terraced", "Flat/Maisonette", "Bungalow",
                                 "Single Family", "Condo", "Townhouse", "Apartment", "Mobile Home", "Duplex", "House",
                                 "End Terrace", "Condo/Townhouse"], ["Commercial", "Residential", "Land", "3 Bedroom",
                                                                     ""]),
    (wt.validate_dwelling_type_value, ["Semi-detached", "Terraced", "Flat/Maisonette", "Townhouse", "Single Family",
                                       "Mobile Home", "End Terrace", "Condominium"],
     ["House", "Flat", "Apartment", "Detached", "Duplex", "Studio", "Villa", ""]),
    (wt.validate_sports_age_group, ["U12", "U-14", "U 8", "12U", "U12 Boys", "Girls U14", "BU10", "Under 16",
                                    "Under-12", "10 & Under", "Under 12s"], ["U", "12", "18-24", "U2B", "Under 200",
                                                                             "U2", ""]),
    (wt.validate_sports_age_group_value, ["U12", "U-14", "16U", "U12 Boys", "U19 Girls", "U23"],
     ["U6", "U8", "U2", "Under 16", "U99", "22U", "42U", ""]),
    (wt.validate_dublin_core_element, ["dc.title", "dc.date.issued", "dc.contributor.author", "dc.identifier.uri",
                                       "dc:creator", "dcterms:created", "dc.title[en_US]", "DC.Title",
                                       "dc.relation.ispartofseries", "dc.description.abstract"],
     ["dc", "dc.foo", "Title", "dc_title", "dc.title.", ""]),
    (wt.validate_keyboard_shortcut, ["Ctrl+C", "Alt+F4", "Shift + Tab", "Cmd+Shift+S", "⌘S", "Ctrl-X",
                                     "Ctrl+K, Ctrl+C", "C-x C-f", "M-x", "F1", "Esc", "Home", "Ctrl + Shift + N",
                                     "Ctrl+K Ctrl+C", "Ctrl+Click"], ["Copy", "Ctrl", "+", ""]),
    (wt.validate_keyboard_shortcut_value, ["Ctrl+C", "Alt + F4", "Shift+Tab", "Cmd-Shift-S", "⌘⇧S",
                                           "Ctrl + Shift + N", "Ctrl+K Ctrl+C"], ["C-x", "M-F", "F1", "S-1", ""]),
    (wt.validate_exif_tag, ["Make", "Model", "Exposure Time", "F-Number", "ISO Speed Ratings", "Focal Length",
                            "Metering Mode", "Flash", "Exposure Bias Value", "Color Space", "Date/Time Original",
                            "White Balance", "ISO:"], ["1/60 sec", "f/5.6", "Canon", ""]),
    (wt.validate_exif_tag_value, ["Exposure Time", "Exposure Program", "Metering Mode", "Focal Length",
                                  "Shutter Speed Value", "Aperture Value", "Exposure Bias Value", "Color Space",
                                  "White Balance", "F-Number"], ["Make", "Model", "Flash", "ISO", "Software",
                                                                 "Date/Time", ""]),
    (wt.validate_military_branch, ["Army", "Navy", "Air Force", "Marine Corps", "Coast Guard", "USMC", "USN", "USAF",
                                   "Army National Guard", "Navy Reserve", "U.S. Army", "Royal Navy", "RAF"],
     ["Police", "Fire", "Infantry", ""]),
    (wt.validate_military_branch_value, ["Marine Corps", "Coast Guard", "USMC", "USAF", "USCG",
                                         "Army National Guard", "U.S. Navy", "Royal Navy"],
     ["Army", "Navy", "Air Force", "Marines", "USA", "Police", ""]),
    (wt.validate_stock_market_index, ["S&P 500", "Dow Jones Industrial Average", "DJIA", "Dow", "Nasdaq Composite",
                                      "Nasdaq-100", "Russell 2000", "FTSE 100", "DAX", "CAC 40", "Nikkei 225",
                                      "Hang Seng", "Euro Stoxx 50", "Bovespa"], ["AAPL", "NYSE", "2,093.25", ""]),
    (wt.validate_stock_market_index_value, ["S&P 500", "Dow Jones Industrials", "Nasdaq Composite", "FTSE 100",
                                            "CAC 40", "Nikkei 225", "Hang Seng", "Russell 2000", "TOPIX"],
     ["Dow", "Nasdaq", "DAX", "SMI", "SET", "AAPL", ""]),
    (wt.validate_stock_exchange, ["NYSE", "NASDAQ", "NYSE MKT", "NYSE Arca", "OTCBB", "OTC Markets",
                                  "London Stock Exchange", "AIM", "TSX", "ASX", "Xetra", "Euronext Paris", "CME",
                                  "NYMEX", "Frankfurt"], ["New York", "S&P 500", "Bitstamp", ""]),
    (wt.validate_stock_exchange_value, ["NYSE", "NASDAQ", "NYSE MKT", "NYSE Arca", "OTCBB", "OTCQB",
                                        "London Stock Exchange", "Toronto Stock Exchange", "Euronext Paris", "Xetra"],
     ["OTC", "AIM", "ICE", "BSE", "AMEX", "Frankfurt", "New York", "TSX", "ASX", ""]),
    (wt.validate_betting_odds, ["9-2", "5/1", "100/30", "11/10", "2-5", "Evs", "9/4F", "+150", "-110", "12-1",
                                "EVENS", "8/13", "1-9", "10/11", "5-2f", "7-2jf"],
     ["0-0", "2015-16", "1/0", "2.50", "-3", "Win", "12/14", "35-38", "9-13", ""]),
    (wt.validate_crime_type, ["Murder", "Rape", "Robbery", "Aggravated Assault", "Burglary", "Larceny-Theft",
                              "Motor Vehicle Theft", "Arson", "Simple Assault", "Vandalism", "DUI",
                              "Anti-social behaviour", "Burglary - Residential", "THEFT", "Assault"],
     ["Slashing", "Holding", "Felony", "2", ""]),
    (wt.validate_crime_type_value, ["Burglary", "Robbery", "Larceny-Theft", "Aggravated Assault",
                                    "Motor Vehicle Theft", "Arson", "Vandalism", "Criminal Mischief", "Shoplifting",
                                    "Burglary (Residential)", "LARCENY/THEFT", "Anti-social behaviour"],
     ["Assault", "Battery", "Theft", "Drugs", "Fraud", "Slashing", "Oui", ""]),
    (wt.validate_crop, ["Corn", "Wheat", "Winter Wheat", "Soybeans", "Barley", "Oats", "Rice", "Sorghum", "Cotton",
                        "Canola", "Sugar Beets", "Potatoes", "Alfalfa", "Hay", "Maize", "Cassava"],
     ["Gold", "Crude Oil", "Cattle", "Apples", ""]),
    (wt.validate_crop_value, ["Wheat", "Winter Wheat", "Soybeans", "Barley", "Oats", "Sorghum", "Canola",
                              "Sugar Beets", "Alfalfa", "Maize", "Cassava"],
     ["Corn", "Rice", "Cotton", "Hay", "Potatoes", "Gold", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value
    assert not func(None)


def test_a_column_of_exif_tags_reaches_half_by_value():
    tags = ["ISO", "Focal Length", "Flash", "Metering Mode", "Shutter Speed Value", "Date/Time",
            "Exposure Bias Value", "Aperture Value", "Color Space", "Exposure Program", "Model", "Make"]
    assert all(map(wt.validate_exif_tag, tags))
    assert sum(map(wt.validate_exif_tag_value, tags)) * 2 >= len(tags)


def test_teams_of_the_service_academies_are_no_branch_by_value():
    teams = ["Army", "Navy", "Air Force", "Army", "Navy"]
    assert all(map(wt.validate_military_branch, teams))
    assert not any(map(wt.validate_military_branch_value, teams))


def test_columns_of_other_things_are_no_type_by_value():
    # found on the first scan of a sample of the corpus: heights of racks in rack units, women's sizes and sock
    # sizes under M/L, the Acura TSX in a column of car models and a product line ASX of a catalogue
    racks = ["18U", "22U", "27U", "42U"]
    assert sum(map(wt.validate_sports_age_group_value, racks)) * 2 < len(racks)
    assert not any(map(wt.validate_betting_odds, ["35-38", "28-30", "39-41", "12/14", "40/42", "8/10", "9-13"]))
    assert not any(map(wt.validate_stock_exchange_value, ["TSX", "TSX", "TSX", "ASX"]))


def test_columns_of_the_test_set_are_no_type():
    # found on the full scan of metacrafter-testdata: Oui and oui of French tables (OUI, operating under the
    # influence, had come in as a crime), the condition Green of variable message signs (the word lists split the
    # entry "coffee, green" at its comma) and BE, which b&e folded to
    assert not any(map(wt.validate_crime_type, ["Oui", "Non", "oui", "BE"]))
    assert not any(map(wt.validate_crop, ["Green", "Not Assessed", "dry", "grain"]))
    assert all(map(wt.validate_dwelling_type, ["House", "Flat", "Multi Storey Flat", "Bungalow", "Maisonette", "Bedsit"]))


def test_no_entry_of_the_word_lists_is_cut_at_a_comma():
    for words in (wt.DWELLING_TYPES, wt.EXIF_TAGS, wt.MILITARY_BRANCHES, wt.STOCK_INDEXES, wt.STOCK_EXCHANGES,
                  wt.CRIME_TYPES, wt.CROPS):
        assert not words & {"green", "dry", "grain", "etc", "possessing", "be", "oui", ""}


FIELDS = [
    ("common/dateandtime.yaml", "sportsseasonbyname", ["Season", "Seasons", "SEASON", "Saison", "Temporada",
                                                      "Stagione", "Regular Season", "Season/Year"],
     ["season ticket", "seasonal"]),
    ("common/realestate.yaml", "dwellingtypebyname", ["Property Type", "Dwelling Type", "Home Type", "Type of Property",
                                                     "Property Style", "Boligtype", "House Type", "Building Type"],
     ["property id", "dwellings"]),
    ("common/sports.yaml", "sportsagegroupbyname", ["Age Group", "Age Groups", "Division", "Div", "Div.", "Age",
                                                   "Category", "Altersklasse", "Age Division"],
     ["age at death", "divisional"]),
    ("common/sports.yaml", "bettingoddsbyname", ["Odds", "ML", "M/L", "Morning Line", "SP", "Starting Price",
                                                "Win Odds", "Odds to Win", "Moneyline"], ["odds ratio", "spa"]),
    ("common/software.yaml", "keyboardshortcutbyname", ["Shortcut", "Shortcuts", "Keyboard Shortcut", "Shortcut Keys",
                                                       "Hotkey", "Keystroke", "Key Combination", "Windows Shortcut",
                                                       "Mac Shortcut", "Tastenkombination"],
     ["short", "key"]),
    ("common/media.yaml", "exiftagbyname", ["Exif Tag", "EXIF", "Tag", "Tag Name", "Camera", "Photo Info"],
     ["tagline", "camera model"]),
    ("common/persons.yaml", "militarybranchbyname", ["Branch", "Service", "Branch of Service", "Military Branch",
                                                    "Service Branch", "Component", "Armed Forces"],
     ["branch office", "service date"]),
    ("common/crossborder_finance.yaml", "stockmarketindexbyname", ["Index", "Indices", "Index Name", "Benchmark",
                                                                  "Market", "Indizes", "Ticker Name"],
     ["index of", "marketing"]),
    ("common/crossborder_finance.yaml", "stockexchangebyname", ["Exchange", "Stock Exchange", "Exch", "Exch.",
                                                               "Listed On", "Listing", "Market", "Börse",
                                                               "Handelsplatz"], ["exchange rate", "listed"]),
    ("common/legal.yaml", "crimetypebyname", ["Crime", "Crimes", "Offense", "Offence Type", "Crime Category",
                                             "Incident Type", "Primary Type", "Nature", "Charge", "Delito",
                                             "Straftat", "Type of Crime"], ["crime rate", "charge amount"]),
    ("common/soils.yaml", "cropbyname", ["Crop", "Crops", "Crop Type", "Commodity", "Cultivo", "Culture",
                                        "Kulturart", "Gewas", "Main Crop"], ["crop yield", "cropped"]),
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
    ("common/realestate.yaml", "dwellingtypevalue"), ("common/sports.yaml", "sportsagegroupvalue"),
    ("common/dublincore.yaml", "dublincoreelementvalue"), ("common/software.yaml", "keyboardshortcutvalue"),
    ("common/media.yaml", "exiftagvalue"), ("common/persons.yaml", "militarybranchvalue"),
    ("common/crossborder_finance.yaml", "stockmarketindexvalue"),
    ("common/crossborder_finance.yaml", "stockexchangevalue"), ("common/legal.yaml", "crimetypevalue"),
    ("common/soils.yaml", "cropvalue"),
]


@pytest.mark.parametrize("path,rule_id", VALUE_RULES, ids=[r[1] for r in VALUE_RULES])
def test_value_rules(path, rule_id):
    spec = load(path, rule_id)
    assert spec["type"] == "data" and spec["match"] == "func"
    module, _, name = spec["rule"].rpartition(".")
    assert module == "metacrafterext.rules.common.webtables" and callable(getattr(wt, name))
    assert 0 < spec["minlen"] <= spec["maxlen"]
