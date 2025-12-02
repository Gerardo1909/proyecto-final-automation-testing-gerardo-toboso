"""
Tests para endpoints de API en https://jsonplaceholder.typicode.com/
"""

import pytest
import requests
import pytest_check as check
from utils.logger import api_logger
from utils.api_utils import validate_api_response

API_URL = "https://jsonplaceholder.typicode.com"


@pytest.mark.api
def test_get_all_posts_should_return_list_when_endpoint_is_called():
    """
    Prueba GET para obtener todos los posts.
    Verifica que la API retorne una lista de posts con la estructura correcta.
    """
    api_logger.info(
        "Iniciando test_get_all_posts_should_return_list_when_endpoint_is_called"
    )

    # Arrange
    endpoint = f"{API_URL}/posts"
    expected_fields = {"userId", "id", "title", "body"}

    # Act
    api_logger.info(f"Realizando GET a {endpoint}")
    response = requests.get(endpoint, timeout=5)

    # Assert
    body = validate_api_response(response, 200, expected_fields)

    check.is_not_none(body, "La respuesta no contiene datos")
    check.is_true(isinstance(body, list), "La respuesta no es una lista")
    check.greater(len(body), 0, "La lista de posts está vacía")

    api_logger.info(f"Test completado exitosamente - {len(body)} posts obtenidos")


@pytest.mark.api
def test_get_single_post_should_return_post_when_valid_id_provided():
    """
    Prueba GET para obtener un post específico por ID.
    Verifica que la API retorne un post individual con todos sus campos.
    """
    api_logger.info(
        "Iniciando test_get_single_post_should_return_post_when_valid_id_provided"
    )

    # Arrange
    post_id = 1
    endpoint = f"{API_URL}/posts/{post_id}"
    expected_fields = {"userId", "id", "title", "body"}

    # Act
    api_logger.info(f"Realizando GET a {endpoint}")
    response = requests.get(endpoint, timeout=5)

    # Assert
    body = validate_api_response(response, 200, expected_fields)

    check.is_not_none(body, "La respuesta no contiene datos")
    check.is_true(isinstance(body, dict), "La respuesta no es un objeto")
    check.equal(
        body.get("id"), post_id, f"El ID del post no coincide. Esperado: {post_id}"
    )

    api_logger.info(
        f"Test completado exitosamente - Post {post_id} obtenido: {body.get('title')}"
    )


@pytest.mark.api
def test_post_create_post_should_return_created_when_valid_data_provided():
    """
    Prueba POST para crear un nuevo post.
    Verifica que la API cree el recurso y retorne status 201 con el recurso creado.
    """
    api_logger.info(
        "Iniciando test_post_create_post_should_return_created_when_valid_data_provided"
    )

    # Arrange
    endpoint = f"{API_URL}/posts"
    new_post = {
        "title": "Test Post Title",
        "body": "Este es el contenido del post de prueba",
        "userId": 1,
    }
    expected_fields = {"id", "title", "body", "userId"}

    # Act
    api_logger.info(f"Realizando POST a {endpoint}")
    response = requests.post(endpoint, json=new_post, timeout=5)

    # Assert
    body = validate_api_response(response, 201, expected_fields)

    check.is_not_none(body, "La respuesta no contiene datos")
    check.equal(body.get("title"), new_post["title"], "El título del post no coincide")
    check.equal(body.get("body"), new_post["body"], "El body del post no coincide")
    check.equal(body.get("userId"), new_post["userId"], "El userId no coincide")
    check.is_not_none(body.get("id"), "El post creado no tiene ID")

    api_logger.info(
        f"Test completado exitosamente - Post creado con ID: {body.get('id')}"
    )


