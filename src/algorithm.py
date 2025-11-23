# Algoritmo A*
from methods import get_connected_stations, get_coords, get_f, get_g, get_h
import networkx as nx
import matplotlib.pyplot as plt
import init

init.init()
G = nx.Graph()
for s in init.data["stations"]:
    station1 = s["name"]
    G.add_node(station1)
    for station2, distance in s["connected_to"].items():
        G.add_edge(station1, station2, weight=distance)


def get_best_path(origin, destination):
    path = nx.astar_path(G, origin, destination, heuristic=get_h, weight='weight')
    return path


if __name__ == "__main__":
    origin = input("Origen: ").strip()
    destination = input("Destino: ").strip()
    path = get_best_path(origin, destination)
    print("Camino encontrado:", path)


'''
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_size=700, node_color="#3A7BDC", font_size=9)
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
plt.show()
'''






