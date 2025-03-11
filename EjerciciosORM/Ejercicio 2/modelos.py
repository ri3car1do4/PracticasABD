from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import String, ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint
from datetime import date
from typing import List

"""
* Usuario(<ins>id</ins>, nombre, email)
* Experto(<ins>id</ins>, pagina)
    - Experto.id -> Usuario.id
* Ocasional(<ins>id</ins>, nAccesos)
    - Ocasional.id -> Usuario.id
* Mensaje(<ins>idMensaje</ins>, <ins>idHilo</ins>, Texto, Fecha, idUsuario)
    - Mensaje.idUsuario -> Usuario.id
    - Mensaje.idHilo -> Hilo.id
* Hilo(<ins>id</ins>, asunto, idModerador)
    - Hilo.idModerador -> Experto.id
* Puntuacion(<ins>id_usuario</ins>, <ins>idMensaje</ins>, <ins>idHilo</ins>, puntuacion)
    - Puntuacion.id_usuario -> Usuario.id
    - Puntuacion.{idMensaje, idHilo} -> Mensaje.{idUsuario, idHilo}
"""
class Base(DeclarativeBase):
    pass

class Usuario(Base):
    """
    * Usuario(<ins>id</ins>, nombre, email)
    """
    __tablename__ = "Usuario"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False)

    mensajes: Mapped[List["Mensaje"]] = relationship(back_populates="usuario")
    puntuaciones: Mapped[List["Puntuacion"]] = relationship(back_populates="usuario")

    def __repr__(self):
        return f"Usuario(id={self.id}, nombre={self.nombre}, " \
               f"email={self.email})"

class Experto(Base):
    """
    * Experto(<ins>id</ins>, pagina)
        - Experto.id -> Usuario.id
    """
    __tablename__ = "Experto"

    id: Mapped[int] = mapped_column(ForeignKey(Usuario.id), primary_key=True, nullable=False)
    pagina: Mapped[str] = mapped_column(String(50), nullable=False)

    hilos: Mapped[List["Hilo"]] = relationship(back_populates="moderador")

    def __repr__(self):
        return f"Experto(id={self.id}, pagina={self.pagina})"

class Ocasional(Base):
    """
    * Ocasional(<ins>id</ins>, nAccesos)
        - Ocasional.id -> Usuario.id
    """
    __tablename__ = "Ocasional"

    id: Mapped[int] = mapped_column(ForeignKey(Usuario.id), primary_key=True, nullable=False)
    nAccesos: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self):
        return f"Ocasional(id={self.id}, nAccesos={self.nAccesos})"

class Hilo(Base):
    """
    * Hilo(<ins>id</ins>, asunto, idModerador)
        - Hilo.idModerador -> Experto.id
    """
    __tablename__= "Hilo"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    asunto: Mapped[str] = mapped_column(String(50), nullable=False)
    idModerador: Mapped[int] = mapped_column(ForeignKey(Experto.id), nullable=False)

    mensajes: Mapped[List["Mensaje"]] = relationship(back_populates="hilo")
    moderador: Mapped["Experto"] = relationship(back_populates="hilos")

    def __repr__(self):
        return f"Hilo(id={self.id}, asunto={self.asunto}, idModerador={self.idModerador})"

class Mensaje(Base):
    """
    * Mensaje(<ins>idMensaje</ins>, <ins>idHilo</ins>, Texto, Fecha, idUsuario)
        - Mensaje.idUsuario -> Usuario.id
        - Mensaje.idHilo -> Hilo.id
    """
    __tablename__= "Mensaje"
    idMensaje: Mapped[int] = mapped_column(nullable=False)
    idHilo: Mapped[int] = mapped_column(ForeignKey(Hilo.id), nullable=False)
    Texto: Mapped[str] = mapped_column(String(100), nullable=False)
    Fecha: Mapped[date] = mapped_column(nullable=False)
    idUsuario: Mapped[int] = mapped_column(ForeignKey(Usuario.id), nullable=False)

    __table_args__ = (PrimaryKeyConstraint("idMensaje", "idHilo"),)

    usuario: Mapped["Usuario"] = relationship(back_populates="mensajes")
    hilo: Mapped["Hilo"] = relationship(back_populates="mensajes")
    puntuaciones: Mapped[List["Puntuacion"]] = relationship(back_populates="mensaje")

    def __repr__(self):
        return f"Mensaje(idMensaje={self.idMensaje}, idHilo={self.idHilo}, Texto={self.Texto}, " \
                f"Fecha={self.Fecha}, idUsuario={self.idUsuario})"

class Puntuacion(Base):
    """
    * Puntuacion(<ins>id_usuario</ins>, <ins>idMensaje</ins>, <ins>idHilo</ins>, puntuacion)
        - Puntuacion.id_usuario -> Usuario.id
        - Puntuacion.{idMensaje, idHilo} -> Mensaje.{idUsuario, idHilo}
    """
    __tablename__ = "Puntuacion"
    id_usuario: Mapped[int] = mapped_column(ForeignKey(Usuario.id), nullable=False)
    idMensaje: Mapped[int] = mapped_column(nullable=False)
    idHilo: Mapped[int] = mapped_column(nullable=False)
    puntuacion: Mapped[int] = mapped_column(nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("id_usuario", "idMensaje", "idHilo"),
        ForeignKeyConstraint(["idMensaje", "idHilo"], [Mensaje.idMensaje, Mensaje.idHilo])
    )

    usuario: Mapped["Usuario"] = relationship(back_populates="puntuaciones")
    mensaje: Mapped["Mensaje"] = relationship(back_populates="puntuaciones")

    def __repr__(self):
        return f"Puntuacion(id_usuario={self.id_usuario}, idMensaje={self.idMensaje}, idHilo={self.idHilo}, " \
                f"puntuacion={self.puntuacion})"