"""Refresh the department codes and names of metacrafterext/rules/ar_country/census.py from the
georef service of datos.gob.ar (Servicio de normalización de direcciones y unidades territoriales,
CC BY 4.0):

    python scripts/update_ar_departments.py [departamentos.json]

Without an argument the list is fetched from apis.datos.gob.ar. The block between the
``# departments:start`` and ``# departments:end`` lines is rewritten; codes that census files of
earlier years use (comunas 02001 to 02015 of the City of Buenos Aires, the Tierra del Fuego
departments before 2017) are kept in census.py outside the block.
"""
import json
import pathlib
import sys
import textwrap
import unicodedata
import urllib.request

URL = "https://apis.datos.gob.ar/georef/api/departamentos?max=1000&campos=id,nombre"
TARGET = pathlib.Path(__file__).resolve().parent.parent / "metacrafterext" / "rules" / "ar_country" / "census.py"


def norm(name):
    text = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    return " ".join(text.replace(".", " ").split())


def main():
    if len(sys.argv) > 1:
        data = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    else:
        with urllib.request.urlopen(URL, timeout=60) as r:
            data = json.load(r)
    rows = data["departamentos"]
    codes = sorted({r["id"] for r in rows})
    names = sorted({norm(r["nombre"]) for r in rows})
    wrap = lambda words: textwrap.fill(" ".join(words), 96, initial_indent="    ", subsequent_indent="    ")
    block = (
        "# departments:start (scripts/update_ar_departments.py, %d departments of georef)\n"
        '_GEOREF_DEPARTMENT_CODES = """\n%s\n"""\n'
        '_GEOREF_DEPARTMENT_NAMES = """\n%s\n"""\n'
        "# departments:end\n" % (len(rows), wrap(codes), "\n".join("    " + n for n in names))
    )
    text = TARGET.read_text(encoding="utf-8")
    start, end = text.index("# departments:start"), text.index("# departments:end\n") + len("# departments:end\n")
    TARGET.write_text(text[:start] + block + text[end:], encoding="utf-8")
    print(f"{len(codes)} codes, {len(names)} names -> {TARGET}")


if __name__ == "__main__":
    main()
