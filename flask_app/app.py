from flask import Flask, request, render_template, redirect, url_for, session, render_template_string
from werkzeug.utils import secure_filename
import hashlib
import os
import filetype
from databases import db
from databases.db import TemaEnum

UPLOAD_FOLDER = 'static/uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "s3cr3t_k3y"


#Ruta para volver al indice
@app.route('/', methods=["GET"])
def index():
    

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
    

#Ruta para confirmar que los datos han sido agregados
@app.route("/agrego_actividad", methods=["POST", "GET"])
def agrego_actividad():

    if request.method == "POST":

        session = db.SessionLocal()

        region = request.form.get("region")
        comuna = request.form.get("comuna")
        sector = request.form.get("sector")
        name = request.form.get("name")
        email = request.form.get("email")
        numero = request.form.get("numero")
        inicio = request.form.get("inicio")
        termino = request.form.get("termino")
        descripcion = request.form.get("descripcion")

        actividad = db.create_actividad(comuna, sector, name, email, numero, inicio, termino, descripcion)

        files = request.files.getlist("file")
        fotos = []

        for file in files:
            if file and file.filename:
                _filename = hashlib.sha256(
                    secure_filename(file.filename) 
                    .encode("utf-8") 
                    ).hexdigest()
                _extension = filetype.guess(file).extension
                img_filename = f"{_filename}.{_extension}"
                
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))
            
            foto = db.add_fotos(os.path.join(app.config["UPLOAD_FOLDER"], img_filename), img_filename, actividad.id)
            fotos.append(foto)


        posibles_temas = ["música", "deporte", "ciencias", "religión", "política", "tecnología", "juegos", "baile", "comida", "otro2"]
        temas = []
        for tema in posibles_temas:
            if tema in request.form:
                temas.append(tema)

        glosa_otro = request.form.get("otroTema")
        if not glosa_otro:
            glosa_otro = "Null"

        for tema in temas:
            db.add_temas(tema, glosa_otro if tema == "otro2" else "Null", actividad.id)

            
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
    else:
        return redirect(url_for("agrego_actividad"))

#Ruta para volver al formulario, utiliza una ruta antes creada y vuelve a llenar con los datos que antes se llenaron si es que el usuario se arrepiente
@app.route('/informacion')
def informacion():
    return render_template('informacion.html')

if __name__ == "__main__":
    app.run(debug=True)
