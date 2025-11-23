# Cargar los datos de estaciones
import json

def init():
    global data
    f = open('../data/stations.json', encoding='utf-8')
    data = json.load(f)
    f.close()
