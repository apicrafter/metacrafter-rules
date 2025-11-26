# -*- coding: utf-8 -*-

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