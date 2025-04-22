# TODO 0 pipem nainstalovat
# https://github.com/JakubSido/adthelpers

# pip install git+https://github.com/JakubSido/adthelpers
# nebo stáhnout zip a instalovat jako pip install <cesta_k_rozbalenému_zipu>


import json
from queue import PriorityQueue

import adthelpers


class Graph:
    def __init__(self) -> None:
        self.edges: dict[int, list[tuple[float, int]]] = {}

    def add_edge(self, src: int, dst: int, weight: float = 0) -> None:
        # TODO 1 napište kód přidání hrany do datové struktury grafu
        
        if src not in self.edges:
            self.edges[src] = []
        if dst not in self.edges:
            self.edges[dst] = []

        self.edges[src].append((weight, dst))
        self.edges[dst].append((weight, src))
        


def load_graph(filename: str) -> Graph:
    graph = Graph()

    # TODO 2 vytvořte graf podle dat ze souboru
    
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)

    for edge in data["links"]:
        node1, node2 = edge["source"], edge["target"]
        graph.add_edge(node1, node2, edge["weight"])
    

    return graph


def load_graph_csv(filename: str) -> Graph:
    graph = Graph()

    # TODO 2 vytvořte graf podle dat ze souboru
    
    with open(filename, encoding="utf-8") as f:
        # skip line
        f.readline()
        for line in f:
            line = line.strip()
            if not line:
                continue
            node1, node2, weight = line.split(",")
            node1, node2, weight = int(node1), int(node2), float(weight)
            graph.add_edge(node1, node2, weight)

    

    return graph


def spanning_tree(graph: Graph) -> None:
    closed: set[int] = set()
    sp_tree: list[tuple[int, int]] = []
    queue: PriorityQueue = PriorityQueue()

    painter = adthelpers.painter.Painter(
        graph,
        visible=queue,
        closed=closed,
        color_edges=sp_tree,
    )
    painter.draw_graph()

    # TODO 3 Implementujte Prim-Jarníkův algoritmus pro nalezení minimální kostry
    
    queue.put((0, (-1, 0)))  # enter the graph -> weight=0, source=-1, target=0

    while not queue.empty() and len(closed) != len(graph.edges):
        # get the edge to add to the spanning tree
        weight, (source, actual) = queue.get()

        # if it is indeed a new node, add it to the spanning tree
        if actual in closed:
            continue

        closed.add(actual)

        if source >= 0:  # source could be -1 for the virtual entrance node
            sp_tree.append((source, actual))


        # add all newly accessible edges to the queue
        for weight, neighbor in graph.edges[actual]:
            if neighbor not in closed:
                queue.put((weight, (actual, neighbor)))
                painter.draw_graph(actual)  # show discovered node

        painter.draw_graph(actual) # show actual spanning tree
    


def reconstruct_path(predecessors: dict[int, int], start_id: int, end_id: int) -> list[int]:
    path = []
    
    current = end_id
    while current != start_id:
        path.append(current)
        current = predecessors[current]
    path.append(start_id)
    path.reverse()
    
    return path



def main() -> None:
    graph = load_graph("09-spanning-tree/data/graph_grid_s3_3.json")

    painter = adthelpers.painter.Painter(
        graph,
        # colors=("red", "blue", "yellow", "grey") # pokud by byl problém s barvami je možné je změnit
    )
    painter.draw_graph()

    # debug to see progress...
    # spanning_tree(graph)


    # don't close before user acknowledges diagrams
    input("Press enter to exit program...")


if __name__ == "__main__":
    main()

