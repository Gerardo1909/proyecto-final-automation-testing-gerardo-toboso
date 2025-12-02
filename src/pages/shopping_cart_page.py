"""
Módulo para página de carrito de compras de https://www.saucedemo.com/
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class ShoppingCartPage:
    """
    Clase que representa la página de carrito de compras de SauceDemo.com.
    """

    _TITLE = (By.CLASS_NAME, "title")
    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _CONTINUE_SHOPPING = (By.ID, "continue-shopping")
    _CHECKOUT_BUTTON = (By.ID, "checkout")
    _REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[data-test*='remove']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_title(self) -> str:
        """
        Obtiene el título de la página del carrito de compras.
        """
        return self.driver.find_element(*self._TITLE).text

    def get_cart_items(self):
        """
        Obtiene la lista de artículos en el carrito de compras.
        """
        return self.driver.find_elements(*self._CART_ITEMS)

    def get_item_names(self):
        """
        Obtiene los nombres de los artículos en el carrito de compras.
        """
        items = self.get_cart_items()
        return [item.find_element(*self._ITEM_NAMES).text for item in items]

    def click_continue_shopping(self):
        """
        Hace clic en el botón de continuar comprando.
        """
        self.driver.find_element(*self._CONTINUE_SHOPPING).click()
        return self

    def click_remove_button_by_index(self, index: int):
        """
        Hace clic en el botón de eliminar para un artículo específico por su índice en la lista del carrito.
        """
        remove_buttons = self.driver.find_elements(*self._REMOVE_BUTTONS)
        if 0 <= index < len(remove_buttons):
            remove_buttons[index].click()
        else:
            raise IndexError("Índice de artículo fuera de rango.")
        return self

    def click_checkout(self):
        """
        Hace clic en el botón de checkout para proceder con la compra.
        """
        self.driver.find_element(*self._CHECKOUT_BUTTON).click()
        return self
