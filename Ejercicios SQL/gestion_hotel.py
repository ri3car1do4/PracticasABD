import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os
import datetime
from typing import Optional, List, Tuple


class GestionHotel:

    def __init__(self):
        self._config_params = self._load_config()
        print(self._config_params)
        self._conexion = psycopg2.connect(**self._config_params)

    def _load_config(self):
        load_dotenv(override=True)

        config_params = {"user": os.environ.get("USER"),
                         "password": os.environ.get("PASSWORD"),
                         "host": os.environ.get("HOST")}

        database = os.environ.get("DATABASE", None)
        if database is not None:
            config_params["database"] = database

        return config_params

    def _create_tables(self):
        with self._conexion.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Alojamientos(
                    IdAlojamiento INTEGER PRIMARY KEY NOT NULL,
                    MaxPersonas INTEGER,
                    Propietario VARCHAR(30) NOT NULL,
                    Ciudad VARCHAR(20) NOT NULL
                );
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Reservas(
                IdReserva INTEGER PRIMARY KEY NOT NULL,
                IdAlojamiento INTEGER REFERENCES Alojamientos(IdAlojamiento),
                FechaEntrada DATE NOT NULL,
                FechaSalida DATE NOT NULL,
                Precio DECIMAL NOT NULL
            );
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Participantes(
                DNI CHAR(9) PRIMARY KEY NOT NULL,
                Nombre VARCHAR(30) NOT NULL,
                Apellido VARCHAR(30) NOT NULL,
                Ciudad VARCHAR(20),
                FechaNacimiento DATE,
                Telefono INTEGER
            );
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Formaliza(
                IdReserva INTEGER REFERENCES Reservas(IdReserva),
                DNI CHAR(9) REFERENCES Participantes(DNI),
                PRIMARY KEY (IdReserva, DNI)
            );
            """)

        self._conexion.commit()

    def iniciar_bd(self):
        datos_alojamientos = [(1, 4, 'Pensiones Loli', 'Madrid'), (2, None, 'Laura Gomez', 'Barcelona'),
                              (3, 2, 'Carlos Ruiz', 'Sevilla'), (4, 8, 'Ana Lopez', 'Valencia'),
                              (5, 3, 'Maria Fernandez', 'Granada'),
                              (6, None, 'Juan Perez', 'Madrid')]

        datos_reservas = [(100, 1, '2025-05-20', '2025-05-25', 900),
                          (101, 1, '2024-01-20', '2024-01-25', 400),
                          (102, 2, '2023-02-01', '2023-02-05', 500),
                          (103, 3, '2022-03-10', '2022-03-12', 200),
                          (104, 3, '2021-04-15', '2021-04-20', 800),
                          (105, 4, '2021-05-05', '2021-05-10', 300),
                          (106, 4, '2023-05-10', '2024-01-02', 100)]

        datos_formaliza = [(101, "12345678A"),
                           (101, "23456789B"),
                           (102, "23456789B"),
                           (103, "34567890C"),
                           (104, "45678901D"),
                           (105, "56789012E"),
                           (105, "45678901D")]

        datos_participantes = [('12345678A', 'Luis', 'Martinez', 'Madrid', '1985-07-14', '600123456'),
                               ('23456789B', 'Elena', 'Sanchez', None, None, None),
                               ('34567890C', 'Miguel', 'Garcia', 'Sevilla', None, '602345678'),
                               ('45678901D', 'Sofía', 'Lopez', None, '1995-01-30', '603456789'),
                               ('56789012E', 'Pablo', 'Hernandez', 'Granada', '2000-09-19', '604567890'),
                               ('11111111F', 'Juan Carlos', 'Redondo', None, '2005-01-30', '612345678')]

        with self._conexion.cursor() as cur:
            psycopg2.extras.execute_batch(cur, "INSERT INTO Alojamientos VALUES (%s, %s, %s, %s)", datos_alojamientos)
            psycopg2.extras.execute_batch(cur, "INSERT INTO Reservas VALUES (%s, %s, %s, %s, %s)", datos_reservas)
            psycopg2.extras.execute_batch(cur, "INSERT INTO Participantes VALUES (%s, %s, %s, %s, %s, %s)", datos_participantes)
            psycopg2.extras.execute_batch(cur, "INSERT INTO Formaliza VALUES (%s, %s)", datos_formaliza)

        self._conexion.commit()

    def inserta_alojamiento(self, id: int, max: Optional[str], propietario: str, ciudad: str) -> None:
        with self._conexion.cursor() as cursor:
            cursor.execute(f"""
            INSERT INTO Alojamiento VALUES (%s, %s, %s, %s) 
            """, (id, max, propietario, ciudad))
        self._conexion.commit()

    def inserta_reservas(self, id: int, idAlojamiento: int, fechaEntrada: datetime.date, fechaSalida: datetime.date, precio: float) -> None:
        with self._conexion.cursor() as cursor:
            cursor.execute(f"""
            INSERT INTO Reservas VALUES (%s, %s, %s, %s, %s) 
            """, (id, idAlojamiento, fechaEntrada, fechaSalida, precio))
        self._conexion.commit()

    def inserta_formaliza(self, idReserva: int, dni: str) -> None:
        with self._conexion.cursor() as cursor:
            cursor.execute(f"""
            INSERT INTO Formaliza VALUES (%s, %s) 
            """, (idReserva, dni))
        self._conexion.commit()

    def inserta_participantes(self, dni: str, nombre: str, apellido: str, ciudad: str, fechaNac: datetime.date, telefono: Optional[int]) -> None:
        with self._conexion.cursor() as cursor:
            cursor.execute(f"""
            INSERT INTO Participantes VALUES (%s, %s, %s, %s, %s, %s) 
            """, (dni, nombre, apellido, ciudad, fechaNac, telefono))
        self._conexion.commit()

    def servicios_por_cliente(self, apellido: str, fecha: datetime.date) -> List[Tuple[str, str]]:
        """
        Queremos implementar una función que liste el nombre de los
        clientes con un apellido dado (**apellido**) y de los servicios que
        han contratado a partir de una fecha concreta (**fecha**), ordenado
        primero por nombre del cliente y después por el del servicio, ambos ascendentemente.
        """
        with self._conexion.cursor() as cursor:
            patron = f"%{apellido}%"
            cursor.execute(f"""
            SELECT Clientes.nombre, Servicios.nombre
            FROM Clientes join Contratado on Clientes.DNI = Contratado.DNICliente
            join Servicios on Servicios.id = Contratado.idServicio
            WHERE Clientes.nombre like %s AND %s <= Contratado.fecha
            ORDER BY Clientes.nombre ASC, Servicios.nombre ASC
            """, (patron, fecha))
            return cursor.fetchall()

    def eliminar_servicios(self) -> None:
        with self._conexion.cursor() as cursor:
            cursor.execute("""
            DELETE FROM Servicios WHERE 
            Servicios.id IN 
            (SELECT Servicios.id 
            FROM Servicios LEFT JOIN Contratado ON Servicios.id = Contratado.idServicio
             WHERE Contratado.idServicio IS NULL);
            """)

        self._conexion.commit()

    def _close_conexion(self):
        self._conexion.close()


if __name__ == "__main__":
    gestion = GestionHotel()
    gestion._create_tables()
    gestion.iniciar_bd()

    gestion._close_conexion()