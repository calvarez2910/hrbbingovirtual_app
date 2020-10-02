from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from datetime import datetime
from time import sleep
from models.Users import User
from models.Users import db
from models.Rifas import Rifa
from models.Rifas import db
from models.Cartones import Carton, CartonSearch
from models.Cartones import db
from models.Transacciones import Transaccion
from models.Transacciones import db
from models.MisRifas import MisRifa
from models.Boletas import Boleta
from models.Boletas import db
import json
import re
import os
import urllib.request
import requests
from werkzeug.utils import secure_filename
import csv
from io import StringIO
import pandas as pd
from pandas import DataFrame, read_csv
from datetime import date
from sqlalchemy import func
from flask_mail import Message, Mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


app = Flask(__name__)

# setup the app

# DEV ONLY comment to prod or test #
app.config.from_object("config.TestingConfig")
# app.config.from_object("config.DevelopmentConfig")
# --------------------------------------

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get(
    "SQLALCHEMY_TRACK_MODIFICATIONS")
app.config['SQLALCHEMY_ECHO'] = False
app.config['UPLOAD_FOLDER'] = os.environ.get("UPLOAD_FOLDER")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SESSION_COOKIE_SECURE'] = os.environ.get("SESSION_COOKIE_SECURE")

# Get postgres env variables
app.config['DBHOST'] = os.environ.get("dbhost")
app.config['DBNAME'] = os.environ.get("dbname")
app.config['DBPASSWORD'] = os.environ.get("dbpassword")
app.config['DBUSER'] = os.environ.get("dbuser")


postgressql = "postgresql+psycopg2://" + \
    app.config['DBUSER'] + ":" + app.config['DBPASSWORD'] + \
    "@" + app.config['DBHOST'] + "/" + app.config['DBNAME']
app.config['SQLALCHEMY_DATABASE_URI'] = postgressql

print('Connected as:')
print(app.config['DBUSER'])


# ENV  #

#

# EMAIL CONFIG
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hrbbingovirtual@gmail.com'
app.config['MAIL_PASSWORD'] = '*****************'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Components set up
mail = Mail(app)
db.init_app(app)
bcrypt = Bcrypt(app)


# setup the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# create the db structure
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(e)


#  setup routes  ##


@app.route('/cartones', methods=["GET", "POST"])
def cartones():
    rifa = Rifa.query.filter(Rifa.idcombinatoria == 2).one()
    if rifa.cerrada == 0:
        idcomb = request.form.get('rifa', None)
        rifaelegida = idcomb
        searb = request.form.get('nroboleta', None)
        searn = request.form.get('nroencarton', None)
        btn = request.form.get('btn', None)
        if idcomb != None:
            session['idcombinatoria'] = idcomb
        desde = request.form.get('btndesde', None)
        hasta = request.form.get('btnhasta', None)
        idcomb = session['idcombinatoria']
        if desde == None and hasta == None or desde == '0':
            desde = 0
            hasta = 50
        elif desde == None:
            desde = int(hasta)
            hasta = int(hasta)+50
        else:
            hasta = int(desde)
            desde = int(desde)-50

        if btn == 'searchBol' and searb != '':
            boletasres = Boleta.query.filter(Boleta.nroboleta == searb,
                                             Boleta.idcombinatoria == idcomb,
                                             Boleta.estado == 0)
            cartres = Carton.query.filter(Carton.nroboleta,
                                          Carton.nroboleta == searb,
                                          Carton.idcombinatoria == 2,
                                          Carton.estado == 0)
        elif btn == 'searchnro' and searn != '':
            boletasids = CartonSearch.query.filter(
                CartonSearch.nros.like("%-" + searn + "-%")).all()
            boletasres = Boleta.query.filter(
                Boleta.nroboleta == searb,
                Boleta.idcombinatoria == idcomb, Boleta.estado == 0)
        else:
            boletasres = Boleta.query.filter(
                Boleta.nroboleta > desde, Boleta.nroboleta
                <= hasta, Boleta.idcombinatoria == idcomb, Boleta.estado == 0)

            cartres = Carton.query.filter(Carton.nroboleta > desde,
                                          Carton.nroboleta <= hasta,
                                          Carton.idcombinatoria == 2,
                                          Carton.estado == 0)
            cantcartone = cartres.count()
            while cantcartone < 80:
                hasta = int(hasta)+50
                cartres = Carton.query.filter(Carton.nroboleta > desde,
                                              Carton.nroboleta <= hasta,
                                              Carton.idcombinatoria == 2,
                                              Carton.estado == 0)
                cantcartone = cartres.count()

            boletasres = Boleta.query.filter(
                Boleta.nroboleta > desde, Boleta.nroboleta
                <= hasta, Boleta.idcombinatoria == idcomb, Boleta.estado == 0)
        nombrerifa = ''
        return render_template('cartones.html',
                               user=current_user,
                               cartones=cartres,
                               desde=desde,
                               hasta=hasta,
                               nombrerifa=nombrerifa,
                               boletasres=boletasres,
                               rifaelegida=rifaelegida)
    else:
        flash('ESTA RIFA YA ESTA CERRADA', 'info')
        return redirect(url_for('index'))


