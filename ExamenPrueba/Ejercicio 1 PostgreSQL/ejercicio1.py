from itertools import count

from flake8.defaults import NOQA_FILE
from jmespath.ast import and_expression
from numba.core.utils import order_by_target_specificity
from requests import session
from sqlalchemy import create_engine, text, select, update, func, and_
from sqlalchemy.orm import Session, load_only
from dotenv import load_dotenv
import os
from modelos import Base, Cartas
import datetime
from typing import Optional, List, Tuple, Dict


class GestionCartas:

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

    def nombre_cara2url(self) -> Dict[str, List[str]]:
        with Session(self._engine) as session:
            stmt = select(
                Cartas.nombre,
                func.array_agg(Cartas.url_mkm)
            ).group_by(Cartas.nombre)

            result = session.execute(stmt)
            return {nombre: urls for nombre, urls in result}


if __name__ == "__main__":
    gestion_tabla = GestionCartas()
    # gestion_tabla.crea_tablas()
    print(gestion_tabla.nombre_cara2url())