from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import String, ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint
from datetime import date
from typing import List

"""
* Alojamiento(<ins>ID</ins>, nombre, calle, numero, codPostal)
* Persona(<ins>NIF</ins>, nombre)
* Agencia(<ins>NIF</ins>, localidad)
* Hotel(<ins>ID</ins>, restaurante, NIF_agencia)
    - Hotel.ID -> Alojamiento.ID
    - Hotel.NIF_agencia -> Agencia.NIF
* Habitacion(<ins>ID_hotel</ins>, <ins>numero</ins>, n_huespedes, tipo)
    - Habitacion.ID_hotel -> Hotel.ID
* Apartamento(<ins>ID</ins>, n_huespedes, NIF)
    - Apartamento.ID -> Alojamiento.ID
    - Apartamento.NIF -> Persona.NIF
* Reserva(<ins>codigo</ins>, ID_alojamiento, precio, entrada, salida)
    - Reserva.ID_alojamiento -> Alojamiento.ID
    - Reserva.NIF_persona -> Persona.NIF
* Huesped(<ins>NIF</ins>, <ins>codigo</ins>):
    - Huesped.NIF -> Persona.NIF
    - Huesped.codigo -> Reserva.codigo
* Acuerda(<ins>ID_hotel</ins>, <ins>ID_apartamento</ins>)
    - Acuerda.ID_hotel -> Hotel.ID
    - Acuerda.ID_apartamento -> Apartamento.ID
* Oferta(<ins>NIF_agencia</ins>, <ins>ID_hotel</ins>, descuento)
    - Oferta.NIF_agencia -> Agencia.NIF
    - Oferta.ID_hotel -> Hotel.ID
"""
class Base(DeclarativeBase):
    pass

class Alojamiento(Base):
    """
    * Alojamiento(<ins>ID</ins>, nombre, calle, numero, codPostal)
    """
    __tablename__ = "Alojamiento"

    ID: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(20), nullable=False)
    calle: Mapped[str] = mapped_column(String(30), nullable=False)
    numero: Mapped[int] = mapped_column(nullable=False)
    codPostal: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self):
        return f"Alojamiento(ID={self.ID}, nombre={self.nombre}, " \
               f"calle={self.calle}, numero={self.numero}, " \
               f"codPostal={self.codPostal})"

class Persona(Base):
    """
    * Persona(<ins>NIF</ins>, nombre)
    """
    __tablename__ = "Persona"

    NIF: Mapped[str] = mapped_column(String(9), rimary_key=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self):
        return f"Persona(NIF={self.NIF}, nombre={self.nombre})"

class Agencia(Base):
    """
    * Agencia(<ins>NIF</ins>, localidad)
    """
    __tablename__ = "Agencia"

    NIF: Mapped[str] = mapped_column(String(9), primary_key=True, nullable=False)
    localidad: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self):
        return f"Agencia(NIF={self.NIF}, localidad={self.localidad})"

class Hotel(Base):
    """
    * Hotel(<ins>ID</ins>, restaurante, NIF_agencia)
        - Hotel.ID -> Alojamiento.ID
        - Hotel.NIF_agencia -> Agencia.NIF
    """
    __tablename__ = "Hotel"

    ID: Mapped[int] = mapped_column(ForeignKey(Alojamiento.ID), primary_key=True, nullable=False)
    restaurante: Mapped[str] = mapped_column(String(20), nullable=False)
    NIF_agencia: Mapped[str] = mapped_column(ForeignKey(Agencia.NIF), String(9), nullable=False)

    def __repr__(self):
        return f"Hotel(ID={self.ID}, restaurante={self.restaurante}, NIF_agencia={self.NIF_agencia})"

class Habitacion(Base):
    """
    * Habitacion(<ins>ID_hotel</ins>, <ins>numero</ins>, n_huespedes, tipo)
        - Habitacion.ID_hotel -> Hotel.ID
    """
    __tablename__= "Habitacion"
    ID_hotel: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    numero: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    n_huespedes: Mapped[int] = mapped_column(nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self):
        return f"Habitacion(ID_hotel={self.ID_hotel}, numero={self.numero}, n_huespedes={self.n_huespedes}, " \
               f"tipo={self.tipo})"

