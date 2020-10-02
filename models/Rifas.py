from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Rifa(db.Model):

    __tablename__ = "rifas"

    idrifa = db.Column('idrifa', db.Integer, primary_key=True)
    idcombinatoria = db.Column('id_combinatoria', db.Integer)
    descripcion = db.Column('descripcion', db.String(255))
    imagencard = db.Column('imagen_card', db.String(255))
    titulo = db.Column('titulo', db.String(255))
    estado = db.Column('Field7', db.Integer)
    url_condgrnerales = db.Column('url_condgrnerales', db.String(255))
    url_ganadores = db.Column('url_ganadores', db.String(255))
    url_fechas = db.Column('url_fechas', db.String(255))
    url_partidas = db.Column('url_partidas', db.String(255))
    fechasorteo = db.Column('fechasorteo', db.DateTime)
    cerrada = db.Column('cerrada', db.Integer)
    url_faq = db.Column('url_faq', db.String(255))

    def __init__(self, idrifa, idcombinatoria, descripcion,
                 url_condgrnerales, url_ganadores,
                 url_fechas, url_partidas, cerrada, url_faq):
        self.idrifa = idrifa
        self.idcombinatoria = idcombinatoria
        self.descripcion = descripcion
        self.imagencard = imagencard
        self.titulo = titulo
        self.estado = estado
        self.url_condgrnerales = url_condgrnerales
        self.url_ganadores = url_ganadores
        self.url_fechas = url_fechas
        self.url_partidas = url_partidas
        self.fechasorteo = fechasorteo
        self.cerrada = cerrada
        self.url_faq = url_faq
