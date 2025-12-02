"""
Tests para el flujo de checkout de https://www.saucedemo.com/
"""

from pathlib import Path

import pytest
import pytest_check as check

from pages.catalog_page import CatalogPage
from utils.csv_reader import CSVReader
from utils.json_reader import JSONReader
from utils.logger import ui_logger

# Cargar nombres de productos desde el archivo JSON
PRODUCTOS_JSON_PATH = Path(__file__).parent.parent / "data" / "productos.json"
json_reader = JSONReader(str(PRODUCTOS_JSON_PATH))
NOMBRES_PRODUCTOS = json_reader.read_field_as_tuples("nombre")
PRODUCTOS_COMPLETOS = json_reader.read_as_dicts()

# Cargar datos de checkout desde el archivo CSV
CHECKOUT_CSV_PATH = Path(__file__).parent.parent / "data" / "checkout.csv"
CASOS_CHECKOUT = CSVReader(str(CHECKOUT_CSV_PATH)).read()


@pytest.mark.ui
def test_checkout_should_display_correct_title_when_user_navigates_to_checkout(
    selenium_driver,
):
    """
    Prueba que verifica que el título de la página de checkout sea correcto.
    """
    ui_logger.info(
        "Iniciando test_checkout_should_display_correct_title_when_user_navigates_to_checkout"
    )

    # Arrange
    catalog_page = CatalogPage(selenium_driver)
    catalog_page.add_product_to_cart_by_index(0)
    cart_page = catalog_page.go_to_cart()
    ui_logger.debug("Navegando a checkout")

    # Act
    checkout_page = cart_page.go_to_checkout()
    title = checkout_page.get_title()
    ui_logger.info(f"Titulo obtenido: {title}")

    # Assert
    check.equal(
        title, "Checkout: Your Information", "El titulo de checkout no es el esperado"
    )
    ui_logger.info("Test completado exitosamente")


@pytest.mark.ui
@pytest.mark.parametrize(
    "first_name, last_name, postal_code, es_valido, descripcion", CASOS_CHECKOUT
)
def test_checkout_should_work_when_information_provided(
    selenium_driver, first_name, last_name, postal_code, es_valido, descripcion
):
    """
    Prueba que verifica el comportamiento del checkout con diferentes datos de información personal.
    """
    ui_logger.info(
        f"Iniciando test_checkout_should_work_when_information_provided - {descripcion}"
    )

    # Arrange
    catalog_page = CatalogPage(selenium_driver)
    catalog_page.add_product_to_cart_by_index(0)
    cart_page = catalog_page.go_to_cart()
    checkout_page = cart_page.go_to_checkout()
    ui_logger.debug("En pagina de checkout")

    # Act
    ui_logger.info(f"Llenando formulario: {descripcion}")
    checkout_page.fill_out_checkout_info(first_name, last_name, postal_code)
    checkout_page.click_continue()

    # Assert
    if es_valido:
        ui_logger.info("Verificando redireccion exitosa a overview")
        check.is_in(
            "/checkout-step-two.html",
            selenium_driver.current_url,
            f"No se redirigió correctamente a overview para {descripcion}. URL actual: {selenium_driver.current_url}",
        )
        ui_logger.info(f"Test completado exitosamente - {descripcion}")
    else:
        ui_logger.info("Verificando que se muestre error")
        check.is_true(
            checkout_page.error_message_displayed(),
            f"Se esperaba error para {descripcion}, pero no se mostro",
        )
        ui_logger.info(f"Error detectado correctamente - {descripcion}")


@pytest.mark.ui
def test_checkout_should_return_to_cart_when_cancel_button_clicked(selenium_driver):
    """
    Prueba que verifica que se regrese al carrito cuando se hace clic en el botón Cancel.
    """
    ui_logger.info(
        "Iniciando test_checkout_should_return_to_cart_when_cancel_button_clicked"
    )

    # Arrange
    catalog_page = CatalogPage(selenium_driver)
    catalog_page.add_product_to_cart_by_index(0)
    cart_page = catalog_page.go_to_cart()
    checkout_page = cart_page.go_to_checkout()
    ui_logger.debug("En pagina de checkout")

    # Act
    ui_logger.info("Haciendo clic en boton Cancel")
    checkout_page.click_cancel()

    # Assert
    check.is_in(
        "/cart.html",
        selenium_driver.current_url,
        "No se redirigió correctamente al carrito",
    )
    ui_logger.info("Test completado exitosamente")


