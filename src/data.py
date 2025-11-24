import json
import networkx as nx

class Data:
    def __init__(self):
        self.data = self.import_data()
        self.graph = self.create_graph(self.data)

    @staticmethod
    def import_data():
        with open('../data/stations.json', encoding='utf-8') as file:
            data = json.load(file)
        return data

    @staticmethod
    def create_graph(data):
        g = nx.Graph()
        for s1 in data['stations']:
            g.add_node(s1['name'], coordinates=s1['coordinates'], line=s1['line'])
            for s2, distance in s1['connected_to'].items():
                g.add_edge(s1['name'], s2, weight=distance)
        return g

    def get_data(self):
        return self.data

    def get_graph(self):
        return self.graph