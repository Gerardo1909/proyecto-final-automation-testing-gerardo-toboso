"""
Módulo que define la interfaz abstracta para lectores de archivos.
Implementa el patrón Strategy para leer diferentes tipos de archivos.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Tuple, Any


class FileReader(ABC):
    """
    Clase abstracta que define la interfaz para lectores de archivos.
    El formato de retorno está optimizado para ser usado con pytest.parametrize.
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._validate_file()

    def _validate_file(self) -> None:
        """
        Valida que el archivo existe y es accesible.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"El archivo {self.file_path} no existe")

        if not self.file_path.is_file():
            raise ValueError(f"La ruta {self.file_path} no es un archivo válido")

    @abstractmethod
    def read(self) -> List[Tuple[Any, ...]]:
        """
        Lee el archivo y devuelve los datos en formato compatible con pytest.parametrize.
        """
        pass
