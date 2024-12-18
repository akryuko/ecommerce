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


# Test case 10: Verify the product image is displayed on the product detail page
def test_product_image(driver):
    # Navigate to the homepage
    base_url = "http://127.0.0.1:8000"
    driver.get(base_url)

    # Wait until the product cards are loaded
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-card")))

    # Find the 'View' button for the first product and click it
    view_button = driver.find_element(By.XPATH, "//div[@class='product-card']//a[contains(@class, 'view-btn')]")
    view_button.click()

    # Wait for the product detail page to load (look for the product image)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card-img-top")))

    # Find the product image on the product detail page
    product_image = driver.find_element(By.CSS_SELECTOR, ".card-img-top")

    # Verify that the product image is displayed
    assert product_image.is_displayed(), "Product image is not displayed on the product detail page."


# Test case 11: Verify the correct product name, description, and price are displayed on the product detail page
def test_product_details(driver):
    # Navigate to the homepage
    base_url = "http://127.0.0.1:8000"
    driver.get(base_url)

    # Wait until the product cards are loaded
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-card")))

    # Extract product details from the first product on the homepage
    product_card = driver.find_element(By.XPATH, "//div[@class='product-card']")
    product_name_homepage = product_card.find_element(By.XPATH, ".//h3").text
    product_price_homepage = product_card.find_element(By.XPATH, ".//p").text.strip()  # Extract only the price part

    # Find the 'View' button for the first product and click on it
    view_button = product_card.find_element(By.XPATH, ".//a[contains(@class, 'view-btn')]")
    view_button.click()

    # Wait for the product detail page to load
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card-title")))

    # Verify the product name
    product_name_detail = driver.find_element(By.CLASS_NAME, "card-title").text
    assert product_name_homepage == product_name_detail, f"Expected product name to be '{product_name_homepage}', but got '{product_name_detail}'"

    # Verify the product price
    product_price_detail = driver.find_element(By.XPATH, "//p[@class='card-text']/strong").text.strip()
    expected_price_detail = f"Price: {product_price_homepage}"  # Add 'Price: ' to the homepage price for comparison
    assert expected_price_detail == product_price_detail, f"Expected product price to be '{expected_price_detail}', but got '{product_price_detail}'"

    # Verify that the product description is displayed on the product detail page
    description_element = driver.find_element(By.CLASS_NAME, "card-text")  # Assuming the description has the 'card-text' class
    assert description_element.is_displayed(), "Product description is not displayed on the product detail page"