class Apartamento(Base):
    """
    * Apartamento(<ins>ID</ins>, n_huespedes, NIF)
        - Apartamento.ID -> Alojamiento.ID
        - Apartamento.NIF -> Persona.NIF
    """
    __tablename__= "Apartamento"
    ID: Mapped[int] = mapped_column(ForeignKey(Alojamiento.ID), primary_key=True, nullable=False)
    n_huspedes: Mapped[int] = mapped_column(nullable=False)
    NIF: Mapped[str] = mapped_column(ForeignKey(Persona.NIF), String(9), nullable=False)

    def __repr__(self):
        return f"Apartamento(ID={self.ID}, n_huespedes={self.n_huspedes}, NIF={self.NIF})"

class Reserva(Base):
    """
    * Reserva(<ins>codigo</ins>, ID_alojamiento, precio, entrada, salida)
        - Reserva.ID_alojamiento -> Alojamiento.ID
        - Reserva.NIF_persona -> Persona.NIF
    """
    __tablename__ = "Reserva"
    codigo: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    ID_alojamiento: Mapped[int] = mapped_column(ForeignKey(Alojamiento.ID), nullable=False)
    NIF_persona: Mapped[str] = mapped_column(ForeignKey(Persona.NIF), String(9), nullable=False)
    precio: Mapped[float] = mapped_column(nullable=False)
    entrada: Mapped[date] = mapped_column(nullable=False)
    salida: Mapped[date] = mapped_column(nullable=False)

    def __repr__(self):
        return f"Reserva(codigo={self.codigo}, ID_alojamiento={self.ID_alojamiento}, NIF_persona={self.NIF_persona}, " \
                f"precio={self.precio}, entrada={self.entrada}, salida={self.salida})"

class Huesped(Base):
    """
    * Huesped(<ins>NIF</ins>, <ins>codigo</ins>):
        - Huesped.NIF -> Persona.NIF
        - Huesped.codigo -> Reserva.codigo
    """
    __tablename__ = "Huesped"
    NIF: Mapped[str] = mapped_column(ForeignKey(Persona.NIF), String(9), primary_key=True, nullable=False)
    codigo: Mapped[int] = mapped_column(ForeignKey(Reserva.codigo), primary_key=True, nullable=False)

    def __repr__(self):
        return f"Huesped(NIF={self.NIF}, codigo={self.codigo})"

class Acuerda(Base):
    """
    * Acuerda(<ins>ID_hotel</ins>, <ins>ID_apartamento</ins>)
        - Acuerda.ID_hotel -> Hotel.ID
        - Acuerda.ID_apartamento -> Apartamento.ID
    """
    __tablename__ = "Acuerda"
    ID_hotel: Mapped[int] = mapped_column(ForeignKey(Hotel.ID), primary_key=True, nullable=False)
    ID_apartamento: Mapped[int] = mapped_column(ForeignKey(Apartamento.ID), primary_key=True, nullable=False)

    def __repr__(self):
        return f"Acuerda(ID_hotel={self.ID_hotel}, ID_apartamento={self.ID_apartamento})"

class Oferta(Base):
    """
    * Oferta(<ins>NIF_agencia</ins>, <ins>ID_hotel</ins>, descuento)
        - Oferta.NIF_agencia -> Agencia.NIF
        - Oferta.ID_hotel -> Hotel.ID
    """
    __tablename__ = "Oferta"
    ID_agencia: Mapped[str] = mapped_column(ForeignKey(Agencia.NIF), String(9), primary_key=True, nullable=False)
    ID_hotel: Mapped[int] = mapped_column(ForeignKey(Hotel.ID), primary_key=True, nullable=False)
    descuento: Mapped[float] = mapped_column(nullable=False)

    def __repr__(self):
        return f"Oferta(ID_hotel={self.ID_hotel}, ID_apartamento={self.ID_apartamento})"