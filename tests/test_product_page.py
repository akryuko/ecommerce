from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time

# Test case 9: Verify that the product page loads successfully when View button for product is clicked
def test_view_button(driver):
    # Navigate to the homepage
    base_url = "http://127.0.0.1:8000"
    driver.get(base_url)

    # Wait until the product cards are loaded
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-card")))

    # Find the 'View' button for the first product
    view_button = driver.find_element(By.XPATH, "//div[@class='product-card']//a[contains(@class, 'view-btn')]")

    # Click on the 'View' button to go to the product detail page
    view_button.click()

    # Wait for the product detail page to load by checking the title of the page or other content
    wait.until(EC.title_contains("Product Detail -"))

    # Get the product name from the product detail page (from the <h3> tag with class 'card-title')
    product_name = driver.find_element(By.XPATH, "//h3[@class='card-title']").text

    time.sleep(2)

    # Optionally, also check for the presence of the product name in the page title
    expected_title = f"Product Detail - {product_name}"
    assert driver.title == expected_title, f"Expected title to be '{expected_title}', but got '{driver.title}'"