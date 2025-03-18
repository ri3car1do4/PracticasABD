"""
Modulo en el que definimos los modelos relacionales de nuestra aplicacion
"""

from typing import List
import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import String, Integer, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

from typing import List
import datetime
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
    fecha_nacimiento: Mapped[datetime.date] = mapped_column(nullable=False)
    pais: Mapped[str] = mapped_column(String(30), nullable=False)
    url_imagen: Mapped[str] = mapped_column(String, nullable=False)
