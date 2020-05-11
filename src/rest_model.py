"""Abstracts JSON response model declarations."""
from flask_restplus import fields, reqparse

from src.app import api
from src.graph_model import FeedBackType, EventType, EcosystemType, StatusType
from src.parse_datetime import to_date_str
from src.sanitizer import unsanitize

POST_PCVE = api.model('PCVE', {
    'ecosystem': fields.String(description='Ecosystem', enum=EcosystemType._member_names_),
    'repo_name': fields.String(description='Repository Name'),
    'event_type': fields.String(description='Event Type', enum=EventType._member_names_),
    'status': fields.String(description='Status', enum=StatusType._member_names_),
    'url': fields.Url(description='url'),
    'id': fields.String(description='Event Id'),
    'number': fields.Integer('PR/Issue number'),
    'api_url': fields.Url(description='Github API'),
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601'),
    'closed_at': fields.DateTime(dt_format='iso8601'),
    'creator_name': fields.String,
    'creator_url': fields.Url(description='Creator Url'),
    'probable_cve': fields.Boolean()
})


class UnsanitizeStringFormat(fields.Raw):
    """Abstract the input string formating."""

    __schema_type__ = 'array'

    def format(self, value):
        """Unsanitizies the input string."""
        return unsanitize(value)


class ISO8601Format(fields.Raw):
    """Abstracts iso8601 string formatting."""

    __schema_type__ = 'string'
    __schema_example__ = '2020-02-23 19:02:15+00:00'

    def format(self, value):
        """Convert given epoch to iso8601 string."""
        return None if value is None else to_date_str(value)


PARSER = reqparse.RequestParser()
PARSER.add_argument('ecosystem', type=str, choices=EcosystemType._member_names_, default="OPENSHIFT", help='Ecosystem')
PARSER.add_argument('updated_yearmonth', type=int, action='append',
                    help='Updated month (yyyyMM format), if not supplied will consider current yearmonth')
PARSER.add_argument('updated_date', type=int, action='append', help='Updated date (yyyyMMdd format)')
PARSER.add_argument('repo', type=str, action='append', help='Repository name')
PARSER.add_argument('feedback', type=str, choices=FeedBackType._member_names_, help='Overall Feedback')
PARSER.add_argument('event_type', type=str, choices=EventType._member_names_, help='Event type')
PARSER.add_argument('status', type=str, choices=StatusType._member_names_, help='Event status')


# had to create a function to overcome linter error
def _check_overall_feedback(x):
    return None if 'overall_feedback' not in x else x['overall_feedback'][0]


GET_PCVE = api.model('GET_PCVE', {
    'ecosystem': fields.List(fields.String, description='Eco system', enum=EcosystemType._member_names_),
    'repo_name': fields.String(attribute=lambda x: x['repo_name'][0], description='Repository Name',
                               example='org14/repo5'),
    'event_type': fields.String(attribute=lambda x: x['event_type'][0], description='Event Type',
                                enum=EventType._member_names_),
    'status': fields.String(attribute=(lambda x: x['status'][0]), description='Status', enum=StatusType._member_names_),
    'url': UnsanitizeStringFormat(attribute=lambda x: x['url'][0],
                                  example='https://github.com/org14/repo5/issues/10742'),
    'event_id': fields.String(attribute=lambda x: x['event_id'][0], description='Event Id from Github'),
    'probable_cve': fields.Boolean(attribute=lambda x: x['probable_cve'][0]),
    'feedback_count': fields.Integer(attribute=lambda x: x['feedback_count'][0],
                                     description='Total received feedback count'),
    'overall_feedback': fields.String(attribute=_check_overall_feedback, description='Overall feddback',
                                      enum=FeedBackType._member_names_),
    'updated_date': fields.Integer(attribute=lambda x: x['updated_date'][0],
                                   description='Updated date (yyyyMMdd format)', example=20200223),
    'created_at': ISO8601Format(attribute=lambda x: x['created_at'][0]),
    'updated_at': ISO8601Format(attribute=lambda x: x['updated_at'][0]),
    'closed_at': ISO8601Format(attribute=lambda x: None if 'closed_at' not in x else x['closed_at'][0]),
    'creator_name': fields.String(attribute=lambda x: x['creator_name'][0], description='Event created by'),
})

FEEDBACK_PARSER = reqparse.RequestParser()
FEEDBACK_PARSER.add_argument('url', type=str, help='Url of the Security event', required=True)

POST_FEEDBACK = api.model('POST_FEEDBACK', {
    'author': fields.String(description='User id of the feedback provider', default='anonymous'),
    'comments': fields.String(description='Feedback text'),
    'url': fields.String(description='Github Issue/PR/Commit absolute(fully qualified) URL'),
    'feedback_type': fields.String(description='Feedback type',
                                   enum=FeedBackType._member_names_)
})

GET_FEEDBACK = api.model('GET_FEEDBACK', {
    'author': fields.String(description='User id of the feedback provider', default='anonymous'),
    'comments': UnsanitizeStringFormat(attribute='comments', example='https://github.com/org14/repo5/issues/10742',
                                       description='Feedback text'),
    'feedback_type': fields.String(description='Feedback type',
                                   enum=FeedBackType._member_names_),
})


POST_GREMLIN = api.model('POST_GREMLIN', {
    'gremlin': fields.String(description='Gremlin query to be passed')
})

POST_GREMLIN = api.model('POST_GREMLIN', {
    'gremlin': fields.String(description='Gremlin query to be passed')
})
