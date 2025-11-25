''' Clase con los métodos para obtener información '''
class Methods:
    # Diccionario con los colores correspondientes a cada línea
    LINE_COLORS = {
        0: "#E6E6E6",
        1: "#d35590",
        3: "#9e9a3a",
        7: "#df8600",
        9: "#8d5544",
        12: "#b89d4e"
    }

    # Diccionario con los intervalos de tiempo entre trenes para cada línea (en minutos)
    LINE_INTERVALS = {
        1: 4,
        3: 3,
        7: 4,
        9: 3,
        12: 2}

    # Constructor
    def __init__(self, data_class):
        self.data = data_class.get_data()

    ''' Método para obtener las líneas de una estación '''
    def get_lines(self, station):
        for s in self.data["stations"]:
            if station == s["name"]:
                lines = s["line"]
                if isinstance(lines, (list, tuple)): # Si la estación tiene varias líneas, devolver una lista con todas las líneas
                    return [line for line in lines]
                else: # Si la estación tiene una sola línea, devolver una lista con esa línea
                    return [lines]
        return None

    ''' Método para obtener la línea entre dos estaciones '''
    def get_line_between(self, station1, station2):
        lines1 = self.get_lines(station1)
        lines2 = self.get_lines(station2)
        common = set(lines1) & set(lines2) # Elegir las líneas comunes entre las dos estaciones
        return next(iter(common), None) # Devolver el primer elemento o None si no hay
    
    ''' Método para obtener todas las estaciones '''
    def get_all_stations(self):
        stations = [s["name"] for s in self.data.get("stations", [])]
        return sorted(stations) # Ordenar las estaciones

    ''' Método para obtener los colores de las líneas en un camino '''
    def get_colors_of_path(self, path):
        lines = [] # Lista para guardar las líneas
        for i in range(len(path) - 1):
            station1 = path[i]
            station2 = path[i + 1]
            line = self.get_line_between(station1, station2) if station1 != station2 else 0 # Si hay trasbordo, asignar la línea 0 (gris)
            lines.append(line)
        return [self.LINE_COLORS.get(line) for line in lines] # Lista con los colores correspondientes a las líneas

    ''' Método para obtener el intervalo de tiempo entre trenes de una línea '''
    def get_line_interval(self, line):
        return self.LINE_INTERVALS.get(line)

