import os.path
import time
from abc import ABC
from typing import Optional, List, Tuple
from tabla_base import TablaBase

class Segmento(TablaBase):
    NUM_REGISTROS = 100

    def __init__(self, nombre_tabla: str):
        self.nombre_tabla = nombre_tabla
        self.tiempos: List[Tuple[str, float]] = []
        self.diccionario = {}
        self.claves = []
        self.escrituras = 0

    def leer(self, clave: int) -> Optional[str]:
        valor = None
        with open(self.nombre_tabla, 'r') as f:
            if clave in self.diccionario:
                offset = self.diccionario[clave]
                f.seek(offset)
                valor = f.readline() # lee la línea hasta un salto de línea
        return valor

    def escribir(self, clave: int, valor: str) -> bool:
        with open(self.nombre_tabla, 'a') as f:
            self.diccionario[clave] = f.tell()
            f.write(f"{clave},{valor}\n")
            self.claves.append(clave)
            self.escrituras += 1

    def claves_almacenadas(self) -> List[int]:
        return self.claves

    def escrituras_realizadas(self) -> int:
        return self.escrituras


class Tabla1_4(TablaBase):

    def __init__(self, nombre_tabla: str):
        self.nombre_tabla = nombre_tabla
        self.tiempos: List[Tuple[str, float]] = []
        self.diccionario = {}

        if os.path.exists(self.nombre_tabla):
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
            if clave in self.diccionario:
                offset = self.diccionario[clave]
                f.seek(offset)
                valor = f.readline() # lee la línea hasta un salto de línea
        fin = time.time()
        self.tiempos.append(("e", fin - inicio))
        return valor

    def escribir(self, clave: int, valor: str) -> bool:
        inicio = time.time()
        with open(self.nombre_tabla, 'a') as f:
            self.diccionario[clave] = f.tell()
            f.write(f"{clave},{valor}\n")
        fin = time.time()
        self.tiempos.append(("e", fin - inicio))
        return 1==1

    def procesar_operaciones(self, archivo: str) -> None:

        with open(archivo, 'r') as f:
            for linea in f:
                partes = linea.strip().split(" ", 2)
                if partes[0] == "l":
                    clave = partes[1]
                    valor = self.leer(clave)
                    if valor is not None:
                        print(valor)
                    else:
                        print(f"Valor de {clave} no encontrado")
                elif partes[0] == "e":
                    clave, valor = partes[1], partes[2]
                    self.escribir(clave, valor)
       
    def tiempos(self) -> List[Tuple[str, float]]:
        return self.tiempos

if __name__ == "__main__":
    tabla1_4 = Tabla1_4("tabla1_3.txt")
    tabla1_4.procesar_operaciones("archivo.txt")