from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class MisRifa(db.Model):

    __tablename__ = "misrifas"

    tran_id = db.Column('tran_id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer)
    nroboleta = db.Column('nroboleta', db.Integer)
    registrado = db.Column('registrado', db.DateTime)
    tipopago = db.Column('tipopago', db.String(255))
    formadepago = db.Column('formadepago', db.String(255))
    estado = db.Column('estado', db.Integer)
    id_combinatoria = db.Column('id_combinatoria', db.Integer)
    username = db.Column('username', db.String(20))
    nombre = db.Column('nombre', db.String(60))
    apellido = db.Column('apellido', db.String(60))
    datos = db.Column('datos', db.String(60))
    rifa = db.Column('rifa', db.String(60))
    estado_gestion = db.Column('estado_gestion', db.String(60))


    def __init__(self, tran_id, user_id, nroboleta):
        self.tran_id = tran_id
        self.user_id = user_id
        self.nroboleta = nroboleta
        self.registrado = registrado
        self.tipopago = tipopago
        self.formadepago = formadepago
        self.estado = estado
        self.id_combinatoria = id_combinatoria
        self.username = username
        self.nombre = nombre
        self.apellido = apellido
        self.datos = datos
        self.rifa = rifa
        self.estado_gestion = estado_gestion
