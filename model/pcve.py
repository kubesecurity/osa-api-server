from flask_restplus import fields
from app import server

pcve = server.api.model('PCVE', {
    'ecosystem': fields.String(description = 'Ecosystem'),
    'repo_name': fields.String(description='Repository Name'),
    'event_type': fields.String(description='Event Type'),
    'status': fields.String(description = 'Status'),
    'url': fields.Url(description = 'url'),
    'id': fields.String(description = 'Event Id'),
    'number': fields.Integer('PR/Issue number'),
    'api_url': fields.Url(description = 'Github API'),
    'created_at': fields.DateTime(dt_format='rfc822'),
    'updated_at': fields.DateTime(dt_format='rfc822'),
    'closed_at': fields.DateTime(dt_format='rfc822'),
    'creator_name': fields.String,
    'creator_url': fields.Url(description = 'Creator Url'),
})
