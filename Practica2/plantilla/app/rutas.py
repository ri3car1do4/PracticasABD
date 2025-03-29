"""
Módulo de Python que contiene las rutas
"""
import functools
from datetime import date

from flask import current_app as app, render_template, redirect, url_for, flash, abort, request
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import select, desc, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import load_only
import email_validator
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager
from .formularios import SignupForm, SignInForm, NuevaLiga
from .modelos import Jugador, Historico, Partido, Usuario, Liga, Participa_liga, Carta


@login_manager.user_loader
def carga_usuario(id_usuario: str):
    return db.session.get(Usuario, int(id_usuario))


@app.route('/registrarse', methods=['GET', 'POST'])
def sign_up():
    # Registro en el sistema.
    # Acepta tanto peticiones 'GET' como 'POST'.
    # En esta funcion de vista, se debe renderizar el formulario de registro de nuevos
    # usuarios con el template "sign_up.html". Una vez el usuario introduzca
    # datos correctamente y se valide el usuario,
    # se comprueba si ese usuario estaba ya registrado previamente. En tal caso, se manda un
    # mensaje flash "Ya existe un usuario con este email" y se vuelve a mostrar el formulario de nuevo.
    # Si el usuario se ha registrado correctamente, se almacena en el sistema y se devuelve
    # como respuesta una redirección a la función de vista del perfil del usuario ("perfil_usuario")
    # con el usuario que se acaba de registrar. Ese usuario se debe loggear.
    form = SignupForm()
    # Valido el formulario (solo para POST)
    if form.validate_on_submit():
        # Creo un objeto usuario
        # De aquellos campos que pueden ser nulos, hago .get en lugar de acceder
        # directamente.
        usuario = Usuario(email=form.data["email"], cumple=form.data["cumple"], password_hash=generate_password_hash(form.data["password"]))

        # Lo intento añadir a la sesión. Si el email ya existe,
        # se genera una excepción 'IntegrityError'.
        try:
            db.session.add(usuario)
            db.session.commit()
            login_user(usuario)
            return redirect(url_for('perfil_usuario', id_usuario=usuario.id))

        # Capturo la excepcion IntegrityError. Esta excepción se lanza con errores en la integridad
        # de los datos. Al violar que el email es unico
        except IntegrityError:
            # Mensajes flash: se muestran en la sesion
            flash("Ya existe un usuario con este email...")

    return render_template("sign_up.html", form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/acceder', methods=['GET', 'POST'])
def sign_in():
    # Acceso de un usuario ya registrado.
    # Acepta tanto peticiones 'GET' como 'POST'.
    #
    # En esta funcion de vista, se debe renderizar el formulario de acceso
    # con el template "sign_in.html". Una vez el usuario introduzca
    # datos correctamente, se comprueba si hay un usuario con ese email.
    # De no ser así, se lanza un mensaje flash con "El email introducido no tiene un usuario asociado" y se vuelve
    # a mostrar el formulario de acceso.
    #
    # En caso de que el email sí exista, se comprueba si la contraseña introducida es correcta. En tal caso,
    # se hace login del usuario en el sistema, y se redirige a la función de 'tirada_diaria' (donde se comprobará
    # si se puede hacer una tirada, y de no ser así, redirigirá al perfil).
    #
    # Si la contraseña es incorrecta, se lanza un mensaje flash con "Contraseña incorrecta" y se vuelve a mostrar
    # el formulario de acceso.
    form = SignInForm()
    # Valido el formulario (solo para POST)
    if form.validate_on_submit():
        email = form.data["email"]
        password = form.data["password"]
        usuario = db.session.scalars(select(Usuario).where(Usuario.email == email).options(load_only(Usuario.email,
                                                                                                  Usuario.password_hash))).first()
        if usuario:
            if check_password_hash(usuario.password_hash, password):
                login_user(usuario) # AttributeError: 'Usuario' object has no attribute 'is_active'
                # print("Redirigiendo")
                return redirect(url_for('tirada_diaria', email=email))
            else:
                flash("Contraseña incorrecta")
        else:
            flash("El email introducido no tiene un usuario asociado")
            redirect(url_for('sign_in'))

    return render_template("sign_in.html", form=form)


@app.route('/perfil/<int:id_usuario>')
@login_required
def perfil_usuario(id_usuario: int):
    # Acceso a la página del perfil del usuario.
    # Debe devolver un código de error 404 si el id introducido no pertenece a ningún usuario.
    # En caso de ser correcto, devuelve como respuesta el template "perfil_usuario.html", el cual
    # debereis implementar vosotros. Para simplificar este template, se os adjunta la funcion
    # "mostrar_liga" en el archivo "macro_mostrar_liga", el cual se debe invocar con cada una de las
    # ligas asociadas al usuario (y otra informacion pertinente).
    usuario = db.first_or_404(select(Usuario).where(Usuario.id == id_usuario))
    ligas_usuario = db.paginate(select(Liga).join(Participa_liga, Liga.id == Participa_liga.id_liga).where(Participa_liga.id_usuario == id_usuario))
    num_usuarios = dict(db.session.execute(select(Participa_liga.id_liga, func.count(Participa_liga.id_usuario)).group_by(Participa_liga.id_liga)).fetchall())
    participa_liga = { liga_id: True for liga_id, in db.session.execute(select(Participa_liga.id_liga).where(Participa_liga.id_usuario == id_usuario)).fetchall() }
    return render_template("perfil_usuario.html", usuario=usuario, ligas=ligas_usuario, num_usuarios=num_usuarios, participa_liga=participa_liga)


@app.route('/jugadores')
def listar_jugadores():
    # Muestra una página con la lista de jugadores.
    # Devuelve como respuesta el template "lista_jugadores.html"
    # que debéis implementar vosotros mismos, el cual debe recibir
    # como parámetro una página de jugadores.
    jugadores = db.paginate(select(Jugador))
    return render_template("lista_jugadores.html", jugadores=jugadores)

@app.route('/perfil_jugador/<int:id_jugador>')
def perfil_jugador(id_jugador: int):
    # Muestra el perfil de un jugador de baloncesto.
    # Devuelve un error 404 si el id no está asociado a ningún jugador.
    # Como respuesta, renderiza el template "perfil_jugador.html".
    jugador = db.first_or_404(select(Jugador).where(Jugador.id_jugador == id_jugador))
    # Lista de tuplas (Historico, Partido) asociados a ese jugador, ordenados por fecha descendente.
    lista_historico_partido = db.session.execute(select(Historico, Partido) \
                                               .join(Historico, Partido.id_partido == Historico.id_partido) \
                                               .join(Jugador, Historico.id_jugador == Jugador.id_jugador) \
                                               .where(Jugador.id_jugador == id_jugador) \
                                               .order_by(desc(Partido.fecha)))
    return render_template("perfil_jugador.html", jugador=jugador, lista_historico_partido=lista_historico_partido)

@app.route('/ligas')
def mostrar_ligas():
    # Muestra la lista de ligas del sistema.
    # Como puede haber numerosas ligas, se utiliza la paginación de las mismas.
    # Devuelve como respuesta el template "mostrar_ligas.html".
    abort(501)


@app.route('/liga/<int:id_liga>')
def mostrar_liga(id_liga: int):
    # Muestra la liga asociada al id "id_liga".
    # Devuelve un error 404 si la liga no existe.
    # Devuelve como respuesta el template "mostrar_liga_participante.html"
    abort(501)


@app.route('/perfil/<int:id_usuario>/liga/<int:id_liga>/cartas')
def cartas_usuario_en_liga(id_usuario: int, id_liga: int):
    # Dado un usuario y una liga, se muestran las cartas de ese usuario
    # asociados a esa liga. Si no existe el id del usuario o el de la liga,
    # se lanzará un error 404.
    # Para mostrar las cartas de un usuario en una liga, utilizaremos una
    # paginacion de las mismas. Esta funcion devuelve el template
    # "mostrar_cartas_liga_participante.html."
    abort(501)


@app.route('/unirse_liga/<int:id_liga>', methods=["GET", "POST"])
def unirse_liga(id_liga: int):
    # Accion de unirse a una liga
    # Debe aceptar tanto métodos "GET" como "POST" (para introducir la contraseña).
    # Hay distintos casos en función del estado del jugador y de la liga. Para todos los casos,
    # se termina redireccionando a 'mostrar_ligas' despues de realizar las acciones pertinentes.
    #
    # * Si el usuario ya se habia unido anteriormente, hay que mandar un mensaje flash "Ya te has unido a esta liga".
    #
    # * Si la liga esta completa, mandamos el mensaje "¡La liga está al máximo!" y volvemos a redireccionar a mostrar
    #   ligas.
    #
    # * Si la liga es publica, se añade el usuario a la liga y se manda un mensaje flash
    # "Te has unido correctamente a la liga". Además, se le asigna una carta aleatoriamente al usuario actual en
    # la liga que se acaba de unir, siguiendo las reglas del enunciado.
    #
    # * Si la liga es privada, se renderiza el template "unirse_liga.html" para renderizar el formulario
    #   que introduce la contraseña. Si se valida, el usuario se añade a la liga y se manda el mismo mensaje flash
    #   que el caso anterior. También se le asigna una carta aleatoriamente.
    abort(501)


@app.route('/crear_liga', methods=["GET", "POST"])
@login_required
def crear_liga():
    # Creacion de una liga.
    # Solo los usuarios registrados pueden acceder a la creacion de ligas. Además, si un usuario ya
    # pertenece a 10 ligas, no se le permite crear una nueva. Si intenta hacerlo, redirigiremos al usuario a su perfil
    # y mandaremos un mensaje flash "Has excedido el numero máximo de ligas.".
    #
    # En caso contrario, crearemos un formulario para introducir los datos de la nueva liga, utilizando el template
    # "crear_liga.html". Los campos nombre y número máximo de participantes son obligatorios,
    # mientras que la contraseña es opcional. Se creara una liga
    # con estos datos, se registrara al creador en esa liga y se le redirigirá posteriormente a su perfil, con
    # un mensaje flash indicando que la liga se ha creado correctamente: "Se ha creado la liga correctamente".)
    num_ligas = db.session.scalars(select(func.count()).where(Participa_liga.id_usuario == current_user.id).group_by(Participa_liga.id_liga)).first()
    if num_ligas is None:
        num_ligas = 0  # Si no hay ligas, asumimos que es 0
    if num_ligas > 10:
        flash("Has excedido el numero máximo de ligas.")
        return redirect(url_for('perfil', id_usuario=current_user.id))
    else:
        nueva_liga = NuevaLiga()
        if nueva_liga.validate_on_submit():
            nombre_liga = nueva_liga.data["nombre"]
            num_max_participantes = nueva_liga.data["numero_participantes_maximo"]
            password = hash(nueva_liga.data["password"])
            liga = Liga(nombre=nombre_liga, numero_participantes_maximo=num_max_participantes, password_hash=password)
            db.session.add(liga)
            db.session.commit()
            db.session.add(Participa_liga(id_liga=liga.id, id_usuario=current_user.id))
            db.session.commit()
            flash("Se ha creado la liga correctamente")
            redirect(url_for('perfil_usuario', id_usuario=current_user.id))
        return render_template('crear_liga.html', form=nueva_liga)



@app.route("/desconexion")
@login_required
def desconectarse():
    # Desconexión de un usuario de la aplicación.
    # Hay que comprobar que el usuario estaba previamente loggeado.
    # Acciones requeridas:
    # * Hacer log-out del usuarios
    # * Mandar un mensaje flash avisando que la desconexion ha sido correcta
    # * Redireccionar a la pagina de inicio
    logout_user()
    flash('Te has desconectado.')
    return redirect(url_for('sign_in'))

@app.route("/tirada_diaria")
@login_required
def tirada_diaria():
    # Tirada diaria de cartas.
    # Hay que comprobar que el usuario estaba previamente loggeado.
    # Se debe comprobar que el usuario no ha realizado esta acción previamente en el mismo día.
    # Si la ha realizado, se redirecciona a su perfil y se muestra el
    # mensaje flash "Ya has obtenido cartas hoy, vuelve mañana."
    # En caso contrario, por cada liga en la que participa el usuario, se selecciona una carta aleatoria en
    # función de la rareza de las cartas y se le añade a las cartas del usuario. Si el usuario ya tenía esa carta,
    # se le suma uno al número de copias. Si es el cumpleaños del usuario, hay que generar una carta de cada categoría.
    # Devuelve como respuesta el template "tirada_diaria.html".
    if current_user.ultima_tirada == date.today():
        flash("Ya has obtenido cartas hoy, vuelve mañana.")
        return redirect(url_for('perfil', id_usuario=current_user.id))
    else:
        lista_liga_carta = []
        """
        participa_liga = db.session.execute(select(Participa_liga.id_liga).where(Participa_liga.id_usuario == current_user.id)).fetchall()
        for liga in participa_liga:
            carta_aleatoria = db.session.scalars(select(Carta).order_by(func.random()).limit(1)).first()
            lista_liga_carta.append((liga, carta_aleatoria))
            # FALTA METER LA CARTA EN LA TABLA CARTA_LIGA
        """
        return render_template("tirada_diaria.html", lista_liga_carta=lista_liga_carta)
