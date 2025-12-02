"""
Módulo para página de checkout de https://www.saucedemo.com/
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.catalog_page import CatalogPage

class CheckoutPage:
    """
    Clase que representa la página de checkout de SauceDemo.com.
    """

    _TITLE = (By.CLASS_NAME, "title")
    _FIRST_NAME_INPUT = (By.ID, "first-name")
    _LAST_NAME_INPUT = (By.ID, "last-name")
    _POSTAL_CODE_INPUT = (By.ID, "postal-code")
    _CONTINUE_BUTTON = (By.ID, "continue")
    _CANCEL_BUTTON = (By.ID, "cancel")  
    _ERROR_MESSAGE = (By.CLASS_NAME, "error-message-container")
    _PAYMENT_INFO = (By.CLASS_NAME, "summary_info_label")
    _SHIPPING_INFO = (By.CLASS_NAME, "summary_info_label")
    _FINISH_BUTTON = (By.ID, "finish")
    _CHECKOUT_ITEMS = (By.CLASS_NAME, "cart_item")
    _CHECKOUT_ITEMS_NAMES = (By.CLASS_NAME, "inventory_item_name")
    
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
    def fill_out_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        """
        Llena el formulario de información de checkout.
        """
        self.driver.find_element(*self._FIRST_NAME_INPUT).send_keys(first_name)
        self.driver.find_element(*self._LAST_NAME_INPUT).send_keys(last_name)
        self.driver.find_element(*self._POSTAL_CODE_INPUT).send_keys(postal_code)
        return self
    
    def click_continue(self):
        """
        Hace clic en el botón "Continue" para proceder con el checkout.
        """
        self.driver.find_element(*self._CONTINUE_BUTTON).click()
        return self
    
    def click_cancel(self):
        """
        Hace clic en el botón "Cancel" para cancelar el checkout.
        """
        self.driver.find_element(*self._CANCEL_BUTTON).click()
        return self
    
    def get_title(self) -> str:
        """
        Obtiene el título de la página de checkout.
        """
        return self.driver.find_element(*self._TITLE).text
    
    def error_message_displayed(self) -> bool:
        """
        Verifica si se muestra un mensaje de error en la página de checkout.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self._ERROR_MESSAGE))
            return True
        except:
            return False
        
    def shipping_info_is_displayed(self) -> bool:
        """
        Verifica si la información de envío está visible en la página de checkout.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self._SHIPPING_INFO))
            return True
        except:
            return False
        
    def payment_info_is_displayed(self) -> bool:
        """
        Verifica si la información de pago está visible en la página de checkout.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self._PAYMENT_INFO))
            return True
        except:
            return False
        
    def get_checkout_items(self):
        """
        Obtiene la lista de artículos en la página de checkout.
        """
        return self.driver.find_elements(*self._CHECKOUT_ITEMS)
        
    def get_checkout_item_names(self):
        """
        Obtiene los nombres de los artículos en la página de checkout.
        """
        items = self.get_checkout_items()
        return [item.find_element(*self._CHECKOUT_ITEMS_NAMES).text for item in items]
    
    def click_finish(self):
        """
        Hace clic en el botón "Finish" para completar el checkout.
        """
        self.driver.find_element(*self._FINISH_BUTTON).click()
        return self