@pytest.mark.api
def test_put_update_post_should_return_updated_when_valid_data_provided():
    """
    Prueba PUT para actualizar completamente un post existente.
    Verifica que la API actualice todos los campos del recurso.
    """
    api_logger.info(
        "Iniciando test_put_update_post_should_return_updated_when_valid_data_provided"
    )

    # Arrange
    post_id = 1
    endpoint = f"{API_URL}/posts/{post_id}"
    updated_post = {
        "id": post_id,
        "title": "Updated Post Title",
        "body": "Contenido completamente actualizado del post",
        "userId": 1,
    }
    expected_fields = {"id", "title", "body", "userId"}

    # Act
    api_logger.info(f"Realizando PUT a {endpoint}")
    response = requests.put(endpoint, json=updated_post, timeout=5)

    # Assert
    body = validate_api_response(response, 200, expected_fields)

    check.is_not_none(body, "La respuesta no contiene datos")
    check.equal(body.get("id"), post_id, "El ID del post no coincide")
    check.equal(
        body.get("title"),
        updated_post["title"],
        "El título no se actualizó correctamente",
    )
    check.equal(
        body.get("body"), updated_post["body"], "El body no se actualizó correctamente"
    )
    check.equal(body.get("userId"), updated_post["userId"], "El userId no coincide")

    api_logger.info(f"Test completado exitosamente - Post {post_id} actualizado")


@pytest.mark.api
def test_patch_partial_update_post_should_return_updated_when_valid_field_provided():
    """
    Prueba PATCH para actualizar parcialmente un post existente.
    Verifica que la API actualice solo los campos enviados.
    """
    api_logger.info(
        "Iniciando test_patch_partial_update_post_should_return_updated_when_valid_field_provided"
    )

    # Arrange
    post_id = 1
    endpoint = f"{API_URL}/posts/{post_id}"
    partial_update = {"title": "Título Parcialmente Actualizado"}
    expected_fields = {"id", "title", "body", "userId"}

    # Act
    api_logger.info(f"Realizando PATCH a {endpoint}")
    response = requests.patch(endpoint, json=partial_update, timeout=5)

    # Assert
    body = validate_api_response(response, 200, expected_fields)

    check.is_not_none(body, "La respuesta no contiene datos")
    check.equal(body.get("id"), post_id, "El ID del post no coincide")
    check.equal(
        body.get("title"),
        partial_update["title"],
        "El título no se actualizó correctamente",
    )
    check.is_not_none(body.get("body"), "El body no debería ser eliminado en un PATCH")
    check.is_not_none(
        body.get("userId"), "El userId no debería ser eliminado en un PATCH"
    )

    api_logger.info(
        f"Test completado exitosamente - Post {post_id} actualizado parcialmente"
    )


@pytest.mark.api
def test_delete_post_should_return_success_when_valid_id_provided():
    """
    Prueba DELETE para eliminar un post existente.
    Verifica que la API retorne un status exitoso al eliminar el recurso.
    """
    api_logger.info(
        "Iniciando test_delete_post_should_return_success_when_valid_id_provided"
    )

    # Arrange
    post_id = 1
    endpoint = f"{API_URL}/posts/{post_id}"

    # Act
    api_logger.info(f"Realizando DELETE a {endpoint}")
    response = requests.delete(endpoint, timeout=5)

    # Assert
    validate_api_response(response, 200)

    check.equal(
        response.status_code, 200, "El status code no indica éxito en la eliminación"
    )

    api_logger.info(f"Test completado exitosamente - Post {post_id} eliminado")


@pytest.mark.api
def test_get_nonexistent_post_should_return_not_found_when_invalid_id_provided():
    """
    Prueba GET con un ID inexistente.
    Verifica que la API maneje correctamente recursos no encontrados.
    """
    api_logger.info(
        "Iniciando test_get_nonexistent_post_should_return_not_found_when_invalid_id_provided"
    )

    # Arrange
    invalid_id = 99999
    endpoint = f"{API_URL}/posts/{invalid_id}"

    # Act
    api_logger.info(f"Realizando GET a {endpoint} con ID inexistente")
    response = requests.get(endpoint, timeout=5)

    # Assert
    validate_api_response(response, 404)

    check.equal(
        response.status_code, 404, "Se esperaba 404 para un recurso inexistente"
    )

    api_logger.info("Test completado exitosamente - Error 404 manejado correctamente")
