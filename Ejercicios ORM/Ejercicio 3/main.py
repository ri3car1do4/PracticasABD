from itertools import count

# from dask.array import delete
from flake8.defaults import NOQA_FILE
from jmespath.ast import and_expression
from numba.core.utils import order_by_target_specificity
from requests import session
from sqlalchemy import create_engine, text, select, update, func, and_, desc, delete
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from modelos import Base, Alojamiento, Persona, Agencia, Hotel, Habitacion, Apartamento, Reserva, Huesped, Acuerda, Oferta
import datetime
from typing import Optional, List, Tuple


class GestionAlojamientos:

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

    def inserta_alojamiento(self, param, param1, param2, param3, param4):
        alojamiento = Alojamiento(ID=param, nombre=param1, calle=param2, numero=param3, codPostal=param4)
        with Session(self._engine) as session:
            session.add(alojamiento)
            session.commit()

    def inserta_persona(self, param, param1):
        persona = Persona(NIF=param, nombre=param1)
        with Session(self._engine) as session:
            session.add(persona)
            session.commit()

    def inserta_agencia(self, param, param1):
        agencia = Agencia(NIF=param, localidad=param1)
        with Session(self._engine) as session:
            session.add(agencia)
            session.commit()

    def inserta_hotel(self, param, param1, param2):
        hotel = Hotel(ID=param, restaurante=param1, NIF_agencia=param2)
        with Session(self._engine) as session:
            session.add(hotel)
            session.commit()

    def inserta_habitacion(self, param, param1, param2, param3):
        habitacion = Habitacion(ID_hotel=param, numero=param1, n_huespedes=param2, tipo=param3)
        with Session(self._engine) as session:
            session.add(habitacion)
            session.commit()

    def inserta_apartamento(self, param, param1, param2):
        apartamento = Apartamento(ID=param, n_huespedes=param1, NIF=param2)
        with Session(self._engine) as session:
            session.add(apartamento)
            session.commit()

    def inserta_reserva(self, param, param1, param2, param3, param4, param5):
        reserva = Reserva(codigo=param, ID_alojamiento=param1, precio=param2, entrada=param3, salida=param4, NIF_persona=param5)
        with Session(self._engine) as session:
            session.add(reserva)
            session.commit()

    def inserta_huesped(self, param, param1):
        huesped = Huesped(NIF=param, codigo=param1)
        with Session(self._engine) as session:
            session.add(huesped)
            session.commit()

    def inserta_acuerda(self, param, param1):
        acuerda = Acuerda(ID_hotel=param, ID_apartamento=param1)
        with Session(self._engine) as session:
            session.add(acuerda)
            session.commit()

    def inserta_oferta(self, param, param1, param2):
        oferta = Oferta(NIF_agencia=param, ID_hotel=param1, descuento=param2)
        with Session(self._engine) as session:
            session.add(oferta)
            session.commit()

    def hoteles_agencia_localidad(self, localidad: str) -> List[str]:
        """
        Devuelve el nombre de todos los hoteles tales que existe una agencia en la localidad dada que ofrece alguna oferta en ese hotel.
        """
        hoteles = []
        with Session(self._engine) as session:
            statetment = select(Alojamiento.nombre) \
                         .join_from(Alojamiento, Hotel, Alojamiento.ID == Hotel.ID) \
                         .join(Agencia, Hotel.NIF_agencia == Agencia.NIF) \
                         .where(Agencia.localidad == localidad)
            query = session.execute(statetment)
            for hotel in query.fetchall():
                hoteles.append(hotel)

        return hoteles

    def restaurantes_codigo_postal(self, codigo_postal: str) -> List[str]:
        """
        Devueve la lista de restaurantes asociadas a un código postal.
        """
        restaurantes = []
        with Session(self._engine) as session:
            statetment = select(Hotel.restaurante) \
                         .join_from(Alojamiento, Hotel, Alojamiento.ID == Hotel.ID) \
                         .where(Alojamiento.codPostal == codigo_postal)
            query = session.execute(statetment)
            for restaurante in query.fetchall():
                restaurantes.append(restaurante)

        return restaurantes

    def grandes_tenedores(self) -> List[Persona]:
        """
        Devueve la lista de personas que son al menos dueños de un total de 5 apartamentos.
        """
        with Session(self._engine) as session:
            statetment = select(Persona) \
                         .join(Apartamento, Persona.NIF == Apartamento.NIF) \
                         .group_by(Persona.NIF) \
                         .having(func.count(Apartamento.ID) >= 5)
            personas = session.execute(statetment).scalars().all()

        return personas

    def elimina_alojamiento_ilegal(self, id_alojamiento) -> List[str]:
        """
        Dado el ID de un alojamiento ilegal, elimina ese alojamiento de la base de datos y sus datos relacionados; y devuelve la lista de NIFs de personas que tenían una reserva de ese alojamiento (a partir de hoy). Tenéis dos opciones para eliminar toda la información relacionada (os recomiendo probar las dos):

        - Podéis fijar "ON DELETE CASCADE" al construir la tabla en las foreign keys (investigad cómo se especifica). Cuando borréis el alojamiento correspondiente, comprobad que las eliminaciones se propagan.
        - Otra opción es operar directamente desde la ORM.
        """
        with Session(self._engine) as session:
            statetment = select(Persona.NIF) \
                         .join(Reserva, Persona.NIF == Reserva.NIF_persona) \
                         .where(Reserva.ID_alojamiento == id_alojamiento) \
                         .where(Reserva.entrada >= datetime.date.today())
            personas = session.execute(statetment).scalars().all()
            # Eliminar registros dependientes manualmente antes de eliminar el Alojamiento...
            session.execute(delete(Alojamiento).where(Alojamiento.ID == id_alojamiento))
            # session.commit()

        return personas

    def mover_reservas(self, codigo_reserva: List) -> None:
        """
        Mueve la reserva especificada (de un hotel) a un apartamento que tenga una habitación disponible en las fechas especificadas. El apartamento debe tener un convenio previo con el hotel. Además, el apartamento debe permitir un número de huespedes superior al número de huespedes asociado a la reserva.  En caso de no haber ningún apartamento disponible con las características requeridas, lanza la excepción propia 'ApartamentoNotFound'.
        """
        pass


