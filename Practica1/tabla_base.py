from typing import List, Tuple, Optional
from abc import abstractmethod, ABC


class TablaBase(ABC):
    """
    Clase abstracta que implementa los metodos comunes a los
    apartados 1.2, 1.3 y 1.4.
    """

    @abstractmethod
    def leer(self, clave: int) -> Optional[str]:
        """
        Lee de la tabla el último valor asociado a la clave "clave".
        Devuelve None si no hay clave
        """
        raise NotImplementedError

    @abstractmethod
    def escribir(self, clave: int, valor: str) -> bool:
        """
        Escribe en la tabla la clave y el valor especificados
        """
        raise NotImplementedError

    @abstractmethod
    def procesar_operaciones(self, archivo: str) -> None:
        """
        Procesa la secuencia de operaciones de lectura y escritura
        en el archivo con nombre "archivo", donde cada línea es de la forma:

        - `l <clave>`: devuelve de la tabla el valor asociado a la clave "<clave>"
           y lo imprime por pantalla.
        - `e <clave> <valor>`: introduce en la tabla el valor "<valor>" asociado
           a la clave "<clave>".
        """
        raise NotImplementedError

    @abstractmethod
    def tiempos(self) -> List[Tuple[str, float]]:
        """
        devuelve una lista con todas las operaciones realizadas y el tiempo que tomaron.
        Cada elemento de la lista es de la forma (<operacion>, <tiempo>),
        donde "<operacion>" es el tipo ("l" o "e") y "<tiempo>" es el tiempo en segundos
        """
        raise NotImplementedError
