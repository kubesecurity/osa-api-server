import src.graph_model import Dependency, Version, Ecosystem, Feedback, ReportedCVE, ProbableCVE

"""
    "ecosystem": "golang",
    "repo_name": "Azure/azure-sdk-for-go",
    "event_type": "IssuesEvent",
    "status": "closed",
    "url": "https://github.com/Azure/azure-sdk-for-go/issues/1204",
    "security_model_flag": 0,
    "cve_model_flag": 0,
    "triage_is_security": 0,
    "triage_is_cve": 0,
    "triage_feedback_comments": "",
    "id": 302919731,
    "number": 1204,
    "api_url": "https://api.github.com/repos/Azure/azure-sdk-for-go/issues/1204",
    "created_at": "2018-03-07 00:27:11+00:00",
    "updated_at": "2019-12-03 09:03:36+00:00",
    "closed_at": "2019-12-03 09:03:36+00:00",
    "creator_name": "vladbarosan",
    "creator_url": "https://github.com/vladbarosan"
"""

class IngestionData:
    def __init__(self, json_data):
        self._payload = json_data

    @property
    def dependency(self) -> Dependency:
        return Dependency(
                dependency_name=self._payload['repo_name'],
                dependency_path=self._payload['url']
                )

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
                event_type=self._get_event_type()
                body='not set'
                title='not set'
                event_id=self._payload['id']
                )
