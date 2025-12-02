"""
Tests para el flujo de uso de catalogo en https://www.saucedemo.com/
"""

import pytest
import pytest_check as check
from pages.catalog_page import CatalogPage
from utils.logger import ui_logger


@pytest.mark.smoke
@pytest.mark.ui
def test_catalog_should_display_correct_title_when_user_is_logged_in(selenium_driver):
    """
    Prueba que verifica que el título del catálogo sea correcto para un usuario logueado.
    """
    ui_logger.info("Iniciando test_catalog_should_display_correct_title_when_user_is_logged_in")
    
    # Arrange
    page = CatalogPage(selenium_driver)
    ui_logger.debug(f"Pagina cargada en: {selenium_driver.current_url}")

    # Act
    title = page.get_title()
    ui_logger.info(f"Titulo obtenido: {title}")

    # Assert
    check.equal(title, "Products", "El titulo del catalogo no es el esperado")
    ui_logger.info("Test completado exitosamente")


@pytest.mark.smoke
@pytest.mark.ui
def test_catalog_should_display_products_when_user_is_logged_in(selenium_driver):
    """
    Prueba que verifica que el catálogo muestre productos al usuario logueado.
    """
    ui_logger.info("Iniciando test_catalog_should_display_products_when_user_is_logged_in")

    # Arrange
    page = CatalogPage(selenium_driver)

    # Act
    products = page.get_products()
    ui_logger.info(f"Productos encontrados: {len(products)}")

    # Assert
    check.greater(len(products), 0, "No se encontraron productos en el catalogo")
    ui_logger.info("Test completado exitosamente")


@pytest.mark.ui
def test_catalog_should_display_menu_when_menu_button_is_clicked(selenium_driver):
    """
    Prueba que verifica que el menú se despliegue al hacer clic en el botón de menú.
    """
    ui_logger.info(
        "Iniciando test_catalog_should_display_menu_when_menu_button_is_clicked"
    )

    # Arrange
    page = CatalogPage(selenium_driver)

    # Act
    ui_logger.info("Haciendo clic en boton de menu")
    page.click_menu_button()

    # Assert
    check.is_true(page.menu_is_displayed(), "El menu no se despliega correctamente")
    ui_logger.info("Test completado exitosamente")


@pytest.mark.ui
def test_catalog_should_display_filters_when_filter_button_is_clicked(selenium_driver):
    """
    Prueba que verifica que las opciones de filtro se desplieguen al hacer clic en el botón de filtro.
    """
    ui_logger.info(
        "Iniciando test_catalog_should_display_filters_when_filter_button_is_clicked"
    )

    # Arrange
    page = CatalogPage(selenium_driver)

    # Act
    page.click_filter_button()
    filters = page.get_filter_options()
    ui_logger.info(f"Filtros encontrados: {len(filters)}")

    # Assert
    check.greater(len(filters), 0, "No se encontraron opciones de filtro")
    ui_logger.info("Test completado exitosamente")


@pytest.mark.ui
def test_catalog_should_display_cart_icon_when_user_is_logged_in(selenium_driver):
    """
    Prueba que verifica que el ícono del carrito de compras se muestre para un usuario logueado.
    """
    ui_logger.info(
        "Iniciando test_catalog_should_display_cart_icon_when_user_is_logged_in"
    )

    # Arrange
    page = CatalogPage(selenium_driver)

    # Act
    is_cart_displayed = page.cart_is_displayed()
    ui_logger.info(f"Icono del carrito visible: {is_cart_displayed}")

    # Assert
    check.is_true(is_cart_displayed, "El icono del carrito no esta visible")
    ui_logger.info("Test completado exitosamente")
