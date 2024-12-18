import time
import pytest
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


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

#Test case 4: Verify that the cart icon is visible and displays the correct number of items in the cart
def test_cart_icon_visibility(driver):
    # Go to the homepage URL (adjust URL as necessary)
    driver.get("http://127.0.0.1:8000")  # Replace with your homepage URL

    # Wait for the cart icon to be visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "cart-icon-container"))
    )

    time.sleep(3)


    # Add an item to the cart (adjust as needed based on your site's functionality)
    add_to_cart_button = driver.find_element(By.CLASS_NAME, "add-to-cart-btn")  # Adjust the selector
    add_to_cart_button.click()

    # Wait for the cart count to be updated
    cart_count = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "cart-count"))
    )

    time.sleep(3)

    # Check if the cart count is not '0'
    assert cart_count.text != "0", f"Cart count should be greater than 0, but found {cart_count.text}"

    # Optionally, check if the cart count is visible
    is_visible = driver.execute_script(
        "return window.getComputedStyle(arguments[0]).display != 'none';", cart_count
    )
    assert is_visible, "Cart count is not visible."

#Test case 5: Verify the presence of sorting options for products (e.g., by price, name, etc.)
def test_sorting_options(driver):
    # Step 1: Go to the product listing page
    driver.get("http://127.0.0.1:8000")  # Replace with the actual product listing page URL
    
    # Step 2: Wait for the sorting dropdown or buttons to be visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "sort"))
    )

    time.sleep(3)

    # Step 3: Verify that sorting options are visible (by price, name, etc.)
    sorting_dropdown = driver.find_element(By.ID, "sort")
    assert sorting_dropdown.is_displayed(), "Sorting options dropdown is not displayed"

    # Verify the presence of specific sorting options (e.g., by price, by name)
    sorting_options = sorting_dropdown.find_elements(By.TAG_NAME, "option")
    assert len(sorting_options) > 0, "No sorting options available"
    
    # Extract option texts and values
    option_texts = [option.text.strip().lower() for option in sorting_options]
    option_values = [option.get_attribute("value") for option in sorting_options]

    # Verify specific options (by value and text)
    assert "price (low to high)" in option_texts, "Price sorting option is not present"
    assert "price (high to low)" in option_texts, "Price sorting option is not present"
    assert "name (a-z)" in option_texts, "Name sorting option is not present"
    assert "name (z-a)" in option_texts, "Name sorting option is not present"

    # Verify sorting option values
    assert "price" in option_values, "Price sorting option value is missing"
    assert "price_desc" in option_values, "Price (High to Low) sorting option value is missing"
    assert "name" in option_values, "Name sorting option value is missing"
    assert "name_desc" in option_values, "Name (Z-A) sorting option value is missing"

    # Step 4: Optionally, interact with the sorting dropdown to verify functionality
    # Select a sorting option (e.g., by price)
    sorting_dropdown.click()  # Open the dropdown
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//option[text()='Price (Low to High)']"))
    )
    price_option = driver.find_element(By.XPATH, "//option[text()='Price (Low to High)']")
    price_option.click()  # Select the price sorting option

    time.sleep(3)

    # Wait for the page to reload and check if the products are sorted by price
    WebDriverWait(driver, 10).until(
        EC.staleness_of(sorting_dropdown)  # Wait for the page to refresh after the sorting action
    )


    # Step 6: Extract the first product price after sorting
    first_product_price_text = driver.find_element(By.CSS_SELECTOR, ".product-card p").text

    # Clean the price string (remove '$' and convert to float for comparison)
    first_product_price = float(first_product_price_text.replace('$', '').strip())

    assert first_product_price > 0, "Product price is not valid after sorting by price"

