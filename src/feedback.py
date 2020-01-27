"""Abstracts Feedback node creation functionality """

from src.graph_model import SecurityEvent, Feedback, FeedBackType
from src.graph_traversel import Traversel
from src.gremlin import execute_query

def _ingest_feedback(payload):
    """Creates Feedback node into the graphdb based on data"""
    # pylint: disable=invalid-name
    g = Traversel()
    # create SecurityEvent obj with only url as property, which is enough
    # to find the existing node to add feedback
    security_event = SecurityEvent(url=payload['url'])
    feedback_ = Feedback(author=payload['author'],
                         feedback_type=FeedBackType[payload['feedback_type']],
                         comments=payload['comments'])
    g.has_node(security_event).add_unique_node(feedback_)
    if feedback_.feedback_type is FeedBackType.NEGATIVE:
        g.weakens(feedback_, security_event)
    else:
        g.reinforces(feedback_, security_event)
    return execute_query(g.next())

def feedback(data):
    """Creates Feedback nodes into the graphdb based on data"""
    for payload in data:
        _ingest_feedback(payload)
    return {'status': 'success'}
