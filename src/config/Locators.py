from selenium.webdriver.common.by import By

class Locators:
    # Navigation
    COMPANY_MENU = (By.XPATH, '//*[@id="navbarNavDropdown"]/ul[1]/li[6]')
    CAREERS_LINK = (By.XPATH, '//*[@id="navbarNavDropdown"]/ul[1]/li[6]/div/div[2]/a[2]')
    
    # Cookies
    COOKIES_BUTTON = (By.ID, "wt-cli-accept-all-btn")
    
    # Career Page Sections
    LOCATIONS_SECTION = (By.XPATH, "//h3[contains(text(), 'Our Locations')]")
    LIFE_SECTION = (By.XPATH, "//h2[text()='Life at Insider']")
    TEAMS_SECTION = (By.XPATH, "//h3[contains(text(), 'Find your calling')]")
    
    # Job Listings
    SEE_ALL_JOBS = (By.XPATH, "//a[contains(@class, 'btn-outline-secondary')]")
    LOCATION_FILTER = (By.XPATH, '//*[@id="top-filter-form"]/div[1]/span/span[1]/span/span[2]')
    DEPARTMENT_FILTER = (By.XPATH, '//*[@id="top-filter-form"]/div[2]/span/span[1]/span/span[2]')
    LOCATION_CLEAR = (By.XPATH, '//*[@id="select2-filter-by-location-container"]/span')
    DEPARTMENT_CLEAR = (By.XPATH, '//*[@id="select2-filter-by-department-container"]/span')
    ISTANBUL_OPTION = (By.XPATH, '//*[@id="filter-by-location"]/option[2]')
    QA_OPTION = (By.XPATH, '//*[@id="filter-by-department"]/option[17]')
    
    # Job Details
    JOB_LISTINGS = (By.CLASS_NAME, "position-list-item")
    POSITION_TITLE = (By.CLASS_NAME, "position-title")
    DEPARTMENT = (By.CLASS_NAME, "position-department")
    LOCATION = (By.CLASS_NAME, "position-location")
    VIEW_ROLE_BUTTON = (By.PARTIAL_LINK_TEXT, "View Role")
