import re
from src.graph_model import Dependency, Version, Ecosystem, Feedback, ReportedCVE, ProbableCVE, SecurityEvent
from src.types import *

class IngestionData:
    _URL_PATTERN = re.compile(r'[:/]+')

    def __init__(self, json_data):
        self._payload = json_data

    @property
    def dependency(self) -> Dependency:
        return Dependency(
                dependency_name=self._payload['repo_name'],
                dependency_path=self._get_dependency_path()
                )

    def _get_dependency_path(self):
        components = self._URL_PATTERN.split(self._payload['url'])
        return '%s://%s/%s/%s' % (components[0], components[1], components[2] , components[3])

    @property
    def version(self) -> Version:
        return Version(
                version=self._payload['created_at'],
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
        return SecurityEvent(
                event_type=self._get_event_type(),
                body=self._payload['url'],
                title=self._payload['url'],
                event_id=str(self._payload['id'])
                )
