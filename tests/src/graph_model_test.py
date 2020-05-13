"""To test Graph Traversel."""
from src.graph_model import BaseModel, Feedback, FeedBackType
from src.graph_traversel import Traversel
from src.ingestion_data import IngestionData
from src.sanitizer import sanitize


def _get_sample_payload_status_closed():
    return {
                 "api_url": "https://api.github.com/repos/org25/repo10/issues/10",
                 "closed_at": "2020-04-20 15:20:15+00:00",
                 "created_at": "2020-04-01 15:20:15+00:00",
                 "creator_name": "user28",
                 "creator_url": "https://github.com/user28",
                 "event_type": "PULL_REQUEST",
                 "id": 10,
                 "number": 4275,
                 "repo_name": "org25/repo10",
                 "status": "CLOSED",
                 "ecosystem": "KUBEVERT",
                 "updated_at": "2020-04-20 15:20:15+00:00",
                 "url": "https://github.com/org25/repo10/issues/10",
                 "probable_cve": False
            }


def _get_sample_payload_status_opened():
    return {
                 "api_url": "https://api.github.com/repos/org25/repo10/issues/10",
                 "closed_at": None,
                 "created_at": "2020-04-01 15:20:15+00:00",
                 "creator_name": "user28",
                 "creator_url": "https://github.com/user28",
                 "event_type": "PULL_REQUEST",
                 "id": 10,
                 "number": 4275,
                 "repo_name": "org25/repo10",
                 "status": "OPENED",
                 "ecosystem": "KUBEVERT",
                 "updated_at": "2020-04-20 15:20:15+00:00",
                 "url": "https://github.com/org25/repo10/issues/10",
                 "probable_cve": True
            }


def test_empty_traversel():
    """Test empty traversal."""
    g = Traversel('g')
    assert str(g) == 'g'


def test_empty_traversel_with_no_graph():
    """Test empty traversal with no graph."""
    g = Traversel(None)
    assert str(g) == ''


def test_empty_traversel_with_anonymous():
    """Test empty traversal with anonymous."""
    g = Traversel(None).anonymous().addV('hello')
    assert str(g) == "addV('hello')"


def test_and_step():
    """Test and step."""
    g = Traversel('g').addV('hello').and_(Traversel.anonymous().addV('world'))
    assert str(g) == "g.addV('hello').and(addV('world'))"


def test_string_sanitization():
    """Test string sanitization."""
    g = Traversel('g').addV('hello').property(a="a'b")
    assert str(g) == "g.addV('hello').property('a', 'a%27b')"


def test_append_with_traversel_step():
    """Test append with traversel step."""
    g0 = Traversel('g').addV('hello').and_(Traversel.anonymous().addV('world'))
    g1 = Traversel.anonymous().addV('hello').and_(Traversel.anonymous().addV('world'))
    g0.append(g1)
    assert str(g0) == "g.addV('hello').and(addV('world')).addV('hello').and(addV('world'))"


def test_append_with_string_step():
    """Test append with string step."""
    g0 = Traversel('g').addV('hello').and_(Traversel.anonymous().addV('world'))
    g0.append("addV('foo')")
    assert str(g0) == "g.addV('hello').and(addV('world')).addV('foo')"


def test_add_update_unique_node_with_diff_properties_status_closed():
    """Test add/update security node."""
    pcve = IngestionData(_get_sample_payload_status_closed())
    se = pcve.security_event
    g = Traversel()
    g.add_update_unique_node_with_diff_properties(pcve.security_event, pcve.updated_security_event).next()
    import pprint
    pprint.pprint(str(g))
    assert ("g.V().has('url', '{san_url}')"
            ".fold()"
            ".coalesce(unfold()"
            ".property('vertex_label', '{vertex_label}')"
            ".property('status', '{e_status}')"
            ".property('updated_at', {updated_at})"
            ".property('closed_at', {closed_at})"
            ".property('ecosystem', '{e_ecosystem}')"
            ".property('probable_cve', '{probable_cve}')"
            ".property('updated_date', {updated_date})"
            ".property('updated_yearmonth', {updated_yearmonth})"
            ".property('updated_year', {updated_year})"
            ", "
            "addV('security_event')"
            ".property('vertex_label', '{vertex_label}')"
            ".property('event_type', '{e_event_type}')"
            ".property('url', '{san_url}')"
            ".property('api_url', '{san_api_url}')"
            ".property('status', '{e_status}')"
            ".property('event_id', '{event_id}')"
            ".property('created_at', {created_at})"
            ".property('updated_at', {updated_at})"
            ".property('closed_at', {closed_at})"
            ".property('repo_name', '{repo_name}')"
            ".property('repo_path', '{san_repo_path}')"
            ".property('ecosystem', '{e_ecosystem}')"
            ".property('creator_name', '{creator_name}')"
            ".property('creator_url', '{san_creator_url}')"
            ".property('probable_cve', '{probable_cve}')"
            ".property('updated_date', {updated_date})"
            ".property('updated_yearmonth', {updated_yearmonth})"
            ".property('updated_year', {updated_year})"
            ".property('feedback_count', {feedback_count})"
            ".property('overall_feedback', '{e_overall_feedback}')"
            ").next()".format(e_status=se.status.value, e_event_type=se.event_type.value,
                              e_ecosystem=se.ecosystem.value, e_overall_feedback=se.overall_feedback.value,
                              san_url=sanitize(se.url), san_api_url=sanitize(se.api_url),
                              san_creator_url=sanitize(se.creator_url), san_repo_path=sanitize(se.repo_path),
                              **pcve.security_event.__dict__) == str(g))


