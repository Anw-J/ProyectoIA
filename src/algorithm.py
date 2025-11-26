# Librerías
from datetime import datetime, timedelta
import heapq # colas con prioridad
import locale
import math

# Clases
from data import Data
from methods import Methods

class Al:
    # Variables globales
    velocity = 600  # Velocidad promedio del metro: 36 km/h = 600 m/min
    transshipment = 6  # Tiempo para realizar un trasbordo: 6 min
    stop_time = 0.5  # Tiempo de parada en cada estación: 30 s = 0.5 min
    opening_time = {0: 5 * 60, 1: 5 * 60, 2: 5 * 60, 3: 5 * 60, 4: 5 * 60, 5: 6 * 60,
                    6: 7 * 60}  # Tiempo de apertura del metro según el día de la semana en minutos desde medianoche

    ''' Método para calcular la heurística entre dos nodos
        Devuelve la distancia euclídea entre las coordenadas de las estaciones
    '''
    @staticmethod
    def h(graph, node1, node2):
        return math.dist(graph.nodes[node1]['coordinates'], graph.nodes[node2]['coordinates'])

    ''' Método principal para el calculo del algoritmo A*
        Se le pasa como parámetros el grafo de estaciones y conexiones, la estación de inicio,
        la estación de destino y la fecha y hora de salida
        Devuelve la ruta óptima, el tiempo de llegada a cada estación, el tiempo total de viaje,
        la fecha y hora de salida y la fecha y hora de llegada
    '''
    def astar_algorithm(self, graph, start_point, end_point, departure_date, departure_time):
        methods = Methods(Data()) # Instancia de la clase Methods
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8') # Configurar a la localización española para el uso de las fechas

        dt = datetime.strptime(f"{departure_date} {departure_time}", "%d %B %Y %H:%M") # Fecha y hora de salida
        weekday = dt.weekday() # Día de la semana (0 -> lunes, 6 -> domingo)
        opening = self.opening_time.get(weekday) # Hora de apertura de ese día de la semana
        dt_in_minutes = dt.hour * 60 + dt.minute # Hora de salida en minutos desde medianoche
        real_departure_minutes = max(dt_in_minutes, opening) # Hora real de salida: Si es antes de la apertura, se ajusta a la hora de apertura
        real_departure_dt = dt.replace(hour=real_departure_minutes // 60, minute=real_departure_minutes % 60) # Fecha y hora real de salida

        open_list = [(0, start_point)]  # Cola con prioridad - (f, node)
        visited = {} # Diccionario con las estaciones visitadas - (estación - (predecesor, hay_trasbordo))

        g_acc = {station: float('inf') for station in graph.nodes()} # Función g acumulada de cada estación
        g_acc[start_point] = 0

        f_acc = {station: float('inf') for station in graph.nodes()} # Función f acumulada de cada estación
        f_acc[start_point] = g_acc[start_point] + self.h(graph, start_point, end_point) # f = g + h

        line_acc = {station: None for station in graph.nodes()} # Línea actual en cada estación
        line_acc[start_point] = None

        while len(open_list) > 0: # Mientras haya estaciones por comprobar
            f, current = heapq.heappop(open_list) # Sacar la estación con menor f

            if current == end_point: # Si se ha llegado a la estación destino
                path = [] # Lista con la ruta óptima
                times = [] # Lista con los tiempos a cada estación

                while current != start_point: # Bucle para recorrer la ruta desde fin a principio
                    predecessor, has_transshipment = visited[current]

                    path.append(current)
                    next_time = real_departure_dt + timedelta(minutes=g_acc[current]) # Hora de llegada a la estación en función de la hora de salida y el tiempo acumulado
                    next_time_str = next_time.strftime("%H:%M") # Formato HH:MM
                    times.append(next_time_str)

                    if has_transshipment: # Si ha habido un trasbordo
                        next_time = real_departure_dt + timedelta(minutes=g_acc[predecessor]) + timedelta(minutes=self.transshipment) # Se añade el tiempo de trasbordo
                        next_time_str = next_time.strftime("%H:%M")
                        times.append(next_time_str)
                        path.append(predecessor) # Se duplica la estación de trasbordo

                    current = predecessor

                path.append(start_point) # Añadir la estación de inicio
                next_time = real_departure_dt
                next_time_str = next_time.strftime("%H:%M")
                times.append(next_time_str) # Añadir hora de salida
                # Invertir las listas: inicio -> fin
                path.reverse()
                times.reverse()

                arrival_dt = real_departure_dt + timedelta(minutes=g_acc[end_point]) # Fecha de llegada como la suma de la fecha de salida y el tiempo total de viaje
                real_departure_dt = real_departure_dt.strftime("%H:%M, %A, %d %B %Y") # Formato para la fecha de salida
                arrival_dt = arrival_dt.strftime("%H:%M, %A, %d %B %Y") # Formato para la fecha de llegada

                return path, times, g_acc[end_point], real_departure_dt, arrival_dt

            for n in graph.neighbors(current): # Para cada vecino de la estación actual
                possible_g = g_acc[current] + graph.get_edge_data(current, n)['weight'] / self.velocity + self.stop_time # Calculo de g: tiempo acumulado + tiempo de viaje del tramo + tiempo de parada
                
                has_trasnshipment = False
                line_between = methods.get_line_between(current, n) # Línea entre la estación actual y el vecino
                if line_acc[current] is not None and line_acc[current] != line_between: # Si hay trasbordo
                    has_trasnshipment = True
                    possible_g += self.transshipment # Sumar a g el tiempo de trasbordo
                    interval_between = methods.get_line_interval(int(line_between)) # Intervalo de tiempo entre trenes de una línea (tiempo de espera hasta la llegada del nuevo tren)
                    if interval_between is not None:
                        possible_g += ((interval_between - (real_departure_minutes + g_acc[current] - opening) % interval_between)) % interval_between # Sumar el tiempo de espera hasta la llegada del nuevo tren

                if possible_g < g_acc[n]: # Si la g calculada es menor que la g acumulada del vecino
                    visited[n] = (current, has_trasnshipment) # Actualizar el predecesor
                    g_acc[n] = possible_g # Actualizar g acumulada
                    f_acc[n] = possible_g + self.h(graph, n, end_point) # Actualizar f acumulada
                    line_acc[n] = line_between # Actualizar línea actual
                    heapq.heappush(open_list, (f_acc[n], n)) # Añadir el vecino a la cola con prioridad

        return None, None, None, None, None # Si no se ha encontrado la ruta