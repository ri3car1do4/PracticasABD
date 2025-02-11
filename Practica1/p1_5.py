import time
from p1_2 import Tabla1_2
from p1_3 import Tabla1_3
from p1_4 import Tabla1_4

if __name__ == "__main__":
    tabla1_2 = Tabla1_2("tabla1_2.txt")
    tabla1_3 = Tabla1_3("tabla1_3.txt")
    tabla1_4 = Tabla1_4("tabla1_4.txt")

    tabla1_2.procesar_operaciones("lecturas.txt")
    tiempos1_2 = tabla1_2.tiempos()
    t1_2e = 0
    t1_2l = 0
    for tiempo in tiempos1_2:
        if tiempo[0] == "e":
            t1_2e += tiempo[1]
        elif tiempo[0] == "l":
            t1_2l += tiempo[1]

    tabla1_3.procesar_operaciones("lecturas.txt")
    tiempos1_3 = tabla1_3.tiempos()
    t1_3e = 0
    t1_3l = 0
    for tiempo in tiempos1_3:
        if tiempo[0] == "e":
            t1_3e += tiempo[1]
        elif tiempo[0] == "l":
            t1_3l += tiempo[1]

    tabla1_4.procesar_operaciones("lecturas.txt")
    tiempos1_4 = tabla1_4.tiempos()
    t1_4e = 0
    t1_4l = 0
    for tiempo in tiempos1_4:
        if tiempo[0] == "e":
            t1_4e += tiempo[1]
        else:
            t1_4l += tiempo[1]

    print(f"Tiempo 1_2(escritura): {t1_2e}\n Tiempo1_2(lectura): {t1_2l}\n")
    print(f"Tiempo 1_3(escritura): {t1_3e}\n Tiempo1_3(lectura): {t1_3l}\n")
    print(f"Tiempo 1_4(escritura): {t1_4e}\n Tiempo1_4(lectura): {t1_4l}\n")