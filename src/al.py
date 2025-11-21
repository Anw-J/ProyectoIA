import networkx as nx
import json

import init

class al:
    def __init__(self):
        self.data = self.import_data()
        self.graph = self.create_graph()

    @staticmethod
    def import_data():
        with open('../data/stations.json') as file:
            data = json.load(file)
        return data

    @staticmethod
    def create_graph(self):
        g = nx.Graph()
        for s1 in self.data['stations']:
            g.add_node(s1["name"])
            for s2, distance in s1['connected to'].items():
                 g.add_edge(s1['name'], s2, weight=distance)
        return g

    def a_algorithm(self, start_point, end_point):
        return self.a_algorithm_aux(start_point, end_point, 0, 0, self.graph, [], 0)

    def a_algorithm_aux(self, actual_point, end_point, h, g, graph, stations, m):
        if actual_point == end_point:
            return stations, m
