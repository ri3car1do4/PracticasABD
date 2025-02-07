from typing import TextIO


def nombre_tabla2archivo(nombre_tabla: str) -> str:
    return f"{nombre_tabla}.txt"


def leer(clave: int, nombre_tabla: str) -> str:
    archivo = nombre_tabla2archivo(nombre_tabla)

    with open(archivo, 'r') as f:
        registros = f.readlines()

        # Iteramos sobre los registros desde el final para encontrar el último con la clave
        for registro in reversed(registros):
            comas = registro.strip().split(',')
            clave_actual = comas[0]
            if int(clave_actual) == clave:
                valor = comas[1]
                if len(comas) > 2:
                    for val in comas[2:]:
                        valor = valor + ',' + val
                return valor


def escribir(clave: int, valor: str, nombre_tabla: str):
    archivo = nombre_tabla2archivo(nombre_tabla)

    with open(archivo, 'a') as f:
        f.write(f"{clave},{valor}\n")


if __name__ == "__main__":
    # El código del script va aquí
    # Escribimos registros random
    escribir(1, "valor_1", "tabla1")
    escribir(2, "valor_2,9", "tabla1")
    escribir(1, "valor_1_modificado", "tabla1")

    # Leemos los registros
    print(leer(1, "tabla1"))  # Imprimira "valor_1_modificado"
    print(leer(2, "tabla1"))  # Imprimira "valor_2"

    # Intentamos leer una clave que no esta
    print(leer(3, "tabla1"))  # Imprimira None