# Test case 6: Verify that the search bar is visible and functional
def test_search(driver):
    # List of possible search queries
    search_queries = ["banana", "apple", "tomato", "avocado", "cherry"]
    
    # Randomly select a search query from the list
    search_query = random.choice(search_queries)
    
    # Open the e-commerce website homepage
    driver.get("http://127.0.0.1:8000")  # Replace with your site URL

    # Wait for the search bar to be visible
    search_bar = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "q"))
    )
    assert search_bar.is_displayed(), "Search bar is not visible on the homepage."

    # Perform a search operation with the randomly selected search query
    search_bar.clear()  # Clear any existing text in the search bar
    search_bar.send_keys(search_query)

    # Locate and click the search button
    search_button = driver.find_element(By.CLASS_NAME, "btn-primary")
    search_button.click()

    # Wait for the search results to load
    product_list = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "product-list"))
    )
    assert product_list.is_displayed(), "Product list is not visible after performing the search."

    # Verify that at least one product card is displayed
    product_cards = product_list.find_elements(By.CLASS_NAME, "product-card")
    assert len(product_cards) > 0, "No products were found in the search results."

    # Verify the first product matches the search query
    product_names = [card.find_element(By.TAG_NAME, "h3").text.lower() for card in product_cards]
    assert any(search_query.lower() in name for name in product_names), (
        f"No products matching '{search_query}' found in the search results."
    )

    # Wait for and verify the "Clear Search" button is visible
    clear_search_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "btn-secondary"))
    )
    assert clear_search_button.is_displayed(), "'Clear Search' button is not visible after performing a search."

    # Click the "Clear Search" button
    clear_search_button.click()

    # Wait for the product list to reset and show all products
    WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.CLASS_NAME, "product-card")) > 0  # Ensure products are visible after reset
    )

    # Verify the search bar is cleared
    cleared_search_bar = WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element_value((By.NAME, "q"), "")
    )
    assert cleared_search_bar, "Search bar was not cleared after clicking 'Clear Search' button."

    # Optionally, verify that the product list is now showing all products
    product_cards_after_clear = driver.find_elements(By.CLASS_NAME, "product-card")
    assert len(product_cards_after_clear) > 0, "Product list is empty after clearing the search."


# Test case 7: Verify that the "Add to Cart" buttons work correctly
def test_add_to_cart(driver):
    # Open the e-commerce website homepage
    driver.get("http://127.0.0.1:8000")  # Replace with your site URL

    # Wait for the product list to load
    product_list = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "product-list"))
    )

    # Verify that at least one "Add to Cart" button is visible
    add_to_cart_buttons = driver.find_elements(By.CLASS_NAME, "add-to-cart-btn")
    assert len(add_to_cart_buttons) > 0, "No 'Add to Cart' buttons found on the homepage."

    # Get the current cart count before adding an item
    cart_count = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "cart-count"))
    )
    initial_cart_count = int(cart_count.text) if cart_count.text.isdigit() else 0

    # Click on the first "Add to Cart" button
    add_to_cart_buttons[0].click()

    # Wait for the cart count to be updated
    WebDriverWait(driver, 10).until(
        lambda d: int(d.find_element(By.ID, "cart-count").text) > initial_cart_count
    )

    # Get the updated cart count and verify it has increased by 1
    updated_cart_count = int(driver.find_element(By.ID, "cart-count").text)
    assert updated_cart_count == initial_cart_count + 1, f"Expected cart count to be {initial_cart_count + 1}, but found {updated_cart_count}"

    # Optionally, check if the cart count is visible
    is_visible = driver.execute_script(
        "return window.getComputedStyle(arguments[0]).display != 'none';", cart_count
    )
    assert is_visible, "Cart count is not visible."


# Test case 8: Verify that the pagination works correctly (if there is pagination for products)
def test_pagination(driver):
    base_url = "http://127.0.0.1:8000"
    driver.get(base_url)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pagination")))

    # Click the "Next" button
    next_btn = driver.find_element(By.LINK_TEXT, "Next")
    next_btn.click()
    wait.until(EC.staleness_of(next_btn))  # Wait for the element to become stale (after clicking)

    # Click the "Previous" button
    prev_btn = driver.find_element(By.LINK_TEXT, "Previous")
    prev_btn.click()
    wait.until(EC.staleness_of(prev_btn))  # Wait for the element to become stale (after clicking)

    # Click the "Last" button
    last_btn = driver.find_element(By.LINK_TEXT, "Last")
    last_btn.click()
    wait.until(EC.staleness_of(last_btn))  # Wait for the element to become stale (after clicking)

    # Click the "First" button
    first_btn = driver.find_element(By.LINK_TEXT, "First")
    first_btn.click()
    wait.until(EC.staleness_of(first_btn))  # Wait for the element to become stale (after clicking)

