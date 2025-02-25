from sqlalchemy import create_engine, text, select, update
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from modelos import Base, Cliente, Contratado, Servicio, Departamento
import datetime
from typing import Optional, List, Tuple


class GestionTelefonica:

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

    def consulta_prueba(self):
        with Session(self._engine) as session:
            result = session.execute(text("select 'Hello world!'"))
            r = result.fetchall()
            print(f"Returned value {r}")

    def crea_tablas(self):
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)

    def inserta_cliente(self, dni: str, nombre: str, gasto: Optional[float]) -> None:
        cliente = Cliente(DNI=dni, nombre=nombre, gasto=gasto)
        with Session(self._engine) as session:
            session.add(cliente)
            session.commit()

    def devolver_clientes(self):
        with Session(self._engine) as session:
            clientes = session.scalars(select(Cliente))
            tres_clientes = clientes.fetchmany(3)
            print(tres_clientes)
            # for cliente in clientes.fetchall():
            # print(cliente)

    def inserta_departamento(self, codigo: int, nombre: str, n_empleados: int, fecha_creacion: datetime.date) -> None:
        departamento = Departamento(codigo=codigo, nombre=nombre,
                                    n_empleados=n_empleados,
                                    fecha_creacion=fecha_creacion)
        with Session(self._engine) as session:
            session.add(departamento)
            session.commit()

    def inserta_servicios(self, id_: int, nombre: str, tarifa: float, codigo_dpto: int) -> None:
        servicio = Servicio(id=id_, nombre=nombre, tarifa=tarifa, departamento=codigo_dpto)
        with Session(self._engine) as session:
            session.add(servicio)
            session.commit()

    def inserta_contratado(self, dni_cliente: str, id_servicio: int, fecha: datetime.date) -> None:
        contratado = Contratado(DNICliente=dni_cliente, idServicio=id_servicio,
                                fecha= fecha)
        with Session(self._engine) as session:
            session.add(contratado)
            session.commit()

    def incrementar_porcentaje_objetos(self, porcentaje: float, patron: str) -> None:
        with Session(self._engine) as session:
            query_servicios = session.scalars(select(Servicio))
            for servicio in query_servicios.fetchall():
                if patron in servicio.nombre:
                    servicio.tarifa = (1 + porcentaje) * servicio.tarifa
                    session.add(servicio)

            session.commit()

    def servicios_por_cliente_consulta(self, apellido: str, fecha: datetime.date) -> List[Tuple[str, str]]:
        """
        Queremos implementar una función que liste el nombre de los clientes con un apellido dado
        (**apellido**) y de los servicios que han contratado
        a partir de una fecha concreta (**fecha**), ordenado primero
        por nombre del cliente y después por el del servicio,
        ambos ascendentemente.

        """
        """
        SELECT
        FROM 
        WHERE
        GROUP BY
        HAVING 
        ORDER BY
        """
        with Session(self._engine) as session:
            patron = f"%{apellido}%"
            statement = select(Cliente.nombre, Servicio.nombre) \
                        .join_from(Cliente, Contratado, Cliente.DNI == Contratado.DNICliente) \
                        .join(Servicio, Contratado.idServicio == Servicio.id) \
                        .where(Cliente.nombre.like(patron)) \
                        .where(Contratado.fecha > fecha) \
                        .order_by(Cliente.nombre.desc(), Servicio.nombre.desc())
            query = session.execute(statement)
            for resultado in query.fetchall():
                print(resultado)

    def servicios_por_cliente_objetos(self, apellido: str, fecha: datetime.date) -> List[Tuple[str, str]]:
        with Session(self._engine) as session:
            clientes_con_apellido = select(Cliente).where(Cliente.nombre.in_(apellido))

    def incrementar_porcentaje_consulta(self, porcentaje: float, patron: str) -> None:
        with Session(self._engine) as session:
            session.execute(update(Servicio) \
                            .where(Servicio.nombre.like(patron)) \
                            .values(tarifa=(1 + porcentaje) * Servicio.tarifa))

    def contratos_cliente(self, dni: str):
        with Session(self._engine) as session:
            cliente = session.get(Cliente, dni)
            contratos = cliente.contratos

            for contrato in contratos:
                print(contrato.cliente.DNI)


if __name__ == "__main__":
    gestion_tabla = GestionTelefonica()
    # gestion_telefonica.consulta_prueba()
    # gestion_tabla.crea_tablas()
    # gestion_tabla.inserta_cliente("12345678A", "Juan Pérez", 1200.50)
    # gestion_tabla.inserta_cliente("87654321B", "María Gómez", 850.75)
    # gestion_tabla.inserta_cliente("11223344C", "Carlos Gómez", None)
    # gestion_tabla.inserta_cliente("44332211D", "Ana Fernández", 620.90)
    # gestion_tabla.inserta_cliente("55554444E", "Luis Martínez", None)
    # gestion_tabla.devolver_clientes()
    #
    # gestion_tabla.inserta_departamento(1, "Atención al Cliente", 25, datetime.date.fromisoformat("2015-06-10"))
    # gestion_tabla.inserta_departamento(2, "Infraestructura", 15, datetime.date.fromisoformat("2012-09-20"))
    # gestion_tabla.inserta_departamento(3, "Desarrollo de Servicios", 40, datetime.date.fromisoformat("2018-03-05"))
    # gestion_tabla.inserta_departamento(4, "Recursos Humanos", 10, datetime.date.fromisoformat("2010-01-15"))  # Sin servicios asociados
    #
    # gestion_tabla.inserta_servicios(101, "Plan Básico Móvil", 19.99, 1)
    # gestion_tabla.inserta_servicios(102, "Plan Fibra 600 Mbps", 34.99, 2)
    # gestion_tabla.inserta_servicios(103, "Plan TV Premium", 15.00, 3)
    # gestion_tabla.inserta_servicios(104, "Soporte Técnico 24/7", 9.99, 1)
    # gestion_tabla.inserta_servicios(105, "Seguridad en la Nube", 25.50, 2)
    # gestion_tabla.inserta_servicios(106, "IoT Empresarial", 45.00, 2)
    #
    # Contrataciones de servicios
    # gestion_tabla.inserta_contratado("12345678A", 101, datetime.date.fromisoformat("2024-01-15"))
    # gestion_tabla.inserta_contratado("87654321B", 103, datetime.date.fromisoformat("2024-02-01"))
    # gestion_tabla.inserta_contratado("11223344C", 104, datetime.date.fromisoformat("2024-02-05"))
    # gestion_tabla.inserta_contratado("44332211D", 102, datetime.date.fromisoformat("2024-01-25"))
    # gestion_tabla.inserta_contratado("12345678A", 102, datetime.date.fromisoformat("2024-02-10"))
    # gestion_tabla.inserta_contratado("55554444E", 105, datetime.date.fromisoformat("2024-03-01"))
    #
    # gestion_tabla.incrementar_porcentaje_consulta(0.1, 'Plan%')
    # gestion_tabla.servicios_por_cliente_consulta('Gómez', datetime.date(2020, 1, 31))
    gestion_tabla.contratos_cliente("12345678A")

