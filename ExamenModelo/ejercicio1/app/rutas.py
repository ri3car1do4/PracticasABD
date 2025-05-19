"""
Módulo de Python que contiene las rutas
"""
from flask import current_app as app, render_template, redirect, url_for, flash, abort
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from . import db
from .formularios import NuevoMazo, AnyadirCarta
from .modelos import Carta, Mazo, CartaEnMazo


@app.route('/')
@app.route('/cartas')
def listar_cartas():
    """
    (+0.3 ptos)

    Funcion que muestra la lista de cartas usando una paginacion,
    invocando al template "lista_cartas.html".
    Se deben mostrar 12 resultados por pagina.
    """
    abort(401)


@app.route('/crear_mazo', methods=['GET', 'POST'])
def crear_mazo():
    """
    (+0.3 ptos)

    Funcion que crea un nuevo mazo, a partir del formulario "NuevoMazo".
    Para mostrar el formulario, se invoca al template "crear_mazo.html".
    En caso de crearse un nuevo mazo de forma satisfactoria, se debe redirigir
    a la funcion de vista "listar_cartas".
    En caso contrario, se vuelve a renderizar el formulario de crear mazo.
    """
    abort(401)

@app.route('/mazo/<int:id_mazo>')
def mostrar_mazo_completo(id_mazo: int):
    """
    (+0.7 ptos)

    Dado el id de un mazo, se muestran todas las cartas asociadas a ese mazo.
    Las cartas se muestran separadas por banquillo o no banquillo.
    Si el id de mazo no existe, se debe abortar con error 404. Como resultado, debe
    renderizar el template "mazos.html".
    """
    abort(401)


@app.route('/mazos_preview/')
def mostrar_mazo_preview_global():
    """
    (+0.7 ptos)

    Funcion que muestra la lista de mazos almacenada en el sistema.
    Se deben mostrar un total de 5 mazos por pagina con una paginacion, utilizando el
    template "mazos_preview.html". Por cada mazo, se deben mostrar la informacion de solo 6 de sus cartas.
    Estas cartas se deben seleccionar por su precio de forma descendente, y en caso de empate, por su nombre.
    Si una carta tiene precio nulo, entonces se debe considerar que el precio es 0.
    """
    abort(401)


@app.route('/mazo/<int:id_mazo>/nueva_carta', methods=['GET', 'POST'])
def introducir_carta_en_mazo(id_mazo: int):
    """
    (+1 pto)

    Funcion para introducir cartas en un mazo concreto. Si el id del
    mazo no existe, se debe abortar con un error 404.

    Para introducir una nueva carta, se debe utilizar el formulario "AnyadirCarta".

    Este formulario recibe como parametro una lista con el nombre de las cartas
    que ya estan almacenadas en el mazo, para evitar volver a introducirlas.

    En caso de que el formulario se valide correctamente, se introduce una nueva carta al mazo
    con la informacion del formulario y se redirige a esta misma funcion con el mazo actual,
    para seguir introduciendo cartas. Tambien se debe actualizar la informacion
    sobre el numero de cartas en un mazo concreto. Por ultimo, se generara un mensaje flash
    indicando que se ha añadido la carta correctamente: "¡Carta añadida correctamente!".

    En caso el formulario no se valide correctamente o que la carta no exista, se debe volver a mostrar el formulario.
    """
    abort(401)
