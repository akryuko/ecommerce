import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import login_user, logout_user  # Ensure this imports your helper functions

# Test case 50: Verify profile page functionality.
def test_profile_page(driver):
    # Log in with valid credentials
    login_user(driver, username="test", password="user12345")
    
    # Navigate to the Profile page
    driver.get("http://localhost:8000/profile/")  # Update with your actual profile page URL
    
    # Check page title
    assert "Profile" in driver.title, "Profile page title does not match."
    
    # Verify the welcome message
    welcome_message = driver.find_element(By.TAG_NAME, "h1").text
    assert "Welcome," in welcome_message, "Welcome message is incorrect."
    
    # Check the "Change Password" button
    change_password_button = driver.find_element(By.LINK_TEXT, "Change Password")
    assert change_password_button.is_displayed(), "Change Password button is not displayed."
    assert change_password_button.get_attribute("href"), "Change Password button does not have a link."
    
    # Verify the order history table or fallback message
    try:
        table = driver.find_element(By.TAG_NAME, "table")
        headers = table.find_elements(By.TAG_NAME, "th")
        assert len(headers) == 4, "Order history table headers do not match expected count."
        
        # If orders exist, check the "View Details" link
        view_details_button = driver.find_element(By.LINK_TEXT, "View Details")
        view_details_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("order"))
        assert "Order Details" in driver.title, "Did not navigate to Order Details page."
    except:
        no_orders_message = driver.find_element(By.CLASS_NAME, "alert").text
        assert "You have no orders yet." in no_orders_message, "No orders message is incorrect."
    
    # Log out after test
    logout_user(driver)
