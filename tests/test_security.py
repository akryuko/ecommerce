from helpers import login_user
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time
from helpers import login_user, logout_user
from selenium.common.exceptions import NoSuchElementException

# Test case 38: Verify that the session is maintained during navigation between pages for logged-in users.
def test_session_persistence(driver):
    # Log in using the helper function
    login_user(driver, username="test", password="user12345")

    # Define pages to test session persistence
    pages = [
        "http://localhost:8000/cart/",
        "http://localhost:8000/",
        "http://localhost:8000/faq/",
        "http://localhost:8000/about/",
    ]

    # Verify session persistence across pages
    for page in pages:
        driver.get(page)
        assert WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.logout-button"))
        ), f"Session lost on page {page}"


# Test case 39: Verify that sensitive data (like passwords) is securely handled during login and registration.
def test_sensitive_data_handling_login(driver):
    # Step 1: Navigate to the login page
    driver.get("http://localhost:8000/login")  # Replace with your actual login URL

    # Step 2: Verify the password field type is 'password'
    password_field = driver.find_element(By.ID, "password")
    assert password_field.get_attribute("type") == "password", "Password field is not properly masked."

def test_sensitive_data_handling_registration(driver):
    # Step 1: Navigate to the registration page
    driver.get("http://localhost:8000/register")  # Replace with your actual registration URL

    # Step 2: Verify the first password field is present and properly configured
    password1_field = driver.find_element(By.ID, "id_password1")
    assert password1_field.get_attribute("type") == "password", "Password field is not properly masked."

    # Step 3: Verify the second password field (confirmation) is present and properly configured
    password2_field = driver.find_element(By.ID, "id_password2")
    assert password2_field.get_attribute("type") == "password", "Password confirmation field is not properly masked."

    # Step 4: Verify the form uses the POST method
    form_element = driver.find_element(By.TAG_NAME, "form")
    assert form_element.get_attribute("method").lower() == "post", "Form method should be POST."

    # Step 5: Verify the 'Register' button is present
    register_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    assert register_button.text == "Register", "Register button text is incorrect."


# Test case 40:  Verify that users are logged out after a period of inactivity.
def test_auto_logout_after_inactivity(driver):

    # Step 1: Ensure the user is logged out
    driver.get("http://localhost:8000")  # Replace with your actual Home page URL
    
    try:
        # Check if the logout button is present
        logout_button = driver.find_element(By.CSS_SELECTOR, ".logout-button")
        logout_button.click()  # Log out the user
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".login-button"))
        )  # Wait until the Login button appears, confirming logout
    except NoSuchElementException:
        # No logout button means the user is already logged out
        login_button = driver.find_element(By.CSS_SELECTOR, ".login-button")
        assert login_button.is_displayed(), "Login button not found; unable to confirm logged-out state."


    # Step 2: Log in with valid credentials
    login_user(driver, username="test", password="user12345")

    logout_button = driver.find_element(By.CSS_SELECTOR, "button.logout-button")

    # Verify the user is redirected to the correct page after login
    assert "/" in driver.current_url  # Verify Home page URL
    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.logout-button"))
    )
    assert logout_button.is_displayed()


    # Step 3: Wait for inactivity timeout (e.g., 5 minutes)
    timeout_duration = 1 * 60  # Adjust to match your application's session timeout setting (in seconds)
    time.sleep(timeout_duration + 10)  # Adding buffer to ensure the session expires

    # Step 4: Try accessing a protected page (e.g., profile)
    driver.get("http://localhost:8000/")  # Replace with an actual protected page URL

    # Step 5: Verify user is logged out and redirected to the login page
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Login"))  # Check if the login link is present
    )
    
    # Assert that the login button is visible and the page redirected to login
    assert "Login" in driver.page_source, "User was not logged out after inactivity."

    # Verify that cart is empty.
    cart_link = driver.find_element(By.CSS_SELECTOR, ".header-actions .cart-icon-container")
    cart_link.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "p.h4"))
    )
    empty_cart_message = driver.find_element(By.CSS_SELECTOR, "p.h4").text
    assert empty_cart_message == "Your cart is empty.", "The cart is not empty after session timeout."
    
 