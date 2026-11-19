"""Rules for the tables of the Many Eyes archive (IBM Many Eyes, 2007 to 2012: 203 534 tables uploaded by its
users, 114 585 distinct headers) and the files of metacrafter-testdata taken from it: sports, positions of
players, medals, video game platforms, genres, zodiac signs, Bible references, parts of the day, vehicle makes
and models, letter grades, course codes, hashtags, post IDs, points in degrees, call signs, stock tickers, B3
tickers, MPA film ratings and the team abbreviations of MLB, the NBA and the NFL.

Matched as tests/test_testdata_baseline.py matches them.
"""
import re

import pytest

from metacrafterext.rules.br import codes as br
from metacrafterext.rules.common import manyeyes as me
from metacrafterext.rules.us import sports as us
from tests.test_testdata_baseline import field_matches, load

VALIDATORS = [
    (me.validate_sport, ["Basketball", "Archery", "Pallavolo", "Fútbol", "Leichtathletik", "Base- und Softball",
                         "American\xa0Football\xa0", "rugby union"],
     ["10", "ESPN", "Yahoo! Sports", "Public Administration", "Arsenal v Chelsea", ""]),
    (me.validate_sports_position, ["QB", "WR", "SS", "1B", "RHP", "PG", "Goalkeeper", "Zagueiro", "Flanker", "3B,OF",
                                   "G-F", "1 point guard", "Locks/Second Row"],
     ["Library Director", "Youth Services", "8", "43.42°S, 172.14°E", ""]),
    (me.validate_medal, ["Gold", "Silver", "Bronze", "Oro", "Plata", "Prata", "Médaille d'or"],
     ["28", "Platinum", "Gold Sponsor", ""]),
    (me.validate_video_game_platform, ["PlayStation 3", "Xbox 360", "Wii", "Nintendo DS", "PS2", "GBA", "PC",
                                       "Play Station 2", "Playstation II, III e PSP", "Game Boy/Game Boy Color"],
     ["Facebook", "DTT", "Linux IA32", "WII, III", ""]),
    (me.validate_zodiac_sign, ["Aries", "Leo", "Capricorn", "sagitarius", "Escorpio", "Steinbock", "Овен"],
     ["100 %", "AOT", "Sign", ""]),
    (me.validate_part_of_day, ["Morning", "Afternoon", "Evening (6pm-9pm)", "Late night", "Noche", "Manhã"],
     ["14:30", "3", "Sometimes", ""]),
    (me.validate_vehicle_make, ["Toyota", "chevrolet", "VW", "Mercedes-Benz", "Land Rover", "1º FIAT",
                                "Ford Motor Company", "AMERICAN MOTORS"],
     ["Caterpillar Inc.", "Acer America", "SAGEM", "Lenovo", "3", ""]),
    (me.validate_vehicle_model, ["Corolla", "Ford Focus", "S10", "Audi A6 3.0 Avant Quattro"], ["3", "27.5", ""]),
    (me.validate_vehicle_model_with_make, ["Ford Focus", "chevrolet chevelle malibu", "Acura MDX", "BMW 325xi Sport"],
     ["Corolla", "iPhone 4", "Thickness (mm)", ""]),
    (me.validate_bible_reference, ["John 3:16", "Genesis 1:1", "1 Samuel 15:2-3", "Mt_28.19", "2_Co_13.14", "Ps 23:1",
                                   "Deuteronomy 2:21-22"],
     ["John 3", "3:16", "Americas Test Kitchen", "Joe 3:16", "AC2:0", ""]),
    (me.validate_letter_grade, ["A", "A-", "B+", "C", "F", "b+"], ["85", "A++", "G", "Pass", ""]),
    (me.validate_course_code, ["CSI 101", "MUS 100", "SI 505", "ACTG3000", "TP-100"],
     ["A101", "FY2003", "APR 2008", "Engineering", ""]),
    (me.validate_genre, ["Drama", "R&B/Soul", "Hip-Hop", "Rap"], ["3", "Homme", "Femme", "Male", "Ordinaire", "Spécialisé", ""]),
    (me.validate_hashtag, ["#wikileaks", "#COVID19", "cablegate"], ["#", "2011", "#0047B2", "a sentence here", ""]),
    (me.validate_iso6709_dms, ["50°40′46.461″N 95°48′26.533″W", "48°51′N 2°21′E", "43.42°S, 172.14°E", "40.8N 72.3E"],
     ["10° 28' N", "-14.242916,-51.412289", ""]),
    (me.validate_x_post_id, ["440322224407314432", "20", "146228147875090432"], ["1.30481E+12", "abc", "0", ""]),
    (me.validate_call_sign, ["KDKA", "WNYC-FM", "KABC-TV", "9A1AA"], ["Radio 1", "101.5", "kdka", ""]),
    (me.validate_tickersymbol, ["AAPL", "SPY", "BRK.B", "BBAS3", "RDS.A"], ["Apple Inc.", "12.5", "aapl", "$", "LB436A", ""]),
    (me.validate_us_mpa_rating, ["G", "PG", "PG-13", "R", "NC-17", "Rated R"], ["8.1", "TV-MA", "NR", ""]),
    (br.validate_br_b3_ticker, ["PETR4", "VALE3", "CPLE6", "B3SA3", "ALLL11"], ["AAPL", "PETR", "PETR12", "petr4", ""]),
    (us.validate_mlb_team_code, ["NYY", "LAD", "CWS", "TOR", "FLA"], ["GSW", "NE", "Yankees", ""]),
    (us.validate_nba_team_code, ["LAL", "GSW", "NYK", "SAS", "NJN"], ["NYY", "NE", "Lakers", ""]),
    (us.validate_nfl_team_code, ["NE", "GB", "NYG", "KC", "JAX"], ["NYY", "GSW", "Patriots", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value
    assert not func(None)


def test_a_column_of_one_league_fits_its_own_validator_best():
    mlb = ["ARI", "ATL", "BAL", "BOS", "CHC", "CWS", "CIN", "CLE", "COL", "DET", "HOU", "KC", "LAA", "LAD", "MIA",
           "MIL", "MIN", "NYM", "NYY", "OAK", "PHI", "PIT", "SD", "SEA", "SF", "STL", "TB", "TEX", "TOR", "WSH"]
    fits = {name: sum(map(func, mlb)) for name, func in (
        ("mlb", us.validate_mlb_team_code), ("nba", us.validate_nba_team_code), ("nfl", us.validate_nfl_team_code))}
    assert fits["mlb"] == len(mlb)
    assert fits["nba"] < fits["mlb"] and fits["nfl"] < fits["mlb"]


FIELDS = [
    ("common/sports.yaml", "sportbyname", ["sport", "Sports", "type of sport", "favorite sport", "Deporte", "esporte",
                                           "Sportart", "disciplina", "Discipline"], ["sporty", "transport", "spot"]),
    ("common/sports.yaml", "sportspositionbyname", ["Position", "pos", "POS.", "player position", "posición", "posição",
                                                    "pos1", "mvp position"], ["poster", "possession", "composition"]),
    ("common/sports.yaml", "medalbyname", ["medal", "Medal Type", "medalla", "medalhas", "médaille", "award"],
     ["medallion", "metal"]),
    ("common/entertainment.yaml", "videogameplatformbyname", ["platform", "Console", "system", "plataforma",
                                                              "piattaforma", "game platform"], ["systems", "consolidated"]),
    ("common/entertainment.yaml", "genrebyname", ["genre", "Genres", "primary genre", "music genre", "genere"],
     ["género", "genero", "general"]),
    ("common/entertainment.yaml", "zodiacsignbyname", ["star sign", "Zodiac", "sign", "signo", "Sternzeichen",
                                                       "знак зодиака"], ["signal", "signature", "design"]),
    ("common/entertainment.yaml", "biblereferencebyname", ["verse", "Reference", "bible verse", "scripture", "citation"],
     ["referee", "preference"]),
    ("common/dateandtime.yaml", "partofdaybyname", ["time of day", "Time of Day doing activity", "daypart",
                                                    "período del día", "Tageszeit"], ["time", "day", "daytime"]),
    ("common/vehicles.yaml", "vehiclemakebyname", ["make", "Vehicle Make", "car make", "manufacturer", "marca",
                                                   "marque", "Marke", "fabricante"], ["maker space", "market"]),
    ("common/vehicles.yaml", "vehiclemodelbyname", ["vehicle model", "car model", "car name", "Vehicle Name",
                                                    "modelo do veículo"], ["model", "car", "name"]),
    ("common/vehicles.yaml", "vehiclemodelwithmakebyname", ["model", "Modelo", "Modell", "model name"],
     ["models used", "modelling"]),
    ("common/education.yaml", "lettergradebyname", ["grade", "Letter Grade", "final grade", "lettergrade"],
     ["grades level", "gradient", "upgrade"]),
    ("common/education.yaml", "coursecodebyname", ["course", "Course Code", "unit code", "module code",
                                                   "courses offered", "(course1)", "course2", "código del curso"],
     ["courseware", "source", "discourse"]),
    ("common/useraccounts.yaml", "hashtagbyname", ["hashtag", "Hashtags", "hash tag", "entities.hashtags.text"],
     ["hash", "tag"]),
    ("common/useraccounts.yaml", "xpostidbyname", ["tweet id", "tweetid", "status_id", "in_reply_to_status_id_str"],
     ["id", "post_id", "id_str"]),
    ("common/telecom.yaml", "callsignbyname", ["call sign", "callsign", "Call Letters", "station call sign"],
     ["call", "station"]),
    ("common/crossborder_finance.yaml", "tickersymbolbyname", ["symbol", "Ticker", "stock symbol", "ticker symbol"],
     ["symbolic", "tick"]),
    ("br/br_finances.yaml", "brb3tickerbyname", ["ativo", "papel", "código de negociação", "ticker", "símbolo"],
     ["ativos totais", "papelaria"]),
    ("us/us_media.yaml", "usmparatingbyname", ["MPAA", "mpaa rating", "MPA Rating", "rated", "rating", "film rating"],
     ["ratio", "rate"]),
    ("us/us_sports.yaml", "mlbteamcodebyname", ["team", "Tm", "opponent", "opp", "home", "away", "MLB Team", "vs."],
     ["teams", "steam"]),
    ("us/us_sports.yaml", "nbateamcodebyname", ["team", "NBA team", "team abbr"], ["teammate"]),
    ("us/us_sports.yaml", "nflteamcodebyname", ["team", "NFL team", "home team"], ["team members"]),
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


def test_value_rules():
    spec = load("common/useraccounts.yaml", "hashtagvalue")
    pattern = re.compile(spec["rule"])
    for value in ["#wikileaks", "#opassange", "#COVID19"]:
        assert pattern.fullmatch(value) and spec["minlen"] <= len(value) <= spec["maxlen"], value
    for value in ["#2011", "wikileaks", "#", "#0047B2", "#fff"]:
        assert not pattern.fullmatch(value), value
    spec = load("common/entertainment.yaml", "videogameplatformvalue")
    words = {w.strip() for w in spec["rule"].split(",")}
    assert {"ps3", "xbox 360", "wii", "nintendo ds"} <= words and all(w == w.lower() for w in words)
    for path, rule_id in (("common/entertainment.yaml", "biblereferencevalue"), ("common/geo.yaml", "iso6709dmsvalue")):
        spec = load(path, rule_id)
        assert spec["match"] == "func" and spec["rule"].startswith("metacrafterext.rules.common.manyeyes.")
