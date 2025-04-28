# TODO 0 pipem nainstalovat
# https://github.com/JakubSido/adthelpers

# pip install git+https://github.com/JakubSido/adthelpers
# nebo stáhnout zip a instalovat jako pip install <cesta_k_rozbalenému_zipu>

import json
from queue import PriorityQueue
from tqdm import tqdm
import adthelpers

import plotly.express as px

class Graph:
    def __init__(self, oriented: bool = False) -> None:
        self.edges: dict[int, list[tuple[float, int]]] = {}
        self.oriented = oriented
        self.edge_count = 0

    def add_edge(self, src: int, dst: int, weight: float = 0) -> None:
        if src not in self.edges:
            self.edges[src] = []
        self.edges[src].append((weight, dst))
        
        if self.oriented:
            return
        
        if dst not in self.edges:
            self.edges[dst] = []
        self.edges[dst].append((weight, src))


    def dijkstra(
        self, start_id: int, end_id: int, show_progress: bool = True,
    ) -> tuple[dict[int, float], dict[int, int]]:
        closed: set[int] = set()
        sp_tree: list[tuple[int, int]] = []
        queue: PriorityQueue = PriorityQueue()

        # navíc
        distances: dict[int, float] = dict()
        predecessors: dict[int, int] = dict()

        if show_progress:
            painter = adthelpers.painter.Painter(
                self,
                visible=queue,
                closed=closed,
                color_edges=sp_tree,
                distances=distances,  # navic
            )
            painter.draw_graph()

        # TODO 1 Implementujte Dijkstrův algoritmus pro nalezení nejkratší cesty
        
        for n in self.edges:
            distances[n] = float("inf")
            predecessors[n] = -1
        # navic
        distances[start_id] = 0

        queue.put((0, (-1, start_id)))  # enter the graph -> weight=0, source=-1, target=0

        while not queue.empty():
            weight, (source, actual) = queue.get()
            if actual == end_id:
                break
            if actual in closed:
                continue
            closed.add(actual)

            # add all newly accessible edges to the queue
            for weight, neighbor in self.edges[actual]:
                if neighbor not in closed:
                    # navic
                    new_distance = distances[actual] + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        predecessors[neighbor] = actual

                    queue.put((new_distance, (actual, neighbor)))

                    if show_progress: 
                        painter.draw_graph(actual)  # show discovered node

        

        return distances, predecessors

def load_graph(filename: str) -> Graph:
    graph = Graph(oriented=False)

    with open(filename, encoding="utf-8") as f:
        data = json.load(f)

    for edge in data["links"]:
        node1, node2 = edge["source"], edge["target"]
        graph.add_edge(node1, node2, edge["weight"])

    return graph


def load_graph_csv(filename: str) -> Graph:
    graph = Graph(oriented=True)

    # TODO 3 Načtěte graf z CSV souboru
    
    with open(filename, encoding="utf-8") as f:
        # skip line
        f.readline()
        for line in tqdm(f):
            line = line.strip()
            if not line:
                continue
            node1, node2, weight = line.split(",")
            node1, node2, weight = int(node1), int(node2), float(weight)
            graph.add_edge(node1, node2, weight)

    
    return graph

def reconstruct_path(
    predecessors: dict[int, int], start_id: int, end_id: int,
) -> list[int]:
    path = []
    ## TODO 2 Implementujte funkci pro rekonstrukci cesty podle předchůdců
    
    current = end_id
    while current != start_id:
        path.append(current)
        current = predecessors[current]
    path.append(start_id)
    path.reverse()
    
    return path

def load_nodes_metadata(filename: str) -> dict[int, tuple[str, str]]:
    """Načte metadata o uzlech z CSV souboru. V případě GPS dat je možné zobrazit trasu na mapě pomocí plotly express.
    Returns:
        dict[int, tuple[str, str]]: metadata uzlů (id uzlu, [latitude, longitude])
    """
    node_info = dict()
    ## TODO 4 Načtěte metadata o uzlech z CSV souboru
    
    with open(filename, "r", encoding="utf8") as fd:
        for i, line in enumerate(fd):
            if i == 0:
                continue
            line = line.replace("\n", "")
            line = line.split(',"POINT(')
            id = line[0]
            lat, long = line[1].replace(')"', "").split(" ")
            node_info[int(id)] = (long, lat)
    
    return node_info


def show_path(
    node_info: dict[int, tuple[str, str]], # metadata uzlů načtená pomocí load_ndodes_metadata
    path: list[int],
):
    """
    Args:
        node_info (dict[int, tuple[str, str]]): metadata uzlů načtená pomocí load_ndodes_metadata
        path (list[int]): cesta získaná pomocí reconstruct_path
    """
    if node_info:
        lats = [float(la) for la, lo in [node_info[p] for p in path]]
        lons = [float(lo) for la, lo in [node_info[p] for p in path]]

        fig = px.line_mapbox(lat=lats, lon=lons, mapbox_style="open-street-map", zoom=12)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, mapbox_center_lat=49.747)
        fig.show()

def demo() -> None:
    graph = load_graph("10-dijkstra/graph_grid_s3_3.json")

    # painter = adthelpers.painter.Painter(
    #     graph,
    #     # colors=("red", "blue", "yellow", "grey") # pokud by byl problém s barvami je možné je změnit
    # )
    # painter.draw_graph()
    start = 0
    end = 8
    distances, predecessors = graph.dijkstra(start, end)
    path = reconstruct_path(predecessors, start, end)
    print(path)
    print(distances[end])


def pilsen() -> None:
    edge_file = "10-dijkstra/pilsen/pilsen_edges_nice.csv"
    node_file = "10-dijkstra/pilsen/pilsen_nodes.csv"
    graph = load_graph_csv(edge_file)
    start = 4651
    end = 4569
    distances, predecessors = graph.dijkstra(start, end, show_progress=False)
    path = reconstruct_path(predecessors, start, end)
    show_path(
        load_nodes_metadata(node_file),
        path,
    )
    print(path)
    print(distances[end])


def main() -> None:
    # demo()
    pilsen()
    input("...")

if __name__ == "__main__":
    main()

