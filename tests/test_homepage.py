import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Fixture for setting up the WebDriver
@pytest.fixture(scope="module")
def driver():
    # Set up Chrome options
    options = Options()
    options.add_argument('--headless')  # Optional: Run in headless mode
    options.add_argument('--disable-gpu')  # Optional: Disable GPU acceleration

    # Set up the Service object for the Chrome driver
    service = Service(ChromeDriverManager().install())

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Provide the driver instance for the tests
    yield driver
    
    # Cleanup: Quit the driver after the tests are done
    driver.quit()

# Test case 1,2: Verify the homepage load and title
def test_homepage_title(driver):
    driver.get("http://127.0.0.1:8000")  # Replace with your local URL
    assert driver.title == "Home - Food Store"  # Replace with the expected title

# Test case 3: Verify products are displayed on the homepage
def test_all_products_displayed(driver):
    driver.get("http://127.0.0.1:8000")  # Replace with your homepage URL

    # Wait for the product list to be visible on the page
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "product-card"))
    )

    # Find all the product elements on the homepage
    product_cards = driver.find_elements(By.CLASS_NAME, "product-card")

    # Check that at least one product card is displayed
    assert len(product_cards) > 0, "No products found on the homepage."

    # Verify that each product has an image, name, and price
    for product_card in product_cards:
        # Check the image
        product_image = product_card.find_element(By.CLASS_NAME, "product-image")
        assert product_image.is_displayed(), "Product image not displayed."

        # Check the product name
        product_name = product_card.find_element(By.TAG_NAME, "h3")
        assert product_name.is_displayed(), "Product name not displayed."

        # Check the product price
        product_price = product_card.find_element(By.TAG_NAME, "p")
        assert product_price.is_displayed(), "Product price not displayed."

        # Optionally, check for the "Add to Cart" and "View" buttons
        add_to_cart_button = product_card.find_element(By.CLASS_NAME, "add-to-cart-btn")
        assert add_to_cart_button.is_displayed(), "'Add to Cart' button not displayed."

        view_button = product_card.find_element(By.CLASS_NAME, "view-btn")
        assert view_button.is_displayed(), "'View' button not displayed."
