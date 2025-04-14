from datetime import datetime
from typing import Dict, Any, List, Tuple
from lorem_text import lorem

import pymongo

class GestionFdIx:

    def __init__(self):
        cliente = pymongo.MongoClient("mongodb://localhost:27017/")
        db = cliente["fdix"]
        self.comments = db["comments"]
        self.movies = db["movies"]
        self.users = db["users"]

    def comentarios_aleatorios(self, n: int) -> List[Dict[str, Any]]:
        # Función que devuelva `n` comentarios aleatorios invocando al método anterior. Para ello, selecciona un
        # usuario y una película aleatoriamente, e introduce un comentario con texto aleatorio.
        comments = []
        for i in range(n):
            user = self.users.find_one({}, {"name": 1, "email": 1}) # Así coge el primero no aleatorio
            movie = self.movies.find_one({}, {"_id": 1}) # Así coge el primero no aleatorio
            comments.append(generar_comentario(user["name"], user["email"], movie["_id"], lorem.paragraph()))
        return comments

    def insertar_comentarios_aleatorios(self, n) -> Dict[str, Any]:
        # Función para insertar una serie de comentarios aleatorios. Además, se actualiza el campo
        # `num_fdix_comments` de la colección `movies` de las películas correspondientes.
        comments = self.comentarios_aleatorios(n)
        movie_id_counts = {}
        for comment in comments:
            movie_id = comment["movie_id"]
            movie_id_counts[movie_id] = movie_id_counts.get(movie_id, 0) + 1
        for movie_id, count in movie_id_counts.items():
            self.movies.update_one({"_id": movie_id}, {"$inc": {"num_fdix_comments": count}})
        self.comments.insert_many(comments)
        return {}

    def borrar_comentarios(self, email: str, fecha_inicial: datetime.date,
                           fecha_final: datetime.date) -> Dict[str, Any]:
        # Función para borrar todos los comentarios de un usuario dado su email en un rango de fechas. Además se
        # actualiza el campo `num_fdix_comments` de la colección `movies` de las películas correspondientes.
        comments = self.comments.find({"email": email, "date": {"$gte": fecha_inicial, "$lte": fecha_final}})
        movie_id_counts = {}
        for comment in comments:
            movie_id = comment["movie_id"]
            movie_id_counts[movie_id] = movie_id_counts.get(movie_id, 0) + 1
        for movie_id, count in movie_id_counts.items():
            self.movies.update_one({"_id": movie_id}, {"$inc": {"num_fdix_comments": -count}})
        comment_ids = [comment["_id"] for comment in comments]
        self.comments.delete_many({"_id": {"$in": comment_ids}})
        return {}

    def actualizar_nombre(self, email: str, nombre_nuevo: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        # Función que cambie el nombre asociado a un email. Para ello, hay que actualizar tanto la colección de
        # usuarios como la de comentarios.
        user = self.users.find_one_and_update({"email": email}, {"$set": {"name": nombre_nuevo}}, return_document=True)
        self.comments.update_many({"email": email}, {"$set": {"name": nombre_nuevo}})
        comment = self.comments.find_one({"email": email, "name": nombre_nuevo})
        return user, comment

    def nuevo_lenguaje(self, titulo: str, idioma: str):
        # Función que, dado el título de una película, añada un nuevo lenguaje a la lista de lenguajes si no lo tenía
        # ya disponible previamente.
        self.movies.update_one({"title": titulo}, {"$addToSet": {"languages": idioma}})

    def reemplazar_comentario(self, id_comentario: str):
        # Dado el id de un comentario, reemplaza el comentario especificado por uno generado aleatoriamente (utilizando
        # la función `generar_comentario`). Comprueba que efectivamente se ha llevado a cabo el reemplazo.
        user = self.users.find_one({}, {"name": 1, "email": 1})  # Así coge el primero no aleatorio
        movie = self.movies.find_one({}, {"_id": 1})  # Así coge el primero no aleatorio
        comment = generar_comentario(user["name"], user["email"], movie["_id"], lorem.paragraph())
        self.comments.replace_one({"_id": id_comentario}, comment)

    # CONSULTAS
    def encontrar_peliculas_idioma(self, n: int, lista_idiomas: List[str]) -> List[Dict[str, Any]]:
        # Devuelve las `n` últimas películas que estén disponibles en una lista de idiomas dado, ordenadas por fecha
        # de estreno. Esquema: (titulo, idiomas, fecha).
        pass

    def mejor_valoradas(self, i: int, j: int) -> List[Dict[str, Any]]:
        # Encuentra las películas en las posiciones `i` y `j` (inclusive), ordenadas de forma descendente según las
        # puntuaciones de `imdb`. Esquema: (titulo, rating).
        pass

    def ganar_categoria(self) -> List[Dict[str, Any]]:
        # Encuentras las películas que hayan ganado en todas las categorías en las que ha estado nominada, ordenada
        # por número de premios de forma descendente y por `_id`. Esquema: (titulo, numeroPremios)
        pass

    def mayor_diferencia_ratings(self, anyo: int) -> List[Dict[str, Any]]:
        # Encuentra las películas que se han estrenado en un año dado en las que la diferencia entre el rating del
        # público y de los críticos sea mayor, ordenadas por esta diferencia. Entonces, se comprueba que la película
        # correspondiente tiene un rating asociado a críticos y a usuarios. Para ello, se utiliza la operación
        # `{"exists": True}`. También hay que utilizar las operaciones `$abs` y `$substract`. Esquema: (titulo,
        # ratingPublico, ratingCriticos, diferencia)
        pass

    # ÍNDICES
    # AGREGACIONES
    def numero_peliculas_por_categoria(self) -> Dict[str, int]:
        # Identifica cuántos elementos tiene cada categoría de producción audiovisual (campo `type`), ordenadas por el
        # número de elementos de manera ascendente. En lugar de devolver la información en una lista de diccionarios,
        # combina toda la información en un único diccionario, donde la clave corresponde a la categoría de producción;
        # y el valor, al número total de películas en esa categoría. Esquema: {categoria: numeroPeliculas}
        pass

    def numero_peliculas_genero(self, genero: str) -> int:
        # Devuelve el número de elementos que hay asociados a un género de película dado. Esquema: numeroPeliculas
        pass

    def han_comentado(self, titulo: str) -> List[Dict[str, str]]:
        # Devuelve la lista de usuarios (`email` y `nombre`) que han comentado en una película dada. Esquema: (email, nombre)
        pass


def generar_comentario(name: str, email: str,
                       movie_id: str, text: str) -> Dict[str, Any]:
    # Función independiente de la clase `GestionFdIx` que devuelva un comentario en formato `JSON`, utilizando como
    # fecha la fecha de hoy (`datetime.datetime.today()`)
    return {
        "name": name,
        "email": email,
        "movie_id": movie_id,
        "text": text,
        "date": datetime.today()
    }



if __name__ == "__main__":
    gestion_fdix = GestionFdIx()
    print(gestion_fdix.actualizar_nombre("sean_bean@gameofthron.es", "Ned Starkn´t"))
    gestion_fdix.nuevo_lenguaje("The Perils of Pauline", "Spanish")
    # gestion_fdix.reemplazar_comentario("573a1390f29313caabcd5b9a")
