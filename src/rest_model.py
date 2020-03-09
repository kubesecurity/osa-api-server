"""Abstracts JSON response model declarations """
from flask_restplus import fields, reqparse, inputs
from src.app import api

from src.graph_model import FeedBackType, EventType
from src.parse_datetime import to_date_str, from_date_str
from src.sanitizer import unsanitize

# pylint: disable=no-member,protected-access
POST_PCVE = api.model('PCVE', {
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
    """Abstracts iso8601 string formatting"""
    def format(self, value):
        """Converts given epoch to iso8601 string"""
        return to_date_str(value)

PARSER = reqparse.RequestParser()
PARSER.add_argument('ecosystem', type=str, help='Ecosystem')
PARSER.add_argument('is_probable_cve',
                    type=inputs.boolean,
                    help='Manually triaged as probable vulnerability')
PARSER.add_argument('feedback', type=inputs.boolean, help='Feedback updated true/false')
PARSER.add_argument('from_date', type=from_date_str, help='Updated range - from')
PARSER.add_argument('to_date', type=from_date_str, help='Updated range - to')
PARSER.add_argument('repo', type=str, action='append', help='Repository name')
PARSER.add_argument('event_type', type=str, choices=(EventType._member_names_), help='Event type')

POST_FEEDBACK = api.model('FEEDBACK', {
    'author': fields.String(description='User id of the feedback provider', default='anonymous'),
    'comments': fields.String(attribute=lambda x: unsanitize(x['comments']),
                              description='Feedback text'),
    'url': fields.String(description='Github Issue/PR/Commit absolute(fully qualified) URL'),
    'feedback_type': fields.String(description='Feedback type',
                                   enum=FeedBackType._member_names_),
    'identified_cve': fields.String(description='Actual CVE details if exists')
})

GET_FEEDBACK = api.model('FEEDBACK', {
    'author': fields.String(description='User id of the feedback provider', default='anonymous',
                            attribute=lambda x: x['author'][0]),
    'comments': fields.String(attribute=lambda x: unsanitize(x['comments'][0]),
                              description='Feedback text'),
    'feedback_type': fields.String(description='Feedback type',
                                   attribute=lambda x: x['feedback_type'][0],
                                   enum=FeedBackType._member_names_),
})

GET_PCVE = api.model('GET_PCVE', {
    'ecosystem': fields.String(description='Ecosystem'),
    'repo_name': fields.String(attribute=lambda x: x['dependency']['dependency_name'][0],
                               description='Repository Name'),
    'event_type': fields.String(attribute=lambda x: x['security_event']['event_type'][0],
                                description='Event Type', enum=EventType._member_names_),
    'status': fields.String(attribute=lambda x: x['security_event']['status'][0],
                            description='Status'),
    'url': fields.String(attribute=lambda x: unsanitize(x['security_event']['url'][0]),
                         description='url'),
    'event_id': fields.String(attribute=lambda x: x['security_event']['event_id'][0],
                              description='Event Id from Github'),
    'probable_vuln_id': fields.String(attribute=lambda x: \
                                        x['probable_vulnerability']['probable_vuln_id'][0],
                                      description='Probable vulnerability ID'),
    'created_at': ISO8601Format(attribute=lambda x: x['security_event']['created_at'][0]),
    'updated_at': ISO8601Format(attribute=lambda x: x['security_event']['updated_at'][0]),
    'closed_at': ISO8601Format(attribute=lambda x: x['security_event']['closed_at'][0]),
    'feedback': fields.Nested(GET_FEEDBACK)
})
