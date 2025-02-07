import time
from typing import Optional, List, Tuple
from tabla_base import TablaBase


class Tabla1_3(TablaBase):

    def __init__(self, nombre_tabla: str):
        self.nombre_tabla = nombre_tabla
        self.tiempos: List[Tuple[str, float]] = []
        self.diccionario = None

        with open(self.nombre_tabla, 'r') as f:
            registros = f.readlines()
            offset = f.tell()
            for registro in registros:
                comas = registro.strip().split(',')
                clave = comas[0]
                self.diccionario[clave] = offset
                valor = comas[1]
                if len(comas) > 2:
                    for val in comas[2:]:
                        valor = valor + ',' + val
                offset = f.tell() + len(valor)


    def leer(self, clave: int) -> Optional[str]:
        inicio = time.time()
        valor = None
        with open(self.nombre_tabla, 'r') as f:
            offset = self.diccionario[clave]
            f.seek(offset)
            valor = f.readline()
        fin = time.time()
        self.tiempos.append(("e", fin - inicio))
        return valor

    def escribir(self, clave: int, valor: str) -> bool:
        inicio = time.time()
        with open(self.nombre_tabla, 'a') as f:
            pass
        fin = time.time()
        self.tiempos.append(("e", fin - inicio))

    def procesar_operaciones(self, archivo: str) -> None:

        with open(archivo, 'r') as f:
            for linea in f:
                partes = linea.strip().split(" ", 2)
                if partes[0] == "l":
                    clave = partes[1]
                    print(self.leer(clave))
                elif partes[0] == "e":
                    clave, valor = partes[1], partes[2]
                    self.escribir(clave, valor)
       
    def tiempos(self) -> List[Tuple[str, float]]:
        return self.tiempos


if __name__ == "__main__":