@app.route('/')
# @login_required
def index():
    rifaelegida = ''
    titulo = 'RIFAS Y BINGOS DISPONIBLES'
    if current_user.is_authenticated:
        res = Rifa.query.filter(Rifa.estado == 1)
        d0 = res[0].fechasorteo
        dias = d0 - datetime.today()
        return render_template('index.html',
                               user=current_user,
                               rifas=res,
                               tituloPag=titulo,
                               rifaelegida=rifaelegida,
                               dias=dias.days)
    else:
        return render_template('front.html', user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():

    # clear the inital flash message
    session.clear()
    if request.method == 'GET':
        return render_template('login.html')

    # get the form data
    username = request.form['username']
    password = request.form['password']

    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True

    # query the user
    try:
        registered_user = User.query.filter_by(username=username).first()
    except Exception as e:
        print(e)
    if registered_user is None:
        flash('usuario no registrado')
        return render_template('login.html')

    # check the passwords
    user_haspwd = registered_user.password
    ispasswordok = bcrypt.check_password_hash(user_haspwd, password)

    if ispasswordok is False:
        flash('Contraseña no validas')
        return render_template('login.html')

    # login the user
    login_user(registered_user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        session.clear()
        return render_template('register.html')

    # get the data from our form
    password = request.form['password']
    conf_password = request.form['confirm-password']
    username = request.form['username']
    email = request.form['email']
    nombre = ''
    apellido = ''
    domiciliopart = ''
    telefonofijo = ''
    telefonocelular = ''
    localidad = ''
    dni = ''
    provincia = ''

    # make sure the password match
    if conf_password != password:
        flash("La Contraseña no coincide")
        return render_template('register.html')

    # check if it meets the right complexity
    check_password = password_check(password)

    # generate error messages if it doesnt pass
    if True in check_password.values():
        for k, v in check_password.items():
            if str(v) == "True":
                flash(k)

        return render_template('register.html')

    # hash the password for storage
    pw_hash = bcrypt.generate_password_hash(password)

    # create a user, and check if its unique
    user = User(username,
                pw_hash,
                email, nombre,
                apellido, domiciliopart,
                telefonofijo, telefonocelular,
                localidad, dni,
                provincia)
    u_unique = user.unique()

    # add the user
    if u_unique == 0:
        db.session.add(user)
        db.session.commit()
        flash("Cuenta Creada")
        html = render_template(
            'msgregistro.html', nombre=nombre, username=username)
        asunto = 'Crecion de cuenta en HRB BINGO VIRTUAL'
        enviarEmail('Su cuenta en HRB VINGO VIRTUAL', html, asunto, email)
        # sleep(2)

        return redirect(url_for('login'))

    # else error check what the problem is
    elif u_unique == -1:
        flash("Email existente.")
        return render_template('register.html')

    elif u_unique == -2:
        flash("Usuario existente.")
        return render_template('register.html')

    else:
        flash("Usuario y Email ya registrado.")
        return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/carton', methods=["GET", "POST"])
def canton():
    if "misrifas" in request.referrer:
        origen = 1
    else:
        origen = 0

    nroboleta = request.form.get('nrocarton', None)
    idcomb = 2  # session['idcombinatoria']
    cartonelegido = Carton.query.filter(
        Carton.nroboleta == nroboleta, Carton.idcombinatoria == idcomb)
    return render_template('carton.html', user=current_user,
                           cartonelegido=cartonelegido,
                           nrocarton=nroboleta, origen=origen)


@app.route('/cartonjugar', methods=["GET", "POST"])
def cartonjugar():
    origen = 0

    nroboleta = request.form.get('nrocarton', None)
    idcomb = 2  # session['idcombinatoria']
    cartonelegido = Carton.query.filter(
        Carton.nroboleta == nroboleta, Carton.idcombinatoria == idcomb)
    return render_template('cartonjugar.html', user=current_user, cartonelegido=cartonelegido, nrocarton=nroboleta, origen=origen)


@app.route('/confirmcarton', methods=["GET", "POST"])
def cartonelegido():
    nrocarton = request.form.get('nrocarton', None)
    idcomb = session['idcombinatoria']
    cartonelegido = Carton.query.filter(
        Carton.nroboleta == nrocarton, Carton.idcombinatoria == idcomb)
    return render_template('confirmcarton.html',
                           user=current_user,
                           cartonelegido=cartonelegido,
                           nrocarton=nrocarton)


@app.route('/profile', methods=["GET", "POST"])
def profile():
    if "usuario" in request.referrer:
        origen = 0
        usuario = User.query.filter(
            User.id == request.form.get('idusuario', None))
        return render_template('profile.html', user=usuario[0], origen=origen)
    else:
        origen = 1
        return render_template('profile.html',
                               user=current_user,
                               origen=origen)


@app.route('/usuarios', methods=["GET", "POST"])
def usuarios():
    usuarios = User.query.order_by(User.id.asc()).all()
    return render_template('usuarios.html',
                           usuarios=usuarios,
                           user=current_user)


@app.route('/venderboleta', methods=["GET", "POST"])
def venderboletas():
    usuarios = User.query.order_by(User.id.asc()).all()
    boletasres = Boleta.query.filter(
        Boleta.idcombinatoria == 2, Boleta.estado == 0)
    usuariofilter = []
    boletas = []
    for x in usuarios:
        usuariofilter.append(
            x.nombre + ' ' + x.apellido + ' - ' + str(x.id))
    for y in boletasres:
        boletas.append(
            str(y.nroboleta))
    return render_template('venderboleta.html',
                           usuarios=usuariofilter,
                           user=current_user, boletas=boletas)


@app.route('/forgotpassword', methods=["GET", "POST"])
def forgotpassword():
    return render_template('forgotpassword.html')


@app.route('/forgotpasswordsend', methods=["GET", "POST"])
def forgotpasswordsend():
    usuario = User.query.filter(
        User.email == request.form.get('email', None))
    if request.form.get('email', None) is None or usuario.count() == 0:
        flash("El email no esta registrado, cree un nuevo usario.")
        return render_template('register.html')
    else:
        # email send to reset
        token = get_reset_token(
            app.config['SECRET_KEY'], 1800, usuario[0].email)
        urltoken = url_for('resetpassword', token=token, _external=True)
        html = render_template('resetpwdemail.html',
                               user=usuario[0], token=urltoken)
        asunto = 'Resetear su contraseña en HRB BINGO VIRTUAL'
        enviarEmail('HRB Bingo Virtual',
                    html, asunto, usuario[0].email)
        flash("Por favor, verifique su correo electronico, recibira instrucciones para resetear su contraseña")
        return render_template('forgotpassword.html')


@app.route('/resetpassword/<token>', methods=["GET", "POST"])
def resetpassword(token):
    uservalid = verify_reset_token(token)
    if uservalid is None:
        flash("El codigo es incorrecto o ya no es valido, vuelva a solicitar uno nuevo")
        return render_template('forgotpassword.html')
    else:
        return render_template('resetpasswordp.html', user=uservalid)


@app.route('/updatepassword', methods=["GET", "POST"])
def updatepassword():

    # get the data from our form
    password = request.form['password']
    conf_password = request.form['confirm-password']
    username = request.form['username']
    usremail = request.form['email']

    usuario = User.query.filter(
        User.email == request.form.get('email', None)).one()

    # make sure the password match
    if conf_password != password:
        flash("La Contraseña no coincide")
        return render_template('register.html')

    # check if it meets the right complexity
    check_password = password_check(password)

    # generate error messages if it doesnt pass
    if True in check_password.values():
        for k, v in check_password.items():
            if str(v) == "True":
                flash(k)
        return render_template('resetpassword.html', user=usuario)

    # hash the password for storage
    pw_hash = bcrypt.generate_password_hash(password)

    # Update password
    userinfoUpd = User.query.filter(
        User.email == request.form.get('email', None)).one()
    userinfoUpd.password = pw_hash
    userinfoUpd.query.session.commit()
    print(username + '-' + usremail + '->' + 'Usuario modifico Password')
    flash("Su contraseña fue actualizada correctamente")
    return redirect(url_for('login'))


@ app.route('/ventabo', methods=["GET", "POST"])
def ventabo():
    estadogest = ''
    nrocarton = request.form.get('nrocarton', None)
    datosgest = request.form.get('datosgest', None)
    cliente = request.form.get('cliente', None)[request.form.get(
        'cliente', None).find("-")+2:len(request.form.get('cliente', None))]
    if request.form.get('cliente', None).find("-") == -1:
        datos = Boleta.query.with_entities(Boleta.estadoboleta, Boleta.idcombinatoria,
                                           func.count(Boleta.idcombinatoria).label("cantidad")) \
            .filter(Boleta.idcombinatoria == 2) \
            .group_by(Boleta.estadoboleta, Boleta.idcombinatoria).all()
        misrifas = MisRifa.query.order_by(MisRifa.registrado.asc()).all()
        flash("NO SE PUDO REGISTRAT LA VENTA, EL CLIENTE NO EXISTE, ELIJALO DE LA LISTA O CREE UNO NUEVO.", 'error')
    else:
        usuarioventa = User.query.filter(User.id == cliente).one()
        cartonCheck = Carton.query.filter(Carton.nroboleta == nrocarton)
        if cartonCheck[0].estado == 0:
            tstamo = datetime.now()
            datos = 'Contactar a ' + usuarioventa.nombre + ' ' + usuarioventa.apellido+', Telefono:' + \
                usuarioventa.telefonocelular + ' email:' + usuarioventa.email + ' ' + datosgest
            estadogest = 'Reservada'
            metodo = 'A confirmar'
            data = [nrocarton, 3]
            newtran = Transaccion(user_id=usuarioventa.id, descripcion=data[1],
                                  nroboleta=nrocarton, tipopago=2, estado=0,
                                  id_combinatoria=2,
                                  formadepago='',
                                  registrado=tstamo,
                                  datos=datos,
                                  estado_gestion=estadogest,
                                  nrocuenta='',
                                  cbu='', dni='',
                                  titular_cuenta='',
                                  fechamodif=tstamo,
                                  usuariogestion='NO ASIGNADO')

            db.session.add(newtran)
            db.session.commit()

            if estadogest == 'Reservada':
                boletaestado = 2
            if estadogest == 'Pagada':
                boletaestado = 1

            cartonUpdate = Carton.query.filter(
                Carton.nroboleta == nrocarton)
            cartonUpdate.update({Carton.estado: boletaestado},
                                synchronize_session=False)
            cartonUpdate.session.commit()
            db.session.commit()
            datos = Boleta.query.with_entities(Boleta.estadoboleta, Boleta.idcombinatoria,
                                               func.count(Boleta.idcombinatoria).label("cantidad")) \
                .filter(Boleta.idcombinatoria == 2) \
                .group_by(Boleta.estadoboleta, Boleta.idcombinatoria).all()
            misrifas = MisRifa.query.order_by(MisRifa.registrado.asc()).all()

            flash("Venta Realizada con exito")
        else:
            flash(
                "Lo sientimos, esa boleta ya no esta disponible, por favor elija otra")

    return '200'

# --------------------------------------


@app.route('/misrifas/<origen>', methods=["GET", "POST"])
def Misrifas(origen):
    misrifas = MisRifa.query.filter(MisRifa.user_id == current_user.id)
    jugar = origen

    return render_template('misrifas.html',
                           user=current_user,
                           misrifas=misrifas,
                           jugar=jugar)


# required function for loading the right user
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# check password complexity


@app.route('/pago', methods=["GET", "POST"])
def pago():
    nrocarton = request.form.get('nrocarton', None)

    # cartonUpdate =Carton.query.filter(Carton.nrocarton == nrocarton).one()
    # cartonUpdate.estado=2
    # cartonUpdate.query.session.commit()

    return render_template('pricing.html',
                           user=current_user,
                           nrocarton=nrocarton)


@app.route('/personaldata', methods=["GET", "POST"])
def personaldata():
    nrocarton = request.form.get('nrocarton', None)
    dataco = []
    dataco = nrocarton.split(",")
    return render_template('checkout.html', user=current_user,
                           nrocarton=nrocarton,
                           dataco=dataco)


@app.route('/guardapersonaldata/<origen>', methods=["GET", "POST"])
def guardapersonaldata(origen):
    if origen == '1':
        userid = current_user.id
    else:
        userid = request.form.get('idusuario')

    userinfoUpd = User.query.filter(User.id == userid).one()
    userinfoUpd.nombre = request.form.get('nombre')
    userinfoUpd.apellido = request.form.get('apellido')
    userinfoUpd.localidad = request.form.get('localidad')
    userinfoUpd.domiciliopart = request.form.get('domiciliopart')
    userinfoUpd.email = request.form.get('email')
    userinfoUpd.telefonofijo = request.form.get('telefonocelular')
    userinfoUpd.telefonocelular = request.form.get('telefonocelular')
    userinfoUpd.dni = request.form.get('dni')
    userinfoUpd.provincia = request.form.get('provincia')
    userinfoUpd.query.session.commit()
    return '200'


@app.route('/confirmdata', methods=["GET", "POST"])
def confirmdata():
    nrocarton = request.form.get('nrocarton', None)
    data = []
    data = nrocarton.split(",")
    return render_template('confirmpersonal.html',
                           user=current_user,
                           nrocarton=nrocarton)


@app.route('/guardatran', methods=["GET", "POST"])
def guardatran():
    nrocarton = request.form.get('nrocarton', None)
    boletaestado = 0
    data = []
    estadogest = ''
    data = nrocarton.split(",")
    cartonCheck = Carton.query.filter(Carton.nroboleta == data[0])
    if cartonCheck[0].estado == 0:
        tstamo = datetime.now()
        if data[1] == '1':
            datos = 'DEBITO EN CUENTA: ' + current_user + ' ' + request.form.get('apellido') + ', Telefono:' + request.form.get(
                'telefonocelular') + ' email:' + request.form.get('email') + ' CBU:' + request.form.get('cbu')
        elif data[1] == '0':
            datos = 'PAGO CON TARJETA DE CREDITO Nro: ****-****-****-4444'

        elif data[1] == '2':
            datos = 'PAGO CON MERCADO PAGO TRAN Nro:12-45478'
            estadogest = 'Pagada'
            metodo = 'Mercado Pago'
        else:
            datos = 'Contactar a ' + current_user.nombre + ' ' + current_user.apellido + \
                ', Telefono:' + current_user.telefonocelular + ' email:' + current_user.email
            estadogest = 'Reservada'
            metodo = 'A confirmar'

        newtran = Transaccion(user_id=current_user.id, descripcion=data[1],
                              nroboleta=data[0], tipopago=data[1], estado=0,
                              id_combinatoria=session['idcombinatoria'],
                              formadepago='',
                              registrado=tstamo, datos=datos,
                              estado_gestion=estadogest,
                              nrocuenta='',
                              cbu='', dni='',
                              titular_cuenta='',
                              fechamodif=tstamo,
                              usuariogestion='NO ASIGNADO')

        db.session.add(newtran)
        db.session.commit()

        if estadogest == 'Reservada':
            boletaestado = 2
        if estadogest == 'Pagada':
            boletaestado = 1

        cartonUpdate = Carton.query.filter(Carton.nroboleta == data[0])
        cartonUpdate.update({Carton.estado: boletaestado},
                            synchronize_session=False)
        cartonUpdate.session.commit()

        cartonelegido = Carton.query.filter(
            Carton.nroboleta == data[0], Carton.idcombinatoria == 2)
        db.session.commit()
        try:
            html = render_template(
                'msgcompra.html', nroboleta=data[0],
                metodopago=metodo,
                email=current_user.email,
                cartonelegido=cartonelegido)
            asunto = 'Nueva Compra en HRB BINGO VIRTUAL'
            enviarEmail('Su compra en HRB Bingo Virtual',
                        html, asunto, current_user.email)
        except Exception as e:
            print(e)

        return render_template('confirmacion.html',
                               user=current_user,
                               nrocarton=nrocarton,
                               data=data)
    else:
        flash("Lo sientimos, esta boleta ya no esta disponible, por favor elija otra")
        return redirect(url_for('index', user=current_user))


@app.route('/backoffice', methods=["GET", "POST"])
def backoffice():
    misrifas = MisRifa.query.order_by(MisRifa.registrado.asc()).all()
    datos = Boleta.query.with_entities(Boleta.estadoboleta, Boleta.idcombinatoria,
                                       func.count(Boleta.idcombinatoria).label("cantidad")).filter(Boleta.idcombinatoria == 2).group_by(Boleta.estadoboleta, Boleta.idcombinatoria).all()

    return render_template('backoffice.html', user=current_user,
                           misrifas=misrifas, datos=datos)


@app.route('/gestiona', methods=["GET", "POST"])
def gestiona():
    misrifas = MisRifa.query.order_by(MisRifa.registrado.asc()).all()
    return render_template('gestion.html',
                           user=current_user, misrifas=misrifas)


@app.route('/guardagestion', methods=["GET", "POST"])
def guardagestion():

    if request.form.get('volver', None) is None:

        tranupd = Transaccion.query.filter(
            Transaccion.tran_id == request.form.get('tran_id', None)).one()
        nroboleta = tranupd.nroboleta
        tranupd.titular_cuenta = request.form.get('titcuenta')
        tranupd.estado_gestion = request.form.get('estado')
        tranupd.datos = request.form.get('datos')
        tranupd.query.session.commit()

        boletaestado = 0
        if request.form.get('estado') == 'Pagada':
            boletaestado = 1

        if request.form.get('estado') == 'Reservada':
            boletaestado = 2

        if request.form.get('estado') == 'Sin vender':
            boletaestado = 0

        if request.form.get('estado') == 'Impaga':
            boletaestado = 3

        cartonUpdate = Carton.query.filter(Carton.nroboleta == nroboleta)
        cartonUpdate.update({Carton.estado: boletaestado},
                            synchronize_session=False)
        cartonUpdate.session.commit()
        db.session.commit()
        # emailsent = enviarEmail()
    datos = Boleta.query. \
        with_entities(Boleta.estadoboleta, Boleta.idcombinatoria,
                      func.count(Boleta.idcombinatoria).label("cantidad")) \
        .filter(Boleta.idcombinatoria == 2) \
        .group_by(Boleta.estadoboleta, Boleta.idcombinatoria).all()
    misrifas = MisRifa.query.order_by(MisRifa.registrado.asc()).all()
    return render_template('backoffice.html', user=current_user,
                           misrifas=misrifas, datos=datos)


@app.route('/getgestion', methods=["GET", "POST"])
def getgestion():
    trxid = request.form.get('nrocarton', None)
    transaccion = Transaccion.query.filter(Transaccion.tran_id == trxid).one()
    usuario = User.query.filter(User.id == transaccion.user_id).one()
    return render_template('gestion.html',
                           user=usuario,
                           transaccion=transaccion,
                           nrocarton=trxid)


@app.route('/guardarifaconfig', methods=["GET", "POST"])
def guardarifaconfig():
    if "rifaconfig" in request.referrer:
        # CONDICIONES GENERALES
        if request.form.get('cond', None == 'condgen'):

            if 'file' not in request.files:
                flash('No hay archivo')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No Hay archivo')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # print('upload_image filename: ' + filename)
                flash('Imagen actualizada')
                # Save in DB
                rifa = Rifa.query.filter(Rifa.idcombinatoria == 2).one()
                rifa.url_condgrnerales = os.path.join(
                    app.config['UPLOAD_FOLDER'], filename)
                rifa.query.session.commit()

                # /////////////////////////
            else:
                flash('Solo estan permitidos -> png, jpg, jpeg, gif')
                return redirect(request.url)

        # FECHAS DE SORTEO
        if request.form.get('fechassort', None == 'fechassort'):

            if 'file' not in request.files:
                flash('No hay archivo')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No Hay archivo')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # print('upload_image filename: ' + filename)
                flash('Imagen actualizada')
                # Save in DB
                rifa = Rifa.query.filter(Rifa.idcombinatoria == 2).one()
                rifa.url_fechas = os.path.join(
                    app.config['UPLOAD_FOLDER'], filename)
                rifa.query.session.commit()

                # /////////////////////////

            else:
                flash('Solo estan permitidos -> png, jpg, jpeg, gif')
                return redirect(request.url)

    # GANADORES
        if request.form.get('ganadores', None == 'ganadores'):

            if 'file' not in request.files:
                flash('No hay archivo')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No Hay archivo')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # print('upload_image filename: ' + filename)
                flash('Imagen actualizada')
                # Save in DB
                rifa = Rifa.query.filter(Rifa.idcombinatoria == 2).one()
                rifa.url_ganadores = os.path.join(
                    app.config['UPLOAD_FOLDER'], filename)
                rifa.query.session.commit()

                # /////////////////////////

            else:
                flash('Solo estan permitidos -> png, jpg, jpeg, gif')
                return redirect(request.url)

    # PARTIDAS
        if request.form.get('partidas', None == 'partidas'):

            if 'file' not in request.files:
                flash('No hay archivo')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No Hay archivo')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # print('upload_image filename: ' + filename)
                flash('Imagen actualizada')
                # Save in DB
                rifa = Rifa.query.filter(Rifa.idcombinatoria == 2).one()
                rifa.url_partidas = os.path.join(
                    app.config['UPLOAD_FOLDER'], filename)
                rifa.query.session.commit()

                # /////////////////////////

        # FAQs
        if request.form.get('faq', None == 'faq'):

            if 'file' not in request.files:
                flash('No hay archivo')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No Hay archivo')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # print('upload_image filename: ' + filename)
                flash('Imagen actualizada')
                # Save in DB
                rifa = Rifa.query.filter(Rifa.idcombinatoria == 2).one()
                rifa.url_faq = os.path.join(
                    app.config['UPLOAD_FOLDER'], filename)
                rifa.query.session.commit()

                # /////////////////////////

            else:
                flash('Solo estan permitidos -> png, jpg, jpeg, gif')
                return redirect(request.url)

        ########

    else:
        rifa = Rifa.query.filter(Rifa.idcombinatoria == 2).one()
        return render_template('rifaconfig.html', user=current_user, rifa=rifa)
    rifa = Rifa.query.filter(Rifa.idcombinatoria == 2).one()
    return render_template('rifaconfig.html', user=current_user, rifa=rifa)


@app.route('/condiciones')
def condiciones():
    rifa = Rifa.query.filter(Rifa.idcombinatoria == 2).one()
    return render_template('condiciones.html', user=current_user, rifa=rifa)


@app.route('/partidas')
def partidas():
    rifa = Rifa.query.filter(Rifa.idcombinatoria == 2).one()
    return render_template('partidas.html', user=current_user, rifa=rifa)


@app.route('/faq')
def faq():
    rifa = Rifa.query.filter(Rifa.idcombinatoria == 2).one()
    return render_template('faq.html', user=current_user, rifa=rifa)


@app.route('/ganadores')
def ganandores():
    rifa = Rifa.query.filter(Rifa.idcombinatoria == 2).one()
    return render_template('ganadores.html', user=current_user, rifa=rifa)


@app.route('/fechasorteos')
def fechassorteos():
    rifa = Rifa.query.filter(Rifa.idcombinatoria == 2).one()
    return render_template('fechasorteos.html', user=current_user, rifa=rifa)


@app.route('/consulta', methods=["GET", "POST"])
def consulta():
    if "consulta" in request.referrer:
        try:
            html = '<p>'+request.form.get('mensaje')+'</p>'
            asunto = 'consulta de '+current_user.username+' '+current_user.email
            enviarEmail('Nueva consulta desde la APP', html,
                        asunto, 'hrbbingovirtual@gmail.com')
        except Exception as e:
            print(e)

        flash('Su consulta se ha enviado')
        return render_template('/blank-page.html',
                               user=current_user, titulo='Consulta Envida')
    else:
        rifa = Rifa.query.filter(Rifa.idcombinatoria == 2).one()
        return render_template('consulta.html', user=current_user, rifa=rifa)


@app.route('/download', methods=["GET", "POST"])
def download():
    "Export a CSV of all sales data"
    query = Boleta.query.filter(Boleta.idcombinatoria == 2)
    df = pd.read_sql(query.statement, query.session.bind)
    resp = make_response(df.to_csv(index=False))
    resp.headers["Content-Disposition"] = "attachment; filename=boletas.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp


@app.route('/estadorifa', methods=["GET", "POST"])
def estadorifa():
    if request.form.get('fecha', None) is None:
        estado = request.form.get('estado', None)
        rifa = Rifa.query.filter(Rifa.idcombinatoria == 2).one()
        if estado == 'true':
            rcerrada = 1
        else:
            rcerrada = 0
        rifa.cerrada = rcerrada
        rifa.query.session.commit()

        print('Cambio de estado de Rifa')
        return '200'
    else:
        fecha = request.form.get('fecha', None)
        rifa = Rifa.query.filter(Rifa.idcombinatoria == 2).one()
        rifa.fechasorteo = fecha
        rifa.query.session.commit()
        print('Cambio de Fecha de Sorteo de Rifa')
        return '200'


@app.route('/nuevousuario', methods=["GET", "POST"])
def nuevousuario():

    # get the data from the new user form
    password = request.form['password']
    username = request.form['username']
    email = request.form['email']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    domiciliopart = request.form['domiciliopart']
    telefonofijo = ''
    telefonocelular = request.form['telefonocelular']
    localidad = request.form['localidad']
    dni = request.form['dni']
    provincia = request.form['provincia']
    # hash the password for storage
    pw_hash = bcrypt.generate_password_hash(password)
    # create a user, and check if its unique
    user = User(username,
                pw_hash,
                email,
                nombre,
                apellido,
                domiciliopart,
                telefonofijo,
                telefonocelular,
                localidad,
                dni,
                provincia)
    u_unique = user.unique()
    # add the user
    if u_unique == 0:
        db.session.add(user)
        db.session.commit()
        return '200'
    # else error check what the problem is
    elif u_unique == -1:
        flash("Email existente.")
        return '502'
    elif u_unique == -2:
        flash("Usuario existente.")
        return '502'
    else:
        flash("Usuario y Email ya registrado.")
        return '502'


# FUNCIONES y UTILS
""" @app.before_request
def update_last_active():
    current_user.last_active = datetime.utcnow() """


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
        credit to: ePi272314
        https://stackoverflow.com/questions/16709638/checking-the-strength-of-a-password-how-to-check-conditions
    """

    # calculating the length
    length_error = len(password) <= 7

    # searching for digits
    # digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    # uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    # lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    # symbol_error = re.search(
    #    r"[ !@#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

    ret = {
        'La contraseña tiene menos de 8 caracteres': length_error,
    }

    return ret


def enviarEmail(bodymsg, msghtml, asunto, emailuser):
    msg = Message(asunto, sender='info@hrb.com', recipients=[emailuser])
    msg.body = bodymsg
    msg.html = msghtml
    mail.send(msg)
    print('enviado mail')
    return "Sent"


def get_reset_token(secret, expires_seconds, u_email):
    s = Serializer(secret, expires_seconds)
    registered_user = User.query.filter_by(email=u_email).first()
    token = s.dumps({'user_id': registered_user.id}).decode('utf-8')
    return token


def verify_reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None
    return User.query.filter_by(id=user_id).first()


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

#  ENVIO DE DATOS PARA JUGAR BINGO ONLINE


@app.route('/emitirjugada', methods=["GET", "POST"])
def emitirjugada():
    return render_template('enviarjugada.html', user=current_user)


@app.route('/exportpdf', methods=["GET", "POST"])
def exportpdf():
    origen = 0
    nroboleta = request.form.get('nrocarton', None)
    idcomb = 2  # session['idcombinatoria']
    cartonelegido = Carton.query.filter(
        Carton.nroboleta == nroboleta, Carton.idcombinatoria == idcomb)
    rendered = render_template('cartonjugar.html',
                               user=current_user,
                               cartonelegido=cartonelegido,
                               nrocarton=nroboleta, origen=origen)
    # POST to PDF API Nro1
    API_ENDPOINT = "https://api.html2pdf.app/v1/generate"

# your API key here
    API_KEY = "8f1b02040bf568c9f60b1f9ce02dccced5c9dc7786dc8ebeb9e593d8a87f5743"

# data to be sent to api
    data_request = {'apiKey': API_KEY,
                    'html': rendered}

# sending post request and saving response as response object
    #response = requests.post(url=API_ENDPOINT, data=data_request)
    #resultado = response.content
    #f = open('static/uploads/test.pdf', 'wb+')
    # f.write(resultado)
    # f.close()
    flash("Lo sientimos, todavia no esta activo este servicio")
    return redirect(url_for('index', user=current_user))


if __name__ == "__main__":
    # change to app.run(host="0.0.0.0"),
    # if you want other machines to be able to reach the webserver.
    app.run(host="0.0.0.0")
