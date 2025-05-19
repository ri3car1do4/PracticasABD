from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import String, ForeignKey, Integer
from datetime import date
from typing import List

class Base(DeclarativeBase):
    pass

# nombre,precio,imagen_scryfall,url_mkm
class Cartas(Base):
    """
     * Cartas(nombre,precio,imagen_scryfall,url_mkm)
     """
    __tablename__ = "cartas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    precio: Mapped[float] = mapped_column(nullable=True)
    imagen_scryfall: Mapped[str] = mapped_column(String(400), nullable=True)
    url_mkm: Mapped[str] = mapped_column(String(400), nullable=True)