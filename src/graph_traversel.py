"""Abstracts gremlin traversel operations for REST call"""

from enum import Enum
from typing import List
from src.graph_model import (BaseModel, SecurityEvent, Dependency, Version,
                             Feedback, ReportedCVE, ProbableCVE)

#(fixme): Use GLV + Driver instead of REST based approach
class Traversel:
    """Abstracts gremlin traversel operations for REST call"""
    # pylint: disable=invalid-name,too-many-public-methods
    def __init__(self, name='g'):
        """Create new Traversel based on name"""
        self._query: List[str] = [name] if isinstance(name, str) else []

    def append(self, query: str) -> 'Traversel':
        """Appends new op into list"""
        self._query.append(query)
        return self

    def as_(self, label: str) -> 'Traversel':
        """Append as step"""
        return self.append("as('{}')".format(label))

    def next(self) -> 'Traversel':
        """Append as next"""
        return self.append('next()')

    def from_(self, as_label) -> 'Traversel':
        """Append as from step based on as_label"""
        return self.append("from('{}')".format(as_label))

    def to(self, as_label) -> 'Traversel':
        """Append as step based on as_label"""
        return self.append("to('{}')".format(as_label))

    def V(self) -> 'Traversel':
        """Append V step for querying"""
        return self.append("V()")

    def query(self) -> List[str]:
        """Returns steps as List"""
        return self._query

    def __str__(self) -> str:
        """Converts steps to query"""
        return '.'.join(self._query)

    def addE(self, label_name: str) -> 'Traversel':
        """Creates Edge based on label_name"""
        return self.append("addE('{}')".format(label_name))

    def addV(self, label_name: str) -> 'Traversel':
        """Creates Vertex based on label_name"""
        return self.append("addV('{}')".format(label_name))

    @staticmethod
    def _value_encoding(val):
        if type(val) in (int, float): # pylint: disable=unidiomatic-typecheck
            return "{}".format(str(val))
        if isinstance(val, Enum):
            return Traversel._value_encoding(val.value)
        return "'{}'".format(str(val))

    def hasLabel(self, label: str) -> 'Traversel':
        """Add hasLabel step"""
        # (fixme) as of supports one arg
        return self.append("hasLabel('{}')".format(label))

    def has(self, **kwargs) -> 'Traversel':
        """Add has step"""
        return self._props('has', **kwargs)

    def property(self, **kwargs) -> 'Traversel':
        """Use a variable size list of properties to get back a .property() querystring."""
        return self._props('property', **kwargs)

    def _props(self, type_: str, **kwargs) -> 'Traversel':
        for k, v in ((k, v) for (k, v) in kwargs.items() if v is not None):
            self.append("{}('{}', {})".format(type_, str(k), self._value_encoding(v)))
        return self

    def valueMap(self) -> 'Traversel':
        """ValueMap step"""
        return self.append('valueMap()')

    def add_node(self, node: BaseModel) -> 'Traversel':
        """Create node and properties based on the node"""
        kwargs = node.properties
        return self.addV(node.vertex_label).property(**kwargs)

    def has_node(self, node: BaseModel) -> 'Traversel':
        """Check existence of node based on label and its primary_key"""
        # (fixme) Use has(...)
        self.V().hasLabel(node.vertex_label)
        for k, v in node.properties.items():
            if k not in node.primary_key:
                continue
            self.append("has('{}', {})".format(str(k), self._value_encoding(v)))
        return self

    def add_unique_node(self, node: BaseModel) -> 'Traversel':
        """Create node and properties only if it doesn't exists"""
        # Ref: https://stackoverflow.com/questions/49758417/cosmosdb-graph-upsert-query-pattern
        g_create_node = Traversel(None).addV(node.vertex_label)
        g_check_node_existence = Traversel(None).has_node(node)
        g_update_properties = Traversel(None).property(**node.properties)
        return (self.append(str(g_check_node_existence))
                .append('fold()')
                .append('coalesce(unfold(), {})'.format(str(g_create_node)))
                .append(str(g_update_properties)))

    def _add_edge(self, edge_label: str, from_: BaseModel, to: BaseModel) -> 'Traversel':
        # Reg: https://stackoverflow.com/questions/52447308/add-edge-if-not-exist-using-gremlin
        g = Traversel(None)
        g.has_node(from_).as_(edge_label).has_node(to).append(
            "coalesce(__.inE('{label}').where(outV().as('{label}')), "
            "addE('{label}').from('{label}'))"
            .format(label=edge_label))
        return self.append(str(g))

    def has_version(self, from_: Dependency, to: Version) -> 'Traversel':
        """Create has_version edge from |from_| to |to|"""
        return self._add_edge('has_version', from_, to)

    def triaged_to(self, from_: SecurityEvent, to: ProbableCVE) -> 'Traversel':
        """Create triaged_to edge from |from_| to |to|"""
        return self._add_edge('triaged_to', from_, to)

    def reported_cve(self, from_: ProbableCVE, to: ReportedCVE) -> 'Traversel':
        """Create reported_cve edge from |from_| to |to|"""
        return self._add_edge('reported_cve', from_, to)

    def affects(self, from_: ReportedCVE, to: Version) -> 'Traversel':
        """Create affects edge from |from_| to |to|"""
        return self._add_edge('affects', from_, to)

    def depends_on(self, from_: Version, to: Version) -> 'Traversel':
        """Create depends_on edge from |from_| to |to|"""
        return self._add_edge('depends_on', from_, to)

    def weakens(self, from_: Feedback, to: SecurityEvent) -> 'Traversel':
        """Create weakens edge from |from_| to |to|"""
        return self._add_edge('weakens', from_, to)

    def reinforces(self, from_: Feedback, to: SecurityEvent) -> 'Traversel':
        """Create reinforces edge from |from_| to |to|"""
        return self._add_edge('reinforces', from_, to)
