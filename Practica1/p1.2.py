import time
from typing import Optional
from tabla_base import TablaBase


class Tabla1_2(TablaBase):

    def __init__(self, nombre_tabla: str):
        self.nombre_tabla = nombre_tabla
        self.tiempos: List[Tuple[str, float]] = []

    def leer(self, clave: int) -> Optional[str]:
        inicio = time.time()
        with open(self.nombre_tabla, 'r') as f:
            registros = f.readlines()

            # Iteramos sobre los registros desde el final para encontrar el último con la clave
            for registro in reversed(registros):
                comas = registro.strip().split(',')
                clave_actual = comas[0]
                valor = None
                if int(clave_actual) == clave:
                    valor = comas[1]
                    if len(comas) > 2:
                        for val in comas[2:]:
                            valor = valor + ',' + val
                        
        fin = time.time()
        self.tiempos.append(("e", fin - inicio))
        return valor

    def escribir(self, clave: int, valor: str) -> bool:
        inicio = time.time()
        with open(self.nombre_tabla, 'a') as f:
            f.write(f"{clave},{valor}\n")
        fin = time.time()
        self.tiempos.append(("e", fin - inicio))

    def procesar_operaciones(self, archivo: str) -> None:

        with open(archivo, 'r') as f:
            for linea in f:
                partes = linea.strip().split(" ", 2)
                if partes[0] == "l":
                    clave = partes[1]
                    print(self.leer(clave))
                elif partes[0] == "e"
                    clave, valor = partes[1], partes[2]
                    self.escribir(clave, valor)
       
    def tiempos(self) -> List[Tuple[str, float]]:
        return self.tiempos


if __name__ == "__main__":
    # El código del script va aquí
    # Escribimos registros random
    escribir(1, "valor_1", "tabla1")
    escribir(2, "valor_2", "tabla1")
    escribir(1, "valor_1_modificado", "tabla1")

    # Leemos los registros
    print(leer(1, "tabla1"))  # Imprimira "valor_1_modificado"
    print(leer(2, "tabla1"))  # Imprimira "valor_2"

    # Intentamos leer una clave que no esta
    print(leer(3, "tabla1"))  # Imprimira None
