# Punto de entrada
import init
import webbrowser
from methods import get_all_stations
from flask import Flask, render_template, request

from src.algorithm import get_best_path

init.init()

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
    path, length = get_best_path(origin, destination)
    return render_template("index.html", path=path, length=length, origin=origin, destination=destination, stations=get_all_stations())


def open_html():
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    open_html()
    app.run(debug=True, use_reloader=False)

