from selenium.webdriver.common.action_chains import ActionChains
from config import HEADLESS, RPA_DIR_DOWNLOADS
from selenium.webdriver.common.by import By
from selenium import webdriver
import time


class Browser:
    def __init__(self):

        # Configuração do browser
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--no-first-run")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-hang-monitor")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--metrics-recording-only")
        options.add_argument("--remote-debugging-port=0")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-prompt-on-repost")
        options.add_argument("--disable-syncdisable-translate")
        options.add_argument("--disable-background-networking")
        options.add_argument("--safebrowsing-disable-auto-update")
        options.add_argument("--disable-features=ChromeWhatsNewUI")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-client-side-phishing-detection")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Define se o navegador vai ficar visível ou não
        if HEADLESS:
            # options.add_argument('--headless')
            options.add_argument("--headless=new")  # headless moderno
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-software-rasterizer")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--disable-features=IsolateOrigins,site-per-process")

        # Define a pasta usada para salvar os downloads
        prefs = {
            "download.default_directory": RPA_DIR_DOWNLOADS,
            "safebrowsing.enabled": True,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "plugins.always_open_pdf_externally": True
        }
        options.add_experimental_option('prefs', prefs)

        self.driver = webdriver.Chrome(options=options)
        self.driver.command_executor.set_timeout(600)

    def search_element(self, value: str, by = By.XPATH, waiting_time: int = 15, delay: int = 0):
        """
        Espera o elemento ficar visível para interagir com ele.
        :param by: Localizador
        :param value: Seletor;
        :param waiting_time: Tempo de espera (em segundos);
        :param delay: Tempo de espera após encontrado (em segundos).
        :return: WebElement.
        """

        for n in range(waiting_time):
            try:
                elementos = self.driver.find_elements(by, value)
                for elemento in elementos:
                    if elemento.is_displayed():
                        time.sleep(delay)
                        return elemento
            except:
                pass
            time.sleep(1)

        return None

    def element_click(self, value: str, by = By.XPATH, waiting_time: int = 15, delay: int = 0) -> bool:
        """
        Espera o elemento ficar visível e clica nele.
        :param by: Localizador
        :param value: Seletor;
        :param waiting_time: Tempo de espera (em segundos);
        :param delay: Tempo de espera antes de clicar.
        :return: True - Se conseguiu clicar no elemento. False se não.
        """

        for n in range(waiting_time):
            try:
                elementos = self.driver.find_elements(by, value)
                for elemento in elementos:
                    if elemento.is_displayed():
                        try:
                            time.sleep(delay)
                            elemento.click()
                            return True
                        except:
                            pass
            except:
                pass
            time.sleep(1)
        return False

    def element_left_click(self, value: str, by = By.XPATH, waiting_time: int = 15, delay: int = 0) -> bool:
        """
        Espera o elemento aparecer e clica nele com o botão esquerdo do mouse.
        :param by: Localizador
        :param value: Seletor;
        :param waiting_time: Tempo de espera (em segundos);
        :param delay: Tempo de espera antes de clicar.
        :return: True - Se conseguiu clicar no elemento. False se não.
        """

        for n in range(waiting_time):
            try:
                elementos = self.driver.find_elements(by, value)
                for elemento in elementos:
                    if elemento.is_displayed():
                        try:
                            time.sleep(delay)
                            action = ActionChains(self.driver)
                            action.click(elemento).perform()
                            return True
                        except:
                            pass
            except:
                pass
            time.sleep(1)
        return False

    def element_right_click(self, value: str, by = By.XPATH, waiting_time: int = 15, delay: int = 0) -> bool:
        """
        Espera o elemento aparecer e clica nele com o botão direito do mouse.
        :param by: Localizador
        :param value: Seletor;
        :param waiting_time: Tempo de espera (em segundos);
        :param delay: Tempo de espera antes de clicar.
        :return: True - Se conseguiu clicar no elemento. False se não.
        """

        for n in range(waiting_time):
            try:
                elementos = self.driver.find_elements(by, value)
                for elemento in elementos:
                    if elemento.is_displayed():
                        try:
                            time.sleep(delay)
                            action = ActionChains(self.driver)
                            action.context_click(elemento).perform()
                            return True
                        except:
                            pass
            except:
                pass
            time.sleep(1)
        return False

    def element_double_click(self, value: str, by = By.XPATH, waiting_time: int = 15, delay: int = 0) -> bool:
        """
        Espera o elemento aparecer e dá um duplo click nele.
        :param by: Localizador
        :param value: Seletor;
        :param waiting_time: Tempo de espera (em segundos);
        :param delay: Tempo de espera antes de clicar.
        :return: True - Se conseguiu clicar no elemento. False se não.
        """

        for n in range(waiting_time):
            try:
                elementos = self.driver.find_elements(by, value)
                for elemento in elementos:
                    if elemento.is_displayed():
                        try:
                            time.sleep(delay)
                            action = ActionChains(self.driver)
                            action.double_click(elemento).perform()
                            return True
                        except:
                            pass
            except:
                pass
            time.sleep(1)
        return False

    def element_displayed(self, value: str, by = By.XPATH, waiting_time: int = 15) -> bool:
        """
        Espera o elemento aparecer ficar visível.
        :param by: Localizador;
        :param value: Seletor;
        :param waiting_time: Tempo de espera (em segundos);
        :return: True - Se o elemento for encontrado e ficar visível. False se não.
        """

        for n in range(waiting_time):
            try:
                elementos = self.driver.find_elements(by, value)
                for elemento in elementos:
                    if elemento.is_displayed():
                        return True
            except:
                pass
            time.sleep(1)
        return False

    def type_keys(self, keys: list, interval: int = 100, waiting_time: int = 0):
        """
        Digita uma tecla ou uma combinação de telhas. Ex.: CONTROL + C
        :param keys: Keyboards a serem teclados;
        :param interval: Tempo de espera (ms) após cada tecla;
        :param waiting_time: Tempo de espera (ms) após teclar.
        """
        action = ActionChains(self.driver)
        for k in keys:
            action.key_down(k)
            action.pause(interval / 1000.0)
        for k in reversed(keys):
            action.key_up(k)
            action.pause(interval / 1000.0)
        action.perform()
        time.sleep(waiting_time)

    def type_text(self, text: str, interval: int = 100, waiting_time: int = 0):
        """
        Digita o texto informado.
        :param text: Caracteres a serem teclados;
        :param interval: Tempo de espera (ms) após cada tecla;
        :param waiting_time: Tempo de espera (ms) após teclar.
        """
        action = ActionChains(self.driver)
        for c in text:
            action.send_keys(c)
            action.pause(interval / 1000.0)
        action.perform()
        time.sleep(waiting_time)

    def stop_browser(self):
        """
        Fecha o navegador
        """
        if not self.driver:
            return
        if self.driver.window_handles:
            self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.close()
        self.driver.quit()

    def __exit__(self):
        self.stop_browser()
