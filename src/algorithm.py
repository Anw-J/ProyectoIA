import math
import heapq # priority queue
import datetime
import locale
from data import Data
from methods import Methods
from datetime import datetime, timedelta

class Al:
    velocity = 600  # 36 km/h = 600 m/min
    transshipment = 6  # 6 min
    stop_time = 0.5  # 30 s = 0.5 min
    opening_time = {0: 5 * 60, 1: 5 * 60, 2: 5 * 60, 3: 5 * 60, 4: 5 * 60, 5: 6 * 60,
                    6: 7 * 60}  # in minutes from midnight

    @staticmethod
    def h(graph, node1, node2):
        return math.dist(graph.nodes[node1]['coordinates'], graph.nodes[node2]['coordinates'])

    def astar_algorithm(self, graph, start_point, end_point, departure_date, departure_time):
        methods = Methods(Data())
        dt = datetime.strptime(f"{departure_date} {departure_time}", "%d %B %Y %H:%M")
        weekday = dt.weekday()
        openning = self.opening_time.get(weekday)
        dt_in_minites = dt.hour * 60 + dt.minute
        real_departure_minutes = max(dt_in_minites, openning)
        real_departure_dt = dt.replace(hour=real_departure_minutes // 60, minute=real_departure_minutes % 60)

        open_list = [(0, start_point)]  # (f, node)
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
                path = []
                times = []
                while current != start_point:
                    predecessor, has_transshipment = visited[current]

                    path.append(current)
                    next_time = real_departure_dt + timedelta(minutes=g_acc[current])
                    next_time_str = next_time.strftime("%H:%M")
                    times.append(next_time_str)
                    if has_transshipment:
                        next_time = real_departure_dt + timedelta(minutes=g_acc[predecessor])
                        next_time += timedelta(minutes=self.transshipment)
                        next_time_str = next_time.strftime("%H:%M")
                        times.append(next_time_str)
                        path.append(predecessor)

                    # current = visited[current]
                    current = predecessor
                path.append(start_point)
                next_time = real_departure_dt
                next_time_str = next_time.strftime("%H:%M")
                times.append(next_time_str)
                path.reverse()
                times.reverse()
                locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
                arrival_dt = real_departure_dt + timedelta(minutes=g_acc[end_point])
                real_departure_dt = real_departure_dt.strftime("%H:%M, %A, %d %B %Y")
                arrival_dt = arrival_dt.strftime("%H:%M, %A, %d %B %Y")

                return path, times, g_acc[end_point], real_departure_dt, arrival_dt

            for n in graph.neighbors(current):
                possible_g = g_acc[current] + graph.get_edge_data(current, n)['weight'] / self.velocity + self.stop_time
                line_between = methods.get_line_between(current, n)
                has_trasnshipment = False
                if line_acc[current] is not None and line_acc[current] != line_between:
                    has_trasnshipment = True
                    possible_g += self.transshipment
                    interval_between = methods.get_line_interval(int(line_between))
                    if interval_between is not None:
                        possible_g += (interval_between - (g_acc[current] % interval_between)) % interval_between

                if possible_g < g_acc[n]:
                    visited[n] = (current, has_trasnshipment)
                    g_acc[n] = possible_g
                    f_acc[n] = possible_g + self.h(graph, n, end_point)
                    line_acc[n] = line_between
                    heapq.heappush(open_list, (f_acc[n], n))

        return None, None, None, None, None