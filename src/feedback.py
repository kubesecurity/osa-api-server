"""Abstracts Feedback node creation functionality."""

from src.graph_model import SecurityEvent, Feedback, FeedBackType
from src.graph_traversel import Traversel
from src.gremlin import execute_query


def feedback(payload):
    """Create Feedback node into the graphdb based on data."""
    # pylint: disable=invalid-name
    g = Traversel()
    # create SecurityEvent obj with only url as property, which is enough
    # to find the existing node to add feedback
    security_event = SecurityEvent(url=payload['url'])
    feedback_ = Feedback(author=payload['author'],
                         feedback_type=FeedBackType[payload['feedback_type']],
                         url=payload['url'],
                         comments=payload['comments'])
    g.has_node(security_event).and_(Traversel.anonymous().add_unique_node(feedback_))
    if feedback_.feedback_type is FeedBackType.NEGATIVE:
        g.weakens(feedback_, security_event)
    else:
        g.reinforces(feedback_, security_event)
    execute_query(g.next())
    return {'status': 'success'}
