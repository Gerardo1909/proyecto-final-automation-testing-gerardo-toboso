"""
Módulo para página de catalogo de https://www.saucedemo.com/
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage


class CatalogPage:
    """
    Clase que representa la página de catálogo de SauceDemo.com.
    """

    _TITLE = (By.CLASS_NAME, "title")
    _PRODUCTS = (By.CLASS_NAME, "inventory_item")
    _ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _ADD_BUTTONS = (By.CSS_SELECTOR, "button[data-test*='add-to-cart']")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    _MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    _MENU_DISPLAY = (By.CLASS_NAME, "bm-menu-wrap")
    _FILTER_BUTTON = (By.CLASS_NAME, "product_sort_container")
    _FILTER_OPTIONS = (By.TAG_NAME, "option")
    _LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        # La página de catalogo solo tiene sentido cuando se inicia sesión
        self.driver = (
            LoginPage(driver)
            .open()
            .do_complete_login("standard_user", "secret_sauce")
            .driver
        )
        self.wait = WebDriverWait(self.driver, 10)

    def get_title(self) -> str:
        """
        Obtiene el título de la página de catálogo.
        """
        return self.driver.find_element(*self._TITLE).text

    def get_products(self):
        """
        Obtiene la lista de productos en el catálogo.
        """
        return self.driver.find_elements(*self._PRODUCTS)

    def add_product_to_cart_by_index(self, index: int):
        """
        Agrega un producto al carrito por su índice en la lista de productos.
        """
        add_buttons = self.driver.find_elements(*self._ADD_BUTTONS)
        if 0 <= index < len(add_buttons):
            add_buttons[index].click()
        else:
            raise IndexError("Índice de producto fuera de rango.")
        return self

    def add_product_to_cart_by_name(self, name: str):
        """
        Agrega un producto al carrito por su nombre.
        """
        products = self.get_products()
        for product in products:
            if product.find_element(*self._ITEM_NAMES).text == name:
                product.find_element(*self._ADD_BUTTONS).click()
                return self
        raise ValueError(f"Producto no encontrado: {name}")

    def get_cart_item_count(self) -> int:
        """
        Obtiene la cantidad de artículos en el carrito.
        """
        try:
            badge = self.driver.find_element(*self._CART_BADGE)
            return int(badge.text)
        except Exception:
            return 0

    def click_menu_button(self):
        """
        Hace clic en el botón del menú.
        """
        self.driver.find_element(*self._MENU_BUTTON).click()
        return self

    def menu_is_displayed(self) -> bool:
        """
        Verifica si el menú está desplegado.
        """
        menu = self.driver.find_element(*self._MENU_DISPLAY)
        return menu.is_displayed()

    def click_filter_button(self):
        """
        Hace clic en el botón de filtro.
        """
        self.driver.find_element(*self._FILTER_BUTTON).click()
        return self

    def get_filter_options(self):
        """
        Obtiene las opciones de filtro disponibles.
        """
        return self.driver.find_elements(*self._FILTER_OPTIONS)

    def cart_is_displayed(self) -> bool:
        """
        Verifica si el ícono del carrito está visible.
        """
        cart_icon = self.driver.find_element(*self._CART_LINK)
        return cart_icon.is_displayed()

    def go_to_cart(self):
        """
        Navega a la página del carrito.
        """
        self.driver.find_element(*self._CART_LINK).click()
        from pages.shopping_cart_page import ShoppingCartPage

        return ShoppingCartPage(self.driver)

    def get_product_names(self):
        """
        Obtiene los nombres de todos los productos en el catálogo.
        """
        name_elements = self.driver.find_elements(*self._ITEM_NAMES)
        return [element.text for element in name_elements]

    def get_add_to_cart_buttons(self):
        """
        Obtiene todos los botones 'Add to cart' del catálogo.
        """
        return self.driver.find_elements(*self._ADD_BUTTONS)

    def do_logout(self):
        """
        Realiza el flujo de cierre de sesión.
        """
        self.driver.find_element(*self._MENU_BUTTON).click()
        self.wait.until(EC.element_to_be_clickable(self._LOGOUT_LINK)).click()
        from pages.login_page import LoginPage

        return LoginPage(self.driver)
