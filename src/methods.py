# Los métodos útiles (getters)
#import geopy.distance
import init
import al2

LINE_COLORS = {
    "1": "#d35590",
    "3": "#9e9a3a",
    "7": "#df8600",
    "9": "#8d5544",
    "12": "#b89d4e"
}

'''def get_coords(station):
    for s in init.data["stations"]:
        if station == s["name"]:
            return s["coordinates"]
    return None

def get_connected_stations(station):
    for s in init.data["stations"]:
        if station == s["name"]:
            return s["connected_to"]
    return None

def get_h(sation1, station2):
    coords_1 = get_coords(sation1)
    coords_2 = get_coords(station2)
    if coords_1 is None or coords_2 is None:
        return 0
    return geopy.distance.distance(coords_1, coords_2).m

def get_g(station1, station2):
    for station, distance in get_connected_stations(station1).items():
        if station == station2:
            return distance
    return -1

def get_f(station1, station2):
    g = get_g(station1, station2)
    h = get_h(station1, station2)
    if g == -1 or h == -1:
        return -1
    return g + h
'''
def get_lines(station):
    for s in init.data["stations"]:
        if station == s["name"]:
            lines = s["line"]
            if isinstance(lines, (list, tuple)):
                return [str(line) for line in lines]
            else:
                return [str(lines)]
    return None

def get_line_between(station1, station2):
    lines1 = get_lines(station1)
    lines2 = get_lines(station2)
    common = set(lines1) & set(lines2)
    return next(iter(common), None)

def get_all_stations():
    stations = [s["name"] for s in init.data.get("stations", [])]
    return sorted(stations)

def get_colors_of_path(path):
    lines = []
    for i in range(len(path) - 1):
        station1 = path[i]
        station2 = path[i + 1]
        line = get_line_between(station1, station2)
        lines.append(line)
    return [LINE_COLORS.get(str(line)) for line in lines]

def get_best_path(origin, destination):
    g = al2.Data().get_graph()
    return al2.Al().astar_algorithm(g, origin, destination)