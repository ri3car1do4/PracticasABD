import os
import time
from typing import Optional, List, Tuple
from tabla_base import TablaBase


class Tabla1_2(TablaBase):

    def __init__(self, nombre_tabla: str):
        self.nombre_tabla = nombre_tabla
        self.tiempos: List[Tuple[str, float]] = []

        # Verificamos si el archivo existe; si no, se crea vacío
        if not os.path.exists(self.nombre_tabla):
            with open(self.nombre_tabla, 'w') as f:
                pass  # Crea el archivo vacío


    def leer(self, clave: int) -> Optional[str]:
        inicio = time.time()
        with open(self.nombre_tabla, 'r') as f:
            registros = f.readlines()
            valor = None

            # Iteramos sobre los registros desde el final para encontrar el último con la clave
            if len(registros) > 0:
                i = len(registros) - 1
                comas = registros[i].strip().split(',')
                while i >= 0 and comas[0] != clave:
                    i -= 1
                    comas = registros[i].strip().split(',')

                if i >= 0:
                    valor = comas[1]
                    if len(comas) > 2:
                        for val in comas[2:]:
                            valor = valor + ',' + val


            #for registro in reversed(registros):
             #   comas = registro.strip().split(',')
              #  clave_actual = comas[0]
               # if int(clave_actual) == clave:
                #    valor = comas[1]
                 #   if len(comas) > 2:
                  #      for val in comas[2:]:
                   #         valor = valor + ',' + val

                        
        fin = time.time()
        self.tiempos.append(("e", fin - inicio))
        return valor

    def escribir(self, clave: int, valor: str) -> bool:
        inicio = time.time()
        with open(self.nombre_tabla, 'a') as f:
            f.write(f"{clave},{valor}\n")
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
    tabla1_2 = Tabla1_2("tabla1_2.txt")
    tabla1_2.procesar_operaciones("archivo.txt")