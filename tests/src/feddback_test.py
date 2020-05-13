"""Testcases for Feddback class."""

from src.feedback import _get_feedback_query
from src.graph_model import FeedBackType
from src.sanitizer import sanitize


def test_add_feedback_test():
    """Test feedback query string."""
    feedback_data = {
        "author": "test",
        "comments": "test comment",
        "url": "https://github.com/spf13/cobra/issues/988",
        "feedback_type": "POSITIVE"
    }
    edge_label = 'reinforces' if feedback_data['feedback_type'] == 'POSITIVE' else 'weakens'

    feedback_query = _get_feedback_query(feedback_data)
    feedback_query_single_line = "".join(feedback_query.replace(" ", "").splitlines())

    expected_query = '''
            g.V().has('author', '{author}').has('feedback_url', '{url}').outE().drop().iterate();
            g.V().has('url', '{url}')
            .and(V().has('author', '{author}').has('feedback_url', '{url}')
            .fold().coalesce(unfold(), addV('feedback')).property('vertex_label', 'feedback')
            .property('author', '{author}').property('feedback_type', '{feedback_type}')
            .property('feedback_url', '{url}').property('comments', '{comments}'))
            .V().has('author', '{author}').has('feedback_url', '{url}').as('reinforces')
            .V().has('url', '{url}').coalesce(__.inE('{edge_label}').where(outV().as('{edge_label}'))
            , addE('{edge_label}').from('{edge_label}')).next();
            result = g.V().has('url','{url}')
            .union(inE().count(), inE().hasLabel('reinforces').count(), inE().hasLabel('weakens').count()).toList();
            g.V().has('url', '{url}')
            .property('feedback_count', result[0])
            .property('overall_feedback', result[1]==result[2] ? 'neutral' :
                (result[2] > result[1] ? 'negative': 'positive'));'''\
        .format(author=feedback_data['author'], comments=sanitize(feedback_data['comments']),
                url=sanitize(feedback_data['url']), edge_label=edge_label, feedback_type=FeedBackType.POSITIVE.value)
    expected_query_single_line = "".join(expected_query.replace(" ", "").splitlines())

    assert(feedback_query_single_line == expected_query_single_line)
