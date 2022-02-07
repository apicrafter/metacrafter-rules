# -*- coding: utf8 -*-
RUS_ACCOUNT_MASK = [7,1,3,7,1,3,7,1,3,7,1,3,7,1,3,7,1,3,7,1,3,7,1]
PLANSCHET_RANGES = [(301, 329), (401, 479)]
# Most common currencies used in Russian banking system. Actually 99% accounts are with code 810
# 756- Swiss Frank, 810 - Ruble, 826 - UK Sterling pound, 840 - USD, 978 - Euro,
VALID_CURRENCY = [756, 810, 826, 840, 978]


def is_bank_account(s):
    """Verifies bank account against most common patterns of accounting type of account and common currencies"""
    pk = int(s[0:3])
    pk_valid = False
    for r in PLANSCHET_RANGES:
        if pk >= r[0] and pk <= r[1]:
            pk_valid = True
            break
    if not pk_valid: return False
    currency = int(s[5:8])
    if currency not in VALID_CURRENCY:
        return False
    return True
