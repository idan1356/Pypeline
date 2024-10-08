from collections import defaultdict, deque
from enum import Enum
from typing import Set, Hashable, DefaultDict, Generator


class CycleError(Exception):
    pass


class DAG:
    class VertexType(Enum):
        WHITE = 0
        GREY = 1
        BLACK = 2

    def __init__(self):
        self._graph: DefaultDict[Hashable, Set[Hashable]] = defaultdict(set)
        self._vertex_predecessors: DefaultDict[Hashable, Set[Hashable]] = defaultdict(set)

    def add_edge(self, from_node_id: Hashable, to_node: Hashable) -> None:
        self._graph[from_node_id].add(to_node)
        self._graph.setdefault(to_node, set())

        self._vertex_predecessors[to_node].add(from_node_id)

    def predecessors(self, vertex: Hashable) -> Set[Hashable]:
        return self._vertex_predecessors.get(vertex, set())

    def has_cycle(self) -> bool:
        vertex_color_dict = {node: self.VertexType.WHITE for node in self._graph}

        def _visit_rec(cur_vertex: Hashable) -> bool:
            vertex_type = vertex_color_dict[cur_vertex]

            if vertex_type == self.VertexType.GREY:
                return True
            elif vertex_type == self.VertexType.BLACK:
                return False

            vertex_color_dict[cur_vertex] = self.VertexType.GREY
            res = any(_visit_rec(neighbor) for neighbor in self._graph[cur_vertex])
            vertex_color_dict[cur_vertex] = self.VertexType.BLACK
            return res

        return any(_visit_rec(node) for node in self._graph if vertex_color_dict[node] == self.VertexType.WHITE)

    def topological_sort(self) -> Generator[Hashable, None, None]:
        in_degree = {node: len(self._vertex_predecessors[node]) for node in self._graph}
        queue = deque(node for node in self._graph if in_degree[node] == 0)

        while queue:
            new_source_node = queue.popleft()

            for neighbor in self._graph[new_source_node]:
                in_degree[neighbor] -= 1

                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

            yield new_source_node

        if any(in_degree[node] != 0 for node in self._graph):
            raise CycleError("A cycle exists in the graph")
