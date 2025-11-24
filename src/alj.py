#!/usr/bin/env python
# coding: utf-8

# In[47]:


import networkx as nx
import json
import math
import heapq # priority queue
import datetime
import methods2 as methods


# In[48]:


class Data:
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
            g.add_node(s1['name'], coordinates=s1['coordinates'], line=s1['line'])
            for s2, distance in s1['connected_to'].items():
                 g.add_edge(s1['name'], s2, weight=distance)
        return g

    def get_data(self):
        return self.data
    
    def get_graph(self):
        return self.graph


# In[49]:


class Al:
    velocity = 600 # 36 km/h = 600 m/min
    transshipment = 8 # 8 min
    stop_time = 0.5 # 30 s = 0.5 min
    months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    opening_time = {0: 5*60, 1: 5*60, 2: 5*60, 3: 5*60, 4: 5*60, 5: 6*60, 6: 7*60} # in minutes from midnight

    @staticmethod
    def h(graph, node1, node2):
        return math.dist(graph.nodes[node1]['coordinates'],graph.nodes[node2]['coordinates'])

    def astar_algorithm(self, graph, start_point, end_point, departure_date, departure_time):
        dd_split = departure_date.split()
        dd_split[1] = self.months[dd_split[1]]
        week_day = datetime.date(int(dd_split[2]), dd_split[1], int(dd_split[0])).weekday() # 0=Monday, 6=Sunday

        open_list = [(0, start_point)] # (f, node)
        visited = {}

        g_acc = {station: float('inf') for station in graph.nodes()}
        g_acc[start_point] = 0

        f_acc = {station: float('inf') for station in graph.nodes()}
        f_acc[start_point] = g_acc[start_point] + self.h(graph, start_point, end_point)

        line_acc = {station: None for station in graph.nodes()}
        line_acc[start_point] = None

        while len(open_list) > 0:
            f, current = heapq.heappop(open_list)

            if current == end_point:
                cont = 0
                path = []
                while current in visited:
                    path.append(current)
                    current = visited[current]
                path.append(start_point)
                path.reverse()
                return path, g_acc[end_point]

            for n in graph.neighbors(current):
                possible_g = g_acc[current] + graph.get_edge_data(current, n)['weight']/self.velocity + self.stop_time
                line_between = methods.get_line_between(current, n)
                if line_acc[current] is not None and line_acc[current] != line_between:
                    possible_g += self.transshipment


                if possible_g < g_acc[n]:
                    visited[n] = current
                    g_acc[n] = possible_g
                    f_acc[n] = possible_g + self.h(graph, n, end_point)
                    line_acc[n] = line_between
                    heapq.heappush(open_list, (f_acc[n], n))

        return None, None


# In[50]:


g = Data().get_graph()
path, time = Al().astar_algorithm(g, 'Observatorio', 'Universidad', '15 March 2024', '08:00')
print('Path: %s\nTime: %.2f min' % (path, time))

