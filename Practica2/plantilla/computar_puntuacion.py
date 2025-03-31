"""
Modulo que permite actualizar las puntuaciones de los usuarios
en las distintas ligas
"""

from app import db, create_app
from app.modelos import Carta, Usuario, Participa_liga, Carta_liga
from sqlalchemy import select, update, and_


def computar_puntuaciones():
    # Creo una instancia de la aplicacion para inicializar la base de datos
    flask_app = create_app()

    # Para ejecutar codigo en el contexto de la aplicacion, debemos utilizar
    # esta sentencia
    with flask_app.app_context():

        usuarios = db.session.scalars(select(Usuario.id)).fetchall()
        for usuario in usuarios:
            ligas = db.session.scalars(select(Participa_liga.id_liga).where(Participa_liga.id_usuario == usuario)).fetchall()
            for liga in ligas:

                cartas_liga = db.session.scalars(
                    select(Carta.puntuacion)
                    .join(Carta_liga, Carta.id_jugador == Carta_liga.id_jugador)
                    .where(and_(Carta_liga.id_liga == liga, Carta_liga.id_usuario == usuario))
                    .group_by(Carta.id_jugador)
                ).fetchall()

                puntuacion_total = sum(cartas_liga) if cartas_liga else 0

                db.session.execute(
                    update(Participa_liga)
                    .where(and_(Participa_liga.id_liga == liga, Participa_liga.id_usuario == usuario))
                    .values(puntuacion_acumulada=puntuacion_total)
                )

            db.session.commit()


if __name__ == "__main__":
    computar_puntuaciones()