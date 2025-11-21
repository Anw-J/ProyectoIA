# Cargar los datos de estaciones
import json

def init():
    global data
    f = open('../data/stations.json')
    data = json.load(f)
    f.close()
