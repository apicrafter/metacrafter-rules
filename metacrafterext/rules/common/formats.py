"""Values that hold another format: JSON and XML documents in a text field, WKB geometries
(hexadecimal or bytes), GML coordinate lists and lists of file format names."""
import ast
import json
import re
import struct
import xml.etree.ElementTree as ElementTree

_GEOJSON_TYPES = frozenset((
    "Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon", "GeometryCollection",
    "Feature", "FeatureCollection",
))


def validate_json_text(value):
    """A JSON object, or an array that holds an object or an array, written as text.

    A GeoJSON geometry or feature is geojson; a flat array of numbers ([30.5, 50.4]) is more
    often a coordinate pair than a document.
    """
    text = str(value).strip()
    if len(text) < 7 or (text[0], text[-1]) not in (("{", "}"), ("[", "]")):
        return False
    try:
        data = json.loads(text)
    except ValueError:
        return False
    if isinstance(data, dict):
        if not data:
            return False
        return not (data.get("type") in _GEOJSON_TYPES
                    and any(k in data for k in ("coordinates", "geometries", "geometry", "features")))
    return isinstance(data, list) and any(isinstance(item, (dict, list)) for item in data)


# Tags of HTML fragments, which parse as XML too: a description in HTML is not an XML document.
_HTML_TAGS = frozenset((
    "a", "abbr", "b", "blockquote", "body", "br", "center", "code", "dd", "div", "dl", "dt", "em", "font",
    "h1", "h2", "h3", "h4", "h5", "h6", "head", "hr", "html", "i", "img", "li", "ol", "p", "pre", "s",
    "small", "span", "strong", "sub", "sup", "table", "tbody", "td", "th", "thead", "tr", "u", "ul",
))


def validate_xml_text(value):
    """A well-formed XML element written as text, other than an HTML fragment.

    Values with a document type declaration are refused before parsing (no entity expansion).
    """
    text = str(value).strip()
    if len(text) < 4 or text[0] != "<" or text[-1] != ">" or "<!DOCTYPE" in text or "<!ENTITY" in text:
        return False
    try:
        root = ElementTree.fromstring(text)
    except (ElementTree.ParseError, ValueError):
        return False
    tag = root.tag.rsplit("}", 1)[-1].lower()
    return tag not in _HTML_TAGS


_HEX = re.compile(r"^[0-9A-Fa-f]+$")


def _wkb_bytes(value):
    if isinstance(value, (bytes, bytearray)):
        return bytes(value)
    text = str(value).strip()
    if text[:2] in ("b'", 'b"'):
        try:
            data = ast.literal_eval(text)
        except (ValueError, SyntaxError):
            return None
        return data if isinstance(data, bytes) else None
    if len(text) % 2 == 0 and _HEX.match(text):
        return bytes.fromhex(text)
    return None


def validate_wkb(value):
    """A geometry in well-known binary: bytes (GeoParquet, GeoPackage) or hexadecimal text.

    The byte order flag (0 or 1), a geometry type of OGC (1-7, with the ISO Z/M/ZM thousands)
    or of PostGIS EWKB (Z, M and SRID flags), and enough bytes for the coordinates.
    """
    data = _wkb_bytes(value)
    if not data or len(data) < 9 or data[0] not in (0, 1):
        return False
    order = "<" if data[0] == 1 else ">"
    (code,) = struct.unpack(order + "I", data[1:5])
    has_srid = bool(code & 0x20000000)
    base = code & 0x0FFFFFFF
    if base % 1000 not in range(1, 8) or base // 1000 > 3:
        return False
    header = 9 if has_srid else 5
    dims = 2 + bool(code & 0x80000000) + bool(code & 0x40000000) + (1 if base // 1000 in (1, 2) else 0) + (
        2 if base // 1000 == 3 else 0)
    if base % 1000 == 1:
        return len(data) == header + 8 * dims
    return len(data) >= header + 4


_NUMBER = re.compile(r"^-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?$")


def validate_gml_poslist(value):
    """Numbers separated by spaces, two or three per position (gml:pos, gml:posList)."""
    parts = str(value).split()
    if len(parts) < 2 or not all(_NUMBER.match(p) for p in parts):
        return False
    return len(parts) % 2 == 0 or len(parts) % 3 == 0


_FILE_FORMATS = frozenset((
    "csv", "tsv", "txt", "xls", "xlsx", "xlsm", "ods", "xml", "json", "jsonl", "ndjson", "geojson", "html", "htm",
    "pdf", "doc", "docx", "odt", "rtf", "ppt", "pptx", "zip", "rar", "7z", "gz", "tar", "rdf", "ttl", "n3",
    "jsonld", "json-ld", "shp", "shapefile", "kml", "kmz", "gml", "gpx", "gpkg", "geopackage", "dbf", "mdb",
    "accdb", "sql", "sqlite", "parquet", "avro", "orc", "yaml", "yml", "png", "jpg", "jpeg", "tif", "tiff", "gif",
    "svg", "mp3", "mp4", "epub", "netcdf", "nc", "hdf5", "sav", "dta", "sdmx", "px", "ics", "gtfs", "api", "wms",
    "wfs", "wmts", "atom", "rss", "odata",
))
_FORMAT_SEP = re.compile(r"\s*[,;|/]\s*|\s+")


def validate_file_formats(value):
    """One or more file format names (CSV, XLSX, GeoJSON, HTML,CSV,XLS,XML)."""
    text = str(value).strip().lower()
    if not text:
        return False
    if text in _FILE_FORMATS:
        return True
    parts = [p.lstrip(".") for p in _FORMAT_SEP.split(text) if p]
    return bool(parts) and all(p in _FILE_FORMATS for p in parts)
