from flask_restplus import fields
from app import server

from src.types import FeedBackType
from src.parse_datetime import to_date_str

POST_PCVE = server.api.model('PCVE', {
    'ecosystem': fields.String(description='Ecosystem'),
    'repo_name': fields.String(description='Repository Name'),
    'event_type': fields.String(description='Event Type'),
    'status': fields.String(description='Status'),
    'url': fields.Url(description='url'),
    'id': fields.String(description='Event Id'),
    'number': fields.Integer('PR/Issue number'),
    'api_url': fields.Url(description='Github API'),
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601'),
    'closed_at': fields.DateTime(dt_format='iso8601'),
    'creator_name': fields.String,
    'creator_url': fields.Url(description='Creator Url'),
})

class ISO8601Format(fields.Raw):
    def format(self, value):
        return to_date_str(value)

GET_PCVE = server.api.model('GET_PCVE', {
    'ecosystem': fields.String(description='Ecosystem'),
    'repo_name': fields.String(attribute='dependency.dependency_name', description='Repository Name'),
    'event_type': fields.String(attribute='security_event.event_type', description='Event Type'),
    'status': fields.String(attribute='security_event.status', description='Status'),
    'url': fields.String(attribute='security_event.url', description='url'),
    'probable_vuln_id': fields.String(attribute='probable_vulnerability.probable_vuln_id', description='Event Id'),
    'created_at': ISO8601Format(attribute='security_event.created_at'),
    'updated_at': ISO8601Format(attribute='security_event.updated_at'),
    'closed_at': ISO8601Format(attribute='security_event.closed_at'),
})

PUT_FEEDBACK = server.api.model('FEEDBACK', {
    'feedback': fields.String(description='Feedback type', enum=FeedBackType._member_names_),
    'identified_cve': fields.String(description='Actual CVE details if exists')
})
