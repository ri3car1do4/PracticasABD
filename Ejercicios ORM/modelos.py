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

    IdAlojamiento: Mapped[str] = mapped_column(String(9), primary_key=True)
    MaxPersonas: Mapped[int] = mapped_column(nullable=True)
    Propietario: Mapped[str] = mapped_column(nullable=False)
    Ciudad: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"Alojamientos(IdAlojamiento={self.IdAlojamiento}, MaxPersonas= {self.MaxPersonas}, " \
               f"Propietario={self.Propietario}, Ciudad={self.Ciudad})"

class Reservas(Base):
    """
    * Reservas(<ins>IdReserva</ins>, IdAlojamiento, FechaEntrada, FechaSalida, Precio)
    - Reserva.IdAlojamiento -> Alojamiento.IdAlojamiento
    """
    __tablename__ = "Reservas"

    IdReserva: Mapped[int] = mapped_column(primary_key=True)
    IdAlojamiento: Mapped[str] = mapped_column(String(50), nullable=False)
    FechaEntrada: Mapped[date] = mapped_column(default=0)
    FechaSalida: Mapped[date] = mapped_column(default=0)
    Precio: Mapped[float] = mapped_column(nullable=False)

    IdAlojamiento: Mapped[List["Alojamientos"]] = relationship(back_populates="Reservas")

    def __repr__(self):
        return f"Reservas(IdReserva={self.IdReserva}, IdAlojamiento={self.IdAlojamiento}, FechaEntrada= {self.FechaEntrada}, " \
               f"FechaSalida={self.FechaSalida}, Precio={self.Precio})"

class Formaliza(Base):
    """
    * Formaliza(<ins>IdReserva</ins>, <ins>DNI</ins>)
        - Formaliza.IdReserva -> Reserva.IdReserva
        - Formaliza.DNI -> Participantes.DNI
    """
    __tablename__= "Formaliza"
    IdReserva: Mapped[int] = mapped_column(primary_key=True)
    DNI: Mapped[str] = mapped_column(String(9), primary_key=True)

    IdReserva: Mapped[List["Reservas"]] = relationship(back_populates="Formaliza")
    DNI: Mapped[List["Participantes"]] = relationship(back_populates="Formaliza")

    def __repr__(self):
        return f"Formaliza(IdReserva={self.IdReserva}, DNI={self.DNI})

class Contratado(Base):
    """
    * Participantes(<ins>DNI</ins>, Nombre, Apellido, Ciudad*, FechaNacimiento*, Telefono*)
    """
    __tablename__ = "Participantes"

    DNI: Mapped[str] = mapped_column(String(9), primary_key=True)
    Nombre: Mapped[int] = mapped_column(ForeignKey(Servicio.id), primary_key=True)
    Apellido: Mapped[date] = mapped_column(nullable=False)
    Ciudad

    def __repr__(self):
        return f"Contratado(DNICliente={self.DNICliente}, idServicio={self.idServicio}, fecha={self.fecha})"
