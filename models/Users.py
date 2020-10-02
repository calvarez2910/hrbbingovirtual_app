from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# define what our database user looks like.


class User(db.Model):

    __tablename__ = "users"

    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    password = db.Column('password', db.Binary, nullable=False)
    email = db.Column('email', db.String(60), unique=True, index=True)
    nombre = db.Column('nombre', db.String(60), index=True)
    apellido = db.Column('apellido', db.String(60),  index=True)
    domiciliopart = db.Column('domicilio_part', db.String(200),  index=True)
    telefonofijo = db.Column('telefono_fijo', db.String(60),  index=True)
    telefonocelular = db.Column('telefono_celular', db.String(60), index=True)
    localidad = db.Column('localidad', db.String(200), index=True)
    registered_on = db.Column('registered_on', db.DateTime)
    Field12 = db.Column('Field12', db.Integer)
    dni = db.Column('dni', db.String(200), index=True)
    provincia = db.Column('provincia', db.String(200), index=True)

    def __init__(self, username,
                 password, email, nombre, apellido,
                 domiciliopart, telefonofijo, telefonocelular,
                 localidad, dni, provincia):
        self.username = username
        self.password = password
        self.email = email
        self.nombre = nombre
        self.apellido = apellido
        self.domiciliopart = domiciliopart
        self.telefonofijo = telefonofijo
        self.telefonocelular = telefonocelular
        self.localidad = localidad
        self.registered_on = datetime.utcnow()
        self.dni = dni
        self.provincia = provincia

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

    # don't judge me...
    def unique(self):

        e_e = email_e = db.session.query(User.email).filter_by(
            email=self.email).scalar() is None
        u_e = username_e = db.session.query(User.username).filter_by(
            username=self.username).scalar() is None

        # none exist
        if e_e and u_e:
            return 0

        # email already exists
        elif e_e == False and u_e == True:
            return -1

        # username already exists
        elif e_e == True and u_e == False:
            return -2

        # both already exists
        else:
            return -3
