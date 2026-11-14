"""Refresh the Arabic country names of metacrafterext/rules/ar/countries.py from Unicode CLDR (the
territory names of the ``ar`` locale, through Babel) and the Arabic translations of ISO 3166-1 of
the Debian iso-codes project (through pycountry):

    pip install babel pycountry
    python scripts/update_ar_country_names.py

The block between the ``# names:start`` and ``# names:end`` lines is rewritten with the folded
names (``countries.country_key``) and their ISO 3166-1 alpha-2 codes. Spellings that neither
source has (بنجلاديش, نيوزلندا, الولايات المتحدة الأمريكية) are kept in countries.py outside
the block.
"""
import gettext
import pathlib
import re
import sys

TARGET = pathlib.Path(__file__).resolve().parent.parent / "metacrafterext" / "rules" / "ar" / "countries.py"
sys.path.insert(0, str(TARGET.parent.parent.parent.parent))

from metacrafterext.rules.ar.countries import country_key  # noqa: E402

NOT_COUNTRIES = {"EU", "EZ", "UN", "QO", "XA", "XB", "ZZ"}


def main():
    import pycountry
    from babel import Locale

    names = {}
    for code, name in Locale("ar").territories.items():
        if re.fullmatch(r"[A-Z]{2}", code) and code not in NOT_COUNTRIES:
            names.setdefault(country_key(name), code)
    iso = gettext.translation("iso3166-1", pycountry.LOCALES_DIR, languages=["ar"])
    for country in pycountry.countries:
        for attr in ("name", "official_name", "common_name"):
            english = getattr(country, attr, None)
            if english and iso.gettext(english) != english:
                names.setdefault(country_key(iso.gettext(english)), country.alpha_2)
    lines = [f'    "{key}": "{code}",' for key, code in sorted(names.items(), key=lambda kv: (kv[1], kv[0]))]
    block = (
        f"# names:start (scripts/update_ar_country_names.py, {len(names)} names of CLDR and iso-codes)\n"
        "_SOURCE_NAMES = {\n" + "\n".join(lines) + "\n}\n# names:end\n"
    )
    text = TARGET.read_text(encoding="utf-8")
    text = re.sub(r"# names:start.*?# names:end\n", lambda _: block, text, flags=re.S)
    TARGET.write_text(text, encoding="utf-8")
    print(f"{len(names)} names written to {TARGET}")


if __name__ == "__main__":
    main()