if __name__ == "__main__":
    gestion_alojamientos = GestionAlojamientos()
    gestion_alojamientos.crea_tablas()

    # Datos de ejemplo

    gestion_alojamientos.inserta_alojamiento(1, 'Hotel Sol', 'Av. del Mar', 23, '28001')
    gestion_alojamientos.inserta_alojamiento(2, 'Hotel Luna', 'Calle Estrella', 45, '28002')
    gestion_alojamientos.inserta_alojamiento(3, 'Apartamento Playa', 'Calle Arena', 12, '11011')
    gestion_alojamientos.inserta_alojamiento(4, 'Apartamento Centro', 'Gran Vía', 101, '28013')

    gestion_alojamientos.inserta_persona('12345678A', 'Carlos Pérez')
    gestion_alojamientos.inserta_persona('87654321B', 'Laura Gómez')
    gestion_alojamientos.inserta_persona('56781234C', 'Ana Martínez')

    gestion_alojamientos.inserta_agencia('A001', 'Madrid')
    gestion_alojamientos.inserta_agencia('A002', 'Barcelona')

    gestion_alojamientos.inserta_hotel(1, "Veratus", 'A001')
    gestion_alojamientos.inserta_hotel(2, "Diverxo", 'A002')

    gestion_alojamientos.inserta_habitacion(1, 101, 2, 'Doble')
    gestion_alojamientos.inserta_habitacion(1, 102, 1, 'Individual')
    gestion_alojamientos.inserta_habitacion(2, 201, 4, 'Familiar')
    gestion_alojamientos.inserta_habitacion(2, 202, 2, 'Doble')

    gestion_alojamientos.inserta_apartamento(3, 4, '12345678A')
    gestion_alojamientos.inserta_apartamento(4, 2, '87654321B') #87654321B

    gestion_alojamientos.inserta_reserva(1001, 1, 150.00, '2025-06-01', '2025-06-07', '12345678A')
    gestion_alojamientos.inserta_reserva(1002, 3, 200.00, '2025-07-01', '2025-07-10', '87654321B')

    gestion_alojamientos.inserta_huesped('12345678A', 1001)
    gestion_alojamientos.inserta_huesped('87654321B', 1002)

    gestion_alojamientos.inserta_acuerda(1, 3)
    gestion_alojamientos.inserta_acuerda(2, 4)

    gestion_alojamientos.inserta_oferta('A001', 1, 10.0)
    gestion_alojamientos.inserta_oferta('A002', 2, 15.0)

    # print(gestion_alojamientos.hoteles_agencia_localidad('Barcelona'))
    # print(gestion_alojamientos.restaurantes_codigo_postal('28001'))
    # print(gestion_alojamientos.grandes_tenedores())
    print(gestion_alojamientos.elimina_alojamiento_ilegal(1))