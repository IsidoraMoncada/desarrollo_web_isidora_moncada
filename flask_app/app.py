from flask import Flask, request, render_template, redirect, url_for, session, render_template_string, jsonify
from werkzeug.utils import secure_filename
import hashlib
import os
from utils.validations import validate_agregar_actividad, validate_file, validate_temas
import filetype
from databases import db
from databases.db import TemaEnum, Actividad,  SessionLocal
from math import ceil
from sqlalchemy import func, cast, Date
from flask_cors import cross_origin



UPLOAD_FOLDER = 'static/uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "s3cr3t_k3y"


#Ruta para volver al indice
@app.route('/', methods=["GET"])
def index():
    PAGE_SIZE = 5
    data = []

    for actividad in db.get_actividad(page_size=PAGE_SIZE):
        comuna = db.get_comuna_by_id(actividad.comuna_id)
        foto = db.get_foto_by_actividad_id(actividad.id)
        ruta = foto.ruta_archivo
        tema = db.get_tema_by_actividad_id(actividad.id)
        tema_final = ""
        if tema.tema.value == "Otro":
            tema_final = tema.glosa_otro
        else:
            tema_final = tema.tema.value

        data.append({
            "inicio": actividad.dia_hora_inicio,
            "termino": actividad.dia_hora_termino,
            "comuna": comuna.nombre,
            "sector": actividad.sector,
            "tema": tema_final,
            "foto": ruta
        })
    return render_template('index.html', data=data)

#Ruta para llegar al form desde el index
@app.route('/agregar_actividad', methods=["GET"])
def agregar_actividad():
    return render_template('formulario.html')

#Ruta para llegar al listado desde el indice
@app.route('/ver_listado', methods=["GET"])
def ver_listado():
    PAGE_SIZE = 5
    data = []
    page_num = request.args.get('page', 1, type=int)
    actividades = db.get_actividad_page(page=page_num, page_size=PAGE_SIZE)
    total_actividades = db.get_total_actividades()
    total_paginas = ceil(total_actividades / PAGE_SIZE)

    for actividad in actividades:
        comuna = db.get_comuna_by_id(actividad.comuna_id)
        fotos = db.get_n_fotos(actividad.id)
        tema = db.get_tema_by_actividad_id(actividad.id)
        tema_final = ""
        if tema.tema.value == "Otro":
            tema_final = tema.glosa_otro
        else:
            tema_final = tema.tema.value

        data.append({
            "id": actividad.id,
            "inicio": actividad.dia_hora_inicio,
            "termino": actividad.dia_hora_termino,
            "comuna": comuna.nombre,
            "sector": actividad.sector,
            "tema": tema_final,
            "fotos": fotos,
            "organizador": actividad.nombre
        })
    
    return render_template('listado.html', data=data, page=page_num, total_pages=total_paginas)

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
        error = ""

        files = request.files.getlist("file")
        fotos = []

        posibles_temas = ["Música", "Deporte", "Ciencias", "Religión", "Política", "Tecnología", "Juegos", "Baile", "Comida", "Otro"]
        temas = []
        for tema in posibles_temas:
            if tema in request.form:
                temas.append(tema)
        
        glosa_otro = request.form.get("otroTema")


        if validate_agregar_actividad(comuna, sector, name, email, numero, inicio, termino, descripcion) and validate_file(files) and validate_temas(temas, glosa_otro):
            print("✅ Validación pasada")
            actividad = db.create_actividad(comuna, sector, name, email, numero, inicio, termino, descripcion)
        
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

            if not glosa_otro:
                glosa_otro = "Null"
            for tema in temas:
                db.add_temas(tema, glosa_otro if tema == "Otro" else "Null", actividad.id)

        else:
            error += "Uno de los campos no es valido. Vuelva al formulario y revise sus respuestas"

            return render_template("formulario.html", error=error)
            
        return """
            <!DOCTYPE html>
            <html lang="es">
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
@app.route('/informacion/<int:id>')
def informacion(id):
    data = []
    actividad = db.get_actividad_by_id(id)
    comuna = db.get_comuna_by_id(actividad.comuna_id)

    data.append({
        "id": actividad.id,
        "inicio": actividad.dia_hora_inicio,
        "termino": actividad.dia_hora_termino,
        "comuna": comuna.nombre,
        "sector": actividad.sector,
        "descripcion": actividad.descripcion,
        "organizador": actividad.nombre,
    })
    
    temas = []
    tema_final = ""
    for tema in db.get_temas(actividad.id):
        if tema.tema.value == "Otro":
            tema_final = tema.glosa_otro
        else:
            tema_final = tema.tema.value

        temas.append({
            "tema": tema_final
        })
    
    fotos = []
    for foto in db.get_fotos(actividad.id):
        foto_img = f"uploads/{foto.nombre_archivo}"
        fotos.append({
            "imagen": url_for('static', filename=foto_img)
        })
        
    return render_template('informacion.html', data=data, temas=temas, fotos=fotos)


@app.route("/get_actividades_por_dia", methods=["GET"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def get_actividades_por_dia():
    session = SessionLocal()  

    try:
        fecha = cast(Actividad.dia_hora_inicio, Date)
        actividades_por_dia = (session.query(fecha, func.count().label("cantidad")).group_by(fecha).order_by(fecha).all())
        fechas = [str(fecha) for fecha, _ in actividades_por_dia]
        cantidades = [cantidad for _, cantidad in actividades_por_dia]
        return jsonify({'fechas': fechas, 'cantidades': cantidades})
    
    finally:
        session.close()

#Ruta para llegar a las estadisticas desde el indice
@app.route('/ver_estadisticas',  methods=["GET"])
def ver_estadisticas():
    return render_template('estadisticas.html')   

if __name__ == "__main__":
    app.run(debug=True)