def test_add_update_unique_node_with_diff_properties_status_opened():
    """Test add/update security node with opended status (closed_at should not come in query)."""
    pcve = IngestionData(_get_sample_payload_status_opened())
    se = pcve.security_event
    g = Traversel()
    g.add_update_unique_node_with_diff_properties(pcve.security_event, pcve.updated_security_event).next()
    import pprint
    pprint.pprint(str(g))
    assert ("g.V().has('url', '{san_url}')"
            ".fold()"
            ".coalesce(unfold()"
            ".property('vertex_label', '{vertex_label}')"
            ".property('status', '{e_status}')"
            ".property('updated_at', {updated_at})"
            ".property('ecosystem', '{e_ecosystem}')"
            ".property('probable_cve', '{probable_cve}')"
            ".property('updated_date', {updated_date})"
            ".property('updated_yearmonth', {updated_yearmonth})"
            ".property('updated_year', {updated_year})"
            ", "
            "addV('security_event')"
            ".property('vertex_label', '{vertex_label}')"
            ".property('event_type', '{e_event_type}')"
            ".property('url', '{san_url}')"
            ".property('api_url', '{san_api_url}')"
            ".property('status', '{e_status}')"
            ".property('event_id', '{event_id}')"
            ".property('created_at', {created_at})"
            ".property('updated_at', {updated_at})"
            ".property('repo_name', '{repo_name}')"
            ".property('repo_path', '{san_repo_path}')"
            ".property('ecosystem', '{e_ecosystem}')"
            ".property('creator_name', '{creator_name}')"
            ".property('creator_url', '{san_creator_url}')"
            ".property('probable_cve', '{probable_cve}')"
            ".property('updated_date', {updated_date})"
            ".property('updated_yearmonth', {updated_yearmonth})"
            ".property('updated_year', {updated_year})"
            ".property('feedback_count', {feedback_count})"
            ".property('overall_feedback', '{e_overall_feedback}')"
            ").next()".format(e_status=se.status.value, e_event_type=se.event_type.value,
                              e_ecosystem=se.ecosystem.value, e_overall_feedback=se.overall_feedback.value,
                              san_url=sanitize(se.url), san_api_url=sanitize(se.api_url),
                              san_creator_url=sanitize(se.creator_url), san_repo_path=sanitize(se.repo_path),
                              **pcve.security_event.__dict__) == str(g))


def test_add_unique_node():
    """Test ad unique node."""
    class Foo(BaseModel):
        vertex_label: str = 'foo'
        foo: str

    g = Traversel('g')
    foo = Foo(foo='bar')
    g.add_unique_node(foo)
    assert ("g.V().has('vertex_label', '{vertex_label}')"
            ".has('foo', '{foo}').fold().coalesce(unfold(), addV('{vertex_label}'))"
            ".property('vertex_label', '{vertex_label}').property('foo', '{foo}')"
            .format(**foo.__dict__) == str(g))


def test_add_with_typed_properties():
    """Test add with typed property."""
    g = Traversel('g')
    g.property(foo=1, bar="1", jazz=1.1)
    assert str(g) == "g.property('foo', 1).property('bar', '1').property('jazz', 1.1)"


def test_property_with_none_value():
    """Test None as property."""
    g = Traversel()
    g.property(a=1, b=None)
    assert str(g) == "g.property('a', 1)"


def test_add_unique_node_with_key():
    """Test ass unique node with key."""
    class Foo(BaseModel):
        vertex_label: str = 'foo'
        primary_key = ('foo', 'bla')
        foo: str
        bar: str

    g = Traversel('g')
    foo = Foo(foo='bar', bar='zoo')
    g.add_unique_node(foo)
    assert ("g.V()"
            ".has('foo', '{foo}').fold().coalesce(unfold(), addV('{vertex_label}'))"
            ".property('vertex_label', '{vertex_label}').property('foo', '{foo}')"
            ".property('bar', '{bar}')".format(**foo.__dict__) == str(g))


def test_drop_out_edge_with_primary_key():
    """Test for drop out edge."""
    g = Traversel()
    feedback = Feedback(author="test", feedback_type=FeedBackType.POSITIVE, comments="test comment",
                        feedback_url="https://api.github.com/repos/org25/repo10/issues/10")
    g.drop_out_edge(feedback)
    assert ("g.V()"
            ".has('author', '{author}')"
            ".has('feedback_url', '{feedback_url}')"
            ".outE().drop().iterate()"
            .format(author=feedback.author, feedback_url=sanitize(feedback.feedback_url)) == str(g))
