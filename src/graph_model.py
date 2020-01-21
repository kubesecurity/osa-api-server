from typing import get_type_hints, Tuple
from src.types import EventType, Severity, FeedBackType

class BaseModel:
    def __init__(self, **kwargs):
        type_hints = get_type_hints(self)
        for k, v in kwargs.items():
            assert type_hints[k] == type(v) or v is None

        self.vertex_label = self.__class__.vertex_label
        self.properties = {'vertex_label': self.vertex_label, **kwargs}
        primary_key = hasattr(self, 'primary_key')
        if primary_key:
            primary_key = ('vertex_label', ) + self.primary_key
        else:
            primary_key = tuple(self.properties.keys())
        assert isinstance(primary_key, tuple)
        self.primary_key = primary_key

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
    primary_key: Tuple[str] = ('author',)
    author: str
    comments: str
    feedback_type: FeedBackType

class Ecosystem(BaseModel):
    vertex_label: str = 'ecosystem'
    ecosystem_name: str

class SecurityEvent(BaseModel):
    vertex_label: str = 'security_event'
    primary_key: Tuple[str] = ('url', )
    event_type: EventType
    body: str
    title: str
    url: str
    status: str
    event_id: str
    created_at: int # iso8601 datetime
    updated_at: int # iso8601 datetime
    closed_at: int # iso8601 datetime
