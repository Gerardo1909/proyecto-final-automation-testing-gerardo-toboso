"""
Módulo para página de login de https://www.saucedemo.com/
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """
    Clase que representa la página de login de SauceDemo.com.
    """
    URL = "https://www.saucedemo.com/"
    _USER_INPUT = (By.ID, "user-name")
    _PASSWORD_INPUT = (By.ID, "password")
    _LOGIN_BUTTON = (By.ID, "login-button")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, 'h3[data-test="error"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        """
        Abre la página de inicio de sesión.
        """
        self.driver.get(self.URL)
        return self

    def enter_username(self, username: str):
        """
        Ingresa el nombre de usuario en el campo correspondiente.
        """
        element = self.wait.until(
            EC.visibility_of_element_located(self._USER_INPUT)
        )
        element.clear()
        element.send_keys(username)
        return self

    def enter_password(self, password: str):
        """
        Ingresa la contraseña en el campo correspondiente.
        """
        element = self.driver.find_element(*self._PASSWORD_INPUT)
        element.clear()
        element.send_keys(password)
        return self

    def click_login(self):
        """
        Hace clic en el botón de inicio de sesión.
        """
        self.driver.find_element(*self._LOGIN_BUTTON).click()
        return self

    def do_complete_login(self, username: str, password: str):
        """
        Realiza el flujo completo de inicio de sesión.
        """
        return self.enter_username(username).enter_password(password).click_login()

    def error_is_displayed(self) -> bool:
        """
        Se verifica si el mensaje de error es visible.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self._ERROR_MESSAGE))
            return True
        except Exception:
            return False

    def get_error_message(self) -> str:
        """
        Obtiene el texto del mensaje de error si está presente.
        """
        if self.error_is_displayed():
            return self.driver.find_element(*self._ERROR_MESSAGE).text
        return ""
