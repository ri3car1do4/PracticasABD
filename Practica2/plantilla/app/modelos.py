"""
Modulo en el que definimos los modelos relacionales de nuestra aplicacion
"""

from typing import List
from datetime import date
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import String, Integer, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

from typing import List
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin


class Jugador(db.Model):
    """
    Jugadores de baloncesto
    """

    id_jugador: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    nombre_equipo: Mapped[str] = mapped_column(String, nullable=True)
    posicion: Mapped[str] = mapped_column(String(20), nullable=False)
    altura: Mapped[float] = mapped_column(Numeric(4, 1), nullable=False)
    peso: Mapped[float] = mapped_column(Numeric(4, 1), nullable=True)
    fecha_nacimiento: Mapped[date] = mapped_column(nullable=False)
    pais: Mapped[str] = mapped_column(String(30), nullable=False)
    url_imagen: Mapped[str] = mapped_column(String, nullable=False)

class Partido(db.Model):
    """
    Partidos de la NBA
    """

    id_partido: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[date] = mapped_column(nullable=False)
    equipo_local: Mapped[str] = mapped_column(String(30), nullable=False)
    equipo_visitante: Mapped[str] = mapped_column(String(30), nullable=False)
    gana_local: Mapped[bool] = mapped_column(Boolean, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)

class Historico(db.Model):
    """
    Historico de partidos de cada jugador
    """

    id_jugador: Mapped[int] = mapped_column(Integer, ForeignKey(Jugador.id_jugador), primary_key=True)
    id_partido: Mapped[int] = mapped_column(Integer, ForeignKey(Partido.id_partido), primary_key=True)
    tiempo_jugado: Mapped[int] = mapped_column(Integer, nullable=False)
    puntos_marcados: Mapped[int] = mapped_column(Integer, nullable=True)
    puntuacion: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False)


class Usuario(db.Model, UserMixin):
    """
    Usuarios de la aplicación
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    cumple: Mapped[date] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    ultima_tirada: Mapped[date] = mapped_column(nullable=True)

class Liga(db.Model):
    """
    Ligas de la aplicación
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False)
    numero_participantes_maximo: Mapped[int] = mapped_column(Integer, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=True)

class Participa_liga(db.Model):
    """
    Asociación Ligas con usuarios
    """

    id_liga: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True)
    puntuacion_acumulada: Mapped[float] = mapped_column(Numeric, default=0, nullable=False)

class Carta(db.Model):
    """
    Carta asociada a cada jugador
    """

    id_jugador: Mapped[int] = mapped_column(Integer, ForeignKey(Jugador.id_jugador), primary_key=True)
    puntuacion: Mapped[float] = mapped_column(Numeric(4, 1), default=0, nullable=False)
    rareza: Mapped[str] = mapped_column(String(15), nullable=False)


class Carta_liga(db.Model):
    """
    Carta de cada usuario asociada a una liga
    """

    id_liga: Mapped[int] = mapped_column(Integer, ForeignKey(Participa_liga.id_liga), primary_key=True)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey(Participa_liga.id_usuario), primary_key=True)
    id_jugador: Mapped[int] = mapped_column(Integer, ForeignKey(Carta.id_jugador), primary_key=True)
    numero_copias: Mapped[int] = mapped_column(Integer, nullable=False, default=0)