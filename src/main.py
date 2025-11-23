# Punto de entrada
import init
import webbrowser
import al
from methods import get_all_stations, get_colors_of_path
from flask import Flask, render_template, request
from src.algorithm import get_best_path

app = Flask(
    __name__,
    template_folder="../web",
    static_folder="../web/static"
)

@app.route("/")
def index():
    return render_template("index.html", stations=get_all_stations())

@app.route("/route", methods=["POST"])
def route():
    origin = request.form.get("origin")
    destination = request.form.get("destination")
    '''
    ala = al.al()
    path = ala.astar_algorithm(ala.graph, origin, destination)
    '''
    path = get_best_path(origin, destination)
    colors = get_colors_of_path(path)
    return render_template(
        "index.html",
        path=path,
        origin=origin,
        destination=destination,
        stations=get_all_stations(),
        colors=colors
    )

if __name__ == "__main__":
    init.init()
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True, use_reloader=False)

