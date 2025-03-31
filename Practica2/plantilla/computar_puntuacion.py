"""
Modulo que permite actualizar las puntuaciones de los usuarios
en las distintas ligas
"""
from typing import List
import random

from Practica2.plantilla.app.rutas import cartas_usuario_en_liga
from app import db, create_app
from app.modelos import Carta, Usuario, Liga, Participa_liga, Carta_liga
from sqlalchemy import select, update, and_


def computar_puntuaciones():
    # Creo una instancia de la aplicacion para inicializar la base de datos
    flask_app = create_app()

    # Para ejecutar codigo en el contexto de la aplicacion, debemos utilizar
    # esta sentencia
    with flask_app.app_context():

        # Seleccionamos las cartas de cada usuario en cada liga
        usuarios = db.session.scalars(select(Usuario.id)).fetchall()
        for usuario in usuarios:
            ligas = db.session.scalars(select(Participa_liga.id_liga).where(Participa_liga.id_usuario == usuario)).fetchall()
            for liga in ligas:
                cartas_liga = db.session.scalars(select(Carta_liga.id_jugador)
                                           .where(and_(Carta_liga.id_liga == liga, Carta_liga.id_usuario == usuario))
                                           .group_by(Carta_liga.id_jugador))
                for carta_liga in cartas_liga:
                    puntuacion_acumulada = db.session.scalars()


if __name__ == "__main__":
    computar_puntuaciones()