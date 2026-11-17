"""Norwegian identifiers found in a 2024 snapshot of DataverseNO (dataverse.no, Dateno source
cdi00001211): references of decisions of the Supreme Court.
"""
import re

_SUPREME_COURT = re.compile(r"HR-(?:19|20)\d{2}-\d{1,5}-[A-Z]|Rt-(?:1[89]|20)\d{2}-\d{1,4}")


def validate_no_supreme_court_reference(value):
    """A reference of a decision of the Supreme Court of Norway: HR-2019-2420-A, HR-2019-1910-U, or the
    yearbook Norsk Retstidende with year and page, Rt-2015-353."""
    return bool(_SUPREME_COURT.fullmatch(str(value).strip()))
