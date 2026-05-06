from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutStepOnePage(BasePage):
    _PAGE_TITLE = (By.CLASS_NAME, "title")
    _FIRST_NAME = (By.ID, "first-name")
    _LAST_NAME = (By.ID, "last-name")
    _POSTAL_CODE = (By.ID, "postal-code")
    _CONTINUE_BUTTON = (By.ID, "continue")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def is_on_checkout_step_one(self) -> bool:
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("checkout-step-one.html")
        )
        texto_atual = self.get_text(self._PAGE_TITLE)
        return "Checkout: Your Information" in texto_atual.strip()

    def _fill_field(self, locator, value: str):
        field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locator)
        )
        
        self.driver.execute_script("""
            var el = arguments[0];
            var val = arguments[1];
            var nativeInputSetter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value'
            ).set;
            nativeInputSetter.call(el, val);
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
        """, field, value)

        actual = field.get_attribute("value")
        if actual != value:
            raise AssertionError(
                f"Falha ao preencher '{locator}'. "
                f"Esperado: '{value}', obtido: '{actual}'"
            )

    def fill_customer_info(self, first_name: str, last_name: str, postal_code: str):
        self._fill_field(self._FIRST_NAME, first_name)
        self._fill_field(self._LAST_NAME, last_name)
        self._fill_field(self._POSTAL_CODE, postal_code)

    def continue_to_overview(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self._CONTINUE_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", btn)
        try:
            error = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self._ERROR_MESSAGE)
            )
            raise AssertionError(f"Erro de validação no formulário: {error.text}")
        except AssertionError:
            raise
        except Exception:
            pass
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("checkout-step-two.html")
        )


class CheckoutStepTwoPage(BasePage):
    _PAGE_TITLE = (By.CLASS_NAME, "title")
    _FINISH_BUTTON = (By.ID, "finish")
    _SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")

    def is_on_checkout_overview(self) -> bool:
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("checkout-step-two.html")
        )
        return self.get_text(self._PAGE_TITLE) == "Checkout: Overview"

    def get_total(self) -> str:
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self._SUMMARY_TOTAL)
        )
        return self.get_text(self._SUMMARY_TOTAL)

    def finish_order(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self._FINISH_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", btn)
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("checkout-complete.html")
        )


class CheckoutCompletePage(BasePage):
    _COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def get_confirmation_message(self) -> str:
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self._COMPLETE_HEADER)
        )
        return self.get_text(self._COMPLETE_HEADER)