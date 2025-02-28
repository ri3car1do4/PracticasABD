from itertools import count

from flake8.defaults import NOQA_FILE
from jmespath.ast import and_expression
from numba.core.utils import order_by_target_specificity
from requests import session
from sqlalchemy import create_engine, text, select, update, func, and_
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from modelos import Base, Usuario, Experto, Ocasional, Mensaje, Hilo, Puntuacion
import datetime
from typing import Optional, List, Tuple


class GestionForo:

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

    def inserta_usuario(self, param, param1, param2):
        usuario = Usuario(id=param, nombre=param1, email=param2)
        with Session(self._engine) as session:
            session.add(usuario)
            session.commit()

    def inserta_experto(self, param, param1):
        experto = Experto(id=param, pagina=param1)
        with Session(self._engine) as session:
            session.add(experto)
            session.commit()

    def inserta_ocasional(self, param, param1):
        ocasional = Ocasional(id=param, nAccesos=param1)
        with Session(self._engine) as session:
            session.add(ocasional)
            session.commit()

    def inserta_hilo(self, param, param1, param2):
        hilo = Hilo(id=param, asunto=param1, idModerador=param2)
        with Session(self._engine) as session:
            session.add(hilo)
            session.commit()

    def inserta_mensaje(self, param, param1, param2, param3, param4):
        mensaje = Mensaje(idMensaje=param, idHilo=param1, Texto=param2, Fecha=param3, idUsuario=param4)
        with Session(self._engine) as session:
            session.add(mensaje)
            session.commit()

    def inserta_puntuacion(self, param, param1, param2, param3):
        puntuacion = Puntuacion(id_usuario=param, idMensaje=param1, idHilo=param2, puntuacion=param3)
        with Session(self._engine) as session:
            session.add(puntuacion)
            session.commit()

    def mensajes_moderados(self) -> List[Tuple[Experto, List[Hilo]]]:
        """
        Devuelve la lista de moderadores y los mensajes de los hilos que moderan
        """
        pass

    def puntuaciones_mayores(self, id_usuario: int, limit: int) -> List[Mensaje]:
        """
        Devuelve la lista de mensajes valorados por el usuario ocasional con id "id_usuario"
        que han recibido mayor puntuacion, ordenados por su puntuación de forma decreciente.
        Esta lista debe contener exactamente "limit" elementos. Si hay menos de "limit" mensajes
        valores, debe devolver una lista con todos los mensajes ordenados.
        """
        pass

    def elimina_puntuaciones_hilo(self, id_hilo: int) -> None:
        """
        Elimina todas las puntuaciones asociadas a mensajes de un hilo.
        """
        pass

    def cambiar_moderador(self, id_hilo: int, nuevo_moderador_id: int) -> None:
        """
        Cambia el moderador del hilo con id "id_hilo" a "nuevo_moderador_id".
        """
        pass

    def expertos_automoderados(self) -> List[Experto]:
        """
        Devueve la lista de expertos que moderan algún hilo en el que
        han enviado al menos un mensaje.
        """
        pass


if __name__ == "__main__":
    gestion_foros = GestionForo()
    gestion_foros.crea_tablas()

    gestion_foros.inserta_usuario(1, 'Carlos Pérez', 'carlos.perez@email.com');
    gestion_foros.inserta_usuario(2, 'Laura Gómez', 'laura.gomez@email.com');
    gestion_foros.inserta_usuario(3, 'Ana Martínez', 'ana.martinez@email.com');
    gestion_foros.inserta_usuario(4, 'Javier Ruiz', 'javier.ruiz@email.com');

    gestion_foros.inserta_experto(1, 'www.carlosperez.com');
    gestion_foros.inserta_experto(2, 'www.lauragomez.com');

    gestion_foros.inserta_ocasional(3, 15);
    gestion_foros.inserta_ocasional(4, 8);

    gestion_foros.inserta_hilo(101, '¿Cómo mejorar el rendimiento en SQL?', 1);
    gestion_foros.inserta_hilo(102, 'Diferencias entre SQL y NoSQL', 2);

    gestion_foros.inserta_mensaje(1001, 101,
                                  'Para mejorar el rendimiento en SQL, usa índices y optimiza las consultas.',
                                  '2025-02-01', 1);
    gestion_foros.inserta_mensaje(1002, 101, 'También puedes evitar SELECT * y normalizar tus tablas.', '2025-02-02',
                                  4);
    gestion_foros.inserta_mensaje(1003, 101, 'Este mensaje es malisimo.', '2025-01-02', 4);
    gestion_foros.inserta_mensaje(1004, 101, 'Te voy a banear', '2025-02-20', 1);
    gestion_foros.inserta_mensaje(1001, 102, 'SQL es relacional, mientras que NoSQL es más flexible en estructura.',
                                  '2025-02-03', 3);
    gestion_foros.inserta_mensaje(1002, 102, 'Depende de la aplicación, SQL es mejor para datos estructurados.',
                                  '2025-02-04', 4);

    gestion_foros.inserta_puntuacion(1, 1001, 101, 5);
    gestion_foros.inserta_puntuacion(1, 1002, 101, 7);
    gestion_foros.inserta_puntuacion(2, 1002, 101, 8);
    gestion_foros.inserta_puntuacion(3, 1002, 102, 5);
    gestion_foros.inserta_puntuacion(4, 1001, 102, 3);