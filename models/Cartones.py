from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Carton(db.Model):

    __tablename__ = "cartones"

    idcarton = db.Column('idcarton', db.Integer, primary_key=True)
    idcombinatoria = db.Column('id_combinatoria', db.Integer)
    nrocarton = db.Column('nro_carton', db.Integer)
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
    nro11 = db.Column('nro11', db.Integer)
    nro12 = db.Column('nro12', db.Integer)
    nro13 = db.Column('nro13', db.Integer)
    nro14 = db.Column('nro14', db.Integer)
    nro15 = db.Column('nro15', db.Integer)
    estado = db.Column('estado', db.Integer)
    nroboleta = db.Column('nroboleta', db.Integer)

    def __init__(self, idrifa, idcombinatoria, descripcion):
        self.idcarton = idcarton
        self.idcombinatoria = idcombinatoria
        self.nrocarton = nrocarton
        self.nro1 = nro1
        self.nro2 = nro2
        self.nro3 = nro3
        self.nro4 = nro4
        self.nro5 = nro5
        self.nro6 = nro6
        self.nro7 = nro7
        self.nro8 = nro8
        self.nro9 = nro9
        self.nro10 = nro10
        self.nro11 = nro11
        self.nro12 = nro12
        self.nro13 = nro13
        self.nro14 = nro14
        self.nro15 = nro15
        self.estado = estado
        self.nroboleta = nroboleta

class CartonSearch(db.Model):

    __tablename__ = "cartones_search"

    nroboleta = db.Column('nroboleta', db.Integer, primary_key=True)
    nros = db.Column('nros', db.String(100))
    idcombinatoria = db.Column('id_combinatoria', db.Integer)


    def __init__(self, nroboleta, nros):
        self.nroboleta = nroboleta
        self.nros = nros
        self.idcombinatoria = idcombinatoria