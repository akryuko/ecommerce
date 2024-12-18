import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Fixture for setting up the WebDriver
@pytest.fixture(scope="module")
def driver():
    # Set up Chrome options
    options = Options()
    # Ensure headless mode is not enabled (comment this line if you want to run headless)
    # options.add_argument('--headless')  # Optional: Run in headless mode
    options.add_argument('--disable-gpu')  # Optional: Disable GPU acceleration

    # Set up the Service object for the Chrome driver
    service = Service(ChromeDriverManager().install())

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Provide the driver instance for the tests
    yield driver
    
    # Cleanup: Quit the driver after the tests are done
    driver.quit()
