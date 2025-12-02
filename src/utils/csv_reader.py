"""
Módulo para leer archivos CSV y convertirlos a formato compatible con pytest.parametrize.
"""
import csv
from typing import List, Tuple, Any
from utils.file_reader import FileReader


class CSVReader(FileReader):
    """
    Lector de archivos CSV.
    """

    def read(self) -> List[Tuple[Any, ...]]:
        """
        Lee un archivo CSV y devuelve una lista de tuplas.
        La primera fila se considera como encabezado y se omite.
        Convierte valores booleanos de string a tipo bool.
        """
        datos = []
        with open(self.file_path, mode='r', encoding='utf-8', newline='') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                valores_procesados = tuple(
                    self._convert_value(valor) for valor in fila.values()
                )
                datos.append(valores_procesados)
        return datos

    def _convert_value(self, valor: str) -> Any:
        """
        Convierte valores string a sus tipos apropiados.
        Principalmente convierte 'True'/'False' a booleanos.
        """
        if valor.lower() == 'true':
            return True
        elif valor.lower() == 'false':
            return False
        try:
            if '.' in valor:
                return float(valor)
            return int(valor)
        except ValueError:
            return valor
