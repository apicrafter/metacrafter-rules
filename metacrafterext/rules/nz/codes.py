"""New Zealand names found in 2024 snapshots of data.govt.nz and of the Biological Heritage data
repository (Dateno sources cdi00001241, cdi00001243): the 16 regions.
"""
import re

_REGION = re.compile(
    r"(?:northland|auckland|waikato|bay of plenty|gisborne|hawke'?s bay|taranaki|manawat[uū]-w(?:h)?anganui"
    r"|wellington|tasman|nelson|marlborough|west coast|canterbury|otago|southland)(?: region)?")


def validate_nz_region(value):
    """A region of New Zealand: Canterbury, Bay of Plenty, Hawke's Bay, Manawatū-Whanganui, Otago Region."""
    return bool(_REGION.fullmatch(" ".join(str(value).split()).lower().replace("’", "'")))
