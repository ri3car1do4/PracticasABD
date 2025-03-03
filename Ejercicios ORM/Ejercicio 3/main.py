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

    def hoteles_agencia_localidad(self, localidad: str) -> List[str]:
        """
        Devuelve el nombre de todos los hoteles tales que existe una agencia en la localidad dada que ofrece alguna oferta en ese hotel.
        """
        pass

    def restaurantes_codigo_postal(self, codigo_postal: str) -> List[str]:
        """
        Devueve la lista de restaurantes asociadas a un código postal.
        """
        pass

    def grandes_tenedores(self) -> List[Persona]:
        """
        Devueve la lista de personas que son al menos dueños de un total de 5 apartamentos.
        """
        pass

    def elimina_alojamiento_ilegal(self, id_alojamiento) -> List[str]:
        """
        Dado el ID de un alojamiento ilegal, elimina ese alojamiento de la base de datos y sus datos relacionados; y devuelve la lista de NIFs de personas que tenían una reserva de ese alojamiento (a partir de hoy). Tenéis dos opciones para eliminar toda la información relacionada (os recomiendo probar las dos):

        - Podéis fijar "ON DELETE CASCADE" al construir la tabla en las foreign keys (investigad cómo se especifica). Cuando borréis el alojamiento correspondiente, comprobad que las eliminaciones se propagan.
        - Otra opción es operar directamente desde la ORM.
        """

    def mover_reservas(self, codigo_reserva: List) -> None:
        """
        Mueve la reserva especificada (de un hotel) a un apartamento que tenga una habitación disponible en las fechas especificadas. El apartamento debe tener un convenio previo con el hotel. Además, el apartamento debe permitir un número de huespedes superior al número de huespedes asociado a la reserva.  En caso de no haber ningún apartamento disponible con las características requeridas, lanza la excepción propia 'ApartamentoNotFound'.
        """
        pass

if __name__ == "__main__":
    gestion_alojamientos = GestionAlojamientos()
    gestion_alojamientos.crea_tablas()
