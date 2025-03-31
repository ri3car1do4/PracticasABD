"""
Modulo que permite introducir la información y los resultados de los partidos
y los introduce en la base de datos
"""
import csv
import os

from app import db, create_app
from app.modelos import Partido, Historico

def anyadir_resultados(lista_partidos):
    flask_app = create_app()

    with flask_app.app_context():
        with open(lista_partidos, newline='', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            next(lector)

            partidos = [
                Partido(
                    id_partido=fila[0],
                    fecha=fila[1],
                    equipo_local=fila[2],
                    equipo_visitante=fila[3],
                    gana_local=(fila[4].strip() == "t"),
                    url=fila[5]
                )
                for fila in lector
            ]

        db.session.add_all(partidos)
        db.session.commit()

def anyadir_historico(lista_historico):
    flask_app = create_app()

    with flask_app.app_context():
        with open(lista_historico, newline='', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            next(lector)

            historicos = [
                Historico(
                    id_partido=fila[0],
                    id_jugador=fila[1],
                    tiempo_jugado=fila[2],
                    puntos_marcados=fila[3],
                    puntuacion=fila[4],
                )
                for fila in lector
            ]

        db.session.add_all(historicos)
        db.session.commit()

if __name__ == "__main__":
    RUTA_ACTUAL = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    anyadir_resultados(os.path.join(RUTA_ACTUAL, "partido2.csv"))
    anyadir_historico(os.path.join(RUTA_ACTUAL, "historico2.csv"))