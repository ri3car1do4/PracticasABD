from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import String, ForeignKey
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

    def __repr__(self):
        return f"Reservas(id={self.id}, pagina={self.pagina})"

class Participantes(Base):
    """
    * Participantes(<ins>DNI</ins>, Nombre, Apellido, Ciudad*, FechaNacimiento*, Telefono*)
    """
    __tablename__ = "Participantes"

    DNI: Mapped[str] = mapped_column(String(9), primary_key=True, nullable=False)
    Nombre: Mapped[str] = mapped_column(String(30), nullable=False)
    Apellido: Mapped[str] = mapped_column(String(30), nullable=False)
    Ciudad: Mapped[str] = mapped_column(String(20), nullable=True)
    FechaNacimiento: Mapped[date] = mapped_column(nullable=True)
    Telefono: Mapped[int] = mapped_column(nullable=True)

    def __repr__(self):
        return f"Participantes(DNI={self.DNI}, Nombre={self.Nombre}, Apellid={self.Apellido}), Ciudad={self.Ciudad}, " \
               f"FechaNacimiento={self.FechaNacimiento}, Telefono={self.Telefono})"

class Formaliza(Base):
    """
    * Formaliza(<ins>IdReserva</ins>, <ins>DNI</ins>)
        - Formaliza.IdReserva -> Reserva.IdReserva
        - Formaliza.DNI -> Participantes.DNI
    """
    __tablename__= "Formaliza"
    IdReserva: Mapped[int] = mapped_column(ForeignKey(Reservas.IdReserva), primary_key=True, nullable=False)
    DNI: Mapped[str] = mapped_column(String(9), ForeignKey(Participantes.DNI), primary_key=True, nullable=False)

    def __repr__(self):
        return f"Formaliza(IdReserva={self.IdReserva}, DNI={self.DNI})"

