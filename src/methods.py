class Methods:
    LINE_COLORS = {
        0: "#E6E6E6",
        1: "#d35590",
        3: "#9e9a3a",
        7: "#df8600",
        9: "#8d5544",
        12: "#b89d4e"
    }

    LINE_INTERVALS = {
        1: 4,
        3: 3,
        7: 4,
        9: 3,
        12: 2}

    def __init__(self, data_class):
        self.data = data_class.get_data()

    def get_lines(self, station):
        for s in self.data["stations"]:
            if station == s["name"]:
                lines = s["line"]
                if isinstance(lines, (list, tuple)):
                    return [line for line in lines]
                else:
                    return [lines]
        return None

    def get_line_between(self, station1, station2):
        lines1 = self.get_lines(station1)
        lines2 = self.get_lines(station2)
        common = set(lines1) & set(lines2)
        return next(iter(common), None)

    def get_all_stations(self):
        stations = [s["name"] for s in self.data.get("stations", [])]
        return sorted(stations)

    def get_colors_of_path(self, path):
        lines = []
        for i in range(len(path) - 1):
            station1 = path[i]
            station2 = path[i + 1]
            line = self.get_line_between(station1, station2) if station1 != station2 else 0
            lines.append(line)
        return [self.LINE_COLORS.get(line) for line in lines]

    def get_line_interval(self, line):
        return self.LINE_INTERVALS.get(line)

