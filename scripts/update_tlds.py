"""Regenerate metacrafterext/rules/common/tlds.py from the IANA list of top-level domains.

Usage: python scripts/update_tlds.py [tlds-alpha-by-domain.txt]

Without an argument the list is downloaded from https://data.iana.org/TLD/tlds-alpha-by-domain.txt.
"""
import pathlib
import re
import sys
import textwrap
import urllib.request

SOURCE = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
TARGET = pathlib.Path(__file__).resolve().parent.parent / "metacrafterext" / "rules" / "common" / "tlds.py"


def main():
    if len(sys.argv) > 1:
        text = pathlib.Path(sys.argv[1]).read_text(encoding="ascii")
    else:
        with urllib.request.urlopen(SOURCE, timeout=60) as response:
            text = response.read().decode("ascii")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    version = lines[0].lstrip("# ").strip() if lines[0].startswith("#") else "unknown"
    tlds = sorted(line.lower() for line in lines if not line.startswith("#"))
    bad = [tld for tld in tlds if not re.fullmatch(r"[a-z0-9-]+", tld)]
    if bad or len(tlds) < 1000:
        raise SystemExit(f"Unexpected TLD list: {len(tlds)} entries, invalid {bad[:5]}")
    body = textwrap.fill(" ".join(repr(t) + "," for t in tlds), width=96,
                         initial_indent="    ", subsequent_indent="    ", break_on_hyphens=False)
    TARGET.write_text(
        '"""Top-level domains of the IANA root zone, lower case; IDN TLDs in their xn-- form.\n\n'
        f"Source: {SOURCE}\n{version}.\n"
        'Regenerate with scripts/update_tlds.py.\n"""\n\n'
        f"TLDS = frozenset({{\n{body}\n}})\n",
        encoding="ascii",
    )
    print(f"{TARGET}: {len(tlds)} TLDs ({version})")


if __name__ == "__main__":
    main()
