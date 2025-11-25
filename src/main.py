# Punto de entrada
import webbrowser
import calendar
from datetime import datetime
from flask import Flask, render_template, request
from methods import Methods
from data import Data
from algorithm import Al

''' Crear la aplicación web Flask '''
app = Flask(
    __name__, # Nombre del modulo actual para que la aplicación sepa donde estamos
    template_folder="../web", # Carpeta donde se encuentra la plantilla HTML
    static_folder="../web/static" # Carpeta donde se encuentran los archivos estáticos como imágenes
)

''' Funcion asociada a la ruta raíz de la aplicación http://127.0.0.1:5000/'''
@app.route("/")
def index():
    return render_template("index.html", stations=methods.get_all_stations())  # Renderiza la plantilla index.html con las informaciones que pasamos como parámetros
                                                                                                # stations: Lista de todas las estaciones para el select de html

''' Funcion asociada a la ruta /route de la aplicación http://127.0.0.1:5000/route'''
@app.route("/route", methods=["POST"]) # Solo acepta peticiones POST, sino no llama a esta función
def route():
    origin = request.form.get("origin") # Obtener origin del campo 'origin' del formulario
    destination = request.form.get("destination") # Obtener destination del campo 'destination' del formulario
    travel_date = request.form.get("travel_date") # Obtener travel_date del campo 'travel_date' del formulario
    html_date = travel_date # Guardar la fecha en formato HTML para mostrarla luego
    travel_time = request.form.get("travel_time") # Obtener travel_time del campo 'travel_time' del formulario
    html_time = travel_time # Guardar la hora en formato HTML para mostrarla luego
    travel_date = change_date_format(travel_date) # Cambiar el formato de la fecha de YYYY-MM-DD a DD MM YYYY para que el algoritmo lo pueda procesar

    path, times, time, real_departure_dt, arrival_dt = Al().astar_algorithm(g, origin, destination, travel_date, travel_time)   # Llamar al algoritmo A* para obtener
                                                                                                                                # la ruta, horas en cada parada, tiempo total, hora real de salida y hora de llegada
                                                                                                                                # hora real de salida depende de la hora de apertura del metro
    colors = methods.get_colors_of_path(path) # Obtener los colores de las lineas de la ruta para que se muestren en la interfaz web

    return render_template( # Renderiza la plantilla index.html con las informaciones que pasamos como parámetros
        "index.html",
        origin=origin,  # Estación de origen
        destination=destination, # Estación de destino
        path=path, # Ruta
        time=round(time), # Tiempo total redondeado
        real_departure_dt=real_departure_dt, # Hora real de salida
        arrival_dt=arrival_dt, # Hora de llegada
        times=times, # Horas en cada parada
        stations=methods.get_all_stations(), # Lista de todas las estaciones
        colors=colors, # Colores de las líneas de la ruta
        html_date=html_date, # Fecha seleccionada por el usuario en formato HTML para que el selector la mantenga tras el envío del formulario
        html_time=html_time # Hora seleccionada por el usuario en formato HTML para que el selector la mantenga tras el envío del formulario
    )

''' Método para cambiar el formato de la fecha de YYYY-MM-DD (lo que devuelve HTML) a DD MM YYYY (lo que procesa A*) '''
def change_date_format(html_date: str):
    dt = datetime.strptime(html_date, "%Y-%m-%d").date() # Convertir string a objeto date
    return f"{dt.day} {calendar.month_name[dt.month]} {dt.year}" # Devolver string en formato DD MM YYYY

''' Punto de entrada, cuando se ejecuta el programa desde main.py '''
if __name__ == "__main__":
    methods = Methods(Data()) # Instanciar la clase Methods
    g = Data().get_graph() # Generar el grafo de estaciones
    webbrowser.open("http://127.0.0.1:5000/") # Abrir en el navegador la interfaz web
    app.run(debug=True, use_reloader=False) # Iniciar el servidor web de Flask



