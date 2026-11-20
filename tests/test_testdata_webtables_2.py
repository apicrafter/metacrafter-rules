"""Rules for six more segments of the WDC Web Tables Corpus 2015 (tables of HTML pages that Web Data Commons
extracted from the Common Crawl of July 2015; 4 978 140 relational tables of 2 555 031 pages on 98 133 hosts) and
the files of metacrafter-testdata taken from them: the venue of games, bats and throws, winning and losing streaks,
penalties, conferences of US college sports, television networks, heights in feet and inches, time ranges, times
relative to now, nutrients, holidays, relationships to the head of a household, grade spans of schools, meeting
days of classes, IOC country codes and errno names.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.common import webtables as wt
from tests.test_testdata_baseline import field_matches, load

VALIDATORS = [
    (wt.validate_home_away, ["Home", "Away", "Neutral", "H", "A", "N", "@", "vs.", "at", "H (9)", "HOME", "Road"],
     ["Home Run", "Chicago", "3-2", ""]),
    (wt.validate_home_away_value, ["Home", "AWAY", "Neutral", "Neutral Site"], ["H", "A", "@", "at", ""]),
    (wt.validate_bats_throws, ["R/R", "L/R", "S/R", "B/L", "R-R", "Left/Right", "R / R"],
     ["R", "6-2", "L/XL", "r/r", ""]),
    (wt.validate_bats_throws_value, ["R/R", "L/R", "S/L"], ["R-R", "Left/Right", ""]),
    (wt.validate_win_loss_streak, ["W3", "L1", "W 2", "1L", "Won 4", "Lost 2", "T1", "W-3"], ["W", "3-2", "L/R", ""]),
    (wt.validate_sports_penalty, ["SLASHING", "Tripping", "Holding", "Cross-Checking", "HIGH STICKING",
                                  "Delay of Game", "UNSPORTSMANLIKE CONDUCT", "YELLOW CARD", "Slashing (2 min)",
                                  "O-HOOKING", "2 min Slashing", "Minor - Hooking", "TOO MANY PLAYERS ON ICE",
                                  "10-MINUTE MISCONDUCT", "HITTING FROM BEHIND"],
     ["2:00", "Robbery", "Penalty", "1-1:00", ""]),
    (wt.validate_sports_penalty_value, ["SLASHING", "Yellow Card", "Cross-Check", "Delay of Game"],
     ["Holding", "Interference", "Boarding", "Fighting", ""]),
    (wt.validate_athletic_conference, ["SEC", "ACC", "Big Ten", "Big 12", "Big XII", "Pac-12", "Big East",
                                       "Conference USA", "Mountain West", "Sun Belt", "Ivy", "MAC", "WAC",
                                       "Independent", "NESCAC", "GLIAC", "Big Ten Conference", "Ohio Valley"],
     ["6-2", "Conference", "NFC", ""]),
    (wt.validate_athletic_conference_value, ["Big Ten", "Big 12", "Pac-12", "Ivy League", "Mountain West"],
     ["SEC", "ACC", "MAC", "WAC", "PSAC", "SWAC", "American", "Independent", ""]),
    (wt.validate_tv_network, ["ESPN", "ABC", "NBC", "ESPN2/ESPN3", "ESPN or ESPN2", "FS1", "SEC Network", "HBO", "A&E",
                              "ESPN3.com", "ESPN-U/ESPN3", "ESPN 2", "TBS or MLBN", "NBCSN"],
     ["8", "TBA", "Channel 9", "AE", ""]),
    (wt.validate_tv_network_value, ["ESPN", "ESPN2/ESPN3", "NBCSN", "HBO", "CBSSN"],
     ["USA", "YES", "History", "FOX", "ABC", "CBS", "TBS", "FXX", "BTN", ""]),
    (wt.validate_height_feet_inches, ["6-2", "5-11", "6'2\"", "5' 10\"", "6'1", "6 ft 2 in", "6'", "6-0", "7-0"],
     ["2-1", "6-12", "72", "180 cm", "6-", ""]),
    (wt.validate_height_feet_inches_value, ["6'2\"", "5' 10\"", "6'1", "6 ft 2 in"], ["6-2", "5-11", ""]),
    (wt.validate_time_range, ["10:00 - 11:00", "9:00am - 5:00pm", "8:30 a.m. - 4:30 p.m.", "12–4:00 pm",
                              "17:00-18:30", "9am to noon", "10:00 – 10:10", "9:00AM - 6:00PM", "9am-5pm",
                              "10 p.m.-2 a.m."],
     ["9-5", "1-1:00", "2015-2016", "Mon-Fri 9-5", "10-11:30", ""]),
    (wt.validate_relative_time, ["2 days ago", "1 hour ago", "an hour ago", "2 years 38 weeks ago", "1h 35min ago",
                                 "about 3 months ago", "5 mins ago", "posted 3 days ago", "a few seconds ago",
                                 "21 day ago"], ["2 days", "Jul 22, 2015", "ago", ""]),
    (wt.validate_nutrient, ["Protein", "Total Fat", "Saturated Fat", "Sodium", "Total Carbohydrate", "Dietary Fiber",
                            "Sugars", "Vitamin C", "Calcium", "of which saturates", "Iron, Fe",
                            "Carbohydrate, by difference", "Riboflavin (B2)", "Ballaststoffe", "- of which sugars",
                            "Calories:", "Vitamin B-6", "Total lipid (fat)", "Fiber, total dietary",
                            "Glucose (dextrose)", "Leucine", "16:0", "18:1 undifferentiated", "20:5 n-3 (EPA)"],
     ["5 g", "Apple", "Nutrition Facts", "12:30", ""]),
    (wt.validate_nutrient_value, ["Protein", "Total Fat", "Cholesterol", "Vitamin C", "Niacin"],
     ["Sodium", "Iron", "Calcium", "Energy", "Water", "Glucose", "Glycine", "16:0", "Fibre", "Total", ""]),
    (wt.validate_holiday, ["New Year's Day", "Martin Luther King, Jr. Day", "Memorial Day", "Independence Day",
                           "Labor Day", "Thanksgiving Day", "Christmas Day", "Good Friday", "Boxing Day",
                           "Labor Day (observed)", "New Year’s Day", "Tag der Arbeit", "Presidents' Day",
                           "Veterans Day", "Christmas"], ["Monday", "July 4", "Spring Break", ""]),
    (wt.validate_holiday_value, ["Labor Day", "Memorial Day", "Good Friday"], ["Christmas", "Easter", "Halloween", ""]),
    (wt.validate_household_relationship, ["Head", "Wife", "Son", "Daughter", "Dau", "Dau.", "Servant", "Boarder",
                                          "Lodger", "Son-in-law", "Granddaughter", "Nephew", "Bro-in-law", "hus",
                                          "Daur", "gdau", "Brother"], ["Director", "Friendship", "32", ""]),
    (wt.validate_household_relationship_value, ["Wife", "Son", "Servant", "Mother-in-law", "Daur"],
     ["Head", "Self", "Partner", "BROTHER", "hus", ""]),
    (wt.validate_grade_span, ["K-5", "6-8", "9-12", "PK-8", "KG - 05", "K-12", "Pre-K to 5", "Grades 7-12", "PK - 05",
                              "06 - 08", "KN - 05"], ["12-9", "5-6-7", "A-F", "PK -", ""]),
    (wt.validate_grade_span_value, ["K-5", "PK-8", "KG - 12", "Pre-K - 5"], ["9-12", "6-8", ""]),
    (wt.validate_class_meeting_days, ["MWF", "TR", "TTh", "MW", "MTWRF", "M W F", "Tu", "Th", "M", "T", "TTH", "M, W",
                                      "Tu, Th", "TuTh", "MTWThF", "M-F"],
     ["Monday", "Mon", "TBA", "13", "Sat", "Daily", ""]),
    (wt.validate_ioc_country_code, ["USA", "GER", "NED", "SUI", "RSA", "CRO", "TPE", "INA", "URS"],
     ["Ger", "DEU", "NLD", "USSR", ""]),
    (wt.validate_errno_name, ["ENOENT", "EACCES", "EAGAIN", "EINVAL", "ETIMEDOUT", "E2BIG", "ECONNREFUSED"],
     ["enoent", "ERROR", "EOF", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value
    assert not func(None)


def test_columns_of_other_things_are_no_type_by_value():
    # found on the first scan of a sample of the corpus: sections AE and BE of a course list (A&E folds to ae),
    # a column of Brother printers, the ticker WAC of a stock site and ABC of AmerisourceBergen
    assert not any(map(wt.validate_tv_network, ["BE", "AE", "AE"]))
    assert not any(map(wt.validate_household_relationship_value, ["BROTHER"] * 4))
    assert not any(map(wt.validate_athletic_conference_value, ["WAC"] * 4))
    assert not any(map(wt.validate_tv_network_value, ["ABC"] * 4))


def test_columns_of_the_test_set_are_no_type():
    # found on the full scan of metacrafter-testdata: height classes of trees in metres, the region Total of a
    # vaccination table, the shapes of microplastics, the area code FXX of French communes and the participant
    # status PSAC of the directory of the Bank of Russia
    trees = ["6-10", "Not Assessed", "<3", "3-6", "15-25", "10-15", "6-10", "6-10"]
    assert sum(map(wt.validate_height_feet_inches_value, trees)) == 0
    assert not wt.validate_nutrient("Total")
    assert not any(map(wt.validate_nutrient_value, ["Fibre", "Fibre", "Fragment"]))
    assert not wt.validate_tv_network_value("FXX")
    assert not wt.validate_athletic_conference_value("PSAC")


def test_a_column_of_minerals_is_no_nutrient_by_value():
    water = ["Calcium", "Magnesium", "Sodium", "Potassium", "Iron", "Manganese", "Chloride"]
    assert all(map(wt.validate_nutrient, water))
    assert not any(map(wt.validate_nutrient_value, water))
    label = ["Calories", "Total Fat", "Saturated Fat", "Cholesterol", "Sodium", "Total Carbohydrate",
             "Dietary Fiber", "Sugars", "Protein", "Vitamin A", "Calcium", "Iron"]
    assert sum(map(wt.validate_nutrient_value, label)) * 2 >= len(label)


def test_a_column_of_home_and_away_letters_needs_its_field_name():
    letters = ["H", "A", "A", "H", "N"]
    assert all(map(wt.validate_home_away, letters))
    assert not any(map(wt.validate_home_away_value, letters))


FIELDS = [
    ("common/sports.yaml", "homeawaybyname", ["H/A", "Home/Away", "HOME/AWAY", "Site", "Loc", "Location", "Venue",
                                             "H/A/N", "Home or Away"], ["home team", "location id"]),
    ("common/sports.yaml", "batsthrowsbyname", ["B/T", "Bats/Throws", "B-T", "Bat/Throw", "T/B", "Bats/ Throws"],
     ["batting average", "throws"]),
    ("common/sports.yaml", "winlossstreakbyname", ["Streak", "Strk", "STK", "Current Streak", "Win Streak"],
     ["streaker", "street"]),
    ("common/sports.yaml", "sportspenaltybyname", ["Offense", "Infraction", "Penalty", "Penalties", "Foul",
                                                  "Penalty Type"], ["offensive line", "penalty minutes"]),
    ("common/sports.yaml", "athleticconferencebyname", ["Conference", "Conf", "Conf.", "CONF", "Current Conference"],
     ["conference record", "confidence"]),
    ("common/media.yaml", "tvnetworkbyname", ["Network", "TV", "Channel", "Broadcast", "Televised", "NET",
                                             "TV Network", "TV/Radio"], ["network address", "channel id"]),
    ("common/common.yaml", "heightfeetinchesbyname", ["Ht.", "Ht", "HT.", "Hgt", "Height (ft)", "Ht (ft-in)"],
     ["height", "height (cm)", "weight"]),
    ("common/common.yaml", "heightfeetinchesmarkedbyname", ["Height", "HEIGHT", "Player Height"],
     ["height (cm)", "weight"]),
    ("common/dateandtime.yaml", "holidaybyname", ["Holiday", "Holidays", "Bank Holiday", "Feiertag", "Fête",
                                                 "Federal Holiday", "Holiday Observed"], ["holiday hours", "holy"]),
    ("common/education.yaml", "gradespanbyname", ["Grades", "Grade Span", "Grade Levels", "Grades Served", "Grade",
                                                 "Grade Range"], ["grade point average", "upgrade"]),
    ("common/education.yaml", "classmeetingdaysbyname", ["Days", "Day(s)", "Meeting Days", "Class Days", "Days Met",
                                                        "Day"], ["days open", "today"]),
    ("common/persons.yaml", "householdrelationshipbyname", ["Relationship", "Relation", "Rel.", "Rel",
                                                           "Relation to Head of Household",
                                                           "RELATION TO HEAD OF HOUSEHOLD", "Relation to Head"],
     ["related links", "relevance"]),
    ("common/medical.yaml", "nutrientbyname", ["Nutrient", "Nutrients", "Nutrition", "Typical Values", "Nährwerte",
                                              "Nutrition Facts", "Vitamins"], ["nutrient value", "nutritionist"]),
    ("common/geo.yaml", "ioccountrycodebyname", ["NOC", "IOC", "Nat", "Nat.", "Nation", "IOC Code"],
     ["national", "nationality"]),
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
    ("common/sports.yaml", "homeawayvalue"), ("common/sports.yaml", "batsthrowsvalue"),
    ("common/sports.yaml", "sportspenaltyvalue"), ("common/sports.yaml", "athleticconferencevalue"),
    ("common/media.yaml", "tvnetworkvalue"), ("common/common.yaml", "heightfeetinchesvalue"),
    ("common/dateandtime.yaml", "timerangevalue"), ("common/dateandtime.yaml", "relativetimevalue"),
    ("common/dateandtime.yaml", "holidayvalue"), ("common/education.yaml", "gradespanvalue"),
    ("common/persons.yaml", "householdrelationshipvalue"), ("common/medical.yaml", "nutrientvalue"),
    ("common/software.yaml", "errnonamevalue"),
]


@pytest.mark.parametrize("path,rule_id", VALUE_RULES, ids=[r[1] for r in VALUE_RULES])
def test_value_rules(path, rule_id):
    spec = load(path, rule_id)
    assert spec["type"] == "data" and spec["match"] == "func"
    module, _, name = spec["rule"].rpartition(".")
    assert module == "metacrafterext.rules.common.webtables" and callable(getattr(wt, name))
    assert 0 < spec["minlen"] <= spec["maxlen"]
