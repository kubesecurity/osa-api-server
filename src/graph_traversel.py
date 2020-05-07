"""Abstracts gremlin traversel operations for REST call."""

from enum import Enum
from typing import List

from src.graph_model import (BaseModel, SecurityEvent, Version, Feedback, ReportedCVE)
from src.sanitizer import sanitize


# (fixme): Use GLV + Driver instead of REST based approach
class Traversel:
    """Abstracts gremlin traversel operations for REST call."""

    def __init__(self, name='g'):
        """Create new Traversel based on name."""
        self._query: List[str] = [name] if isinstance(name, str) else []

    @staticmethod
    def anonymous() -> 'Traversel':
        """Create anonymous()Traversel."""
        return Traversel(None)

    def append(self, query) -> 'Traversel':
        """Append new op into list."""
        if isinstance(query, str):
            self._query.append(query)
        elif isinstance(query, Traversel):
            self._query += query._query  # pylint: disable=protected-access
        return self

    def and_(self, step: 'Traversel') -> 'Traversel':
        """Append and step into list."""
        return self.append('and({})'.format(str(step)))

    def as_(self, label: str) -> 'Traversel':
        """Append as step."""
        return self.append("as('{}')".format(label))

    def next(self) -> 'Traversel':
        """Append as next."""
        return self.append('next()')

    def from_(self, as_label) -> 'Traversel':
        """Append as from step based on as_label."""
        return self.append("from('{}')".format(as_label))

    def to(self, as_label) -> 'Traversel':
        """Append as step based on as_label."""
        return self.append("to('{}')".format(as_label))

    def V(self) -> 'Traversel':
        """Append V step for querying."""
        return self.append("V()")

    def query(self) -> List[str]:
        """Return steps as List."""
        return self._query

    def __str__(self) -> str:
        """Convert steps to query."""
        return '.'.join(self._query)

    def addE(self, label_name: str) -> 'Traversel':
        """Create Edge based on label_name."""
        return self.append("addE('{}')".format(label_name))

    def addV(self, label_name: str) -> 'Traversel':
        """Create Vertex based on label_name."""
        return self.append("addV('{}')".format(label_name))

    @staticmethod
    def _value_encoding(val):
        if type(val) in (int, float):  # pylint: disable=unidiomatic-typecheck
            return "{}".format(str(val))
        if isinstance(val, Enum):
            return Traversel._value_encoding(val.value)
        return "'{}'".format(sanitize(str(val)))

    def hasLabel(self, label: str) -> 'Traversel':
        """Add hasLabel step."""
        # (fixme) as of supports one arg
        return self.append("hasLabel('{}')".format(label))

    def has(self, **kwargs) -> 'Traversel':
        """Add has step."""
        return self._props('has', **kwargs)

    def property(self, **kwargs) -> 'Traversel':
        """Use a variable size list of properties to get back a .property() querystring."""
        return self._props('property', **kwargs)

    def _props(self, type_: str, **kwargs) -> 'Traversel':
        for k, v in ((k, v) for (k, v) in kwargs.items() if v is not None):
            self.append("{}('{}', {})".format(type_, str(k), self._value_encoding(v)))
        return self

    def valueMap(self) -> 'Traversel':
        """Valuemap step."""
        return self.append('valueMap()')

    def add_node(self, node: BaseModel) -> 'Traversel':
        """Create node and properties based on the node."""
        kwargs = node.properties
        return self.addV(node.vertex_label).property(**kwargs)

    def has_node(self, node: BaseModel) -> 'Traversel':
        """Check existence of node based on label and its primary_key."""
        # (fixme) Use has(...)
        self.V()
        for k, v in node.properties.items():
            if k not in node.primary_key:
                continue
            self.append("has('{}', {})".format(str(k), self._value_encoding(v)))
        return self

    def add_unique_node(self, node: BaseModel) -> 'Traversel':
        """Create node and properties only if it doesn't exists."""
        # Ref: https://stackoverflow.com/questions/49758417/cosmosdb-graph-upsert-query-pattern
        return (self.append(self.anonymous().has_node(node))
                .append('fold()')
                .append('coalesce(unfold(), {})'.format(
                    self.anonymous().addV(node.vertex_label)))
                .append(self.anonymous().property(**node.properties)))

    def add_update_unique_node_with_diff_properties(self, node: BaseModel, update_node: BaseModel) -> 'Traversel':
        """Create node and property only if not exist else update passed properties."""
        return (self.append(self.anonymous().has_node(node))
                .append('fold()')
                .append('coalesce(unfold().{update_property}, {add_vertex}.{add_property})'.format(
                        update_property=self.anonymous().property(**update_node.properties),
                        add_vertex=self.anonymous().addV(node.vertex_label),
                        add_property=self.anonymous().property(**node.properties)
                        )))

    def _add_edge(self, edge_label: str, from_: BaseModel, to: BaseModel) -> 'Traversel':
        # Reg: https://stackoverflow.com/questions/52447308/add-edge-if-not-exist-using-gremlin
        return (self.append(self.anonymous().has_node(from_))
                .as_(edge_label).has_node(to).append(
                    "coalesce(__.inE('{label}').where(outV().as('{label}')), "
                    "addE('{label}').from('{label}'))"
                    .format(label=edge_label)))

    def _add_edge_with_property(self, edge_label: str, feedback: str, from_: BaseModel, to: BaseModel) -> 'Traversel':
        return (self.append(self.anonymous().has_node(from_))
                .as_(edge_label).has_node(to).append(
                    "coalesce(__.inE('{label}').where(outV().as('{label}')), "
                    "addE('{label}').from('{label}').property('feedback_t','{feedback}'))"
                    .format(label=edge_label, feedback=feedback)))

    def affects(self, from_: ReportedCVE, to: Version) -> 'Traversel':
        """Create affects edge from |from_| to |to| ."""
        return self._add_edge('affects', from_, to)

    def depends_on(self, from_: Version, to: Version) -> 'Traversel':
        """Create depends_on edge from |from_| to |to| ."""
        return self._add_edge('depends_on', from_, to)

    def weakens(self, from_: Feedback, to: SecurityEvent) -> 'Traversel':
        """Create weakens edge from |from_| to |to| ."""
        return self._add_edge('weakens', from_, to)

    def reinforces(self, from_: Feedback, to: SecurityEvent) -> 'Traversel':
        """Create reinforces edge from |from_| to |to| ."""
        return self._add_edge('reinforces', from_, to)

    def drop_out_edge(self, node: BaseModel) -> 'Traversel':
        """Drop out edge based on primary key."""
        self.V()
        for k, v in node.properties.items():
            if k in node.primary_key:
                self.append("has('{}', {})".format(str(k), self._value_encoding(v)))
        self.append("outE().drop().iterate()")
        return self
