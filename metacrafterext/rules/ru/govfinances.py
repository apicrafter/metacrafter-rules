from .orgs import _check_inn

def is_iku_iko_code(s):
    """Validates if value is IKU/IKO code, Russian government customer assigned code composed from INN and KPP codes"""
    if len(s) != 20: return False
    if int(s[0]) in [0, 9]: return False
    if not _check_inn(s[1:11]): return False
#    if not _check_kpp(s[11:20]): return False
    return True

def is_ikz_code(s):
    """Validates if value is IKZ code, Russian government purchase number composed from INN and KPP codes"""
    if len(s) != 36: return False
    if int(s[0]) in [0, 9]: return False
    if not _check_inn(s[1:11]): return False
#    if not _check_kpp(s[11:20]): return False
    return True

def is_ikg_code(s):
    """Validates if value is IKG code, Russian government contract number composed from INN code"""
    if len(s) != 20: return False
    if (int(s[0]) > 5) or (int(s[0]) == 0): return False
    if not _check_inn(s[1:11]): return False
    if not int(s[11:13]) > 30: return False
    return True
