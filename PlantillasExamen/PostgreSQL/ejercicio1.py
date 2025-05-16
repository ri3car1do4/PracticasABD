from itertools import count

from flake8.defaults import NOQA_FILE
from jmespath.ast import and_expression
from numba.core.utils import order_by_target_specificity
from requests import session
from sqlalchemy import create_engine, text, select, update, func, and_
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from modelos import Base #, Alojamientos, Reservas, Formaliza, Participantes
import datetime
from typing import Optional, List, Tuple

# OJOOOOO
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

    # CONSULTA EJEMPLO
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

if __name__ == "__main__":
    gestion_tabla = GestionHotel()
    gestion_tabla.crea_tablas()