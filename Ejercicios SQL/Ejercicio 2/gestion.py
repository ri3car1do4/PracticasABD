import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os
import datetime
from typing import Optional, List, Tuple


class Gestion:

    def __init__(self):
        self._config_params = self._load_config()
        print(self._config_params)
        self._conexion = psycopg2.connect(**self._config_params)
        print(self._conexion)

    def _load_config(self):
        load_dotenv(override=True)

        config_params = {"user": os.environ.get("USER"),
                         "password": os.environ.get("PASSWORD"),
                         "host": os.environ.get("HOST"),
                         "port": os.environ.get("PORT")}

        database = os.environ.get("DATABASE", None)
        if database is not None:
            config_params["database"] = database

        return config_params

    def _close_conexion(self):
        self._conexion.close()


if __name__ == "__main__":
    gestion = Gestion()
    gestion._close_conexion()