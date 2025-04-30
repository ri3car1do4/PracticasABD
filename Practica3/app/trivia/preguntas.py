"""
Modulo que contiene diferentes modelos de consulta para la seccion de "trivia".
"""
import random
from typing import List
from abc import ABC, abstractmethod
from .operaciones_coleccion import OperacionesEurovision
from .. import mongo


# Clases para encapsular las preguntas y respuestas generadas aleatoriamente
class Trivia(ABC):
    """
    Clase abstracta con los metodos que deben implementar todas las preguntas de trivia.
    """
    @abstractmethod
    def __init__(self, parametros: OperacionesEurovision):
        # Obligamos a que todos los constructores les pasen un objeto con los parametros aleatorios
        pass

    @property
    @abstractmethod
    def pregunta(self) -> str:
        """
        Pregunta que se debe mostrar
        """
        pass

    @property
    @abstractmethod
    def opciones_invalidas(self) -> List[str]:
        """
        Lista de opciones invalidas. Deben ser exactamente 3
        """
        pass

    @property
    @abstractmethod
    def respuesta(self) -> str:
        """
        Respuesta correcta
        """
        pass

    @property
    @abstractmethod
    def puntuacion(self) -> int:
        """
        Puntuacion asociada a la pregunta
        """
        pass

    def to_dict(self):
        # Sorteamos aleatoriamente las respuestas
        respuestas = [self.respuesta, *self.opciones_invalidas]
        random.shuffle(respuestas)

        # Funcion que genera la informacion que pasamos al script de trivia en el formato adecuado
        return {"pregunta": self.pregunta,
                "correcta": respuestas.index(self.respuesta),
                "respuestas": respuestas,
                "puntuacion": self.puntuacion,
                "tipo": "pregunta"}


class PrimerAnyoParticipacion(Trivia):
    """
    Pregunta que anyo fue el primero en el que participo un pais seleccionado aleatoriamente
    """

    def __init__(self, parametros: OperacionesEurovision):
        self._pais = parametros.paises_participantes_aleatorios(1)[0]
        self._respuesta = list(parametros.agregacion([
            {"$match": {"concursantes.pais": self._pais}},
            {"$sort": {"anyo": 1}},
            {"$limit": 1},
            {"$project": {"_id": "$anyo"}}
        ]))[0]["_id"]
        self._opciones_invalidas = [item["_id"] for item in list(parametros.agregacion([
            {"$match": {"anyo": {"$ne": self._respuesta}}},
            {"$group": {"_id": "$anyo"}},
            {"$project": {"_id": 1}},
            {"$sample": {"size": 3}}
        ]))]

    @property
    def pregunta(self) -> str:
        return f"¿En qué año participó por primera vez {self._pais}?"

    @property
    def opciones_invalidas(self) -> List[str]:
        return self._opciones_invalidas

    @property
    def respuesta(self) -> str:
        return self._respuesta

    @property
    def puntuacion(self) -> int:
        """
        Puntuacion asociada a la pregunta
        """
        return 2


class CancionPais(Trivia):
    """
    Pregunta de que pais es el interprete de una cancion, dada el titulo de la cancion
    """

    def __init__(self, parametros: OperacionesEurovision):
        # Obtenemos una participacion para la respuesta
        self._cancion = parametros.participacion_aleatoria(1, [
            {"$addFields": {"concursantes": "$concursantes.cancion"}}
        ])[0]
        self._respuesta = parametros.participacion_aleatoria(1, [
            {"$match": {"concursantes.cancion": self._cancion}},
            {"$addFields": {"concursantes": "$concursantes.pais"}},
        ])[0]
        self._opciones_invalidas = parametros.participacion_aleatoria(3, [
            {"$match": {"concursantes.pais": {"$ne": self._respuesta}}},
            {"$group": {"_id": "$concursantes.pais"}},
            {"$addFields": {"concursantes": "$_id"}}
        ])

    @property
    def pregunta(self) -> str:
        return f"¿De que país es el intérprete de la canción '{self._cancion}'?"

    @property
    def opciones_invalidas(self) -> List[str]:
        return self._opciones_invalidas

    @property
    def respuesta(self) -> str:
        return self._respuesta

    @property
    def puntuacion(self) -> int:
        """
        Puntuacion asociada a la pregunta
        """
        return 1


class MejorClasificacion(Trivia):
    """
    Pregunta: ¿Que cancion/pais obtuvo la mejor posicion en un anyo dado?

    Respuesta: las respuestas deben ser de la forma cancion/pais.

    IMPORTANTE: la solucion debe ser unica. Ademas, todos las opciones
    deben haber participado el mismo anyo.
    """
    def __init__(self, parametros: OperacionesEurovision):
        self._anyo = parametros.anyo_aleatorio(1)[0]
        result = parametros.participacion_aleatoria(1, [
            {"$match": {"anyo": self._anyo}},
            {"$sort": {"concursantes.puntuacion": -1}},
            {"$limit": 1},
        ])[0]
        self._respuesta = (result["pais"], result["cancion"])
        results = parametros.participacion_aleatoria(3, [
            {"$match": {"$and": [{"anyo": self._anyo}, {"concursantes.pais": { "$ne" : result["pais"]}}]}}
        ])
        self._opciones_invalidas = [ (result["pais"], result["cancion"]) for result in results ]

    @property
    def pregunta(self) -> str:
        return f"¿Que canción/país obtuvo la mejor posición en {self._anyo}?"

    @property
    def opciones_invalidas(self) -> List[str]:
        return self._opciones_invalidas

    @property
    def respuesta(self) -> str:
        return self._respuesta

    @property
    def puntuacion(self) -> int:
        return 3


class MejorMediaPuntos(Trivia):
    """
    Pregunta que pais ha tenido mejor media de resultados en un periodo determinado.

    IMPORTANTE: la solucion debe ser unica.
    """
    def __init__(self, parametros: OperacionesEurovision):
        self._anyo_inicial = parametros.anyo_aleatorio(1, [
            {"$match": {"anyo": {"$lt": 2022}}}
        ])[0]
        self._anyo_final = parametros.anyo_aleatorio(1, [
            {"$match": {"anyo": {"$gt": self._anyo_inicial}}}
        ])[0]
        self._respuesta = parametros.participacion_aleatoria(1, [
            {"$match": {"$and": [{"anyo": {"$gte": self._anyo_inicial}}, {"anyo": {"$lte": self._anyo_final}}]}},
            {"$group": {"_id": "$concursantes.pais", "media": {"$avg": "$concursantes.puntuacion"}}},
            {"$sort": {"media": -1}},
            {"$limit": 1},
            {"$addFields": {"concursantes": "$_id"}},
        ])[0]
        self._opciones_invalidas = parametros.participacion_aleatoria(3, [
            {"$match": {"$and": [{"anyo": {"$gte": self._anyo_inicial}}, {"anyo": {"$lte": self._anyo_final}}]}},
            {"$group": { "_id": "$concursantes.pais", "media": {"$avg": "$concursantes.puntuacion"}}},
            {"$addFields": {"concursantes": "$_id"}},
            {"$match": {"concursantes": {"$ne": self._respuesta}}}
        ])

    @property
    def pregunta(self) -> str:
        return f"¿Qué país quedó mejor posicionado de media entre los años {self._anyo_inicial} y {self._anyo_final}?"

    @property
    def opciones_invalidas(self) -> List[str]:
        return self._opciones_invalidas

    @property
    def respuesta(self) -> str:
        return self._respuesta

    @property
    def puntuacion(self) -> int:
        return 4
