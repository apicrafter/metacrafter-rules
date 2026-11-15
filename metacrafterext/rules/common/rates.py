"""Validators for interest rates: percentages (6,00%), reference rates with a spread (Badlar + 2%,
LIBOR 12M + 3,70%, CER + 0,1%) and rates in words (tasa fija anual del 21%, 30 % de la TNA del BNA).

Found in the public debt profiles and the credit lines of the province of Mendoza (Datos Abiertos
Mendoza) for metacrafter-testdata.
"""
import re
import unicodedata

# Reference rates of loans and bonds: Argentine (BADLAR, TM20, TAMAR, the CER and UVA indexes, the
# TNA of the Banco de la Nación), and international (LIBOR, SOFR, EURIBOR, SONIA, €STR, prime).
_REFERENCE = (r"badlar|libor|sofr|euribor|sonia|e?str|€str|tamar|tm20|cer|uva|tna(?: del bna)?|prime(?: rate)?"
              r"|tasa (?:pasiva|activa)(?: del bna| bna)?|letras? (?:del )?tesoro|10 ?-?y(?:ear)? bond|bonos? del tesoro")
_SPREAD = r"[+-]\s*\d+(?:[.,]\d+)?\s*(?:%|bps|pb|pbs|p\.?\s?p\.?|puntos(?: porcentuales)?)?"
_REFERENCE_RATE = re.compile(r"^(?:\d+(?:[.,]\d+)?\s*%\s*(?:/|o)\s*)?(?:" + _REFERENCE + r")\b[^%+\-]{0,40}(?:" + _SPREAD + r")?$")
_PERCENT = re.compile(r"^[+-]?\d{1,3}(?:[.,]\d+)?\s*%$")
_IN_WORDS = re.compile(r"\d+(?:[.,]\d+)?\s*%")
_RATE_WORDS = re.compile(r"\b(?:tasa|tna|tea|tem|interes|rate|taux|zins)")


def _fold(value):
    text = unicodedata.normalize("NFKD", str(value).strip().lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(text.split())


# Reference rates that need a spread to be told from other words: uva is a grape, cer, prime, str
# and tna are abbreviations of other things.
_AMBIGUOUS_REFERENCE = re.compile(r"^(?:cer|uva|e?str|€str|prime|tna|tasa|letras?|bonos?|10)\b")


def validate_interest_rate_reference(value):
    """A reference rate with or without a spread: Badlar + 2%, Libor + 3,70%, CER + 0,1%, BADLAR
    Bancos Privados, EURIBOR 6M + 0.5% (for value rules on any field; 6,00% is any percentage, and
    Uva or CER need the spread)."""
    text = _fold(value)
    if not _REFERENCE_RATE.match(text):
        return False
    return not _AMBIGUOUS_REFERENCE.match(text) or bool(re.search(_SPREAD, text))


def validate_interest_rate(value):
    """An interest rate in a field named for it: 6,00%, 11.41 %, Badlar + 2%, tasa fija anual del 21%,
    30 % de la TNA del BNA, 15% / BADLAR Bancos Privados (not Semestral or a bare number)."""
    text = _fold(value)
    if not text:
        return False
    if _PERCENT.match(text) or _REFERENCE_RATE.match(text):
        return True
    if "/" in text and all(validate_interest_rate(part) for part in text.split("/") if part.strip()):
        return True
    return len(text) <= 80 and bool(_IN_WORDS.search(text)) and bool(_RATE_WORDS.search(text))


# ---------------------------------------------------------------- amounts
# Amounts written with dots as thousands separators and a decimal comma, as Spanish, Argentine
# and other European tables write them (6.613.703,03, -136.786,75, 0,00, 0), optionally after a
# currency sign or code ($ 298.278.261,30, ARS 3.662,50, USD 44,59).
_CURRENCY_MARK = r"(?:\$|ARS|USD|U\$S|US\$|EUR|€)"
_EUROPEAN_NUMBER = r"-?(?:\d{1,3}(?:\.\d{3})+|\d+)(?:,\d{1,4})?"
_AMOUNT = re.compile(r"^(?:" + _CURRENCY_MARK + r"\s?)?" + _EUROPEAN_NUMBER + r"$")
_MARKED_AMOUNT = re.compile(r"^" + _CURRENCY_MARK + r"\s?" + _EUROPEAN_NUMBER + r"$|^" + _EUROPEAN_NUMBER + r"\s?" + r"(?:€|EUR)$")


def validate_es_amount(value):
    """An amount in a field named for a stage of a budget: 6.613.703,03, 0,00, 0, -136.786,75,
    $ 298.278.261,30, a dash for none (not 2018/01, a date or text)."""
    text = str(value).strip()
    return text in ("-", "—") or bool(_AMOUNT.match(text))


def validate_marked_amount(value):
    """An amount with a currency sign or code and dots as thousands separators or a decimal comma:
    $ 298.278.261,30, ARS 3.662,50, USD 44,59, 1.234,50 € (for value rules on any field; $5 or
    USD alone are not one)."""
    text = " ".join(str(value).split())
    if not _MARKED_AMOUNT.match(text):
        return False
    return "," in text or "." in text
