from typing import List
from . import db
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Carta(db.Model):
    """
    Cartas de MTG
    """
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    nombre = None
    precio = None
    imagen_scryfall = None
    url_mkm = None


class Mazo(db.Model):
    """
    Mazo de Cartas
    """
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    nombre = None
    num_cartas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class CartaEnMazo(db.Model):
    """
    Representa que una carta está en un mazo, el número de copias asociada, y si está en el banquillo o no.
    """
    id_carta = None
    id_mazo = None
    numero_copias = None
    banquillo = None
