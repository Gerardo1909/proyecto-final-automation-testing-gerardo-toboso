"""
Módulo para leer archivos JSON y convertirlos a formato compatible con pytest.parametrize.
"""

import json
from typing import List, Tuple, Any, Dict
from utils.file_reader import FileReader


class JSONReader(FileReader):
    """
    Lector de archivos JSON.
    """

    def read(self) -> List[Tuple[Any, ...]]:
        """
        Lee un archivo JSON y devuelve una lista de tuplas.
        Espera un array de objetos JSON y convierte cada objeto a una tupla de valores.
        """
        with open(self.file_path, mode="r", encoding="utf-8") as archivo:
            datos_json = json.load(archivo)
        if not isinstance(datos_json, list):
            raise ValueError(
                f"El archivo JSON debe contener un array. "
                f"Se encontró: {type(datos_json).__name__}"
            )
        datos = []
        for item in datos_json:
            if isinstance(item, dict):
                datos.append(tuple(item.values()))
            else:
                datos.append((item,))

        return datos

    def read_as_dicts(self) -> List[Dict[str, Any]]:
        """
        Lee el archivo JSON y devuelve los datos como lista de diccionarios.
        """
        with open(self.file_path, mode="r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def read_field_as_tuples(self, field_name: str) -> List[Tuple[Any]]:
        """
        Lee el archivo JSON y extrae un campo específico de cada objeto,
        devolviéndolo como lista de tuplas de un solo elemento.
        Útil para parametrizar tests con un solo valor.

        Args:
            field_name: Nombre del campo a extraer de cada objeto JSON

        Returns:
            Lista de tuplas con el valor del campo.
            Ejemplo: [('Sauce Labs Backpack',), ('Sauce Labs Bike Light',)]
        """
        datos_json = self.read_as_dicts()
        return [(item[field_name]) for item in datos_json if field_name in item]
