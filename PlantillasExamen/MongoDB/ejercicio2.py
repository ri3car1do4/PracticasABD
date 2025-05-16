from datetime import datetime
from typing import Dict, Any, List, Tuple

from bson import ObjectId
from lorem_text import lorem
import os
import pymongo

# OJOOOOOO
class GestionFdIx:

    def __init__(self):
        cliente = pymongo.MongoClient(f"mongodb://{os.environ.get('HOST')}:{os.environ.get('PORT')}/{os.environ.get('DATABASE')}")
        # OJOOOOOO
        db = cliente["fdix"]
        self.comments = db["comments"]
        self.movies = db["movies"]
        self.users = db["users"]

    # CONSULTA EJEMPLO
    def encontrar_peliculas_idioma(self, n: int, lista_idiomas: List[str]) -> List[Dict[str, Any]]:
        # Devuelve las `n` últimas películas que estén disponibles en una lista de idiomas dado, ordenadas por fecha
        # de estreno. Esquema: (titulo, idiomas, fecha).
        return list(self.movies.find({"languages": {"$all": lista_idiomas}}, {"title": 1, "languages": 1,
                "released": 1, "_id": 0}).sort({"released": -1}).limit(n))

if __name__ == "__main__":
    gestion_fdix = GestionFdIx()