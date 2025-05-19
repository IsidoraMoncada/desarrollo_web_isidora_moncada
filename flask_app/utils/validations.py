import re
import filetype
from datetime import datetime

def validate_region(value):
    return value

def validate_comuna(value):
    return value

def validate_sector(value):
    value = value.strip()
    return len(value) < 100 or not value

def validate_nombre(value):
    value = value.strip()
    return value and len(value) < 200

def validate_email(value):
    reg = r'^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$'
    value = value.strip()
    return value and len(value) < 100 and re.fullmatch(reg, value) is not None

def validate_numero(value):
    reg = r'^\+\d{3}\.\d{8}$'
    value = value.strip()
    return re.fullmatch(reg, value) or not value

def validate_contacto(value, otro=None):
    if len(value):
        return True

    if value == "Otro":
        if not otro:
            return False
        otro = otro.strip()
        if len(otro) < 4 or len(otro) > 50:
            return False
    return True


def validate_inicio(value):
    value = value.strip()
    reg = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$'
    return value and re.fullmatch(reg, value) is not None

def validate_termino(value_i, value_t):
    value_i = value_i.strip()
    value_t = value_t.strip()
    reg = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$'

    if re.fullmatch(reg, value_t) is None:
        return False
    
    if validate_inicio(value_i) == False:
        return False

    try:
        inicio = datetime.fromisoformat(value_i)
        termino = datetime.fromisoformat(value_t)
    except ValueError:
        return False

    
    if inicio > termino:
        return False
    
    return True

def validate_descripcion(value):
   value = value.strip()
   return len(value) > 3  or not value

def validate_temas(temas, otro_valor=None):

    if not temas or len(temas) == 0:
        return False

    if "Otro" in temas:
        if not otro_valor:
            return False
        otro_valor = otro_valor.strip()
        if len(otro_valor) < 3 or len(otro_valor) > 15:
            return False

    return True

def validate_file(value):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

    # check if a file was submitted
    if value is None:
        return False    
    
    # check if a file was submitted
    if len(value) > 5 or len(value) < 1 or not value:
        return False
    
    for file in value:
        if file.filename.strip() == "":
            return False
        
        file_bytes = file.read()
        file.seek(0)

        # check file extension
        ftype_guess = filetype.guess(file_bytes)

        if ftype_guess.extension not in ALLOWED_EXTENSIONS:
            return False
        
        # check mimetype
        if ftype_guess.mime not in ALLOWED_MIMETYPES:
            return False
    return True


def validate_agregar_actividad(comuna, sector, name, email, numero, inicio, termino, descripcion):
    return validate_comuna(comuna) and validate_sector(sector) and validate_nombre(name) and validate_email(email) and validate_numero(numero) and validate_inicio(inicio) and validate_termino(inicio, termino) and validate_descripcion(descripcion)


