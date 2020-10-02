from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Transaccion(db.Model):

    __tablename__ = "transacciones"

    tran_id = db.Column('tran_id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer)
    nroboleta = db.Column('nroboleta', db.Integer)
    registrado = db.Column('registrado', db.DateTime)
    tipopago = db.Column('tipopago', db.Integer)
    formadepago = db.Column('formadepago', db.Integer)
    estado = db.Column('estado', db.Integer)
    id_combinatoria = db.Column('id_combinatoria', db.Integer)
    datos = db.Column('datos', db.String(255))
    estado_gestion = db.Column('estado_gestion', db.String(255))
    nrocuenta = db.Column('nrocuenta', db.String(255))
    cbu = db.Column('cbu', db.String(255))
    dni = db.Column('dni', db.String(255))
    titular_cuenta = db.Column('titular_cuenta', db.String(255))
    fechamodif = db.Column('fechamodif', db.DateTime)
    usuariogestion = db.Column('usuariogestion', db.String(255))



    def __init__(self, user_id, descripcion, nroboleta, tipopago, formadepago, estado, id_combinatoria, registrado, datos, estado_gestion,nrocuenta, cbu, dni, titular_cuenta, fechamodif, usuariogestion):
        self.user_id = user_id
        self.nroboleta = nroboleta
        self.registrado = registrado
        self.tipopago = tipopago
        self.formadepago = formadepago
        self.estado = estado
        self.id_combinatoria = id_combinatoria
        self.datos = datos
        self.estado_gestion = estado_gestion
        self.nrocuenta = nrocuenta
        self.cbu = cbu
        self.dni = dni
        self.titular_cuenta = titular_cuenta
        self.fechamodif = fechamodif
        self.usuariogestion = usuariogestion