@pytest.mark.ui
def test_checkout_overview_should_display_payment_and_shipping_info(selenium_driver):
    """
    Prueba que verifica que la página de overview muestre información de pago y envío.
    """
    ui_logger.info(
        "Iniciando test_checkout_overview_should_display_payment_and_shipping_info"
    )

    # Arrange
    catalog_page = CatalogPage(selenium_driver)
    catalog_page.add_product_to_cart_by_index(0)
    cart_page = catalog_page.go_to_cart()
    checkout_page = cart_page.go_to_checkout()

    # Act
    ui_logger.info("Completando formulario de checkout")
    checkout_page.fill_out_checkout_info("John", "Doe", "12345")
    checkout_page.click_continue()

    # Assert
    ui_logger.info("Verificando informacion de pago y envio")
    check.is_true(
        checkout_page.payment_info_is_displayed(),
        "La informacion de pago no esta visible",
    )
    check.is_true(
        checkout_page.shipping_info_is_displayed(),
        "La informacion de envio no esta visible",
    )
    ui_logger.info("Test completado exitosamente")


@pytest.mark.ui
@pytest.mark.parametrize("nombre_producto", NOMBRES_PRODUCTOS)
def test_checkout_overview_should_display_added_product(
    selenium_driver, nombre_producto
):
    """
    Prueba parametrizada que verifica que el overview muestre el producto agregado correctamente.
    """
    ui_logger.info(
        f"Iniciando test_checkout_overview_should_display_added_product - Producto: {nombre_producto}"
    )

    # Arrange
    catalog_page = CatalogPage(selenium_driver)
    ui_logger.info(f"Agregando producto: {nombre_producto}")
    catalog_page.add_product_to_cart_by_name(nombre_producto)
    cart_page = catalog_page.go_to_cart()
    checkout_page = cart_page.go_to_checkout()

    # Act
    checkout_page.fill_out_checkout_info("John", "Doe", "12345")
    checkout_page.click_continue()
    item_names = checkout_page.get_checkout_item_names()
    ui_logger.info(f"Productos en checkout: {item_names}")

    # Assert
    check.is_in(
        nombre_producto,
        item_names,
        f"El producto {nombre_producto} no esta en checkout",
    )
    ui_logger.info(f"Test completado exitosamente - {nombre_producto}")


@pytest.mark.ui
def test_checkout_overview_should_display_multiple_products_when_multiple_added(
    selenium_driver,
):
    """
    Prueba que verifica que el overview muestre todos los productos cuando se agregan múltiples.
    """
    ui_logger.info(
        "Iniciando test_checkout_overview_should_display_multiple_products_when_multiple_added"
    )

    # Arrange
    catalog_page = CatalogPage(selenium_driver)
    expected_count = len(PRODUCTOS_COMPLETOS)

    ui_logger.info(f"Agregando {expected_count} productos al carrito")
    for producto in PRODUCTOS_COMPLETOS:
        catalog_page.add_product_to_cart_by_name(producto["nombre"])

    cart_page = catalog_page.go_to_cart()
    checkout_page = cart_page.go_to_checkout()

    # Act
    checkout_page.fill_out_checkout_info("John", "Doe", "12345")
    checkout_page.click_continue()
    checkout_items = checkout_page.get_checkout_items()
    ui_logger.info(f"Productos en checkout overview: {len(checkout_items)}")

    # Assert
    check.equal(
        len(checkout_items),
        expected_count,
        f"Se esperaban {expected_count} productos pero se encontraron {len(checkout_items)}",
    )
    ui_logger.info("Test completado exitosamente")


@pytest.mark.ui
def test_checkout_should_complete_when_finish_button_clicked(selenium_driver):
    """
    Prueba que verifica que el checkout se complete cuando se hace clic en el botón Finish.
    """
    ui_logger.info("Iniciando test_checkout_should_complete_when_finish_button_clicked")

    # Arrange
    catalog_page = CatalogPage(selenium_driver)
    catalog_page.add_product_to_cart_by_index(0)
    cart_page = catalog_page.go_to_cart()
    checkout_page = cart_page.go_to_checkout()

    # Act
    ui_logger.info("Completando proceso de checkout")
    checkout_page.fill_out_checkout_info("John", "Doe", "12345")
    checkout_page.click_continue()
    ui_logger.info("Haciendo clic en boton Finish")
    checkout_page.click_finish()

    # Assert
    check.is_in(
        "/checkout-complete.html",
        selenium_driver.current_url,
        "No se completo el checkout correctamente",
    )
    ui_logger.info("Test completado exitosamente")


@pytest.mark.ui
def test_checkout_overview_should_display_correct_title(selenium_driver):
    """
    Prueba que verifica que el título de la página de overview sea correcto.
    """
    ui_logger.info("Iniciando test_checkout_overview_should_display_correct_title")

    # Arrange
    catalog_page = CatalogPage(selenium_driver)
    catalog_page.add_product_to_cart_by_index(0)
    cart_page = catalog_page.go_to_cart()
    checkout_page = cart_page.go_to_checkout()

    # Act
    checkout_page.fill_out_checkout_info("John", "Doe", "12345")
    checkout_page.click_continue()
    title = checkout_page.get_title()
    ui_logger.info(f"Titulo de overview: {title}")

    # Assert
    check.equal(
        title, "Checkout: Overview", "El titulo de checkout overview no es el esperado"
    )
    ui_logger.info("Test completado exitosamente")
