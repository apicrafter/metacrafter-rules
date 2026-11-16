"""Periods, bands and classification symbols found in the data.gov.au files of metacrafter-testdata
(a snapshot of the Australian national open data portal): financial years (2014-15), months with an
English month name and a year (Sep-17), quarters with their year (2021Q04), money ranges ($100K - $5m)
and International Patent Classification symbols (A47G  23/02)."""
import re

# 2014-15, 2014–15, 2014/15, 1999-00, 2014-2015, 2010/2011, FY2014-15, FY 2014-15, FY201415.
_FISCAL_YEAR = re.compile(r"^(?:FY ?)?((?:1[89]|20)\d{2})(?:[-–/]((?:1[89]|20)?\d{2})|(\d{2}))$", re.I)
_SHORT_FISCAL_YEAR = re.compile(r"^(?:FY ?)?(?:1[89]|20)\d{2}(?:[-–/]\d{2}|\d{2})$", re.I)


def _fiscal_years(value):
    m = _FISCAL_YEAR.match(str(value).strip())
    if not m:
        return None
    first = int(m.group(1))
    second = m.group(2) or m.group(3)
    if len(second) == 2:
        return first, (first // 100 * 100 + int(second)) if int(second) != 0 or first % 100 == 99 else first + 1
    return first, int(second)


def validate_fiscal_year(value):
    """A financial year of two consecutive years: 2014-15, 2010–11, 1999-00, 2014/15, 2014-2015, FY201213
    (not 2014-16, 2014-12 or a single year)."""
    years = _fiscal_years(value)
    if not years:
        return False
    first, second = years
    if first % 100 == 99 and second == first // 100 * 100:
        second += 100
    return second == first + 1


def validate_fiscal_year_short(value):
    """A financial year with the second year in two digits or an FY prefix (2014-15, FY2014-15, FY201415):
    a value rule must not take year ranges of four-digit years (2019-2020, year_range)."""
    text = str(value).strip()
    if not (_SHORT_FISCAL_YEAR.match(text) or text[:2].upper() == "FY"):
        return False
    return validate_fiscal_year(text)


_MONTHS = ("jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|sept|september|"
           "oct|october|nov|november|dec|december")
_YEARMONTH_ENGLISH = re.compile(rf"^(?:{_MONTHS})\.?[- ](?:\d{{2}}|(?:1[6-9]|20)\d{{2}})$", re.I)


def validate_yearmonth_english(value):
    """A month and a year with an English month name: Sep-17, Aug-2011, June 2014, Jan 1841 (not 17-Sep,
    2017-09, September)."""
    return bool(_YEARMONTH_ENGLISH.match(str(value).strip()))


_HAS_YEAR = re.compile(r"(?:^|\D)(?:1[6-9]|20)\d{2}(?:\D|$)|^[A-Za-z]{3,9}\.?[- ]\d{2}$")


def validate_not_yearmonth(value):
    """A month field value that is not a month of a year: Jul-19 and 2019-07 are yearmonth, 7, 07, July
    and Juli are months."""
    return not _HAS_YEAR.search(str(value).strip())


_YEAR_QUARTER = re.compile(r"^(?:(?:1[89]|20)\d{2}[- ]?Q0?[1-4]|Q[1-4][- ](?:1[89]|20)\d{2})$", re.I)


def validate_year_quarter(value):
    """A quarter with its year: 2021Q04, 2022Q03, 2021-Q4, 2021 Q4, Q4 2021 (not 2021Q5 or Q4)."""
    return bool(_YEAR_QUARTER.match(str(value).strip()))


_AMOUNT = r"(?:[$€£] ?)?\d[\d,]*(?:\.\d+)? ?(?:[kKmMbB]n?|million|billion)?"
_MONEY_RANGE = re.compile(
    rf"^(?:[a-z]\. ?)?(?:"
    rf"(?:equal to or )?(?:less than|greater than|more than|under|over|up to)(?: or equal to)? \$ ?{_AMOUNT}"
    rf"|[<>≤≥]=? ?\$ ?{_AMOUNT}"
    rf"|\$ ?{_AMOUNT}(?: ?(?:-|–|to|and)(?: less than| ?<)? ?\$? ?{_AMOUNT}|\+| or (?:more|over|above|less))"
    rf"|{_AMOUNT} ?(?:-|–|to)(?: less than)? ?{_AMOUNT}"
    rf"|(?:refund|debit|loss|income|profit)s? (?:between|of) \$ ?{_AMOUNT}(?: and \$ ?{_AMOUNT})?"
    rf")$",
    re.I,
)
# Bands without bounds: Loss/nil, a. Loss, b. Nil, b. $0 (with its letter: a bare 0 is an amount).
_MONEY_BAND_WORDS = re.compile(r"^(?:[a-z]\. ?)?(?:loss|nil|loss/nil|nil/loss|loss or nil|nil or loss|all ranges|"
                               r"less than \$0|no (?:income|tax|turnover|refund or debit))\.?$|^[a-z]\. ?\$0$", re.I)


def validate_money_range(value):
    """A band of money amounts: $100K - $5m, < $100K, > $2.5m, b. $18,201 to $37,000, a. 10,000 to less
    than 50,000, $0-$49999, Equal to or greater than $25,001, e. Refund between $2,000 and $3,999, and the
    band words Loss/nil, a. Less than $0, b. $0 (not 0, 25, $5,000 or 18-24)."""
    text = re.sub(r"\s+", " ", str(value).strip())
    if _MONEY_BAND_WORDS.match(text):
        return True
    if not _MONEY_RANGE.match(text):
        return False
    # 10,000 to 50,000 without a currency sign must be a band of large amounts or carry a letter.
    if "$" not in text and not re.match(r"^[a-z]\. ?", text, re.I) and not re.search(r"\d{1,3},\d{3}", text):
        return False
    return True


_IPC = re.compile(r"^[A-HY]\d{2}[A-Z](?: *\d{1,4} */ *\d{2,6})?$")
_IPC_GROUP = re.compile(r"^[A-HY]\d{2}[A-Z] *\d{1,4} */ *\d{2,6}$")


def validate_ipc_code(value):
    """An International Patent Classification symbol: A47G  23/02, A47G23/02, G06Q 90/00, H04L (not
    I01B 1/00 or A47G 23)."""
    return bool(_IPC.match(str(value).strip()))


def validate_ipc_group(value):
    """An IPC symbol down to the group (A47G  23/02): a value rule does not take subclasses alone."""
    return bool(_IPC_GROUP.match(str(value).strip()))


# Patent and plant variety numbers of IPGOD that the registry has records for.
_PCT = re.compile(r"^PCT/[A-Z]{2}(?:(?:19|20)\d{2}/\d{6}|\d{2}/\d{5})$")
_WO = re.compile(r"^WO ?(?:(?:19|20)\d{2}/?\d{6}|\d{2}/?\d{5,6})(?: ?A[1-489])?$")
_UPOV = re.compile(r"^[A-Z]{5}(?:_[A-Z]{3}(?:_[A-Z]{1,3})?)?(?:_[1-9][A-Z0-9]{0,5})?$")


def validate_pct_application_number(value):
    """A PCT international application number: PCT/AU1980/000001, PCT/US95/03744 (not PCT/AU1980/1)."""
    return bool(_PCT.match(str(value).strip()))


def validate_wo_publication_number(value):
    """A PCT international publication number: WO1980/002164, WO80/02164, WO 2004/012345 A1."""
    return bool(_WO.match(str(value).strip()))


def validate_upov_code(value):
    """A UPOV code of a plant taxon: SOLAN_LYC, LILIU, PRUNU_PER_NUC, OCIMU_BAS (not Lilium or LIL)."""
    return bool(_UPOV.match(str(value).strip()))


# ------------------------------------------------------------------ seasons
# Found in 2024 snapshots of DataverseNO (dataverse.no, Dateno source cdi00001211).
_SEASONS = frozenset(("spring", "summer", "autumn", "fall", "winter"))


def validate_season_name(value):
    """A season of the year in English: Spring, summer, Autumn, FALL, Winter (not 1986/87 or wet)."""
    return str(value).strip().lower() in _SEASONS
