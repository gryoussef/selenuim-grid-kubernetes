import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from config.config_test import TestConfig
import logging
import os
from datetime import datetime
import time

def pytest_configure():
    """Configure logging for the test suite."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('reports/test_execution.log'),
            logging.StreamHandler()
        ]
    )
    
    os.makedirs('reports', exist_ok=True)
    os.makedirs('screenshots', exist_ok=True)

def create_driver(selenium_grid_url, options, attempt=1, max_attempts=3):
    """Create a driver with retry logic"""
    try:
        driver = webdriver.Remote(
            command_executor=selenium_grid_url,
            options=options
        )
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        return driver
    except WebDriverException as e:
        if attempt < max_attempts:
            logging.warning(f"Attempt {attempt} failed to create driver. Retrying in 5 seconds...")
            time.sleep(5)
            return create_driver(selenium_grid_url, options, attempt + 1, max_attempts)
        raise e

@pytest.fixture(scope="function")
def driver(request):
    """Setup WebDriver for each test with retries."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.set_capability('se:noVNC', True)
    
    selenium_grid_url = os.getenv('SELENIUM_GRID_URL', 'http://selenium-hub:4444/wd/hub')
    
    # Create driver with retries
    try:
        driver = create_driver(selenium_grid_url, options)
        yield driver
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on test failure"""
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    
    if report.when == 'call':
        if report.failed and hasattr(item, 'funcargs') and 'driver' in item.funcargs:
            driver = item.funcargs['driver']
            take_screenshot(driver, item.name)

def take_screenshot(driver, name):
    """Take screenshot and save it"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_name = f"screenshots/{name}_{timestamp}.png"
        driver.save_screenshot(screenshot_name)
        return screenshot_name
    except:
        logging.error("Failed to take screenshot", exc_info=True)
        return None