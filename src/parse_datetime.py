"""ISO8601 related helper functions."""

from datetime import datetime, timezone
from dateutil.parser import isoparse


def from_date_str(str_: str) -> int:
    """Convert iso8601 format string to timestamp."""
    try:
        return int(isoparse(str_).timestamp())
    except:
        return ""


def get_date(epoch: int) -> int:
    """Get date into 'yyyyMMdd' format from timestamp."""
    date = datetime.fromtimestamp(int(epoch), timezone.utc)
    return int("{year}{month:02d}{date:02d}".format(year=date.year, month=date.month, date=date.day))


def get_yearmonth(epoch: int) -> int:
    """Get year & month combination in 'yyyyMM' format from timestamp."""
    date = datetime.fromtimestamp(int(epoch), timezone.utc)
    return int("{year}{month:02d}".format(year=date.year, month=date.month))


def get_year(epoch: int) -> int:
    """Get Year in yyyy format from timestamp."""
    return datetime.fromtimestamp(int(epoch), timezone.utc).year


def to_date_str(epoch: int) -> str:
    """Convert timestamp to iso8601 format string."""
    try:
        return datetime.fromtimestamp(int(epoch), timezone.utc).isoformat(' ')
    except:
        return ""
