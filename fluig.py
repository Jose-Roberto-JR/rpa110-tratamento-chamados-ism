from config import LOG_FALHA, FLUIG_URL, FLUIG_USER, FLUIG_PWD
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from browser import Browser


class Fluig(Browser):

    def login(self):
        """
        Realiza o login no Tasy.
        """
        # Abre o navegador e acessa o Tasy
        self.driver.get(FLUIG_URL)

        # Informa o usuário
        self.search_element(by=By.ID, value="loginUsername", waiting_time=60).send_keys(FLUIG_USER)

        # Informa o senha
        self.search_element(by=By.ID, value="loginPassword").send_keys(FLUIG_PWD)

        # Entrar
        self.search_element(by=By.ID, value="loginPassword").send_keys(Keys.ENTER)

        # Verificar se aparece o popup de 'Atenção'. Clicar em 'Ok' caso apareça
        if self.search_element(by=By.XPATH, value="//*[contains(text(), 'Atenção') or contains(text(), 'Attention')]", waiting_time=5):
            self.search_element(by=By.XPATH, value="//*[contains(text(), 'Ok')]", delay=1).click()

        # Verificar se o login foi realizado com sucesso
        if self.element_displayed(value="//a[text() = 'Funções']", waiting_time=60):
            return

        # Verificar se a senha está errada
        if self.element_displayed(value="//*[contains(text(), 'Usuário ou senha inválido.')]", waiting_time=1):
            raise Exception([LOG_FALHA, "Usuário ou senha inválido."])

        # Reportar falha genérica
        raise Exception([LOG_FALHA, "Login não confirmado"])