from flask import Flask, request, render_template, redirect, url_for, session, render_template_string
from werkzeug.utils import secure_filename
import hashlib
import os
UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.secret_key = 'una_clave_secreta_segura'


#Ruta para volver al indice
@app.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        return render_template('index.html')

#Ruta para llegar al form desde el index
@app.route('/agregar_actividad', methods=["GET"])
def agregar_actividad():
    return render_template('formulario.html')

#Ruta para llegar al listado desde el indice
@app.route('/ver_listado', methods=["GET"])
def ver_listado():
    return render_template('listado.html')

#Ruta para llegar a las estadisticas desde el indice
@app.route('/ver_estadisticas',  methods=["GET"])
def ver_estadisticas():
    return render_template('estadisticas.html')

#Ruta para volver al formulario, utiliza una ruta antes creada y vuelve a llenar con los datos que antes se llenaron si es que el usuario se arrepiente
@app.route('/volver_formulario')
def volver_formulario():
    return redirect('/agregar_actividad')

#Ruta por si el usuario decide sí se devolverá o si agregara la actividad
@app.route("/pregunta_confirmacion", methods=["POST", "GET"])
def pregunta_confirmacion():
    if request.method == "POST":
        datos = request.form.to_dict()  # Aquí accedes a los datos enviados por el formulario
        print(datos)  # Esto es para prueba, luego lo puedes guardar en BD, etc.
        session['datos_formulario'] = datos

        confirmacion_html = """
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Confirmación</title>
            <style>
                #validationBox {
                    background-color: #ddffdd;
                    border-left: 6px solid #4CAF50;
                    padding: 20px;
                    margin: 40px auto;
                    max-width: 600px;
                    font-family: Arial, sans-serif;
                }
                #validationButtons button {
                    margin-top: 10px;
                    margin-right: 10px;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
            
            </style>
        </head>
        <body>
            <div id="validationBox">
                <p id="validationMessage">¿Está seguro que desea agregar esta actividad?</p>
                <div>
                    <form action="/agrego_actividad" method="POST" style="display:inline;">
                        <button type="submit">Sí, estoy seguro</button>
                    </form>
                    <form action="/volver_formulario" method="GET" style="display:inline;">
                        <button type="submit">No, quiero volver al formulario</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
        """
        # Opcional: redirigir a una página de confirmación
        return render_template_string(confirmacion_html)


@app.route("/agrego_actividad", methods=["POST", "GET"])
def agrego_actividad():
    datos = session.get('datos_formulario')

    if datos:
        return """
            <html>
            <head>
                <title>Confirmación</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f9f9f9;
                        padding: 20px;
                    }
                    #val-box {
                        background-color: #ddffdd;
                        border-left: 6px solid #4CAF50;
                        padding: 20px;
                        max-width: 600px;
                        margin: 0 auto;
                        border-radius: 5px;
                    }
                </style>
            </head>
            <body>
                <div id="val-box">
                    <h2>¡Actividad agregada con éxito!</h2>
                    <p>Hemos recibido su información, muchas gracias y suerte en su actividad.</p>
                    <button onclick="window.location.href='/'">Volver a la portada</button>
                </div>
            </body>
            </html>
            """


if __name__ == "__main__":
    app.run(debug=True)
