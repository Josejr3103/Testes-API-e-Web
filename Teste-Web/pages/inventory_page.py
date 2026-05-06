from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage(BasePage):
    _PAGE_TITLE = (By.CLASS_NAME, "title")
    _PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    _ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def is_on_inventory_page(self) -> bool:
        return self.get_text(self._PAGE_TITLE) == "Products"

    def add_products_to_cart(self, count: int = 2):
        buttons = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self._ADD_TO_CART_BUTTONS)
        )
        for button in buttons[:count]:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(button))
            self.driver.execute_script("arguments[0].click();", button)

    def wait_for_cart_count(self, expected_count: int):
        if expected_count > 0:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self._CART_BADGE)
            )
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element(self._CART_BADGE, str(expected_count))
            )
        else:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(self._CART_BADGE)
            )

    def get_cart_item_count(self) -> int:
        try:
            badge = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self._CART_BADGE)
            )
            return int(badge.text)
        except Exception:
            return 0

    def go_to_cart(self):
        cart_icon = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self._CART_LINK)
        )
        self.driver.execute_script("arguments[0].click();", cart_icon)