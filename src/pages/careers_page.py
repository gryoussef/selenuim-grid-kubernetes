import time
from pages.base_page import BasePage
from config.Locators import Locators
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

class CareersPage(BasePage):
    def accept_cookies(self):
        """Accept cookies if present."""
        try:
            self.click_element(Locators.COOKIES_BUTTON, timeout=5)
            self.logger.info("Accepted cookies")
        except TimeoutException:
            self.logger.info("No cookies button found or already accepted")

    def verify_sections(self):
        """Verify all required sections are visible."""
        sections = [
            Locators.LOCATIONS_SECTION,
            Locators.LIFE_SECTION,
            Locators.TEAMS_SECTION
        ]
        for section in sections:
            assert self.is_element_visible(section), f"Section not visible: {section}"
        self.logger.info("Verified all career page sections")

    def navigate_to_qa_jobs(self):
        """Navigate to QA jobs listing."""
        # Scroll to the element first
        element = self.wait_until_present(Locators.SEE_ALL_JOBS)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)  # Wait for scroll to complete
        ActionChains(self.driver).move_to_element(element).pause(0.5).click().perform()
        self.logger.info("Navigated to QA jobs listing")

    def apply_filters(self):
        """Apply location and department filters."""
        self.click_element(Locators.LOCATION_CLEAR)
        self.click_element(Locators.DEPARTMENT_CLEAR)
        self.click_element(Locators.LOCATION_FILTER, retries=3)
        self.click_element(Locators.ISTANBUL_OPTION, timeout=5, retries=3)
        self.click_element(Locators.DEPARTMENT_FILTER, retries=3)
        self.click_element(Locators.QA_OPTION, timeout=5, retries=3)
        self.logger.info("Applied job filters")

    def get_job_listings(self):
        """Get all job listings after filtering."""
        try:
            time.sleep(3)
            self.driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
            time.sleep(3)
            self.driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'})")
            time.sleep(3)
            self.wait_until_visible(Locators.JOB_LISTINGS)
            # Get and return all job listings
            job_listings = self.driver.find_elements(*Locators.JOB_LISTINGS)
            return job_listings

        except Exception as e:
            self.logger.error(f"Failed to get job listings: {str(e)}")
            return []

    def verify_job_details(self, job):
        """Verify details of a single job listing."""
        ActionChains(self.driver).move_to_element(job).perform()
        position = job.find_element(*Locators.POSITION_TITLE).text
        department = job.find_element(*Locators.DEPARTMENT).text
        location = job.find_element(*Locators.LOCATION).text

        assert "Quality Assurance" in position, f"Invalid position: {position}"
        assert "Quality Assurance" in department, f"Invalid department: {department}"
        assert "Istanbul, Turkey" in location, f"Invalid location: {location}"
        self.logger.info(f"Verified job details - Position: {position}")

    def verify_application_redirect(self, job):
        """Verify job application redirect."""
        original_window = self.driver.current_window_handle
        job.find_element(*Locators.VIEW_ROLE_BUTTON).click()
        
        self.wait.until(lambda d: len(d.window_handles) > 1)
        for window in self.driver.window_handles:
            if window != original_window:
                self.driver.switch_to.window(window)
                break

        assert "lever.co" in self.driver.current_url, "Not redirected to Lever application page"
        self.logger.info("Verified application page redirect")
        
        self.driver.close()
        self.driver.switch_to.window(original_window)