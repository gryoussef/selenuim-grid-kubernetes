from pages.home_page import HomePage
from pages.careers_page import CareersPage
from config.config_test import TestConfig
import logging

logger = logging.getLogger(__name__)

class TestInsiderCareers:
    def test_home_page(self, driver):
        """Test home page navigation and verification."""
        home_page = HomePage(driver)
        driver.get(TestConfig.BASE_URL)
        home_page.verify_title()

    def test_careers_page_sections(self, driver):
        """Test careers page navigation and section verification."""
        home_page = HomePage(driver)
        careers_page = CareersPage(driver)
        
        driver.get(TestConfig.BASE_URL)
        home_page.navigate_to_careers()
        careers_page.verify_sections()

    def test_qa_jobs_workflow(self, driver):
        """Test QA jobs filtering and verification workflow."""
        careers_page = CareersPage(driver)
        
        driver.get(TestConfig.CAREERS_URL)
        careers_page.accept_cookies()
        careers_page.navigate_to_qa_jobs()
        careers_page.apply_filters()
        
        job_listings = careers_page.get_job_listings()
        assert len(job_listings) > 0, "No job listings found"
        
        if job_listings:
            for job in job_listings:
                careers_page.verify_job_details(job)
                careers_page.verify_application_redirect(job)