"""
Modulo para hacer cuestiones de trivia relacionadas con videos de Youtube. Creamos una clase TriviaVideo que extiende
a Trivia y almacena el id de reproduccion de video
"""

from abc import ABC, abstractmethod
from typing import List
from pathlib import Path

from.operaciones_coleccion import OperacionesEurovision
from .preguntas import Trivia


def extraer_id_url(url) -> str:
    """
    Para renderizar el juego, necesitamos extraer el id desde la url del video.
    Utilizamos expresiones regulares
    """
    try:
        return Path(url).name
    except:
        # Return id for Rick Roll
        return "dQw4w9WgXcQ"


class TriviaVideo(Trivia, ABC):
    """
    Clase abstracta que contiene los metodos que deben incorporar las preguntas asociadas a videos.
    """
    @property
    @abstractmethod
    def url(self) -> str:
        pass

    def to_dict(self):
        # Modifica el diccionario de Trivia con la url del video
        # y el tipo "video"
        super_dict = super().to_dict()
        super_dict["url"] = self.url
        # Extraemos el id de la URL
        super_dict["url_id"] = extraer_id_url(self.url)
        super_dict["tipo"] = "video"
        return super_dict


class PaisActuacion(TriviaVideo):
    """
    ¿Que pais represento la cancion?
    """
    def __init__(self, parametros: OperacionesEurovision):
        result = parametros.participacion_aleatoria(1, [
            {"$match": {"concursantes.url_youtube": {"$ne": None}}}
        ])[0]
        self._url = result["url_youtube"]
        self._respuesta = result["pais"]
        self._opciones_invalidas = parametros.paises_participantes_aleatorios(3, [
            {"$match": {"concursantes.pais": {"$ne": self._respuesta}}}
        ])

    @property
    def url(self) -> str:
        return self._url

    @property
    def pregunta(self) -> str:
        return "¿A qué país representó esta canción?"

    @property
    def opciones_invalidas(self) -> List[str]:
        return self._opciones_invalidas

    @property
    def respuesta(self) -> str:
        return self._respuesta

    @property
    def puntuacion(self) -> float:
        return 3


class NombreCancion(TriviaVideo):
    """
    ¿Cual es el titulo de esta cancion?

    NOTA: para dificultar la respuesta, se deben seleccionar canciones del mismo pais.
    """
    def __init__(self, parametros: OperacionesEurovision):
        result = parametros.participacion_aleatoria(1, [
            {"$match": {"concursantes.url_youtube": {"$ne": None}}}
        ])[0]
        self._url = result["url_youtube"]
        self._respuesta = result["cancion"]
        self._opciones_invalidas = [item["cancion"] for item in parametros.participacion_aleatoria(3, [
            {"$match": {"$and": [{"concursantes.cancion": {"$ne" : self._respuesta}}, {"concursantes.pais": result["pais"]}]}}
        ])]

    @property
    def url(self) -> str:
        return self._url

    @property
    def pregunta(self) -> str:
        return "¿Cual es el titulo de esta cancion?"

    @property
    def opciones_invalidas(self) -> List[str]:
        return self._opciones_invalidas

    @property
    def respuesta(self) -> str:
        return self._respuesta

    @property
    def puntuacion(self) -> float:
        return 2


class InterpreteCancion(TriviaVideo):
    """
    ¿Quien interpreto esta cancion?

    NOTA: para dificultar la respuesta, se deben seleccionar interpretes del mismo pais.
    """
    def __init__(self, parametros: OperacionesEurovision):
        result = parametros.participacion_aleatoria(1, [
            {"$match": {"concursantes.url_youtube": {"$ne": None}}}
        ])[0]
        self._url = result["url_youtube"]
        self._respuesta = result["artista"]
        self._opciones_invalidas = [item["artista"] for item in parametros.participacion_aleatoria(3, [
            {"$match": {"$and": [{"concursantes.artista": {"$ne" : self._respuesta}}, {"concursantes.pais": result["pais"]}]}}
        ])]

    @property
    def url(self) -> str:
        return self._url

    @property
    def pregunta(self) -> str:
        return f"¿Qué artista interpretó esta canción?"

    @property
    def opciones_invalidas(self) -> List[str]:
        return self._opciones_invalidas

    @property
    def respuesta(self) -> str:
        return self._respuesta

    @property
    def puntuacion(self) -> float:
        return 4
