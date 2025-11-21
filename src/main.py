# Punto de entrada
import init
from methods import get_all_stations
from flask import Flask, jsonify, render_template

init.init()
app = Flask(__name__, template_folder="../web")


@app.route("/")
def index():
    return render_template("index.html", stations=get_all_stations())

if __name__ == "__main__":
    app.run(debug=True)

