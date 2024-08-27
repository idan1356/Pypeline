from dataclasses import dataclass

import pytest
from typing import Sequence, Tuple, Hashable, Optional, List

from core.workflow.dag import DAG, CycleError


@dataclass
class DAGTestCaseData:
    test_name: str
    edges: List[Tuple[str, str]]
    has_cycle: bool
    topological_sort: Optional[List[List[str]]] = None


simple_dag_data = DAGTestCaseData(
    test_name='simple_dag',
    edges=[('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E')],
    has_cycle=False,
    topological_sort=[['A', 'C', 'B', 'D', 'E'], ['A', 'B', 'C', 'D', 'E']],
)

empty_graph_data = DAGTestCaseData(
    test_name='empty_graph',
    edges=[],
    has_cycle=False,
    topological_sort=[[]]
)

single_edge_dag_data = DAGTestCaseData(
    test_name='single_edge_dag',
    edges=[('A', 'B')],
    has_cycle=False,
    topological_sort=[['A', 'B']]
)


disjointed_dag_data = DAGTestCaseData(
    test_name='disjointed_dag',
    edges=[('A', 'B'), ('C', 'D')],
    has_cycle=False,
    topological_sort=[['A', 'B', 'C', 'D'], ['A', 'C', 'B', 'D'], ['A', 'C', 'D', 'B'],
                      ['C', 'D', 'A', 'B'], ['C', 'A', 'D', 'B'], ['C', 'A', 'B', 'D']]
)

multi_source_dag_data = DAGTestCaseData(
    test_name='multi_source_dag',
    edges=[('A', 'C'), ('B', 'C'), ('C', 'D')],
    has_cycle=False,
    topological_sort=[['A', 'B', 'C', 'D'], ['B', 'A', 'C', 'D']]
)

complex_dag_data = DAGTestCaseData(
    test_name='complex_dag',
    edges=[('A', 'C'), ('B', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'F'),
           ('E', 'F'), ('E', 'G'), ('F', 'H'), ('G', 'H')],
    has_cycle=False,
    topological_sort=[
        ['A', 'B', 'D', 'C', 'E', 'G', 'F', 'H'],
        ['A', 'B', 'D', 'C', 'E', 'F', 'G', 'H'],
        ['A', 'B', 'C', 'D', 'E', 'G', 'F', 'H'],
        ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
        ['B', 'A', 'D', 'C', 'E', 'G', 'F', 'H'],
        ['B', 'A', 'D', 'C', 'E', 'F', 'G', 'H'],
        ['B', 'A', 'C', 'D', 'E', 'G', 'F', 'H'],
        ['B', 'A', 'C', 'D', 'E', 'F', 'G', 'H'],
        ['B', 'D', 'A', 'C', 'E', 'G', 'F', 'H'],
        ['B', 'D', 'A', 'C', 'E', 'F', 'G', 'H'],
        ['B', 'D', 'C', 'A', 'E', 'G', 'F', 'H'],
        ['B', 'D', 'C', 'A', 'E', 'F', 'G', 'H'],
        ['A', 'B', 'C', 'E', 'D', 'G', 'F', 'H'],
        ['A', 'B', 'C', 'E', 'D', 'F', 'G', 'H'],
        ['B', 'A', 'C', 'E', 'D', 'G', 'F', 'H'],
        ['B', 'A', 'C', 'E', 'D', 'F', 'G', 'H']
    ]
)

simple_cycle_data = DAGTestCaseData(
    test_name='simple_cycle',
    edges=[('A', 'B'), ('B', 'C'), ('C', 'A')],
    has_cycle=True
)

complex_cycle_data = DAGTestCaseData(
    test_name='complex_cycle',
    edges=[('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'B')],
    has_cycle=True
)

self_loop_data = DAGTestCaseData(
    test_name='self_loop',
    edges=[('A', 'A')],
    has_cycle=True
)


all_test_data = [simple_dag_data, single_edge_dag_data, disjointed_dag_data, multi_source_dag_data,
                 complex_dag_data, simple_cycle_data, complex_cycle_data, self_loop_data, empty_graph_data]


@pytest.fixture
def dag_factory():
    def _create_dag(edges: Optional[Sequence[Tuple[Hashable, Hashable]]]) -> DAG:
        dag = DAG()

        if edges:
            for from_node, to_node in edges:
                dag.add_edge(from_node, to_node)
        return dag

    return _create_dag


@pytest.fixture
def sample_dag():
    dag = DAG()
    dag.add_edge('A', 'B')
    dag.add_edge('A', 'C')
    dag.add_edge('B', 'D')
    dag.add_edge('C', 'D')
    dag.add_edge('D', 'E')
    return dag


def test_add_edge_creates_vertices(sample_dag):
    for char in ['A', 'B', 'C', 'D', 'E']:
        assert char in sample_dag._graph


def test_add_edge_increases_in_degree(dag_factory):
    new_dag = dag_factory(None)
    new_dag.add_edge('A', 'B')
    assert new_dag._in_degree('A') == 0
    assert new_dag._in_degree('B') == 1
    new_dag.add_edge('A', 'C')
    new_dag.add_edge('B', 'C')
    assert new_dag._in_degree('A') == 0
    assert new_dag._in_degree('B') == 1
    assert new_dag._in_degree('C') == 2


def test_add_edge_handles_new_nodes(dag_factory):
    dag = dag_factory(None)
    dag.add_edge('X', 'Y')
    assert 'X' in dag._graph
    assert 'Y' in dag._graph


@pytest.mark.parametrize("test_data", all_test_data)
def test_dag_has_cycle(dag_factory, test_data):
    dag = dag_factory(test_data.edges)
    assert dag.has_cycle() == test_data.has_cycle


@pytest.mark.parametrize("test_data", filter(lambda test_case: not test_case.has_cycle, all_test_data))
def test_topological_sort_acyclic_graphs(dag_factory, test_data):
    dag = dag_factory(test_data.edges)
    topological_sort = list(dag._topological_sort_generator())
    assert topological_sort in test_data.topological_sort


@pytest.mark.parametrize("test_data", filter(lambda test_case: test_case.has_cycle, all_test_data))
def test_topological_sort_with_cycle_raises_error(dag_factory, test_data):
    dag = dag_factory(test_data.edges)
    with pytest.raises(CycleError):
        list(dag._topological_sort_generator())
