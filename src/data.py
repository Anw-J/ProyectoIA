# Librerías
import json
import networkx as nx

class Data:
    # Constructor
    def __init__(self):
        self.data = self.import_data()
        self.graph = self.create_graph(self.data)

    ''' Método para importar los datos del archivo json '''
    @staticmethod
    def import_data():
        with open('../data/stations.json', encoding='utf-8') as file:
            data = json.load(file)
        return data

    ''' Método para crear el grafo a partir de los datos importados '''
    @staticmethod
    def create_graph(data):
        g = nx.Graph()
        for s1 in data['stations']:
            g.add_node(s1['name'], coordinates=s1['coordinates'], line=s1['line']) # Nodos - estaciones, con atributos coordenadas y líneas
            for s2, distance in s1['connected_to'].items(): # Para cada estación conectada
                g.add_edge(s1['name'], s2, weight=distance) # Aristas - conexión entre estaciones, con peso como la distancia entre estaciones
        return g

    ''' Getters '''
    def get_data(self):
        return self.data

    def get_graph(self):
        return self.graph