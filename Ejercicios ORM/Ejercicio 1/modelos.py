from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import String, ForeignKey
from datetime import date
from typing import List

"""
* Alojamientos(<ins>IdAlojamiento</ins>, MaxPersonas*, Propietario, Ciudad)
* Reservas(<ins>IdReserva</ins>, IdAlojamiento, FechaEntrada, FechaSalida, Precio)
    - Reserva.IdAlojamiento -> Alojamiento.IdAlojamiento
* Formaliza(<ins>IdReserva</ins>, <ins>DNI</ins>)
    - Formaliza.IdReserva -> Reserva.IdReserva
    - Formaliza.DNI -> Participantes.DNI
* Participantes(<ins>DNI</ins>, Nombre, Apellido, Ciudad*, FechaNacimiento*, Telefono*)
"""
class Base(DeclarativeBase):
    pass

class Alojamientos(Base):
    """
    * Alojamientos(<ins>IdAlojamiento</ins>, MaxPersonas*, Propietario, Ciudad)
    """
    __tablename__ = "Alojamientos"

    IdAlojamiento: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    MaxPersonas: Mapped[int] = mapped_column(nullable=True)
    Propietario: Mapped[str] = mapped_column(String(30), nullable=False)
    Ciudad: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self):
        return f"Alojamientos(IdAlojamiento={self.IdAlojamiento}, MaxPersonas= {self.MaxPersonas}, " \
               f"Propietario={self.Propietario}, Ciudad={self.Ciudad})"

class Reservas(Base):
    """
    * Reservas(<ins>IdReserva</ins>, IdAlojamiento, FechaEntrada, FechaSalida, Precio)
    - Reserva.IdAlojamiento -> Alojamiento.IdAlojamiento
    """
    __tablename__ = "Reservas"

    IdReserva: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    IdAlojamiento: Mapped[int] = mapped_column(ForeignKey(Alojamientos.IdAlojamiento), nullable=False)
    FechaEntrada: Mapped[date] = mapped_column(nullable=False)
    FechaSalida: Mapped[date] = mapped_column(nullable=False)
    Precio: Mapped[float] = mapped_column(nullable=False)

    def __repr__(self):
        return f"Reservas(IdReserva={self.IdReserva}, IdAlojamiento={self.IdAlojamiento}, FechaEntrada= {self.FechaEntrada}, " \
               f"FechaSalida={self.FechaSalida}, Precio={self.Precio})"

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

