"""
Esta solucion asume que el nombre de la base de datos es 'bluesky'
y que la contraseña del proyecto es 'password'.
"""
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase
from typing import List

class GestionBluesky:

    def __init__(self):
        self._driver = self._conexion_bbdd()
        self._database = os.environ.get('DATABASE')

    def _conexion_bbdd(self):
        driver = GraphDatabase.driver(
            f"neo4j://{os.environ.get('HOST')}:{os.environ.get('PORT')}/",
            auth=(os.environ.get("USER"), os.environ.get("PASSWORD"))
        )
        # Lo incluyo para que salte excepcion si no me
        # consigo conectar
        driver.verify_connectivity()
        return driver

    def crear_cuenta(self):
        """
        Crea la cuenta de ABDucidos

        Etiqueta: la etiqueta es :Cuenta.
        Propiedades:
            * cuenta: ABDucidos.bsky.social
            * nombre: Ampliación de Bases de Datos
            * bio: Bases de Datos Relacionales, No SQL... ¡Tenemos de todo!
            * num_followers: 0
            * num_following: 0
            * num_posts: 0

        Además, introduce un post con '¡Hola mundo!'
        """
        pass

    def posts_ofensivos(self):
        """
        Vamos a reemplazar la etiqueta :Post por :PostOfensivo en aquellos posts aquellos posts que incluyan
        el siguiente vocabulario, independientemente de mayúsculas y minúsculas:
        gilipoll, subnormal, twitter y asshole. Además, para las cuentas
        que han escrito un post ofensivo, vamos a añadir la
        propiedad num_posts_ofensivos con el número de post ofensivos.
        """
        pass

    def tasa_followback(self, cuenta: str) -> float:
        """
        La tasa de followback se computa como el cociente entre
        el número de cuentas que sigue un usuario (denominador)
        y cuántas de esas cuentas le siguen también (numerador).
        Implementa una función que, dada una cuenta, compute su
        tasa de followback.
        """
        # Hay que hacer un segundo with para que no de
        # error al combinar dos agregaciones
        pass

    def posts_similares(self, palabra_clave: str) -> List[str]:
        """
        Dada una palabra clave, queremos encontrar la conexión más corta
        entre usuarios que hayan escrito algún post que incluyan esta palabra clave.
        La función `posts_similares` debe devolver la secuencia de usuarios que conectan
        a los dos usuarios con estos posts.
        """

        # Hay que tener cuidado, ya que shortestPath encuentra el camino
        # mas corto entre cualesquiera dos posts que cumplan la condicion. Tenemos que asegurarnos que
        # solo devolvemos el camino mas corto entre los caminos mas cortos de dos posts
        # cualesquiera.
        pass


if __name__ == "__main__":
    load_dotenv(override=True)

    gestion = GestionBluesky()
    # print("Crear cuenta", gestion.crear_cuenta())
    # print("Post ofensivos", gestion.posts_ofensivos())
    # cuenta = "ucm.es"
    # print(f"Tasa Followback Cuenta {cuenta}: {gestion.tasa_followback(cuenta)}")
    # print(gestion.posts_similares("obrera"))
