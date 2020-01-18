import re
from src.graph_model import Dependency, Version, Ecosystem, Feedback, ReportedCVE, ProbableCVE, SecurityEvent
from src.types import *
from src.parse_datetime import from_date_str

class IngestionData:
    _URL_PATTERN = re.compile(r'[:/]+')

    def __init__(self, json_data):
        self._payload = json_data
        self._sec = None

    @property
    def dependency(self) -> Dependency:
        return Dependency(
                dependency_name=self._payload['repo_name'],
                dependency_path=self._get_dependency_path()
                )

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
        return '%s://%s/%s/%s' % (components[0], components[1], components[2] , components[3])

    @property
    def version(self) -> Version:
        return Version(
                version=self._version_str(),
                dependency_name=self._payload['repo_name']
                )

    @property
    def probable_cve(self) -> ProbableCVE:
        pcve_id = 'PCVE-{repo_name}-{number}'.format(**self._payload)
        return ProbableCVE(probable_vuln_id=pcve_id)

    @property
    def ecosystem(self) -> Ecosystem:
        return Ecosystem(ecosystem_name=self._payload['ecosystem'])

    def _get_event_type(self) -> EventType:
        event = self._payload['event_type']
        if event == 'IssuesEvent':
            return EventType.ISSUE
        elif event == 'PullRequestEvent':
            return EventType.PULL_REQUEST
        raise Exception('Unknown event type = {}' % event)

    @property
    def security_event(self) -> SecurityEvent:
        self._sec = self._sec or SecurityEvent(
                event_type=self._get_event_type(),
                body=self._payload['url'],
                title=self._payload['url'],
                event_id=str(self._payload['id']),
                created_at=self._created_at(),
                updated_at=self._updated_at(),
                closed_at=self._closed_at()
                )
        return self._sec
