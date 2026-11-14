# -*- coding: utf-8 -*-
import datetime
import re

def is_valid_time(s):
    if not s: return False
    if len(s) not in [5,8]: return False
    parts = s.split(':')
    if len(parts) not in [2,3]: return False
    if parts[0].isdigit():
        if int(parts[0]) >= 0 and int(parts[0]) <= 24:
            if parts[1].isdigit():
                if int(parts[1]) >= 0 and int(parts[1]) <= 59:
                    if len(parts) == 3:
                        if parts[2].isdigit():
                            if int(parts[2]) >= 0 and int(parts[2]) <= 59:
                                return True
                    else:
                        return True
    return False

def is_valid_timerange(s):
    if not s: return False
    if len(s) != 11: return False
    if not is_valid_time(s[0:5]): return False
    if not is_valid_time(s[6:]): return False
    return True


def is_iso_date(s):
    """ISO 8601 calendar date in the extended form YYYY-MM-DD that exists in the calendar.

    Rejects days that the month does not have (2025-02-30, 2023-02-29) and year 0000.
    """
    if not isinstance(s, str) or len(s) != 10 or s[4] != '-' or s[7] != '-':
        return False
    year, month, day = s[0:4], s[5:7], s[8:10]
    if not all(part.isascii() and part.isdigit() for part in (year, month, day)):
        return False
    try:
        datetime.date(int(year), int(month), int(day))
    except ValueError:
        return False
    return True


# Milliseconds from 1900-01-01 to 2100-01-01 (UTC).
_MS_MIN, _MS_MAX = -2208988800000, 4102444800000
_UNIXTIME_MS = re.compile(r"^-?\d{11,13}(?:\.0+)?$")


def validate_unixtime_ms(value):
    """Unix time in milliseconds: an integer of 11 to 13 digits (negative before 1970) from
    1900 to 2100 (1689019752000, -1019869200000). ArcGIS REST and GeoJSON exports and
    JavaScript-backed APIs write dates this way (metacrafter-rules #70)."""
    text = str(value).strip()
    if not _UNIXTIME_MS.match(text):
        return False
    return _MS_MIN <= int(float(text)) < _MS_MAX


def validate_not_unixtime_ms(value):
    """A value of a timestamp field that is not Unix time in milliseconds (unixtime_ms): seconds
    (1471181882) or a written date and time (2024-01-05T10:00:00)."""
    return bool(str(value).strip()) and not validate_unixtime_ms(value)


_DECIMAL_YEAR = re.compile(r"^(?:1[5-9]|2[01])\d{2}(?:\.\d{1,6})?$")


def validate_decimal_year(value):
    """A year with the elapsed part of the year as a fraction (1994.83, 2019.0417), or a whole
    year in the same column (2004), between 1500 and 2199."""
    return bool(_DECIMAL_YEAR.match(str(value).strip()))


_EXCEL_DATETIME = re.compile(r"^([1-5]\d{4})\.(\d{1,17})$")


def validate_excel_serial_datetime(value):
    """A date and time as an Excel serial number: days since 30 December 1899 with the time of
    day as the fraction (45175.42585648148 is 6 September 2023, 10:13:14), from 1927 (10000) to
    2173 (99999). A whole day (45175 or 45175.0) is excel_serial_date. The Dataverse .tab exports
    of Excel sheets write timestamps this way (RDA-UNR survey of researchers, metacrafter-testdata
    2026-11-14)."""
    match = _EXCEL_DATETIME.match(str(value).strip())
    return bool(match) and match.group(2).strip("0") != ""


# One date of a date range: day-month-year with - . or / and a year of 2 or 4 digits (5-4-02,
# 27.05.2002, 1/3/2020), or year-month-day (2020-01-01).
_RANGE_DATE = r"(?:\d{1,2}[-./]\d{1,2}[-./](?:\d{2}|\d{4})|\d{4}-\d{2}-\d{2})"
_DATE_RANGE = re.compile(
    rf"^(?:(?:del?|from|du|vom|von|desde)\s+)?(?P<a>{_RANGE_DATE})"
    r"(?:\s*(?:/|-|–|—)\s*|\s+(?:al|a|hasta|to|till|until|through|au|à|bis)\s+)"
    rf"(?P<b>{_RANGE_DATE})$",
    re.IGNORECASE,
)


def _range_date(text):
    if len(set(re.findall(r"[-./]", text))) != 1:
        return None  # 5-4.02: the separators of one date are the same
    parts = re.split(r"[-./]", text)
    if len(parts[0]) == 4:
        year, month, day = (int(p) for p in parts)
    else:
        day, month, year = (int(p) for p in parts)
        if year < 100:
            year += 2000 if year < 70 else 1900
    try:
        return datetime.date(year, month, day)
    except ValueError:
        return None


def validate_date_range(value):
    """A period between two dates written as one value: 5-4-02 al 27-5-02, 22-1-02/27-2-02 (cuts
    of alfalfa of the INTA Rafaela cultivar network), 01.03.2020 - 31.03.2020, the ISO 8601
    interval 2020-01-01/2020-03-31. Both dates must exist and the second may not come before the
    first."""
    match = _DATE_RANGE.match(" ".join(str(value).split()))
    if not match:
        return False
    start, end = _range_date(match.group("a")), _range_date(match.group("b"))
    return start is not None and end is not None and start <= end
