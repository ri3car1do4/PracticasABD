"""
Modulo que permite actualizar las puntuaciones de los usuarios
en las distintas ligas
"""
from typing import List
import random

from Practica2.plantilla.app.rutas import cartas_usuario_en_liga
from app import db, create_app
from app.modelos import Carta, Usuario, Liga
from sqlalchemy import select, update


def computar_puntuaciones():
    # Creo una instancia de la aplicacion para inicializar la base de datos
    flask_app = create_app()

    # Para ejecutar codigo en el contexto de la aplicacion, debemos utilizar
    # esta sentencia
    with flask_app.app_context():

        # Seleccionamos las cartas de cada usuario en cada liga
        usuarios = db.session.scalars(select(Usuario.id)).fetchall()
        for
        cartas = db.session.scalars(select(Carta.id)).fetchall()
        seleccionar_usuarios_mazos_aleatorios(cartas, usuarios, 200)


if __name__ == "__main__":
    computar_puntuaciones()