"""
Módulo de utilidades para validación de respuestas API.
"""

import pytest_check as check


def validate_api_response(
    response, expected_status, expected_fields=None, max_time=15.0
):
    """
    Función helper para validar respuestas API con los 5 niveles de validación.

    Args:
        response: Objeto Response de requests
        expected_status: Código de status HTTP esperado
        expected_fields: Set de campos esperados en la respuesta JSON (opcional)
        max_time: Tiempo máximo de respuesta en segundos (default 15.0)

    Returns:
        Dict con el JSON de la respuesta si existe, None si no hay contenido
    """
    # Nivel 1: Status Code
    check.equal(
        response.status_code,
        expected_status,
        f"Status code incorrecto. Esperado: {expected_status}, Obtenido: {response.status_code}",
    )

    # Nivel 2: Headers
    if expected_status != 204:  # 204 No Content puede no tener Content-Type
        check.is_in(
            "application/json",
            response.headers.get("Content-Type", ""),
            f"Content-Type incorrecto. Obtenido: {response.headers.get('Content-Type')}",
        )

    # Nivel 3-4: Estructura y contenido (si hay expected_fields)
    body = None
    if expected_fields and response.text:
        try:
            body = response.json()
            # Para listas, validar el primer elemento
            if isinstance(body, list) and len(body) > 0:
                actual_fields = set(body[0].keys())
            elif isinstance(body, dict):
                actual_fields = set(body.keys())
            else:
                actual_fields = set()

            check.is_true(
                expected_fields <= actual_fields,
                f"Campos faltantes en la respuesta. Esperados: {expected_fields}, Obtenidos: {actual_fields}",
            )
        except Exception as e:
            check.fail(f"Error al parsear JSON: {str(e)}")

    # Nivel 5: Performance
    elapsed_time = response.elapsed.total_seconds()
    check.less(
        elapsed_time,
        max_time,
        f"Respuesta muy lenta. Tiempo: {elapsed_time:.2f}s, Máximo: {max_time}s",
    )

    # Retornar el body parseado si existe
    if response.text and expected_status != 204:
        return response.json() if body is None else body
    return None
