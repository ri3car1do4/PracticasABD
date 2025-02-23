import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os
import datetime
from typing import Optional, List, Tuple


class GestionHotel:

    def __init__(self):
        self._config_params = self._load_config()
        # print(self._config_params)
        self._conexion = psycopg2.connect(**self._config_params)
        self._create_tables()

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

    def misma_ciudad(self) -> List[Tuple[str, str]]: # Esquema: (Nombre, Apellido)
        with self._conexion.cursor() as cursor:
            cursor.execute(f"""
            SELECT Participantes.Nombre, Participantes.Apellido
            FROM Alojamientos join Reservas on Alojamientos.IdAlojamiento = Reservas.IdAlojamiento
            join Formaliza on Reservas.IdReserva = Formaliza.IdReserva
            join Participantes on Formaliza.DNI = Participantes.DNI
            WHERE Participantes.Ciudad IS NOT NULL AND Participantes.Ciudad = Alojamientos.Ciudad
            ORDER BY Participantes.Apellido ASC
            """)
            return cursor.fetchall()

    def informacion_reservas(self) -> List[Tuple[str, str, int, int, float]]: # Esquema: (Nombre, Apellido, NumReservas, NumCiudades, SumaPrecios)
        with self._conexion.cursor() as cursor:
            cursor.execute(f"""
            SELECT Participantes.Nombre, Participantes.Apellido, COALESCE(COUNT(DISTINCT Reservas.IdReserva), 0), 
            COALESCE(COUNT(DISTINCT Alojamientos.Ciudad), 0), COALESCE(SUM(Reservas.Precio), 0)
            FROM Participantes 
            LEFT JOIN Formaliza ON Formaliza.DNI = Participantes.DNI
            LEFT JOIN Reservas ON Formaliza.IdReserva = Reservas.IdReserva
            LEFT JOIN Alojamientos ON Reservas.IdAlojamiento = Alojamientos.IdAlojamiento
            GROUP BY Participantes.DNI
            """)
            return cursor.fetchall()

    def reservas_no_formalizadas(self) -> List[Tuple[str, int]]: # Esquema: (idReserva, Precio)
        with self._conexion.cursor() as cursor:
            cursor.execute(f"""
            SELECT Reservas.IdReserva, Reservas.Precio
            FROM Reservas 
            LEFT JOIN Formaliza ON Reservas.IdReserva = Formaliza.IdReserva
            WHERE Formaliza.DNI IS NULL
            ORDER BY Reservas.Precio
            """)
            return cursor.fetchall()

    def sin_reservas(self, fecha: datetime.date) -> List[Tuple[str, int, str]]: # Esquema: (idAlojamiento, MaxPersonas, Ciudad)
        with self._conexion.cursor() as cursor:
            cursor.execute(f"""
            SELECT Alojamientos.idAlojamiento, COALESCE(Alojamientos.MaxPersonas, 0), Alojamientos.Ciudad
            FROM Alojamientos 
            LEFT JOIN Reservas ON Alojamientos.IdAlojamiento = Reservas.IdAlojamiento 
            AND %s BETWEEN Reservas.FechaEntrada AND Reservas.FechaSalida
            WHERE Reservas.IdReserva IS NULL 
            """, (fecha,))
            return cursor.fetchall()

    def mas_reservas_anyo(self, anyo: int) -> List[Tuple[str, int]]: # Esquema: (Ciudad, NumReservas)
        with self._conexion.cursor() as cursor:
            cursor.execute(f"""
            SELECT Alojamientos.Ciudad, COUNT(*) as NumReservas
            FROM Alojamientos 
            JOIN Reservas ON Alojamientos.IdAlojamiento = Reservas.IdAlojamiento 
            WHERE %s = EXTRACT(YEAR FROM Reservas.FechaEntrada)
            GROUP BY Alojamientos.Ciudad
            ORDER BY NumReservas DESC
            LIMIT 1
            """, (anyo,))
            return cursor.fetchall()

    def listar_Alojamientos(self, ciudad: str):
        with self._conexion.cursor() as cursor:
            cursor.execute(f"""
            SELECT IdAlojamiento, Propietario FROM Alojamientos WHERE Alojamientos.Ciudad = %s
            """, (ciudad,))
            alojamientos = cursor.fetchall()

        if len(alojamientos) > 0:
            print(f"Número de Alojamientos de {ciudad}: {len(alojamientos)}")
            print("---")
            for alojamiento in alojamientos:
                print(f"Alojamiento: {alojamiento[0]} Propietario: {alojamiento[1]}")
                with self._conexion.cursor() as cursor:
                    cursor.execute(f"""
                    SELECT IdReserva, FechaEntrada, Precio FROM Reservas WHERE Reservas.IdAlojamiento = %s ORDER BY Reservas.FechaEntrada
                    """, (alojamiento[0],))
                    reservas = cursor.fetchall()
                precio = 0
                if len(reservas) > 0:
                    for reserva in reservas:
                        print(f"ID: {reserva[0]} FechaEntrada: {reserva[1]} Precio: {reserva[2]}")
                        precio += reserva[2]
                print("---")
                print(f"Total reservas: {len(reservas)} Total Precio: {precio}")
                print("---")
        else:
            print("No hay alojamientos en la ciudad")

    def aplicar_descuento(self, propietario: str, fecha_inicio: datetime.date, fecha_fin: datetime.date, descuento: float):



    def _close_conexion(self):
        self._conexion.close()


if __name__ == "__main__":
    gestion = GestionHotel()
    # gestion.iniciar_bd()
    # print(gestion.misma_ciudad())
    # print(gestion.informacion_reservas())
    # print(gestion.reservas_no_formalizadas())
    # print(gestion.sin_reservas(datetime.date(2025, 5, 21)))
    # print(gestion.mas_reservas_anyo(2021))
    gestion.listar_Alojamientos('Madrid')
    gestion._close_conexion()