from itertools import count

from flake8.defaults import NOQA_FILE
from jmespath.ast import and_expression
from numba.core.utils import order_by_target_specificity
from requests import session
from sqlalchemy import create_engine, text, select, update, func, and_
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from modelos import Base, Alojamientos, Reservas, Formaliza, Participantes
import datetime
from typing import Optional, List, Tuple


class GestionHotel:

    def __init__(self):
        self._engine = self._carga_engine()

    def _carga_engine(self):
        load_dotenv(override=True)

        user = os.environ.get("USER")
        password = os.environ.get("PASSWORD")
        host = os.environ.get("HOST")
        database = os.environ.get("DATABASE")

        conexion_str = f"postgresql+psycopg2://{user}:{password}@{host}/{database}"
        engine = create_engine(conexion_str, echo=True)
        return engine

    def crea_tablas(self):
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)

    def inserta_alojamiento(self, idAlojamiento: int, maxPersonas: Optional[int], propietario: str, ciudad: str) -> None:
        alojamiento = Alojamientos(IdAlojamiento=idAlojamiento, MaxPersonas=maxPersonas, Propietario=propietario, Ciudad=ciudad)
        with Session(self._engine) as session:
            session.add(alojamiento)
            session.commit()

    def inserta_reserva(self, idReserva: int, idAlojamiento: int, fechaEntrada: datetime.date, fechaSalida: datetime.date,
                            precio: float) -> None:
        reserva = Reservas(IdReserva=idReserva, IdAlojamiento=idAlojamiento, FechaEntrada=fechaEntrada,
                                   FechaSalida=fechaSalida, Precio=precio)
        with Session(self._engine) as session:
            session.add(reserva)
            session.commit()

    def inserta_formaliza(self, idReserva: int, dni: str) -> None:
        formaliza = Formaliza(IdReserva=idReserva, DNI=dni)
        with Session(self._engine) as session:
            session.add(formaliza)
            session.commit()

    def inserta_participante(self, dni: str, nombre: str, apellido: str, ciudad: Optional[str],
                             fechaNacimiento: Optional[datetime.date], telefono: Optional[int]) -> None:
        participante = Participantes(DNI=dni, Nombre=nombre, Apellido=apellido, Ciudad=ciudad,
                                     FechaNacimiento=fechaNacimiento, Telefono=telefono)
        with Session(self._engine) as session:
            session.add(participante)
            session.commit()

    def misma_ciudad(self):
        with Session(self._engine) as session:
            statetment = select(Participantes.Nombre, Participantes.Apellido) \
                         .join_from(Alojamientos, Reservas, Alojamientos.IdAlojamiento == Reservas.IdAlojamiento) \
                         .join(Formaliza, Reservas.IdReserva == Formaliza.IdReserva) \
                         .join(Participantes, Formaliza.DNI == Participantes.DNI) \
                         .where(Participantes.Ciudad.isnot(None)) \
                         .where(Participantes.Ciudad == Alojamientos.Ciudad) \
                         .order_by(Participantes.Apellido.asc())
            query = session.execute(statetment)
            for resultado in query.fetchall():
                print(resultado)

    def informacion_reservas(self):
        with Session(self._engine) as session:
            statetment = select(Participantes.Nombre, Participantes.Apellido,
                                func.coalesce(func.count(Reservas.IdReserva), 0),
                                func.coalesce(func.count(Alojamientos.Ciudad), 0),
                                func.coalesce(func.sum(Reservas.Precio), 0)) \
                         .outerjoin_from(Participantes, Formaliza, Participantes.DNI == Formaliza.DNI) \
                         .outerjoin(Reservas, Formaliza.IdReserva == Reservas.IdReserva) \
                         .outerjoin(Alojamientos, Reservas.IdAlojamiento == Alojamientos.IdAlojamiento) \
                         .group_by(Participantes.DNI)
            query = session.execute(statetment)
            for resultado in query.fetchall():
                print(resultado)

    def reservas_no_formalizadas(self):
        with Session(self._engine) as session:
            statetment = select(Reservas.IdReserva, Reservas.Precio) \
                         .outerjoin_from(Reservas, Formaliza, Reservas.IdReserva == Formaliza.IdReserva) \
                         .where(Formaliza.DNI.is_(None)) \
                         .order_by(Reservas.Precio)
            query = session.execute(statetment)
            for resultado in query.fetchall():
                print(resultado)

    def sin_reservas(self, fecha: datetime.date):
        with Session(self._engine) as session:
            statetment = select(Alojamientos.IdAlojamiento, func.coalesce(Alojamientos.MaxPersonas, 0), Alojamientos.Ciudad) \
                         .outerjoin_from(Alojamientos, Reservas, and_(Alojamientos.IdAlojamiento == Reservas.IdAlojamiento,
                                         Reservas.FechaEntrada <= fecha, Reservas.FechaSalida >= fecha)) \
                         .where(Reservas.IdReserva.is_(None))
            query = session.execute(statetment)
            for resultado in query.fetchall():
                print(resultado)

    def mas_reservas_anyo(self, anyo: int):
        with Session(self._engine) as session:
            statetment = select(Alojamientos.Ciudad, func.count()) \
                         .join_from(Alojamientos, Reservas, and_(Alojamientos.IdAlojamiento == Reservas.IdAlojamiento)) \
                         .where(func.extract('year', Reservas.FechaEntrada) == anyo) \
                         .group_by(Alojamientos.Ciudad) \
                         .order_by(func.count().desc()) \
                         .limit(1)
            query = session.execute(statetment)
            for resultado in query.fetchall():
                print(resultado)

    def listar_alojameintos(self, ciudad: str):
        with Session(self._engine) as session:
            statetment = select(Alojamientos.IdAlojamiento, Alojamientos.Propietario) \
                         .select_from(Alojamientos) \
                         .where(Alojamientos.Ciudad == ciudad)
            query = session.execute(statetment)
            alojamientos = query.fetchall()
            # session scalars options query fetchall: reservas = alojamientos.reservas (ahorrar consultas)
        if len(alojamientos) > 0:
            print(f"Número de Alojamientos de {ciudad}: {len(alojamientos)}\n---")
            for alojamiento in alojamientos:
                print(f"Alojamiento: {alojamiento[0]} Propietario: {alojamiento[1]}")
                with Session(self._engine) as session:
                    alojamiento.reservas
                    statetment = select(Reservas.IdReserva, Reservas.FechaEntrada, Reservas.Precio) \
                        .select_from(Reservas) \
                        .where(Reservas.IdAlojamiento == alojamiento[0]) \
                        .order_by(Reservas.FechaEntrada)
                    query = session.execute(statetment)
                    reservas = query.fetchall()
                precio = 0
                if len(reservas) > 0:
                    for reserva in reservas:
                        print(f"ID: {reserva[0]} FechaEntrada: {reserva[1]} Precio: {reserva[2]}")
                        precio += reserva[2]
                print("---")
                print(f"Total reservas: {len(reservas)} Total Precio: {precio}\n---")
        else:
            print("No hay alojamientos en la ciudad")

    def aplicar_descuento(self, propietario: str, fecha_inicio: datetime.date, fecha_fin: datetime.date, descuento: float):
        descuento_aplicado = None
        with (Session(self._engine) as session):
            statetment = select(Reservas.IdReserva, Reservas.Precio) \
                         .join_from(Reservas, Alojamientos, Reservas.IdAlojamiento == Alojamientos.IdAlojamiento) \
                         .where(Alojamientos.Propietario == propietario) \
                         .where(Reservas.FechaEntrada <= fecha_fin) \
                         .where(Reservas.FechaSalida >= fecha_inicio)
            query = session.execute(statetment)
            reservas = query.fetchall()
            if reservas:
                with Session(self._engine) as session:
                    subquery = select(Reservas.IdReserva) \
                               .join_from(Reservas, Alojamientos, Reservas.IdAlojamiento == Alojamientos.IdAlojamiento) \
                               .where(Alojamientos.Propietario == propietario) \
                               .where(Alojamientos.Propietario == propietario) \
                               .where(Reservas.FechaEntrada <= fecha_fin) \
                               .where(Reservas.FechaSalida >= fecha_inicio)
                    statetment = update(Reservas) \
                                 .where(Reservas.IdReserva.in_(subquery)) \
                                 .values(Precio= Reservas.Precio - (Reservas.Precio * descuento/100))
                    query = session.execute(statetment)
                    statetment = select(Reservas.IdReserva, Reservas.Precio) \
                        .join_from(Reservas, Alojamientos, Reservas.IdAlojamiento == Alojamientos.IdAlojamiento) \
                        .where(Alojamientos.Propietario == propietario) \
                        .where(Reservas.FechaEntrada <= fecha_fin) \
                        .where(Reservas.FechaSalida >= fecha_inicio)
                    query = session.execute(statetment)
                    descuento_aplicado = query.fetchall()
                    # session.commit()
            if descuento_aplicado is not None:
                print(f"Descuento aplicado a la Reserva: {descuento_aplicado[0][0]} en {propietario} con descuento de {descuento} "
                      f"entre {fecha_inicio} y {fecha_fin}.\nPrecio ahora: {descuento_aplicado[0][1]}")
            else:
                print("No hay descuentos por estas fecha.")


