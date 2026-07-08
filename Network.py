from typing import Optional
from dataclasses import dataclass, field
from typing import Dict, Tuple
from Edge import Edge
from Node import Node
from ValidationError import ValidationError

@dataclass
class Network:
    nodes: Dict[str, Node]
    edges: Dict[Tuple[str, str], Edge]

    def get_edge(self, from_node: str, to_node: str) -> Edge:
        key = (from_node, to_node)
        if key not in self.edges:
            raise ValidationError(f'Missing edge: {from_node} -> {to_node}')
        return self.edges[key]