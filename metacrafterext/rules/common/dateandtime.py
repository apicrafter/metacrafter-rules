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
