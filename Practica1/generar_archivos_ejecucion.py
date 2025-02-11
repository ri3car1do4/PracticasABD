import sys
import random
import numpy as np

# Valores por defecto
NUM_COMMANDS = 2000
MAX_CLAVES = 50
MAX_SIZE_VALOR = 10
READ_PROB = 0.01


def comandos_aleatorios(num_commands: int = NUM_COMMANDS, max_claves: int = MAX_CLAVES,
                        max_size_valor: int = MAX_SIZE_VALOR, read_prob: float = READ_PROB):
    """
    Generador que produce datos aleatorios en función de nuestro formato de ejecución de comandos
    """
    for i in range(num_commands):
        c = np.random.choice(["l", "e"], p=[1-read_prob, read_prob])
        clave = random.randint(0, max_claves)
        if c == "e":
            random_data = random.randbytes(random.randint(1, max_size_valor))
            yield f"{c} {clave} {random_data}"
        else:
            yield f"{c} {clave}"


def escribir_comandos_aleatorios_archivo(filename: str) -> None:
    with open(filename, 'w') as f:
        for random_command in comandos_aleatorios():
            # Es mejor escribirlos uno a uno para así
            # evitar cargar todos los comandos directamente en memoria
            f.write(random_command + '\n')


if __name__ == "__main__":
    # Este script nos permite generar archivos
    # para probar las distintas implementaciones
    # sys.argv[1] devuelve el primer string leído por
    # consola, sys.argv[2] el segundo y así sucesivamente
    escribir_comandos_aleatorios_archivo(sys.argv[1])
