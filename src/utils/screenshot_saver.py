"""
Módulo para guardar capturas de pantalla durante las pruebas automatizadas.
"""

import os

from selenium.common.exceptions import WebDriverException


def take_screenshot(driver, route):
    """
    Toma una captura de pantalla y la guarda.
    """
    try:
        # Asegurarnos de que la carpeta destino existe
        directory = os.path.dirname(route)
        if directory:
            os.makedirs(directory, exist_ok=True)

        success = driver.save_screenshot(route)
        if success:
            print(f"Captura de pantalla guardada en {route}")
        else:
            print(f"No se pudo guardar la captura de pantalla en {route}")
    except (WebDriverException, OSError) as e:
        print(f"Error al guardar la captura de pantalla: {e}")
