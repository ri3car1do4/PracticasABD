import os
import datetime
import pymongo
import random
from dotenv import load_dotenv
from typing import List, Dict, Any, Tuple
from lorem_text import lorem
from bson.objectid import ObjectId


class GestionFdIx:

    def __init__(self):
        self._connection = self._create_connection()
        self._db = self._connection["fdix"]

    def _create_connection(self):
        load_dotenv(override=True)
        return pymongo.MongoClient(f"mongodb://{os.environ.get('HOST')}:{os.environ.get('PORT')}/")

    def actualizar_nombre(self, email: str, nombre_nuevo: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Crea una función que cambie el nombre asociado a un email. Para ello, hay que
        actualizar tanto la colección de usuarios como la de comentarios. No es necesario devolver
        el resultado de las actualizaciones.
        """
        pass


    def numero_peliculas_genero(self, genero: str) -> int:
        """
        Devuelve el número de elementos que hay asociados
        a un género de película dado.
        """
        pass

    def han_comentado(self, titulo: str) -> List[Dict[str, str]]:
        """
        Devuelve la lista de usuarios (email y nombre)
        que han comentado en una película dada
        """
        pass

    def pelicula_mas_comentada(self, fecha: datetime.datetime, lista_peliculas: List[str]) -> str:
        """
        Devuelve el título de la película que tiene mayor discusión entre
        una lista de películas. Para medir la discusión, contamos cuántos
        comentarios hay asociados a esa película. El parametro "lista_peliculas"
        contiene la lista con los titulos de las peliculas.
        """
        pass

if __name__ == "__main__":
    gestion = GestionFdIx()
    # print(gestion.actualizar_nombre("sean_bean@gameofthron.es", "Ned Starkn't"))
    # print(gestion.numero_peliculas_genero("Drama"))
    # print(gestion.han_comentado("High and Dizzy"))
    # print(gestion.pelicula_mas_comentada(datetime.datetime(2015, 1, 1),
    #                                      ["The Mummy", "High and Dizzy", "Cinderella", "Shrek 2"]))

