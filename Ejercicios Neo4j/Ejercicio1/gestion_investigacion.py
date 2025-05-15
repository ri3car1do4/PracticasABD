import os

from dotenv import load_dotenv
from neo4j import GraphDatabase
from typing import Dict, List, Tuple, Any


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

    def consulta_1_1_2(self) -> Dict[str, int]:
        # Devuelve cuántos crímenes se han cometido de cada tipo (propiedad type de los nodos con la etiqueta Crime).
        # En lugar de devolver la solución como una lista de diccionarios, devuelve un único diccionario que tiene
        # como claves los distintos tipos, y como valores el número de crímenes cometidos de ese tipo. A los crímenes
        # sin tipo, se le asigna el nombre Sin tipo en la solución.
        records, _, _ = self._driver.execute_query(
            """
            MATCH (c:Crime)
            RETURN coalesce(c.type, "Sin tipo") AS tipo, count(*) AS num_crimenes
            """, database_=self._db
        )
        return {record["tipo"]: record["num_crimenes"] for record in records }

    # Consulta 1.1.3
    def crimenes_investigados_inspector(self, apellido: str) -> List[Dict[str, str]]:
        # Dado el apellido de un inspector (campo surname de un nodo con etiqueta Officer), devuelve los crímenes que ha
        # investigado (relación INVESTIGATED_BY). Esquema: (id_crimen, tipo_crimen, progreso). El progreso se refiere
        # a last_outcome.
        records, _, _ = self._driver.execute_query(
            """
            MATCH (c:Crime)-[:INVESTIGATED_BY]->(o:Officer)
            WHERE o.surname = $apellido
            RETURN c.id AS id_crimen, c.type AS tipo_crimen, c.last_outcome AS progreso
            """, database_=self._db, apellido=apellido
        )
        return [dict(record) for record in records]

    # Consulta 1.1.4 (REVISAR)
    def personas_llamadas_sospechosas(self, id_crimen: str) -> List[Dict[str, Any]]:
        # Dado el id de un crimen, devuelve la lista de personas a las que un sospechoso (relación PARTY_TO) ha llamado
        # más de una vez, considerando únicamente las llamadas que haya durado más de 30 minutos. Investiga en la base
        # datos cómo recuperar la información de las llamadas.
        # Esquema (nombre_sospechosos, apellido_sospechoso, nombre_llamada, apellido_llamada, num_llamadas).
        # num_llamadas se refiere al número de llamadas que supera 30 minutos.
        records, _, _ = self._driver.execute_query(
            """
            MATCH (p:Person)-[:PARTY_TO]->(c:Crime)
            WHERE c.id = $id_crimen
            MATCH (p)-[:HAS_PHONE]->(ph:Phone)<-[:CALLER]-(pc:PhoneCall)
            WHERE toInteger(pc.call_duration) > 30
            MATCH (pc)-[:CALLED]->(ph2:Phone)<-[:HAS_PHONE]-(p2:Person)
            WITH p.name AS nombre_sospechoso, p.surname AS apellido_sospechoso, p2.name AS nombre_llamada, 
            p2.surname AS apellido_llamada, count(pc) AS num_llamadas
            WHERE num_llamdas > 1 
            RETURN nombre_sospechoso, apellido_sospechoso, nombre_llamada, apellido_llamada, num_llamadas
            """, database_=self._db, id_crimen=id_crimen
        )
        return [dict(record) for record in records]

    # Consulta 1.2.1
    def lista_crimenes(self, num_placa: str, delito: str) -> List[str]:
        # En primer lugar, vamos a determinar cuáles son estos crímenes. Para ello, filtramos aquellos crímenes relacionados
        # con drogas (type: "Drugs") que están investigados actualmente por el inspector (relación INVESTIGATED_BY). Para
        # determinar que crímenes están siendo investigados, filtramos aquellos que tienen la propiedad last_outcome con valor
        # "Under investigation" en el crimen correspondiente.
        records, _, _ = self._driver.execute_query(
            """
            MATCH (c:Crime)-[:INVESTIGATED_BY]->(o:Officer)
            WHERE c.type = $delito AND c.last_outcome = "Under investigation" AND o.badge_no = $num_placa
            RETURN c.id AS crimen
            """, database_=self._db, delito=delito, num_placa=num_placa
        )
        return [record["crimen"] for record in records]

    # Consulta 1.2.2
    def sospechosos_crimenes(self, ids_crimen: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        # Una vez tenemos la lista de crímenes del inspecto, vamos a investigar quiénes son los sopechosos de los crímenes
        # anteriores. Como ya tenemos la lista de ids de los crímenes sobre los que queremos consultar, vamos a crear una
        # que, dada una lista de ids, nos devuelva la información sobre las personas que han participado en esos crímenes
        # (relación PARTY_TO).
        #
        # Los datos se van a devolver como un diccionario, tal que dado el id de un crimen, devuelva una lista con la
        # información de cada sospechoso. Esquema: (id, nombre, apellido). El id se refiere al campo nhs_no.
        #
        # Nota: dentro de collect(), se pueden renombrar los campos con la notación de diccionario, p.e. collect({nombre: p.name}).
        records, _, _ = self._driver.execute_query(
            """
            MATCH (p:Person)-[:PARTY_TO]->(c:Crime)
            WHERE c.id in &lista_ids
            RETURN p.nhs_no AS id, collect({nombre: p.name, apellido: p.surname}) AS nombre_apellido
            """, database_=self._db, list_ids=ids_crimen
        )
        return {record["id"]: record["nombre_apellido"] for record in records}

    # Consulta 1.2.3
    def informacion_delito(self, ids_crimen: List[str]) -> Dict[str, Dict[str, Any]]:
        # Otra parte importante de la investigación es determinar la localización del delito y las pruebas del mismo.
        # Un delito está conectado con una localización a través de la relación OCCURRED_AT, y una prueba conecta con
        # un delito a través de la relación INVOLVED_IN, teniendo además de tipo "Evidence".
        #
        # Para facilitar este proceso, vamos a implementar una función que, dados los ids de los delitos, devuelve un
        # diccionario con la localización y la lista de pruebas. Este diccionario tiene como clave el id del delito
        # correspondiente, y como valor un diccionario con dos campos: **localizacion** tiene la dirección del delito
        # (address) y **prueba** contiene una lista con las descripciones de las pruebas involucradas.
        records, _, _ = self._driver.execute_query(
            """
            MATCH (c:Crime)-[:OCCURRED_AT]->(l:Location)
            WHERE c.id in $lista_ids
            MATCH (o:Object)-[:INVOLVED_IN]->(c)
            WHERE  o.type = "Evidence"
            RETURN l.address AS localizacion, collect(o.description) AS pruebas
            """, database_=self._db, lista_ids=ids_crimen
        )

    def conexiones_sospechosos(self, sospechosos: List[str]) -> Dict[Tuple[str, str], List[List[str]]]:
        # Una vez hemos recopilado más información sobre los sospechosos, queremos averiguar si hay algún tipo de relación
        # entre ellos. Para ello, dada una lista de sospechosos (identificados por su id), devuelve todas las conexiones
        # entre los mismos, usando todos los caminos más cortos. Esto quiere decir que por cada par de sospechosos en la
        # lista, se deben construir todos los caminos más cortos que los conecten. Para que la consulta no se demasiado
        # costosa, solo vamos a considerar caminos de longuitud máxima 3. Además, para evitar repeticiones en el resultado,
        # comprobaremos que id_p1 < id_p2, donde id_p1 y id_p2 son los ids de dos sospechosos.
        #
        # Los sospechosos pueden esar conectados por las siguientes relaciones: KNOWS, KNOWS_LW (vive con esa persona),
        # KNOWS_SN (conoce por relaciones sociales), FAMILY_REL (son familia), KNOWS_PHONE (conoce el tlf). El formato
        # de salida es un diccionario que, dada la tupla de ids de dos sospechosos ordenados por su id, devuelva una lista
        # con las conexiones. Estas conexiones contienen la siguiente información: (id, nombre, apellido) de cada una
        # de estas personas. Además, se devuelven los resultados sin repeticiones.
        records, _, _ = self._driver.execute_query(
            """
            MATCH (p1: Person)
            MATCH (p2: Person)
            WHERE p1.nhs_no in $sospechosos AND p2.nhs_no in $sospechosos AND p1.nhs_no < p2.nhs_no
            MATCH p = allShortestPaths((p1)-[:KNOWS | KNOWS_LW | KNOWS_PHONE | KNOWS_SN | FAMILY_REL*..3]-(p2))
            RETURN p1.nhs_no AS id1, p2.nhs_no AS id2, collect(DISTINCT [nodo in nodes(p) | 
            {id:nodo.nhs_no, nombre:nodo.name, apellido:nodo.surname}]) AS relacionados
            """, database_=self._db, sospechosos=sospechosos
        )
        return {(record["id1"], record["id2"]): record["relacionados"] for record in records}

if __name__ == "__main__":
    gestion_investigacion = GestionInvestigacion()
    # print(gestion_investigacion.consulta_1_1_1())
    # print(gestion_investigacion.consulta_1_1_2())
    # print(gestion_investigacion.crimenes_investigados_inspector("Larive"))
    # print(gestion_investigacion.personas_llamadas_sospechosas("34f16237cac32a82724094222dd3b92bfe9f415864638071e144154d078d0af8"))
    # print(gestion_investigacion.lista_crimenes("26-5234182", "Drugs"))
    # print(gestion_investigacion.sospechosos_crimenes(gestion_investigacion.lista_crimenes("26-5234182", "Drugs")))
    # print(gestion_investigacion.informacion_delito(gestion_investigacion.lista_crimenes("26-5234182", "Drugs")))
    print(gestion_investigacion.conexiones_sospechosos(['879-22-8665', '249-54-6589', '455-19-0708']))
