"""Abstracts Feedback node creation functionality."""

from src.graph_model import SecurityEvent, Feedback, FeedBackType
from src.graph_traversel import Traversel
from src.gremlin import execute_query
from src.sanitizer import sanitize


def _query_template():
    return '''
            {drop_existing_edge};
            {add_feedback_query};
            {update_security_event};'''


def _update_security_event_template():
    return '''
            result = g.V().has('url','{url}')
            .union(inE().count(), inE().hasLabel('reinforces').count(), inE().hasLabel('weakens').count()).toList();
            g.V().has('url', '{url}')
            .property('feedback_count', result[0])
            .property('overall_feedback', result[1]==result[2] ? 'neutral' :
                (result[2] > result[1] ? 'negative': 'positive'))'''


def _get_feedback_teamplate():
    return '''
            g.V()
            .has('url', '{url}')
            .inE().outV()
            .local(properties().group().by(key()).by(value()))'''


# this step we need to perform as earlier feedback is positive user uploading new feedback with negative
# then earlier 'reinforces' edge we need to delete and then we can add new 'weaken' edge
def _drop_edge_query(feedback_: Feedback):
    return str(Traversel().drop_out_edge(feedback_))


def _add_feedback_query(feedback_: Feedback):
    g = Traversel()

    # create SecurityEvent obj with only url as property, which is enough
    # to find the existing node to add feedback
    security_event = SecurityEvent(url=feedback_.feedback_url)

    g.has_node(security_event).and_(Traversel.anonymous().add_unique_node(feedback_))
    if feedback_.feedback_type is FeedBackType.NEGATIVE:
        g.weakens(feedback_, security_event)
    else:
        g.reinforces(feedback_, security_event)

    return str(g.next())


def _update_security_event(url: str) -> str:
    return _update_security_event_template().format(url=sanitize(url))


def _get_feedback_query(payload) -> str:
    feedback_ = Feedback(author=payload['author'], feedback_type=FeedBackType[payload['feedback_type']],
                         feedback_url=payload['url'], comments=payload['comments'])

    return _query_template().format(drop_existing_edge=_drop_edge_query(feedback_),
                                    add_feedback_query=_add_feedback_query(feedback_),
                                    update_security_event=_update_security_event(payload['url']))


def add_feedback(payload):
    """Create Feedback node into the graphdb based on data."""
    execute_query(_get_feedback_query(payload))
    return {'status': 'success'}


def get_feedback(payload):
    """Get the feedbacks for a given security url."""
    query = _get_feedback_teamplate().format(url=sanitize(payload['url']))
    return execute_query(query)['result']['data']
