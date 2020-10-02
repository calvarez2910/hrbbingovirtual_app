from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Boleta(db.Model):

    __tablename__ = "boletasview"

    idcombinatoria = db.Column('id_combinatoria', db.Integer)
    carton1 = db.Column('carton1', db.Integer)
    carton2 = db.Column('carton2', db.Integer)
    nroboleta = db.Column('nroboleta', db.Integer, primary_key=True)
    estado = db.Column('estado', db.Integer)
    nro1 = db.Column('nro1', db.Integer)
    nro2 = db.Column('nro2', db.Integer)
    nro3 = db.Column('nro3', db.Integer)
    nro4 = db.Column('nro4', db.Integer)
    nro5 = db.Column('nro5', db.Integer)
    nro6 = db.Column('nro6', db.Integer)
    nro7 = db.Column('nro7', db.Integer)
    nro8 = db.Column('nro8', db.Integer)
    nro9 = db.Column('nro9', db.Integer)
    nro10 = db.Column('nro10', db.Integer)
    c2nro1 = db.Column('c2nro1', db.Integer)
    c2nro2 = db.Column('c2nro2', db.Integer)
    c2nro3 = db.Column('c2nro3', db.Integer)
    c2nro4 = db.Column('c2nro4', db.Integer)
    c2nro5 = db.Column('c2nro5', db.Integer)
    c2nro6 = db.Column('c2nro6', db.Integer)
    c2nro7 = db.Column('c2nro7', db.Integer)
    c2nro8 = db.Column('c2nro8', db.Integer)
    c2nro9 = db.Column('c2nro9', db.Integer)
    c2nro10 = db.Column('c2nro10', db.Integer)
    estadoboleta = db.Column('estadoboleta', db.String(255))
    tran_id = db.Column('tran_id', db.Integer)
    username = db.Column('username', db.String(255))
    nombre = db.Column('nombre', db.String(255))
    apellido = db.Column('apellido', db.String(255))
    email = db.Column('email', db.String(255))
    telefono_celular = db.Column('telefono_celular', db.String(255))
    localidad = db.Column('localidad', db.String(255))

    def __init__(self, carton1, idcombinatoria, carton2, nroboleta, estado):
        self.carton1 = carton1
        self.idcombinatoria = idcombinatoria
        self.carton2 = carton2
        self.nroboleta = nroboleta
        self.estado = estado
        self.nro1 = nro1
        self.nro2 = nro2
        self.nro3 = nro3
        self.nro4 = nro4
        self.nro5 = nro5
        self.nro6 = nro6
        self.nro7 = nro7
        self.nro8 = nro8
        self.nro9 = nro8
        self.nro10 = nro10
        self.c2nro1 = c2nro1
        self.c2nro2 = c2nro2
        self.c2nro3 = c2nro3
        self.c2nro4 = c2nro4
        self.c2nro5 = c2nro5
        self.c2nro6 = c2nro6
        self.c2nro7 = c2nro7
        self.c2nro8 = c2nro8
        self.c2nro9 = c2nro8
        self.c2nro10 = c2nro10
        self.estadoboleta = estadoboleta
        self.tran_id = tran_id
        self.username = username
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono_celular = telefono_celular
        self.localidad = localidad
