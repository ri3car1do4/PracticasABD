from datetime import datetime
from typing import Dict, Any, List, Tuple

from bson import ObjectId
from dotenv import load_dotenv
from lorem_text import lorem
import os
import pymongo

class GestionVentas:

    def __init__(self):
        load_dotenv(override=True)
        cliente = pymongo.MongoClient(f"mongodb://{os.environ.get('HOST')}:{os.environ.get('PORT')}/{os.environ.get('DATABASE')}")
        db = cliente["examen"]
        self.ventas = db["ventas"]

    # Contar Documentos
    def numero_documentos(self) -> int:
        # Función que devuelve los documentos totales de la colección.
        return self.ventas.count_documents({})

if __name__ == "__main__":
    gestion_ventas = GestionVentas()
    print(f"Nº de ventas: ", gestion_ventas.numero_documentos())