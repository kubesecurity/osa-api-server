"""To test Graph Traversel"""
from src.graph_model import BaseModel, Dependency
from src.graph_traversel import Traversel

# pylint: disable=missing-function-docstring, invalid-name,blacklisted-name, missing-class-docstring, too-few-public-methods
def test_empty_traversel():
    g = Traversel('g')
    assert str(g) == 'g'

def test_add_node_dependency_node():
    g = Traversel('g')
    dependency = Dependency(dependency_name='foo', dependency_path='http://foo.bar/zoo.git')
    g.add_node(dependency).next()
    assert(
        "g.addV('{vertex_label}').property('vertex_label', '{vertex_label}')"
        ".property('dependency_name', '{dependency_name}')"
        ".property('dependency_path', '{dependency_path}')"
        ".next()"
        .format(**dependency.__dict__) == str(g)
    )

def test_has_version_traversal():
    g = Traversel('g')
    dependency = Dependency(dependency_name='foo', dependency_path='http://foo.bar/zoo.git')
    g.add_node(dependency).add_node(dependency).has_version(dependency, dependency).next()
    assert(
        "g.addV('{vertex_label}').property('vertex_label', '{vertex_label}')"
        ".property('dependency_name', '{dependency_name}')"
        ".property('dependency_path', '{dependency_path}')"
        ".addV('{vertex_label}').property('vertex_label', '{vertex_label}')"
        ".property('dependency_name', '{dependency_name}')"
        ".property('dependency_path', '{dependency_path}')"
        ".V().hasLabel('{vertex_label}').has('vertex_label', '{vertex_label}')"
        ".has('dependency_name', '{dependency_name}')"
        ".has('dependency_path', '{dependency_path}')"
        ".as('has_version').V().hasLabel('{vertex_label}')"
        ".has('vertex_label', '{vertex_label}')"
        ".has('dependency_name', '{dependency_name}')"
        ".has('dependency_path', '{dependency_path}')"
        ".coalesce(__.inE('has_version').where(outV().as('has_version')), addE('has_version')"
        ".from('has_version')).next()"
        .format(**dependency.__dict__) == str(g)
    )

def test_add_unique_node():
    class Foo(BaseModel):
        vertex_label: str = 'foo'
        foo: str
    g = Traversel('g')
    foo = Foo(foo='bar')
    g.add_unique_node(foo)
    assert(
        "g.V().hasLabel('{vertex_label}').has('vertex_label', '{vertex_label}')"
        ".has('foo', '{foo}').fold().coalesce(unfold(), addV('{vertex_label}'))"
        ".property('vertex_label', '{vertex_label}').property('foo', '{foo}')"
        .format(**foo.__dict__) == str(g)
    )

def test_add_with_typed_properties():
    g = Traversel('g')
    g.property(foo=1, bar="1", jazz=1.1)
    assert str(g) == "g.property('foo', 1).property('bar', '1').property('jazz', 1.1)"

def test_property_with_none_value():
    g = Traversel()
    g.property(a=1, b=None)
    assert str(g) == "g.property('a', 1)"

def test_add_unique_node_with_key():
    class Foo(BaseModel):
        vertex_label: str = 'foo'
        primary_key = ('foo', 'bla')
        foo: str
        bar: str
    g = Traversel('g')
    foo = Foo(foo='bar', bar='zoo')
    g.add_unique_node(foo)
    assert(
        "g.V().hasLabel('{vertex_label}').has('vertex_label', '{vertex_label}')"
        ".has('foo', '{foo}').fold().coalesce(unfold(), addV('{vertex_label}'))"
        ".property('vertex_label', '{vertex_label}').property('foo', '{foo}')"
        ".property('bar', '{bar}')"
        .format(**foo.__dict__) == str(g)
    )
