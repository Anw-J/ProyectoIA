# Punto de entrada
import webbrowser
import calendar
from datetime import datetime
from flask import Flask, render_template, request
from methods import Methods
from data import Data
from algorithm import Al


app = Flask(
    __name__,
    template_folder="../web",
    static_folder="../web/static"
)

@app.route("/")
def index():
    return render_template("index.html", stations=methods.get_all_stations())

@app.route("/route", methods=["POST"])
def route():
    origin = request.form.get("origin")
    destination = request.form.get("destination")
    travel_date = request.form.get("travel_date")
    html_date = travel_date
    travel_time = request.form.get("travel_time")
    html_time = travel_time
    travel_date = change_date_format(travel_date)


    path, times, time, real_departure_dt, arrival_dt = Al().astar_algorithm(g, origin, destination, travel_date, travel_time)
    print(times)
    colors = methods.get_colors_of_path(path)

    return render_template(
        "index.html",
        origin=origin,
        destination=destination,
        path=path,
        time=round(time),
        real_departure_dt=real_departure_dt,
        arrival_dt=arrival_dt,
        times=times,
        stations=methods.get_all_stations(),
        colors=colors,
        html_date=html_date,
        html_time=html_time
    )

def change_date_format(html_date: str):
    dt = datetime.strptime(html_date, "%Y-%m-%d").date()
    return f"{dt.day} {calendar.month_name[dt.month]} {dt.year}"

if __name__ == "__main__":
    methods = Methods(Data())
    g = Data().get_graph()
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True, use_reloader=False)



