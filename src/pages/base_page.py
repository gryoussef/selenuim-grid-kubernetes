from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from config.config_test import TestConfig
import logging

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TestConfig.TIMEOUT)
        self.logger = logging.getLogger(self.__class__.__name__)

    def click_element(self, locator, timeout=None, retries=0):
        """Click an element with explicit wait, logging, and optional retries."""
        wait_time = timeout or TestConfig.TIMEOUT
        attempt = 0
        while attempt <= retries:
            try:
                element = self.wait_until_clickable(locator, timeout=wait_time)
                element.click()
                self.logger.info(f"Clicked element: {locator}")
                return
            except (TimeoutException, ElementClickInterceptedException) as e:
                self.logger.error(f"Attempt {attempt + 1} failed to click element: {locator}")
                if attempt == retries:
                    raise e
                attempt += 1

    def wait_until_visible(self, locator, timeout=None):
        """Wait until element is visible."""
        wait_time = timeout or TestConfig.TIMEOUT
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException as e:
            self.logger.error(f"Element not visible: {locator}")
            raise e

    def wait_until_clickable(self, locator, timeout=None):
        """Wait until element is clickable."""
        wait_time = timeout or TestConfig.TIMEOUT
        try:
            return self.wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException as e:
            self.logger.error(f"Element not clickable: {locator}")
            raise e

    def wait_until_present(self, locator, timeout=None):
        """Wait until element is present in DOM."""
        wait_time = timeout or TestConfig.TIMEOUT
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException as e:
            self.logger.error(f"Element not present: {locator}")
            raise e

    def get_text(self, locator):
        """Get text of an element with explicit wait."""
        element = self.wait_until_visible(locator)
        return element.text

    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible."""
        try:
            self.wait_until_visible(locator, timeout=timeout)
            return True
        except TimeoutException:
            return False
