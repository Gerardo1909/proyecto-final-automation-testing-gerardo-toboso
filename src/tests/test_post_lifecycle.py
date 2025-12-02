"""
Tests E2E para el ciclo de vida completo de un post en JSONPlaceholder.
Simula el flujo real: Crear -> Leer -> Actualizar -> Eliminar (CRUD).
"""

import pytest
import requests
import pytest_check as check
from utils.logger import e2e_logger
from utils.api_utils import validate_api_response

API_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="module")
def created_post():
    """
    Fixture que simula la creación de un post.
    """
    e2e_logger.info("Creando post para el ciclo de vida E2E")

    endpoint = f"{API_URL}/posts"
    payload = {
        "title": "Post para testing E2E",
        "body": "Contenido del post de prueba para el ciclo de vida completo",
        "userId": 1,
    }
    expected_fields = {"id", "title", "body", "userId"}

    e2e_logger.info(f"POST a {endpoint} con payload: {payload}")
    response = requests.post(endpoint, json=payload, timeout=5)

    # Validar la respuesta con la función helper
    post_data = validate_api_response(response, 201, expected_fields)

    if post_data:
        e2e_logger.info(f"POST exitoso, ID retornado: {post_data.get('id')}")
        # Usamos ID 1 (existente) para las siguientes operaciones
        post_data["id"] = 1
        e2e_logger.info("Usando post existente ID 1 para el resto del flujo E2E")
    else:
        post_data = {"id": 1, "userId": 1, "title": "", "body": ""}

    return post_data


@pytest.mark.e2e
@pytest.mark.api
def test_post_lifecycle_step_1_create_post_should_return_201_with_id(created_post):
    """
    Paso 1 del ciclo de vida: Crear un post.
    Verifica que el post se cree correctamente con status 201 y retorne un ID.
    """
    e2e_logger.info("PASO 1: Validando creación del post")

    # Arrange & Act (realizado en la fixture)
    post_data = created_post

    # Assert
    check.is_not_none(post_data, "No se recibió respuesta de la creación del post")
    check.is_not_none(post_data.get("id"), "El post creado no tiene ID")
    check.equal(
        post_data.get("title"), "Post para testing E2E", "El título no coincide"
    )
    check.equal(
        post_data.get("body"),
        "Contenido del post de prueba para el ciclo de vida completo",
        "El body no coincide",
    )
    check.equal(post_data.get("userId"), 1, "El userId no coincide")

    e2e_logger.info(f"Post creado correctamente con ID: {post_data.get('id')}")


@pytest.mark.e2e
@pytest.mark.api
def test_post_lifecycle_step_2_read_created_post_should_return_200_with_data(
    created_post,
):
    """
    Paso 2 del ciclo de vida: Leer el post existente.
    Verifica que el post pueda ser recuperado mediante GET.
    """
    e2e_logger.info("PASO 2: Leyendo el post")

    # Arrange
    post_id = created_post.get("id")
    endpoint = f"{API_URL}/posts/{post_id}"
    expected_fields = {"userId", "id", "title", "body"}

    # Act
    e2e_logger.info(f"GET a {endpoint}")
    response = requests.get(endpoint, timeout=5)

    # Assert
    body = validate_api_response(response, 200, expected_fields)

    check.is_not_none(body, "La respuesta no contiene datos")
    check.equal(body.get("id"), post_id, f"El ID no coincide. Esperado: {post_id}")
    check.is_not_none(body.get("title"), "El título no debería estar vacío")
    check.is_not_none(body.get("body"), "El contenido no debería estar vacío")

    e2e_logger.info(f"Post {post_id} recuperado exitosamente")


@pytest.mark.e2e
@pytest.mark.api
def test_post_lifecycle_step_3_update_post_with_patch_should_return_200(created_post):
    """
    Paso 3 del ciclo de vida: Actualizar parcialmente el post con PATCH.
    Verifica que el post pueda ser actualizado parcialmente.
    """
    e2e_logger.info("PASO 3: Actualizando parcialmente el post con PATCH")

    # Arrange
    post_id = created_post.get("id")
    endpoint = f"{API_URL}/posts/{post_id}"
    partial_update = {"title": "Titulo actualizado por QA"}
    expected_fields = {"id", "title", "body", "userId"}

    # Act
    e2e_logger.info(f"PATCH a {endpoint} con datos: {partial_update}")
    response = requests.patch(endpoint, json=partial_update, timeout=5)

    # Assert
    body = validate_api_response(response, 200, expected_fields)

    check.is_not_none(body, "La respuesta no contiene datos")
    check.equal(body.get("id"), post_id, "El ID no debería cambiar")
    check.equal(
        body.get("title"),
        partial_update["title"],
        "El titulo no se actualizo correctamente",
    )
    check.is_not_none(body.get("body"), "El body no debería eliminarse en PATCH")
    check.is_not_none(body.get("userId"), "El userId no debería eliminarse en PATCH")

    e2e_logger.info(f"Post {post_id} actualizado parcialmente con exito")


@pytest.mark.e2e
@pytest.mark.api
def test_post_lifecycle_step_4_update_post_with_put_should_return_200(created_post):
    """
    Paso 4 del ciclo de vida: Actualizar completamente el post con PUT.
    Verifica que el post pueda ser actualizado completamente.
    """
    e2e_logger.info("PASO 4: Actualizando completamente el post con PUT")

    # Arrange
    post_id = created_post.get("id")
    endpoint = f"{API_URL}/posts/{post_id}"
    full_update = {
        "title": "Post completamente actualizado",
        "body": "Nuevo contenido completo del post despues de PUT",
        "userId": 1,
    }
    expected_fields = {"id", "title", "body", "userId"}

    # Act
    e2e_logger.info(f"PUT a {endpoint} con datos completos")
    response = requests.put(endpoint, json=full_update, timeout=5)

    # Assert
    body = validate_api_response(response, 200, expected_fields)

    check.is_not_none(body, "La respuesta no contiene datos")
    check.equal(body.get("id"), post_id, "El ID no deberia cambiar")
    check.equal(
        body.get("title"),
        full_update["title"],
        "El titulo no se actualizo correctamente",
    )
    check.equal(
        body.get("body"), full_update["body"], "El body no se actualizo correctamente"
    )
    check.equal(body.get("userId"), full_update["userId"], "El userId no coincide")

    e2e_logger.info(f"Post {post_id} actualizado completamente con exito")


@pytest.mark.e2e
@pytest.mark.api
def test_post_lifecycle_step_5_delete_post_should_return_200(created_post):
    """
    Paso 5 del ciclo de vida: Eliminar el post.
    Verifica que el post pueda ser eliminado correctamente.
    """
    e2e_logger.info("PASO 5: Eliminando el post")

    # Arrange
    post_id = created_post.get("id")
    endpoint = f"{API_URL}/posts/{post_id}"

    # Act
    e2e_logger.info(f"DELETE a {endpoint}")
    response = requests.delete(endpoint, timeout=5)

    # Assert
    validate_api_response(response, 200)

    e2e_logger.info(f"Post {post_id} eliminado correctamente")