if __name__ == "__main__":
    gestion_tabla = GestionHotel()
    gestion_tabla.crea_tablas()
    gestion_tabla.inserta_alojamiento(1, 4, 'Pensiones Loli', 'Madrid')
    gestion_tabla.inserta_alojamiento(2, None, 'Laura Gomez', 'Barcelona')
    gestion_tabla.inserta_alojamiento(3, 2, 'Carlos Ruiz', 'Sevilla')
    gestion_tabla.inserta_alojamiento(4, 8, 'Ana Lopez', 'Valencia')
    gestion_tabla.inserta_alojamiento(5, 3, 'Maria Fernandez', 'Granada')
    gestion_tabla.inserta_alojamiento(6, None, 'Juan Perez', 'Madrid')

    gestion_tabla.inserta_reserva(100, 1, datetime.date(2025, 5, 20), datetime.date(2025, 5, 25), 900)
    gestion_tabla.inserta_reserva(101, 1, datetime.date(2024, 1, 20), datetime.date(2024, 1, 25), 400)
    gestion_tabla.inserta_reserva(102, 2, datetime.date(2023, 2, 1), datetime.date(2023, 2, 5), 500)
    gestion_tabla.inserta_reserva(103, 3, datetime.date(2022, 3, 10), datetime.date(2022, 3, 12), 200)
    gestion_tabla.inserta_reserva(104, 3, datetime.date(2021, 4, 15), datetime.date(2021, 4, 20), 800)
    gestion_tabla.inserta_reserva(105, 4, datetime.date(2021, 5, 5), datetime.date(2021, 5, 10), 300)
    gestion_tabla.inserta_reserva(106, 4, datetime.date(2023, 5, 10), datetime.date(2024, 1, 2), 100)

    gestion_tabla.inserta_participante('12345678A', 'Luis', 'Martinez', 'Madrid', datetime.date(1985, 7, 14), 600123456)
    gestion_tabla.inserta_participante('23456789B', 'Elena', 'Sanchez', None, None, None)
    gestion_tabla.inserta_participante('34567890C', 'Miguel', 'García', 'Sevilla', None, 602345678)
    gestion_tabla.inserta_participante('45678901D', 'Sofía', 'Lopez', None, datetime.date(1995, 1, 30), 603456789)
    gestion_tabla.inserta_participante('56789012E', 'Pablo', 'Hernandez', 'Granada', datetime.date(2000, 9, 19), 604567890)
    gestion_tabla.inserta_participante('11111111F', 'Juan Carlos', 'Redondo', None, datetime.date(2005, 1, 30), 612345678)

    gestion_tabla.inserta_formaliza(101, '12345678A')
    gestion_tabla.inserta_formaliza(101, '23456789B')
    gestion_tabla.inserta_formaliza(102, '23456789B')
    gestion_tabla.inserta_formaliza(103, '34567890C')
    gestion_tabla.inserta_formaliza(104, '45678901D')
    gestion_tabla.inserta_formaliza(105, '56789012E')
    gestion_tabla.inserta_formaliza(105, '45678901D')

    # gestion_tabla.misma_ciudad()
    # gestion_tabla.informacion_reservas()
    # gestion_tabla.reservas_no_formalizadas()
    # gestion_tabla.sin_reservas(datetime.date(2025, 5, 21))
    # gestion_tabla.mas_reservas_anyo(2021)
    # gestion_tabla.listar_alojameintos('Madrid')
    gestion_tabla.aplicar_descuento("Pensiones Loli", datetime.date(2025, 5, 1),
                                     datetime.date(2025, 5, 31), 12.5)
    gestion_tabla.aplicar_descuento("Pensiones Loli", datetime.date(2025, 1, 1),
                                    datetime.date(2025, 1, 31), 12.5)