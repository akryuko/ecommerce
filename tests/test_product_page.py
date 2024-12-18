from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException


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


# Test case 12: Verify the "Add to Cart" button works on the product page
def test_add_to_cart_button(driver):
    # Step 1: Navigate to the homepage
    base_url = "http://127.0.0.1:8000"
    driver.get(base_url)

    # Step 2: Wait for the product cards to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-card")))

    # Step 3: Click the "View" button of the first product
    view_button = driver.find_element(By.XPATH, "//div[@class='product-card']//a[contains(@class, 'view-btn')]")
    view_button.click()

    # Step 4: Wait for the Product Detail page to load
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "add-to-cart-btn")))

    # Step 5: Get the initial cart count
    try:
        # If the cart count is not visible (i.e., cart is empty), set it to 0
        cart_count_element = driver.find_element(By.ID, "cart-count")
        initial_cart_count = int(cart_count_element.text) if cart_count_element.text else 0
    except NoSuchElementException:
        # Handle the case where the cart count element does not exist at all
        initial_cart_count = 0

    # Step 6: Click the "Add to Cart" button
    add_to_cart_button = driver.find_element(By.CLASS_NAME, "add-to-cart-btn")
    add_to_cart_button.click()

    # Step 7: Wait for the cart count to be updated
    WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.ID, "cart-count").text and int(d.find_element(By.ID, "cart-count").text) > initial_cart_count
    )

    # Step 8: Get the updated cart count and verify it has increased by 1
    updated_cart_count = int(driver.find_element(By.ID, "cart-count").text)
    assert updated_cart_count == initial_cart_count + 1, f"Expected cart count to be {initial_cart_count + 1}, but found {updated_cart_count}"


# Test case 13: Verify the "Back" and "Go to Cart" buttons work on the product page
def test_navigation_buttons_on_product_page(driver):
    # Step 1: Navigate to the homepage
    base_url = "http://127.0.0.1:8000/"
    driver.get(base_url)

    # Step 2: Wait for the product cards to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-card")))

    # Step 3: Click the "View" button of the first product to go to the product page
    view_button = driver.find_element(By.XPATH, "//div[@class='product-card']//a[contains(@class, 'view-btn')]")
    view_button.click()

    # Step 4: Wait for the Product Detail page to load
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card-title")))

    # Verify the current URL contains "product_detail"
    assert "product_detail" in driver.current_url, "Did not navigate to the Product Detail page."

    # Step 5: Test the "Back" button
    try:
        back_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@onclick, 'window.history.back()')]")))
        back_button.click()
    except TimeoutException:
        raise AssertionError("Back button not found or not clickable on the Product Detail page.")

    # Wait for the homepage to reload
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-card")))

    # Verify the current URL is the homepage
    assert driver.current_url == base_url, "Back button did not navigate to the homepage."

    # Step 6: Navigate back to the product page for the next test
    view_button = driver.find_element(By.XPATH, "//div[@class='product-card']//a[contains(@class, 'view-btn')]")
    view_button.click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card-title")))

    # Step 7: Test the "Go to Cart" button
    try:
        go_to_cart_button = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/cart/')]")))
        go_to_cart_button.click()
    except TimeoutException:
        raise AssertionError("Go to Cart button not found or not clickable on the Product Detail page.")

    # Wait for the Cart page to load
    try:
        cart_heading = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[text()='Your Cart']")))
        assert cart_heading.is_displayed(), "The cart page did not display the 'Your Cart' heading."
    except TimeoutException:
        raise AssertionError("Cart page heading 'Your Cart' was not found.")
