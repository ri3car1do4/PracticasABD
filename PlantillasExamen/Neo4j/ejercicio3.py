import os

from dotenv import load_dotenv
from neo4j import GraphDatabase
from typing import Dict, List, Tuple, Any

# OJOOOOO
class GestionInvestigacion:

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

    # CONSULTA EJEMPLO
    def consulta_1_1_1(self):
        # Devuelve la dirección de las 10 localizaciones (Location) en que se han cometido más crímenes
        # (relación OCCURRED_AT). Esquema: (direccion, num_crimenes).
        records, _, _ = self._driver.execute_query(
            """
            MATCH (c:Crime)-[:OCCURRED_AT]->(l:Location) 
            RETURN l.address AS address, count(*) AS num_crimenes
            ORDER BY num_crimenes DESC 
            LIMIT 10
            """, database_=self._db
        )
        return [dict(record) for record in records]

if __name__ == "__main__":
    gestion_investigacion = GestionInvestigacion()