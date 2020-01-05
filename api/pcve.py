from flask import Flask
from flask_restplus import Api, Namespace, Resource, fields

from app import server
from model.pcve import pcve
from flask_restplus import reqparse

app, api = server.app, server.api

parser = reqparse.RequestParser()
parser.add_argument('ecosystem', type=str, help='Eco System')
parser.add_argument('isCve', type=bool, help='Is Actually a CVE ?')
parser.add_argument('feedback', type=bool, help='feedback updated true/false')
parser.add_argument('fromDate', type=str, help='From Date')
parser.add_argument('toDate', type=str, help='To Date')
parser.add_argument('repo', type=str, help='Repository Name')
parser.add_argument('eventType', type=str, help='Event Type')

cve_db = [
    {
      "repoName": "grpc/grpc","eventType": "Issues","status": "Open",
      "url": "https://github.com/grpc/grpc/issues/19910",
      "creatorUrl": "https://github.com/jpeel",
      "eventId": "19910"
     },
    {
      "repoName": "grpc/grpc","eventType": "Pull Request","status": "Open",
      "url": "https://github.com/grpc/grpc/issues/198765",
      "creatorUrl": "https://github.com/jmorgan",
      "eventId": "198765"
    },
]

@api.route('/api/v1/pcve')
class Cve(Resource):

    @api.marshal_list_with(pcve)
    @api.param('ecosystem', 'Eco System')
    @api.param('isCve', 'Is Cve Registered - True/False')
    @api.param('feedback', 'Feedback - True/False')
    @api.param('fromDate', 'From Date')
    @api.param('toDate', 'To Date')
    @api.param('repo', 'Repository Name')
    @api.param('eventType', 'Event Type - Pull/Issue/Commit')
    def get(self):
        args = parser.parse_args()
        #you can remove the code below. Just wrote to test if request params are getting passed

        print('query parameter received  ' )
        print(args['ecosystem'])
        for idx, item in enumerate(cve_db):
            item['ecosystem'] = args['ecosystem']
            print('updated item ')
            print(item)
            cve_db[idx] = item
            print('updated cve_db ')
            print(cve_db)
        print('final updated version ')
        print(cve_db)
        return cve_db

    @api.expect(pcve)
    def post(self):
        return 'success'

    @api.expect(pcve)
    @api.marshal_list_with(pcve)
    @api.doc("Api to update the feedback for probable cve. True/False")
    def put(self):

        #update the feedback text
        return api.payload

