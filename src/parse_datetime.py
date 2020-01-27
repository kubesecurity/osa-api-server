"""ISO8601 related helper functions"""

from datetime import datetime, timezone
from dateutil.parser import isoparse

def from_date_str(str_: str) -> int:
    ''' converts iso8601 format string to timestamp '''
    return int(isoparse(str_).timestamp())

def to_date_str(epoch: int) -> str:
    ''' converts timestamp to iso8601 format string '''
    try:
        return datetime.fromtimestamp(int(epoch), timezone.utc).isoformat(' ')
    except: # pylint: disable=bare-except
        return ""
