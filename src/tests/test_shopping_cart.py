"""
Tests para el flujo de uso del carrito de compras en https://www.saucedemo.com/
"""

from pathlib import Path

import pytest
import pytest_check as check

from pages.catalog_page import CatalogPage
from utils.json_reader import JSONReader
from utils.logger import ui_logger

# Cargar nombres de productos desde el archivo JSON
PRODUCTOS_JSON_PATH = Path(__file__).parent.parent / "data" / "productos.json"
json_reader = JSONReader(str(PRODUCTOS_JSON_PATH))
NOMBRES_PRODUCTOS = json_reader.read_field_as_tuples("nombre")
PRODUCTOS_COMPLETOS = json_reader.read_as_dicts()


@pytest.mark.smoke
@pytest.mark.ui
def test_product_should_be_added_to_cart_when_add_to_cart_button_is_clicked(
    selenium_driver,
):
    """
    Prueba que verifica que un producto se agregue al carrito al hacer clic en el botón "Add to cart".
    """
    # Arrange
    catalog_page = CatalogPage(selenium_driver)

    # Act
    ui_logger.info("Iniciando test_product_should_be_added_to_cart_when_add_to_cart_button_is_clicked")
    catalog_page.add_product_to_cart_by_index(0)
    item_count = catalog_page.get_cart_item_count()
    ui_logger.info(f"Cantidad de productos en carrito: {item_count}")

    # Assert
    check.equal(item_count, 1, "El producto no se agrego correctamente al carrito")
    ui_logger.info("Test completado exitosamente")


@pytest.mark.ui
def test_multiple_products_should_be_added_to_cart_when_add_to_cart_buttons_are_clicked(
    selenium_driver,
):
    """
    Prueba que verifica que múltiples productos se agreguen al carrito al hacer clic en varios botones "Add to cart".
    """
    ui_logger.info(
        "Iniciando test_multiple_products_should_be_added_to_cart_when_add_to_cart_buttons_are_clicked"
    )

    # Arrange
    catalog_page = CatalogPage(selenium_driver)
    expected_count = 6

    # Act
    ui_logger.info(f"Agregando {expected_count} productos al carrito")
    for _ in range(expected_count):
        catalog_page.add_product_to_cart_by_index(0)
    item_count = catalog_page.get_cart_item_count()
    ui_logger.info(f"Productos agregados: {item_count}")

    # Assert
    check.equal(item_count, expected_count, 
        f"Se esperaban {expected_count} productos pero se encontraron {item_count}"
    )
    ui_logger.info("Test completado exitosamente")


@pytest.mark.ui
@pytest.mark.parametrize("nombre_producto", NOMBRES_PRODUCTOS)
def test_cart_should_display_product_when_added_and_cart_icon_clicked(
    selenium_driver, nombre_producto
):
    """
    Test parametrizado que verifica que el carrito muestre el producto correcto
    cuando se agrega y se accede al carrito.
    """
    ui_logger.info(
        f"Iniciando test_cart_should_display_product_when_added_and_cart_icon_clicked - Producto: {nombre_producto}"
    )

    # Arrange
    catalog_page = CatalogPage(selenium_driver)
    ui_logger.info(f"Agregando producto al carrito: {nombre_producto}")
    catalog_page.add_product_to_cart_by_name(nombre_producto)

    # Act
    cart_page = catalog_page.go_to_cart()
    cart_items = cart_page.get_cart_items()
    item_names = cart_page.get_item_names()
    ui_logger.info(f"Productos en carrito: {item_names}")

    # Assert
    check.equal(len(cart_items), 1, "El carrito no contiene exactamente 1 producto")
    check.is_in(nombre_producto, item_names, 
        f"El producto {nombre_producto} no esta en el carrito"
    )
    ui_logger.info(f"Test completado exitosamente - {nombre_producto}")


@pytest.mark.ui
@pytest.mark.parametrize("nombre_producto", NOMBRES_PRODUCTOS)
def test_cart_should_display_all_products_when_multiple_products_added(
    selenium_driver, nombre_producto, productos_agregados=PRODUCTOS_COMPLETOS
):
    """
    Prueba que verifica que el carrito muestre todos los productos cuando se agregan múltiples productos.
    """
    # Arrange
    catalog_page = CatalogPage(selenium_driver)

    # Act
    for producto in productos_agregados:
        catalog_page.add_product_to_cart_by_name(producto["nombre"])

    cart_page = catalog_page.go_to_cart()
    cart_items = cart_page.get_cart_items()
    item_names = cart_page.get_item_names()

    # Assert
    check.equal(len(cart_items), len(productos_agregados), 
        f"Se esperaban {len(productos_agregados)} productos pero se encontraron {len(cart_items)}"
    )
    check.is_in(nombre_producto, item_names, 
        f"El producto {nombre_producto} no esta en el carrito"
    )


@pytest.mark.smoke
@pytest.mark.ui
def test_cart_should_remove_product_when_remove_button_is_clicked(selenium_driver):
    """
    Prueba que verifica que un producto se elimine del carrito al hacer clic en el botón "Remove".
    """
    ui_logger.info(
        "Iniciando test_cart_should_remove_product_when_remove_button_is_clicked"
    )

    # Arrange
    catalog_page = CatalogPage(selenium_driver)
    catalog_page.add_product_to_cart_by_index(0)
    ui_logger.info("Producto agregado al carrito")
    page = catalog_page.go_to_cart()
    ui_logger.info("Navegando al carrito")

    # Act
    page.click_remove_button_by_index(0)
    ui_logger.info("Producto removido del carrito")
    cart_items = page.get_cart_items()

    # Assert
    check.equal(len(cart_items), 0, "El carrito no esta vacio despues de remover el producto")
    ui_logger.info("Test completado exitosamente")
