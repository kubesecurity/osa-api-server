from typing import get_type_hints, List
from src.types import EventType, Severity, FeedBackType

class BaseModel:
    def __init__(self, **kwargs):
        type_hints = get_type_hints(self)
        for k, v in kwargs.items():
            assert type_hints[k] == type(v) or v is None

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
    created_at: int # iso8601 datetime
    updated_at: int # iso8601 datetime
    closed_at: int # iso8601 datetime


class Traversel:
    def __init__(self, name='g'):
        self._query: List[str] = [name] if type(name) is str else [];

    def append(self, query: str) -> 'Traversel':
        self._query.append(query)
        return self

    def as_(self, label: str) -> 'Traversel':
        return self.append("as('{}')".format(label))

    def next(self) -> 'Traversel':
        return self.append('next()')

    def from_(self, as_label) -> 'Traversel':
        return self.append("from('{}')".format(as_label))

    def to(self, as_label) -> 'Traversel':
        return self.append("to('{}')".format(as_label))

    def V(self) -> 'Traversel':
        return self.append("V()")

    def query(self) -> List[str]:
        return self._query

    def __str__(self) -> str:
        return '.'.join(self._query)

    def addE(self, label_name: str) -> 'Traversel':
        return self.append("addE('{}')".format(label_name))

    def addV(self, label_name: str) -> 'Traversel':
        return self.append("addV('{}')".format(label_name))

    @staticmethod
    def _value_encoding(val):
        if type(val) in (int, float):
            return "{}".format(str(val))
        else:
            return "'{}'".format(str(val))

    def hasLabel(self, label: str) -> 'Traversel':
        # (fixme) as of supports one arg
        return self.append("hasLabel('{}')".format(label))

    def has(self, **kwargs) -> 'Traversel':
        return self._props('has', **kwargs)

    def property(self, **kwargs) -> 'Traversel':
        """Use a variable size list of properties to get back a .property() querystring."""
        return self._props('property', **kwargs)

    def add_node(self, node: BaseModel) -> 'Traversel':
        kwargs = node.properties
        return self.addV(node.vertex_label).property(**kwargs)

    def _props(self, type_: str, **kwargs) -> 'Traversel':
        for k, v in ((k, v) for (k, v) in kwargs.items() if v is not None):
            self.append("{}('{}', {})".format(type_, str(k), self._value_encoding(v)))
        return self

    def valueMap(self) -> 'Traversel':
        return self.append('valueMap()')

    def has_node(self, node: BaseModel, *props: str) -> 'Traversel':
        # (fixme) Use has(...)
        props = None if len(props) is 0 else props
        self.V().hasLabel(node.vertex_label)
        for k, v in node.properties.items():
            if props is not None and k not in props or v is None:
                continue
            self.append("has('{}', {})".format(str(k), self._value_encoding(v)))
        return self

    def add_unique_node(self, node: BaseModel, *props: str) -> 'Traversel':
        # Reference: https://stackoverflow.com/questions/49758417/cosmosdb-graph-upsert-query-pattern
        g0 = Traversel(None).addV(node.vertex_label)
        g1 = Traversel(None).has_node(node, *props)
        g2 = Traversel(None).property(**node.properties)
        return self.append(str(g1)).append('fold()').append('coalesce(unfold(), {})'.format(str(g0))).append(str(g2))

    def _add_edge(self, edge_label: str, from_: BaseModel, to: BaseModel) -> 'Traversel':
        # Reference: https://stackoverflow.com/questions/52447308/add-edge-if-not-exist-using-gremlin
        g = Traversel(None)
        g.has_node(from_).as_(edge_label).has_node(to).append(
                "coalesce(__.inE('{label}').where(outV().as('{label}')), addE('{label}').from('{label}'))".format(label=edge_label))
        return self.append(str(g))

    def has_version(self, from_: Dependency, to: Version) -> 'Traversel':
        return self._add_edge('has_version', from_, to)

    def triaged_to(self, from_: SecurityEvent, to: ProbableCVE) -> 'Traversel':
        return self._add_edge('triaged_to', from_, to)

    def reported_cve(self, from_: ProbableCVE, to: ReportedCVE) -> 'Traversel':
        return self._add_edge('reported_cve', from_, to)

    def affects(self, from_: ReportedCVE, to: Version) -> 'Traversel':
        return self._add_edge('affects', from_, to)

    def depends_on(self, from_: Version, to: Version) -> 'Traversel':
        return self._add_edge('depends_on', from_, to)

