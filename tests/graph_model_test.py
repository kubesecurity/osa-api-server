import pytest
from src.graph_model import *

def test_empty_traversel():
    g = Traversel('g')
    assert 'g' == str(g)

def test_addV_dependency_node():
    g = Traversel('g')
    dependency = Dependency(dependency_name='foo', dependency_path='http://foo.bar/zoo.git')
    g.addV(dependency).next()
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
    g.addV(dependency).as_('from').addV(dependency).as_('to').has_version('from', 'to').next()
    assert(
        "g.addV('{vertex_label}').property('vertex_label', '{vertex_label}')"
        ".property('dependency_name', '{dependency_name}').property('dependency_path', '{dependency_path}')"
        ".as('from').addV('{vertex_label}').property('vertex_label', '{vertex_label}')"
        ".property('dependency_name', '{dependency_name}').property('dependency_path', '{dependency_path}')"
        ".as('to').addE('has_version').from('from').to('to')"
        ".next()"
        .format(**dependency.__dict__) == str(g)
    )


