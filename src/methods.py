# Los métodos útiles (getters)
import geopy.distance
import init


def get_coords(station):
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


def get_line(station):
    for s in init.data["stations"]:
        if station == s["name"]:
            return s["line"]
    return None
