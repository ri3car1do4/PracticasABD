import os.path
import time
from abc import ABC
from typing import Optional, List, Tuple
from tabla_base import TablaBase
from pathlib import Path

class Segmento(TablaBase):

    NUM_REGISTROS = 50

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
        return True

    def procesar_operaciones(self, archivo: str) -> None:
        pass

    def tiempos(self) -> List[Tuple[str, float]]:
        pass

    def claves_almacenadas(self) -> List[int]:
        return self.claves

    def escrituras_realizadas(self) -> int:
        return self.escrituras


class Tabla1_4(TablaBase):

    def __init__(self, nombre_tabla: str):
        self.nombre_tabla = nombre_tabla
        self.tiempos: List[Tuple[str, float]] = []

        self.dir = Path('Practica1')
        self.dir.mkdir(exist_ok=True)

        self.segmentos = self._cargar_segmentos()
        self.nSegmentos = len(self.segmentos)
        self.consolidacion = 0

        for segemento in self.segmentos:
            for clave in segemento.claves_almacenadas():
                self.diccionario[clave] = None

    def _cargar_segmentos(self) -> List[Segmento]:
        segmentos = []
        for archivo in self.dir.glob("*.txt"):
            segmentos.append(Segmento(str(archivo)))
        return segmentos

    def _nuevo_segmento(self) -> Segmento:
        self.nSegmentos += 1
        segmento = Segmento(f"{self.nSegmentos}.txt")
        self.segmentos.append(segmento)
        self.consolidacion += 1
        if self.consolidacion >= 10:
            self._consolidacion()
        return segmento

    def _consolidacion(self):
        self.consolidacion = 0
        segmento_consolidado = self._nuevo_segmento() # Segmento de consolidación

        claves_almacenadas = {}
        for segmento in reversed(self.segmentos):
            for clave in segmento.claves_almacenadas():
                if clave not in claves_almacenadas:
                    valor = segmento.leer(clave)
                    if valor is not None:
                        segmento_consolidado.escribir(clave, valor.strip())
                        claves_almacenadas[clave] = None

        # Eliminar los segmentos antiguos menos el consolidado
        for segmento in self.segmentos:
            os.remove(segmento.nombre_tabla)

        self.segmentos = [segmento_consolidado]



    def leer(self, clave: int) -> Optional[str]:
        inicio = time.time()
        valor = None
        if len(self.segmentos) > 0:
            i = len(self.segmentos) - 1
            while i >= 0 and self.segmentos[i].leer(clave) is None:
                i -= 1
            if i >= 0:
                valor = self.segmentos[i].leer(clave)
        fin = time.time()
        self.tiempos.append(("e", fin - inicio))
        return valor

    def escribir(self, clave: int, valor: str) -> bool:
        inicio = time.time()
        if not self.segmentos or self.segmentos[-1].escrituras_realizadas() >= Segmento.NUM_REGISTROS:
            self.segmentos.append(self._nuevo_segmento())

        self.segmentos[-1].escribir(clave, valor)

        fin = time.time()
        self.tiempos.append(("e", fin - inicio))
        return True

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
    tabla1_4 = Tabla1_4("tabla1_4.txt")
    tabla1_4.procesar_operaciones("archivo2.txt")