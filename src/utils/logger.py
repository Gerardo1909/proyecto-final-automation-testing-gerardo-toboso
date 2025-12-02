"""
Módulo para logging de la aplicación.
"""

import logging
import os
from logging.handlers import RotatingFileHandler


LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def get_logger(name="tests_logger", filename="test.log"):
    """
    Obtiene un logger configurado con handlers de consola y archivo.

    Args:
        name: Nombre del logger (por defecto "tests_logger")

    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)

    # Evitar duplicar handlers si el logger ya existe
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Formato detallado para mejor observabilidad
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s - %(message)s", datefmt="%H:%M:%S"
    )

    # Handler para archivo con rotación
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, filename),
        maxBytes=1024 * 1024,  # 1MB por archivo
        backupCount=5,  # Mantener 5 archivos históricos
        encoding="utf-8"  # Codificación UTF-8 para caracteres especiales
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


# Loggers
ui_logger = get_logger(name="ui_logger", filename="ui.log")
api_logger = get_logger(name="api_logger", filename="api.log")
e2e_logger = get_logger(name="e2e_logger", filename="e2e.log")
