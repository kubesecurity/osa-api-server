"""Contains type definitions for the data model."""
from enum import Enum
from typing import get_type_hints, Tuple


class EcosystemType(Enum):
    """Define the ecosystem that security event is part of."""

    OPENSHIFT = "openshift"
    KNATIVE = "knative"
    KUBEVERT = "kubevert"


class StatusType(Enum):
    """Define the status of event."""

    OPENED = "opened"
    CLOSED = "closed"
    REOPENED = "reopened"
    OTHER = "other"


class EventType(Enum):
    """Define the eventtype type, possible values: ISSUE/PULL_REQUEST/COMMIT."""

    ISSUE = "ISSUE"
    PULL_REQUEST = "PULL_REQUEST"
    COMMIT = "COMMIT"
    # (fixme) It has to be removed once ingestion data is corrected
    IssuesEvent = ISSUE
    PullRequestEvent = PULL_REQUEST


class Severity(Enum):
    """Denote the severity of an identified CVE."""

    HIGH = "high"
    LOW = "low"
    MODERATE = "moderate"


class FeedBackType(Enum):
    """Denote the type of feedback(POSITIVE/NEGATIVE)."""

    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    NONE = "none"


# pylint: disable=too-few-public-methods
# (fixme): Why not pydantic?
class BaseModel:
    """Base class for all model objects."""

    def __init__(self, **kwargs):
        """Create graph model object based on kwargs and ensure its type."""
        type_hints = get_type_hints(self)
        for k, v in kwargs.items():  # pylint: disable=invalid-name
            assert type_hints[k] == type(v) or v is None, (
                'hint for "{}" is {}, actual {}'.format(k, type_hints[k], type(v)))

        self.vertex_label = self.__class__.vertex_label  # pylint: disable=no-member

        self.properties = {'vertex_label': self.vertex_label, **kwargs}
        primary_key = hasattr(self, 'primary_key')
        if primary_key:
            primary_key = self.primary_key  # pylint: disable=no-member,
            # access-member-before-definition
        else:
            primary_key = tuple(self.properties.keys())
        assert isinstance(primary_key, tuple)
        self.primary_key = primary_key

        self.__dict__.update(kwargs)


class Version(BaseModel):
    """Model description for Version."""

    vertex_label: str = 'dependency_version'
    version: str
    dependency_name: str


class ReportedCVE(BaseModel):
    """Model description for ReportedCVE."""

    vertex_label: str = 'reported_cve'
    cve_id: str
    cvss: float
    severity: Severity


class Feedback(BaseModel):
    """Model description for Feedback."""

    vertex_label: str = 'feedback'
    primary_key: Tuple[str] = ('feedback_url', 'author',)
    author: str
    comments: str
    feedback_type: FeedBackType
    feedback_url: str


class SecurityEvent(BaseModel):
    """Model description for SecurityEvent."""

    vertex_label: str = 'security_event'
    primary_key: Tuple[str] = ('url', )
    event_type: EventType
    url: str
    api_url: str
    status: StatusType
    event_id: str
    created_at: int  # iso8601 datetime
    updated_at: int  # iso8601 datetime
    closed_at: int  # iso8601 datetime
    repo_name: str
    repo_path: str
    ecosystem: EcosystemType
    probable_cve: bool
    overall_feedback: FeedBackType
    feedback_count: int
    creator_name: str
    creator_url: str
    updated_date: int  # yyyyMMdd format
    updated_yearmonth: int  # yyyyMM format
    updated_year: int  # yyyy format
