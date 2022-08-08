from typing import List
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import math


def generate_tsp_instance(n_nodes: int = 20, radius: float = 1.0) -> nx.Graph:
    """Generate TSP instance."""
    graph: nx.Graph = nx.random_geometric_graph(n_nodes, radius=radius)
    pos = nx.get_node_attributes(graph, "pos")

    # calculating distance between nodes.
    for i in range(len(pos)):
        for j in range(i + 1, len(pos)):
            distance = math.hypot(pos[i][0] - pos[j][0], pos[i][1] - pos[j][1])
            graph.add_edge(i, j, weight=distance)

    return graph


def visualize_tsp_instance(graph: nx.Graph) -> None:
    """Visualize tsp instance."""
    nx.draw(graph)
    plt.draw()
    plt.title("TSP Problem")
    plt.savefig("test.png")


def visualize_tsp_solution(graph: nx.Graph, path: List[int], fitness: float) -> None:
    """Visualie tsp instance and its solution."""
    pos = np.array([ele for ele in nx.get_node_attributes(graph, "pos").values()])
    plt.scatter(pos[:, 0], pos[:, 1])
    for i in range(len(pos) - 1):
        start_idx, end_idx = path[i], path[i + 1]
        start_pos, end_pos = pos[start_idx], pos[end_idx]
        plt.arrow(
            start_pos[0],
            start_pos[1],
            end_pos[0] - start_pos[0],
            end_pos[1] - start_pos[1],
            width=0.008,
            length_includes_head=True,
        )
    start_idx = path[0]
    plt.arrow(
        pos[end_idx][0],
        pos[end_idx][1],
        pos[start_idx][0] - pos[end_idx][0],
        pos[start_idx][1] - pos[end_idx][1],
        width=0.008,
        length_includes_head=True,
    )
    plt.title(f"{fitness:.3f}")
    plt.savefig("test.png")


def timer(fn):
    from time import perf_counter

    def inner(*args, **kwargs):
        start_time = perf_counter()
        to_execute = fn(*args, **kwargs)
        end_time = perf_counter()
        execution_time = end_time - start_time
        print("{0} took {1:.8f}s to execute".format(fn.__name__, execution_time))
        return to_execute

    return inner


if __name__ == "__main__":
    graph = generate_tsp_instance()
    visualize_tsp_instance(graph)
