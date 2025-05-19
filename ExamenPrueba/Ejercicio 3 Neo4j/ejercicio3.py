import os

from dotenv import load_dotenv
from neo4j import GraphDatabase
from typing import Dict, List, Tuple, Any

class GestionPole:

    def __init__(self):
        self._driver = self._conexion_bbdd()
        self._db = "pole"

    def _conexion_bbdd(self):
        load_dotenv(override=True)
        driver = GraphDatabase.driver(
            f"neo4j://{os.environ.get('HOST')}:{os.environ.get('PORT')}/",
            auth=(os.environ.get("USER"), os.environ.get("PASSWORD"))
        )

        # Si no se produce error, nos hemos conectado correctamente
        driver.verify_connectivity()
        return driver

    # Determinar Número de Personas
    def cuenta_personas(self) -> int:
        # Función que devuelve el número total de personas en la base de datos
        records, _, _ = self._driver.execute_query(
            """
            MATCH (p: Person)
            RETURN count(p) AS num_personas
            """, database_=self._db
        )
        return records[0]["num_personas"]

if __name__ == "__main__":
    gestion_pole = GestionPole()
    print(gestion_pole.cuenta_personas())