from flask_restplus import fields
from app import server

cve = server.api.model('Cve', {
    'repoName': fields.String(description='Repository Name'),
    'eventType': fields.String(description='Event Type'),
    'status': fields.String(description = 'Status'),
    'url': fields.String(description = 'url'),
    'creatorUrl': fields.String(description = 'Creator Url'),
    'eventId': fields.String(description = 'Event Id'),
    'ecosystem': fields.String(description = 'EcoSystem')
})