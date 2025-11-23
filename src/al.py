import networkx as nx
import json
import math
import heapq # priority queue

class al:
    def __init__(self):
        self.data = self.import_data()
        self.graph = self.create_graph(self.data)

    @staticmethod
    def import_data():
        with open('../data/stations.json') as file:
            data = json.load(file)
        return data

    @staticmethod
    def create_graph(data):
        g = nx.Graph()
        for s1 in data['stations']:
            g.add_node(s1['name'], coordinates=s1['coordinates'])
            for s2, distance in s1['connected_to'].items():
                 g.add_edge(s1['name'], s2, weight=distance)
        return g

    def h(self, graph, node1, node2):
        return math.dist(graph.nodes[node1]['coordinates'],graph.nodes[node2]['coordinates'])

    def astar_algorithm(self, graph, start_point, end_point):
        open_list = [(start_point, 0)] # (node, f)
        visited = {}
        g_acc = {station: float('inf') for station in graph.nodes()}
        g_acc[start_point] = 0

        f_acc = {station: float('inf') for station in graph.nodes()}
        f_acc[start_point] = self.h(graph, start_point, end_point)

        while len(open_list) > 0:
            current, f = heapq.heappop(open_list)

            if current == end_point:
                path = []
                while current in visited:
                    path.append(current)
                    current = visited[current]
                path.append(start_point)
                return path

            for n in graph.neighbors(current):
                possible_g = g_acc[current] + graph.get_edge_data(current, n)['weight']

                if possible_g < g_acc[n]:
                    visited[n] = current
                    g_acc[n] = possible_g
                    f_acc[n] = possible_g + self.h(graph, n, end_point)
                    heapq.heappush(open_list, (f_acc[n], n))


        return None


