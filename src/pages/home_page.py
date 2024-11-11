from pages.base_page import BasePage
from config.Locators import Locators
from selenium.common.exceptions import TimeoutException

class HomePage(BasePage):
    def navigate_to_careers(self):
        """Navigate to careers page from home page."""
        self.click_element(Locators.COMPANY_MENU)
        self.click_element(Locators.CAREERS_LINK)
        self.logger.info("Navigated to careers page")

    def verify_title(self):
        """Verify home page title contains 'Insider'."""
        assert "Insider" in self.driver.title, "Home page title doesn't contain 'Insider'"
        self.logger.info("Verified home page title")