"""Abbreviations of the teams of Major League Baseball, the NBA and the NFL, found in the tables of the Many Eyes
archive (IBM Many Eyes, 2007 to 2012): box scores, standings, rosters, drafts and fantasy league tables.

The sets hold the current teams with the variants that sources use (CWS and CHW, KC and KCR) and the teams that
moved or were renamed since the 1990s (MON, FLA, NJN, SEA, OAK, SD, STL). The leagues share many codes (ATL,
BOS, CHI): a column of one league passes its own validator for every value and the others for part of them.
"""
from metacrafterext.rules.common.b13 import text

MLB_TEAMS = frozenset(
    "ARI AZ ATL BAL BOS CHC CHN CWS CHW CHA CIN CLE COL DET HOU KC KCR KCA LAA ANA CAL LAD LA LAN MIA FLA MIL MIN "
    "NYM NYN NYY NYA OAK ATH PHI PIT SD SDP SDN SEA SF SFG SFN STL SLN TB TBR TBD TBA TEX TOR WSH WSN WAS MON FLO".split()
)
NBA_TEAMS = frozenset(
    "ATL BOS BKN BRK NJN NJ CHA CHO CHH CHI CLE DAL DEN DET GSW GS HOU IND LAC LAL MEM VAN MIA MIL MIN NOP NOH NOK NO "
    "NYK NY OKC SEA ORL PHI PHX PHO POR SAC SAS SA TOR UTA UTAH WAS WSH WSB".split()
)
NFL_TEAMS = frozenset(
    "ARI ARZ ATL BAL BUF CAR CHI CIN CLE DAL DEN DET GB GNB HOU IND JAX JAC KC KAN LV LVR OAK LAC SD SDG LAR LA STL "
    "MIA MIN NE NWE NO NOR NYG NYJ PHI PIT SEA SF SFO TB TAM TEN WAS WSH".split()
)


def _code(value):
    return text(value).upper()


def validate_mlb_team_code(value):
    """An MLB team abbreviation: NYY, LAD, CWS, TOR, FLA (not GSW, NE, Yankees)."""
    return _code(value) in MLB_TEAMS


def validate_nba_team_code(value):
    """An NBA team abbreviation: LAL, GSW, NYK, SAS, NJN (not NYY, NE, Lakers)."""
    return _code(value) in NBA_TEAMS


def validate_nfl_team_code(value):
    """An NFL team abbreviation: NE, GB, NYG, KC, JAX (not NYY, GSW, Patriots)."""
    return _code(value) in NFL_TEAMS
