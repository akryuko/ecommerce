import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import random

# Define screen sizes for responsiveness testing
SCREEN_SIZES = {
    "desktop": (1920, 1080),
    "tablet": (768, 1024),
    "mobile": (375, 667),
}

# Test case 42: Verify that the website is responsive on different screen sizes (desktop, tablet, mobile).
@pytest.mark.parametrize("device, size", SCREEN_SIZES.items())
def test_elements_visibility(driver, device, size):
    """Verify required elements are visible on all screen sizes."""
    # Set browser window size
    driver.set_window_size(size[0], size[1])
    
    # Navigate to the e-commerce website
    driver.get("http://127.0.0.1:8000")
    
    # Verify Cart Icon
    cart_icon = driver.find_element(By.CLASS_NAME, "cart-icon-container")
    assert cart_icon.is_displayed(), f"Cart icon should be visible on {device} screens."
    
    # Verify Login Button
    login_button = driver.find_element(By.CLASS_NAME, "login-button")
    assert login_button.is_displayed(), f"Login button should be visible on {device} screens."
    
    # Verify Search Bar
    search_bar = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search products..."]')
    assert search_bar.is_displayed(), f"Search bar should be visible on {device} screens."
    
    # Verify Sort Dropdown
    sort_dropdown = driver.find_element(By.ID, "sort")
    assert sort_dropdown.is_displayed(), f"Sort dropdown should be visible on {device} screens."
    
    # Verify Product Grid
    product_list = driver.find_element(By.CLASS_NAME, "product-list")
    assert product_list.is_displayed(), f"Product grid should be visible on {device} screens."
    
    # Verify at least one product card is displayed
    product_cards = driver.find_elements(By.CLASS_NAME, "product-card")
    assert len(product_cards) > 0, f"Product cards should be visible on {device} screens."


# Test case 43: Verify that the header and footer are correctly displayed across all pages.
# Pages to test
PAGES = [
    "/",  # Home page
    "/cart/",  # Cart page
    "/product_detail/1/",  # Example product detail page with ID=1
    "/faq/",  # FAQ page
    "/about/",  # About Us page
    "/terms/",  # Terms and Conditions page
]

@pytest.mark.parametrize("page", PAGES)
def test_header_and_footer(driver, page):
    """Verify header and footer are displayed correctly and contain the required elements."""
    base_url = "http://127.0.0.1:8000"  # Replace with your base URL
    driver.get(base_url + page)

    # Verify Header
    header = driver.find_element(By.CLASS_NAME, "header")
    assert header.is_displayed(), f"Header should be visible on page: {page}"

    # Verify logo in header
    logo = driver.find_element(By.CSS_SELECTOR, ".logo a img")
    assert logo.is_displayed(), f"Logo should be visible in the header on page: {page}"

    # Verify cart icon in header
    cart_icon = driver.find_element(By.CSS_SELECTOR, ".cart-icon-container")
    assert cart_icon.is_displayed(), f"Cart icon should be visible in the header on page: {page}"

    # Verify login button in header
    login_button = driver.find_element(By.CSS_SELECTOR, ".login-button")
    assert login_button.is_displayed(), f"Login button should be visible in the header on page: {page}"

    # Verify Footer
    footer = driver.find_element(By.CLASS_NAME, "footer")
    assert footer.is_displayed(), f"Footer should be visible on page: {page}"

    # Verify Contact Us section in footer
    contact_us = driver.find_element(By.CSS_SELECTOR, ".footer-contact")
    assert contact_us.is_displayed(), f"Contact Us section should be visible in the footer on page: {page}"

    # Verify navigation links in footer
    nav_links = driver.find_elements(By.CSS_SELECTOR, ".footer-nav-links ul li a")
    assert len(nav_links) > 0, f"Footer navigation links should be present on page: {page}"

    # Verify Payment Methods section in footer
    payment_methods = driver.find_element(By.CSS_SELECTOR, ".footer-payment")
    assert payment_methods.is_displayed(), f"Payment Methods section should be visible in the footer on page: {page}"

    # Verify Social Media section in footer
    social_media = driver.find_element(By.CSS_SELECTOR, ".footer-social-media")
    assert social_media.is_displayed(), f"Social Media section should be visible in the footer on page: {page}"

    # Verify footer-bottom copyright text
    footer_bottom = driver.find_element(By.CSS_SELECTOR, ".footer-bottom p")
    assert "© 2024 My Ecommerce Store" in footer_bottom.text, \
        f"Footer copyright text should be correct on page: {page}"

 
 # Test case 44: Verify that product images are displayed properly on all devices.
@pytest.mark.parametrize("device, size", SCREEN_SIZES.items())
def test_product_images_displayed(driver, device, size):
    """Verify product images are displayed properly on all devices."""
    base_url = "http://127.0.0.1:8000"  # Replace with your base URL
    driver.set_window_size(size[0], size[1])  # Set the browser window size
    driver.get(base_url + "/")  # Navigate to the product listing page

    # Find all product images
    product_images = driver.find_elements(By.CSS_SELECTOR, ".product-image")
    assert len(product_images) > 0, "No product images found on the page."

    for image in product_images:
        # Check if the image is displayed
        assert image.is_displayed(), f"Product image not displayed: {image.get_attribute('alt')}"

        # Optional: Check that the image source is not empty
        src = image.get_attribute("src")
        assert src, f"Product image source (src) is empty: {image.get_attribute('alt')}"


# Test case 45: Verify that the "Add to Cart" button is functional on mobile devices.
# Define mobile screen size
MOBILE_SCREEN_SIZE = (375, 667)

def test_add_to_cart_on_mobile(driver):
    """
    Verify that the "Add to Cart" button is functional on mobile devices.
    """
    # Set the window size for mobile devices
    driver.set_window_size(MOBILE_SCREEN_SIZE[0], MOBILE_SCREEN_SIZE[1])

    # Step 1: Navigate to the e-commerce website's homepage
    driver.get("http://127.0.0.1:8000")

    # Step 2: Locate all "Add to Cart" buttons on the page
    products = driver.find_elements(By.CSS_SELECTOR, ".product-card .add-to-cart-btn")
    assert len(products) > 0, "No products found on the homepage."

    # Step 3: Randomly select 1 to 3 products to add to the cart
    num_products_to_add = random.randint(1, 3)
    selected_products = random.sample(products, num_products_to_add)

    for product in selected_products:
        product.click()

    # Step 4: Navigate to the Cart page
    cart_link = driver.find_element(By.CSS_SELECTOR, ".header-actions .cart-icon-container")
    cart_link.click()

    # Expected Results: Verify that the correct number of products appears in the cart
    cart_items = driver.find_elements(By.CSS_SELECTOR, "table.table-bordered tbody tr")
    assert len(cart_items) == num_products_to_add, (
        f"Expected {num_products_to_add} items in the cart, but found {len(cart_items)}."
    )

    # Verify each product's details in the cart
    for i, cart_item in enumerate(cart_items, start=1):
        product_name = cart_item.find_element(By.CSS_SELECTOR, "td:first-child").text
        product_quantity = cart_item.find_element(By.CSS_SELECTOR, "td:nth-child(4) span").text
        assert product_quantity == "1", f"Product {i} quantity in cart is incorrect."
        print(f"Product {i}: {product_name} added successfully with quantity {product_quantity}.")