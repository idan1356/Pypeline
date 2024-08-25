from ..code_execution.code_executor import CodeExecutionStrategy
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class DAGNode:
    node_code: str
    execution_strategy: CodeExecutionStrategy
    next: Optional['DAGNode'] = field(default=None)

    def execute(self):
        return self.execution_strategy.execute_code(self.node_code)


class DAG:
    def __init__(self):
        self.nodes: Dict[str, DAGNode] = {}  # Maps node IDs to DAGNode objects
        self.edges: Dict[str, List[str]] = {}  # Maps node IDs to lists of successor node IDs

    def add_node(self, node_id: str, node: DAGNode):
        if node_id in self.nodes:
            raise ValueError(f"Node with ID {node_id} already exists.")
        self.nodes[node_id] = node
        self.edges[node_id] = []

    def add_edge(self, from_node_id: str, to_node_id: str):
        if from_node_id not in self.nodes or to_node_id not in self.nodes:
            raise ValueError("Both nodes must be added to the graph before adding an edge.")
        self.edges[from_node_id].append(to_node_id)

    def _topological_sort(self) -> List[str]:
        """Returns core topologically sorted list of node IDs."""
        visited = set()
        stack = []
        temp_stack = set()

        def _visit(node_id: str):
            if node_id in temp_stack:
                raise ValueError("Graph is not core DAG (cycle detected)")
            if node_id not in visited:
                temp_stack.add(node_id)
                for neighbor in self.edges[node_id]:
                    _visit(neighbor)
                temp_stack.remove(node_id)
                visited.add(node_id)
                stack.append(node_id)

        for node_id in self.nodes:
            if node_id not in visited:
                _visit(node_id)

        return stack[::-1]  # Reverse to get the correct order

    def execute(self) -> List[object]:
        """Executes all nodes in topologically sorted order and returns their outputs."""
        sorted_nodes = self._topological_sort()
        results = []
        for node_id in sorted_nodes:
            result = self.nodes[node_id].execute()
            results.append(result)
        return results
