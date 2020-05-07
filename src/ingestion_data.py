"""Ingestion related data handling."""

import re

from src.graph_model import (Version, EventType, SecurityEvent, FeedBackType, StatusType, EcosystemType)
from src.parse_datetime import from_date_str, get_date, get_year, get_yearmonth


class IngestionData:
    """Encapsulates ingestion data."""

    _URL_PATTERN = re.compile(r'[:/]+')

    def __init__(self, json_data):
        """Init method."""
        self._payload = json_data
        self._sec = None
        self._update_sec = None

    def _timestamp(self, field_name: str):
        return from_date_str(self._payload[field_name])

    def _updated_at(self) -> int:
        return self._timestamp('updated_at')

    def _closed_at(self) -> int:
        return self._timestamp('closed_at') if self._payload['closed_at'] is not None else None

    def _created_at(self) -> int:
        return self._timestamp('created_at')

    def _version_str(self) -> str:
        # (fixme) As of now consider created time as version. It has to be
        # mapped to a proper semantic version of a given package.
        return str(self._created_at())

    def _get_dependency_path(self) -> str:
        components = self._URL_PATTERN.split(self._payload['url'])
        return '%s://%s/%s/%s' % (components[0], components[1], components[2], components[3])

    @property
    def version(self) -> Version:
        """Create Version object from json_data."""
        return Version(version=self._version_str(),
                       dependency_name=self._payload['repo_name'])

    @property
    def security_event(self) -> SecurityEvent:
        """Create SecurityEvent object from json_data."""
        self._sec = self._sec or SecurityEvent(event_type=EventType[self._payload['event_type']],
                                               # body=self._payload['body'],
                                               # title=self._payload['title'],
                                               url=self._payload['url'],
                                               api_url=self._payload['api_url'],
                                               status=StatusType[self._payload['status']],
                                               event_id=str(self._payload['id']),
                                               created_at=self._created_at(),
                                               updated_at=self._updated_at(),
                                               closed_at=self._closed_at(),
                                               repo_name=self._payload['repo_name'],
                                               repo_path=self._get_dependency_path(),
                                               ecosystem=EcosystemType[self._payload['ecosystem']],
                                               creator_name=self._payload['creator_name'],
                                               creator_url=self._payload['creator_url'],
                                               probable_cve=self._payload['probable_cve'],
                                               updated_date=get_date(self._updated_at()),
                                               updated_yearmonth=get_yearmonth(self._updated_at()),
                                               updated_year=get_year(self._updated_at()),
                                               feedback_count=0,
                                               overall_feedback=FeedBackType.NONE
                                               )
        return self._sec

    @property
    def updated_security_event(self) -> SecurityEvent:
        """Create SecurityEvent object from json_data."""
        self._update_sec = self._update_sec or SecurityEvent(status=StatusType[self._payload['status']],
                                                             updated_at=self._updated_at(),
                                                             closed_at=self._closed_at(),
                                                             ecosystem=EcosystemType[self._payload['ecosystem']],
                                                             probable_cve=self._payload['probable_cve'],
                                                             updated_date=get_date(self._updated_at()),
                                                             updated_yearmonth=get_yearmonth(self._updated_at()),
                                                             updated_year=get_year(self._updated_at()))
        return self._update_sec
