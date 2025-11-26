# -*- coding: utf8 -*-

RUS_MIDNAME_POSTFIXES = ['вич', 'вна']

def is_russian_fullname(s):
    """Ever simple Russian fullname matcher by midname postfix"""
    parts = s.lower().split()
    if len(parts) != 3: return False
    if parts[2][-3:] in RUS_MIDNAME_POSTFIXES:
        return True
    return False

