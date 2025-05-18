import pymysql
from sqlalchemy import create_engine, Column, Integer, DateTime, BigInteger, String, ForeignKey, Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import enum
import json

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8"

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


#Creación de tabla region
class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)

    comunas = relationship("Comuna", back_populates="region")

#Creación de tabla comuna
class Comuna(Base):
    __tablename__ = 'comuna'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)

    region = relationship("Region", back_populates="comunas")
    actividades = relationship("Actividad", back_populates="comuna")

#Creación de tabla actividad
class Actividad(Base):
    __tablename__ = 'actividad'

    id = Column(Integer, primary_key=True, autoincrement=True)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    sector = Column(String(100))
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15))
    dia_hora_inicio = Column(DateTime, nullable=False)
    dia_hora_termino = Column(DateTime)
    descripcion = Column(String(500))

    comuna = relationship("Comuna", back_populates="actividades")
    fotos = relationship("Foto", back_populates="actividad")
    contactos = relationship("ContactarPor", back_populates="actividad")
    temas = relationship("ActividadTema", back_populates="actividad")

#Creación de tabla foto
class Foto(Base):
    __tablename__ = 'foto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

    actividad = relationship("Actividad", back_populates="fotos")

class ContactoTipoEnum(enum.Enum):
    whatsapp = "whatsapp"
    telegram = "telegram"
    X = "X"
    instagram = "instagram"
    tiktok = "tiktok"
    otra = "otra"

#Creación de tabla contactar_por
class ContactarPor(Base):
    __tablename__ = 'contactar_por'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum(ContactoTipoEnum), nullable=False)
    identificador = Column(String(150), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

    actividad = relationship("Actividad", back_populates="contactos")

class TemaEnum(str, enum.Enum):
    música = "música"
    deporte = "deporte"
    ciencias = "ciencias"
    religión = "religión"
    política = "política"
    tecnología = "tecnología"
    juegos = "juegos"
    baile = "baile"
    comida = "comida"
    otro2 = "otro2"

#Creación de tabla actividad_tema
class ActividadTema(Base):
    __tablename__ = 'actividad_tema'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tema = Column(Enum(TemaEnum), nullable=False)
    glosa_otro = Column(String(15))
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

    actividad = relationship("Actividad", back_populates="temas")

Base.metadata.create_all(engine)


def create_actividad(comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion):
    
    session = SessionLocal()

    nueva_actividad = Actividad(
        comuna_id = comuna_id, 
        sector = sector, 
        nombre = nombre, 
        email = email, 
        celular = celular, 
        dia_hora_inicio = dia_hora_inicio, 
        dia_hora_termino = dia_hora_termino, 
        descripcion = descripcion
        )
    
    session.add(nueva_actividad)
    session.commit()
    session.refresh(nueva_actividad)
    session.close()

    return nueva_actividad

def add_fotos(ruta_archivo, nombre_archivo, actividad_id):
    session = SessionLocal()

    nuevas_fotos = Foto(
        ruta_archivo = ruta_archivo,
        nombre_archivo = nombre_archivo,
        actividad_id = actividad_id
    )

    session.add(nuevas_fotos)
    session.commit()
    session.refresh(nuevas_fotos)
    session.close()

    return nuevas_fotos

def add_contactos(nombre, identificador, actividad_id):
    session = SessionLocal()
    contactos = ContactarPor(
        nombre = nombre,
        identificador = identificador,
        actividad_id = actividad_id
        )

    session.add(contactos)
    session.commit()
    session.refresh(contactos)
    session.close()

    return contactos

def add_temas(tema, glosa_otro, actividad_id):
    session = SessionLocal()

    temas = ActividadTema(
        tema = tema,
        glosa_otro=glosa_otro if tema.lower() == "otro2" else "Null",
        actividad_id = actividad_id
    )

    session.add(temas)
    session.commit()
    session.refresh(temas)
    session.close()

    return temas

def get_actividad(page_size):
    session = SessionLocal()
    actividad = session.query(Actividad).limit(page_size).all()
    session.close()
    return actividad

