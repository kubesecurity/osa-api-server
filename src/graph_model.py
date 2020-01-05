from typing import get_type_hints
from typing import List
from src.types import EventType, Severity, FeedBackType

class BaseModel:
    def __init__(self, **kwargs):
        type_hints = get_type_hints(self)
        for k, v in kwargs.items():
            assert type_hints[k] == type(v)

        self.vertex_label = self.__class__.vertex_label
        self.properties = {'vertex_label': self.vertex_label, **kwargs}
        self.__dict__.update(kwargs)

class Dependency(BaseModel):
    vertex_label: str = 'dependency'
    dependency_name: str
    dependency_path: str

class Version(BaseModel):
    vertex_label: str = 'dependency_version'
    version: str
    dependency_name: str

class ProbableCVE(BaseModel):
    vertex_label: str = 'probable_vulnerability'
    probable_vuln_id: str

class ReportedCVE(BaseModel):
    vertex_label: str = 'reported_cve'
    cve_id: str
    cvss: float
    severity: Severity

class Feedback(BaseModel):
    vertex_label: str = 'feedback'
    body: str
    author: str
    event_id: str
    event_type: EventType
    feedback_type: FeedBackType

class Ecosystem(BaseModel):
    vertex_label: str = 'ecosystem'
    ecosystem_name: str

class SecurityEvent(BaseModel):
    vertex_label: str = 'security_event'
    event_type: EventType
    body: str
    title: str
    event_id: str

class Traversel:
    def __init__(self, name='g'):
        self._query: List[str] = [ name ];

    def append(self, query: str) -> 'Traversel':
        self._query.append(query)
        return self

    def addV(self, node: 'BaseModel') -> 'Traversel':
        kwargs = node.properties
        return self.addVLabel(node.vertex_label).property(**kwargs)

    def as_(self, label: str) -> 'Traversel':
        return self.append("as('{}')".format(label))

    def next(self) -> 'Traversel':
        return self.append('next()')

    def from_(self, as_label) -> 'Traversel':
        return self.append("from('{}')".format(as_label))

    def to(self, as_label) -> 'Traversel':
        return self.append("to('{}')".format(as_label))

    def query(self) -> List[str]:
        return self._query

    def __str__(self) -> str:
        return '.'.join(self._query)

    def addE(self, label_name: str) -> 'Traversel':
        return self.append("addE('{}')".format(label_name))

    def addVLabel(self, label_name: str) -> 'Traversel':
        return self.append("addV('{}')".format(label_name))

    def property(self, **kwargs) -> 'Traversel':
        """Use a variable size list of properties to get back a .property() querystring."""
        for p, val in kwargs.items():
            self.append("property('{}', '{}')".format(str(p), str(val)))
        return self

    def has_version(self, from_: Dependency, to: Version) -> 'Traversel':
        return self.addE('has_version').from_(from_).to(to)

    def triaged_to(self, from_: SecurityEvent, to: ProbableCVE) -> 'Traversel':
        return self.addE('triaged_to').from_(from_).to(to)

    def reported_cve(self, from_: ProbableCVE, to: ReportedCVE) -> 'Traversel':
        return self.addE('reported_cve').from_(from_).to(to)

    def affects(self, from_: ReportedCVE, to: Version) -> 'Traversel':
        return self.addE('reported_cve').from_(from_).to(to)

    def depends_on(self, from_: Version, to: Version) -> 'Traversel':
        return self.addE('depends_on').from_(from_).to(to)

