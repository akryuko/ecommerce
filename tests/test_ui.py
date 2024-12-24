import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


# Test case 42: Verify that the website is responsive on different screen sizes (desktop, tablet, mobile).
# Define screen sizes for responsiveness testing
SCREEN_SIZES = {
    "desktop": (1920, 1080),
    "tablet": (768, 1024),
    "mobile": (375, 667),
}

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

 