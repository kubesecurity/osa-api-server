"""Ingestion related data handling."""

import re
from src.graph_model import (Dependency, Version, Ecosystem, EventType,
                             ProbableCVE, SecurityEvent)
from src.parse_datetime import from_date_str


class IngestionData:
    """Encapsulates ingestion data."""

    _URL_PATTERN = re.compile(r'[:/]+')

    def __init__(self, json_data):
        """Init method."""
        self._payload = json_data
        self._sec = None

    @property
    def dependency(self) -> Dependency:
        """Create Dependency object from json_data."""
        return Dependency(dependency_name=self._payload['repo_name'],
                          dependency_path=self._get_dependency_path())

    def _timestamp(self, field_name: str):
        try:
            return from_date_str(self._payload[field_name])
        except:
            return None

    def _updated_at(self) -> int:
        return self._timestamp('updated_at')

    def _closed_at(self) -> int:
        return self._timestamp('closed_at')

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
    def probable_cve(self) -> ProbableCVE:
        """Create ProbableCVE object from json_data."""
        pcve_id = 'PCVE-{repo_name}-{number}'.format(**self._payload)
        return ProbableCVE(probable_vuln_id=pcve_id)

    @property
    def ecosystem(self) -> Ecosystem:
        """Create Ecosystem object from json_data."""
        return Ecosystem(ecosystem_name=self._payload['ecosystem'])

    @property
    def security_event(self) -> SecurityEvent:
        """Create SecurityEvent object from json_data."""
        self._sec = self._sec or SecurityEvent(event_type=EventType[self._payload['event_type']],
                                               body=self._payload['url'],
                                               title=self._payload['url'],
                                               url=self._payload['url'],
                                               status=self._payload['status'],
                                               event_id=str(self._payload['id']),
                                               created_at=self._created_at(),
                                               updated_at=self._updated_at(),
                                               closed_at=self._closed_at())
        return self._sec
