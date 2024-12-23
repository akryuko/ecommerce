from helpers import login_user
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

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
