"""Rules for the tables of the Plotly community feed (the VizNet corpus of Plotly charts, 2015 to 2018: 1 090 629
charts of Plotly users, 1 013 540 distinct tables) and the files of metacrafter-testdata taken from it: NYC 311
complaint types, social networks, marketing channels, GICS sectors, emotions, sentiment labels, energy sources,
weather conditions, planets, cryptocurrency exchanges, log levels, credit ratings, Amazon EC2 instance types,
web browsers and operating systems by value, and colors in the CSS notations of charts.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.common import plotly as pl
from tests.test_testdata_baseline import field_matches, load

VALIDATORS = [
    (pl.validate_nyc_311_complaint_type, ["Noise - Residential", "HEAT/HOT WATER", "Blocked Driveway", "Rodent",
                                          "Missed Collection (All Materials)", "PLUMBING", "Electric", "Street Light Condition"],
     ["Pothole on Main St", "311", "Brooklyn", ""]),
    (pl.validate_nyc_311_complaint_type_value, ["Noise - Residential", "HEAT/HOT WATER", "Blocked Driveway", "Rodent",
                                                "General Construction/Plumbing", "Special Projects Inspection Team (SPIT)"],
     ["Electric", "Noise", "Snow", "PLUMBING", "Safety", ""]),
    (pl.validate_social_network, ["Facebook", "Twitter", "Instagram", "LinkedIn", "Pinterest", "Reddit", "VKontakte",
                                  "Weibo", "StumbleUpon", "Google+"],
     ["Email", "Google", "Web", "X", "Telegram", ""]),
    (pl.validate_marketing_channel, ["Organic Search", "Paid Search", "Referral", "Affiliates", "(Other)",
                                     "Other Advertising", "Direct", "Social", "Email"],
     ["Google", "Facebook", "Phone", ""]),
    (pl.validate_marketing_channel_value, ["Organic Search", "Paid Search", "Referral", "(Other)", "Affiliates",
                                           "Paid Social"],
     ["Direct", "Social", "Email", "Display", ""]),
    (pl.validate_gics_sector, ["Consumer Discretionary", "Information Technology", "Health Care", "Financials",
                               "Telecommunication Services", "Consumer Cyclical", "Energy", "Healthcare"],
     ["Banking", "Retail", "3", ""]),
    (pl.validate_gics_sector_value, ["Consumer Discretionary", "Consumer Staples", "Financials", "Industrials",
                                     "Health Care", "Information Technology", "Communication Services"],
     ["Energy", "Technology", "Real Estate", "Retail", ""]),
    (pl.validate_emotion, ["anger", "disgust", "fear", "joy", "sadness", "surprise", "anticipation", "Happy", "Boredom"],
     ["positive", "negative", "tweets", "Neutral", "love", "trust", ""]),
    (pl.validate_sentiment, ["positive", "negative", "neutral", "very positive", "pos", "neg", "neu", "Positivo"],
     ["0.43", "joy", "good", ""]),
    (pl.validate_energy_source, ["Coal", "Natural Gas", "Nuclear", "Hydro", "Wind Offshore", "Solar PV", "Biomass",
                                 "CCGT", "Fossil Hard coal", "Biofuels & Waste"],
     ["Residential", "Transport", "450 MW", "Gas", "Wind", "Solar", ""]),
    (pl.validate_weather_condition, ["Clear", "Partly Cloudy", "Overcast", "Rain", "Light Snow", "Thunderstorm", "Fog",
                                     "Breezy and Mostly Cloudy", "Rain/Sleet", "clear-day"],
     ["Dry", "Wet", "23 °C", ""]),
    (pl.validate_weather_condition_value, ["Partly Cloudy", "Overcast", "Light Rain", "Thunderstorm", "Drizzle",
                                           "Foggy", "Sunny"],
     ["Clear", "Rain", "Snow", "Fair", ""]),
    (pl.validate_planet, ["Mercury", "Earth", "Jupiter", "Neptune", "Pluto", "Mercury (planet)", "SATURN"],
     ["Moon", "Sun", "Ceres", "Planet X", ""]),
    (pl.validate_crypto_exchange, ["Binance", "Coinbase", "GDAX", "Kraken", "Bitfinex", "Bitstamp", "Poloniex",
                                   "cex.io", "BTC-e"],
     ["Bitcoin", "BTC", "NASDAQ", "Gemini", ""]),
    (pl.validate_log_level, ["INFO", "WARN", "ERROR", "DEBUG", "FATAL", "TRACE", "Informational", "SEVERE", "error",
                             "warning", "notice"],
     ["High", "3", "Failed", ""]),
    (pl.validate_log_level_value, ["INFO", "WARN", "ERROR", "CRITICAL", "debug", "info", "warn", "fatal", "TRACE",
                                   "Debug"],
     ["error", "warning", "critical", "Error", "ALL", "notice", "trace", ""]),
    (pl.validate_credit_rating, ["AAA", "AA+", "BBB-", "B", "CCC", "D", "Aaa", "Baa2", "A1", "AA+u"],
     ["AAAA", "A++", "4", "Aaa1", ""]),
    (pl.validate_credit_rating_value, ["AAA", "AA+", "BBB-", "BB", "Baa2", "Caa1", "AAAu"],
     ["A", "B+", "C", "A1", "B2", "F", "SD", "sd", "CC", ""]),
    (pl.validate_aws_ec2_instance_type, ["t2.micro", "m4.large", "c5.2xlarge", "c7gn.xlarge", "m7i-flex.large",
                                         "mac1.metal", "u-6tb1.112xlarge", "c7i.metal-24xl"],
     ["m4-large", "t2", "file.large", "db.t2.micro", ""]),
    (pl.validate_web_browser_value, ["Chrome", "Firefox", "Safari", "Internet Explorer", "Opera", "Chrome Mobile",
                                     "Android Browser", "Mobile Safari"],
     ["Facebook", "IE", "Other", "Unknown", "Windows", ""]),
    (pl.validate_operating_system_value, ["Windows", "iOS", "Android", "Linux", "macOS", "OS X 10.10", "Windows 7",
                                          "Chrome OS", "android 4.4.3"],
     ["Mac", "Unix", "Other", "Unknown", "Chrome", ""]),
    (pl.validate_rgb_color, ["rgb(255, 99, 71)", "rgb(10,10,10)", "rgb (31, 120, 180)"],
     ["rgb(256,0,0)", "220,220,220", "rgba(10,10,10,1)", ""]),
    (pl.validate_rgba_color, ["rgba(179,226,205,1)", "rgba(222, 45, 38, 0.8)", "rgba (255, 0, 0, 1)", "rgba(0,0,0,0)",
                              "rgba(54,166,179,0.3240155)"],
     ["rgba(256,0,0,1)", "rgba(0,0,0,2)", "rgb(255, 99, 71)", ""]),
    (pl.validate_hsl_color, ["hsl(0, 100%, 50%)", "hsl(0.0,50%,50%)", "hsl(360.0,50%,50%)", "hsl(51.4285714286,50%,50%)"],
     ["hsl(361,50%,50%)", "0, 100%, 50%", "hsla(360, 100%, 50%,0.25)", ""]),
    (pl.validate_hex_color, ["#2ca02c", "#FFF", "#1F5FBF"], ["2ca02c", "#12345", "#wikileaks", "#2C155B00", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value
    assert not func(None)


def test_a_column_of_gics_sectors_is_mostly_sectors_by_value():
    sectors = ["Energy", "Materials", "Industrials", "Consumer Discretionary", "Consumer Staples", "Health Care",
               "Financials", "Information Technology", "Communication Services", "Utilities", "Real Estate"]
    assert sum(map(pl.validate_gics_sector_value, sectors)) / len(sectors) > 0.5
    industries = ["Technology", "Healthcare", "Energy", "Retail", "Banking", "Real Estate"]
    assert sum(map(pl.validate_gics_sector_value, industries)) / len(industries) < 0.5


def test_a_column_of_letter_grades_is_no_credit_rating_by_value():
    grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "D", "F"]
    assert not any(map(pl.validate_credit_rating_value, grades))
    ratings = ["AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-"]
    assert sum(map(pl.validate_credit_rating_value, ratings)) / len(ratings) > 0.5


FIELDS = [
    ("us/us_nyc.yaml", "usnyc311complainttypebyname", ["Complaint Type", "complaint_type", "complaint",
                                                       "Problem (formerly Complaint Type)", "311 complaint type"],
     ["complaints received", "descriptor"]),
    ("common/crossborder_finance.yaml", "gicssectorbyname", ["sector", "GICS Sector", "Sector Name", "sectors",
                                                             "industry sector"], ["subsector", "sector code"]),
    ("common/crossborder_finance.yaml", "creditratingbyname", ["credit rating", "Bond Rating", "S&P", "Moody's",
                                                               "Fitch", "S&P_(long_term)", "Moody's_(long_term)",
                                                               "issuer rating", "Riesgo"], ["rating", "grade", "sp"]),
    ("common/cryptocurrency.yaml", "cryptoexchangebyname", ["exchange", "Exchange Name", "market", "venue"],
     ["exchange rate", "markets"]),
    ("common/environment.yaml", "weatherconditionbyname", ["weather", "Weather Condition", "conditions", "summary",
                                                           "icon", "weather_main", "weather description"],
     ["weather station", "temperature"]),
    ("common/environment.yaml", "energysourcebyname", ["fuel", "Fuel Type", "energy source", "technology",
                                                       "production type", "Type of power", "PsrType", "primary fuel"],
     ["fuel cost", "source"]),
    ("common/science.yaml", "planetbyname", ["planet", "Planet Name", "planets"], ["planetarium", "plant"]),
    ("common/software.yaml", "loglevelbyname", ["level", "log level", "levelname", "severity", "log_severity"],
     ["water level", "levels"]),
    ("common/software.yaml", "awsec2instancetypebyname", ["instance type", "InstanceType", "instance size",
                                                          "ec2 instance type"], ["instance", "instance class"]),
    ("common/analytics.yaml", "socialnetworkbyname", ["social network", "Social Media", "platform", "network",
                                                      "social", "social media site"], ["site", "socialist"]),
    ("common/analytics.yaml", "marketingchannelbyname", ["channel", "Default Channel Grouping", "channel grouping",
                                                         "traffic source", "acquisition channel"],
     ["channel id", "source"]),
    ("common/analytics.yaml", "sentimentbyname", ["sentiment", "Sentiment Label", "polarity", "tweet sentiment",
                                                  "sentiment_class"], ["sentimental", "senti"]),
    ("common/analytics.yaml", "emotionbyname", ["emotion", "Emotions", "emotion label", "mood"],
     ["emotional", "motion"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    spec = load(path, rule_id)
    assert spec["key"]
    assert spec["validator"].startswith("metacrafterext.rules.common.plotly.") and spec["needs_values"] is True
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUE_RULES = [
    ("us/us_nyc.yaml", "usnyc311complainttypevalue"), ("common/crossborder_finance.yaml", "gicssectorvalue"),
    ("common/crossborder_finance.yaml", "creditratingvalue"), ("common/cryptocurrency.yaml", "cryptoexchangevalue"),
    ("common/environment.yaml", "weatherconditionvalue"), ("common/environment.yaml", "energysourcevalue"),
    ("common/science.yaml", "planetvalue"), ("common/software.yaml", "loglevelvalue"),
    ("common/software.yaml", "awsec2instancetypevalue"), ("common/common.yaml", "rgbacolorvalue"),
    ("common/common.yaml", "rgbcolorvalue"), ("common/common.yaml", "hslcolorvalue"),
    ("common/common.yaml", "hexcolorvalue"), ("common/analytics.yaml", "socialnetworkvalue"),
    ("common/analytics.yaml", "marketingchannelvalue"), ("common/analytics.yaml", "webbrowservalue"),
    ("common/analytics.yaml", "operatingsystemvalue"), ("common/analytics.yaml", "emotionvalue"),
]


@pytest.mark.parametrize("path,rule_id", VALUE_RULES, ids=[r[1] for r in VALUE_RULES])
def test_value_rules(path, rule_id):
    spec = load(path, rule_id)
    assert spec["type"] == "data" and spec["match"] == "func"
    module, _, name = spec["rule"].rpartition(".")
    assert module == "metacrafterext.rules.common.plotly" and callable(getattr(pl, name))
    assert 0 < spec["minlen"] <= spec["maxlen"]
