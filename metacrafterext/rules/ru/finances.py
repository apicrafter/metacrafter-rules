# -*- coding: utf8 -*-
RUS_ACCOUNT_MASK = [7,1,3,7,1,3,7,1,3,7,1,3,7,1,3,7,1,3,7,1,3,7,1]
PLANSCHET_RANGES = [(301, 329), (401, 479)]
# Most common currencies used in Russian banking system. Actually 99% accounts are with code 810
# 756- Swiss Frank, 810 - Ruble, 826 - UK Sterling pound, 840 - USD, 978 - Euro,
# 156 - Yuan, 344 - Hong Kong dollar, 356 - Indian rupee, 392 - Yen, 398 - Tenge,
# 643 - Ruble (ISO 4217), 784 - UAE dirham, 933 - Belarusian ruble, 949 - Turkish lira
VALID_CURRENCY = [156, 344, 356, 392, 398, 643, 756, 784, 810, 826, 840, 933, 949, 978]


def is_bank_account(s):
    """Verifies bank account against most common patterns of accounting type of account and common currencies

    A Russian account number has 20 digits: the balance account of the chart of accounts
    (digits 1-5), the currency code (6-8), a check digit computed with the bank BIC (9) and
    the account itself. Without the BIC the check digit cannot be verified, so the balance
    account and the currency are checked. Zero-padded codes (00000000000000000111) fail.
    """
    if not isinstance(s, str) or len(s) != 20 or not s.isdigit():
        return False
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
