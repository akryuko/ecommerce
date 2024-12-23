import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import random
import string
import time


# Test case 20: Verify that a user can successfully register with valid details.
def generate_unique_username(base="testuser"):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"{base}_{timestamp}_{random_suffix}"


def test_user_registration(driver):
    # Step 1: Open the Home page
    driver.get("http://localhost:8000/")  # Replace with your actual Home page URL

    # Step 2: Click the 'Login' button
    login_button = driver.find_element(By.LINK_TEXT, "Login")  # Adjust selector if needed
    login_button.click()

    # Step 3: Verify the Login page is opened
    assert "/auth/login/" in driver.current_url

    # Step 4: Click the 'Register here' link
    register_link = driver.find_element(By.LINK_TEXT, "Register here")
    register_link.click()

    # Step 5: Verify the Registration page is opened
    assert "/register/" in driver.current_url

    # Step 6: Fill in the registration form
    unique_username = generate_unique_username()
    driver.find_element(By.ID, "id_username").send_keys(unique_username)
    driver.find_element(By.ID, "id_password1").send_keys("Password123!")
    driver.find_element(By.ID, "id_password2").send_keys("Password123!")

    # Step 7: Submit the registration form
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Step 8: Verify redirection to the Login page
    assert "/auth/login/" in driver.current_url

    # Step 9: Log in with the new user credentials
    driver.find_element(By.ID, "username").send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("Password123!")  # Replace with the actual password field ID
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Step 10: Verify redirection to the Home page and presence of 'Log out' button
    assert "/" in driver.current_url  # Verify Home page URL
    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.logout-button"))
    )
    assert logout_button.is_displayed()


# Test case 21: Verify that a user cannot register with invalid details (e.g., missing fields, invalid format).
def test_user_registration_invalid_details(driver):
    # Step 1: Open the Home page
    driver.get("http://localhost:8000/")  # Replace with your actual Home page URL

    # Step 2: Click the 'Login' button
    login_button = driver.find_element(By.LINK_TEXT, "Login")  # Adjust selector if needed
    login_button.click()

    # Step 3: Verify the Login page is opened
    assert "/auth/login/" in driver.current_url

    # Step 4: Click the 'Register here' link
    register_link = driver.find_element(By.LINK_TEXT, "Register here")
    register_link.click()

    # Step 5: Verify the Registration page is opened
    assert "/register/" in driver.current_url

    # Step 6: Attempt to submit the form with missing fields
    driver.find_element(By.ID, "id_username").send_keys("")  # Missing username
    driver.find_element(By.ID, "id_password1").send_keys("Password123!")
    driver.find_element(By.ID, "id_password2").send_keys("Password123!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Step 7: Verify error messages are displayed
    # Check if the tooltip for missing username field is displayed
    username_field = driver.find_element(By.ID, "id_username")
    assert "Please fill out this field." in username_field.get_attribute("validationMessage")

    # Step 8: Attempt to submit the form with mismatched passwords
    driver.find_element(By.ID, "id_username").send_keys("testuser_invalid")
    driver.find_element(By.ID, "id_password1").send_keys("Password123!")
    driver.find_element(By.ID, "id_password2").send_keys("DifferentPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Step 9: Verify the error message for mismatched passwords
    password_error = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".errorlist li"))
    )
    assert "The two password fields didn’t match." in password_error.text

    # Step 10: Attempt to register with an existing username
    existing_username = "alex135"  # Use a username that is already registered
    driver.find_element(By.ID, "id_username").send_keys(existing_username)
    driver.find_element(By.ID, "id_password1").send_keys("Password123!")
    driver.find_element(By.ID, "id_password2").send_keys("Password123!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Step 11: Verify the error message for existing username
    username_error = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".errorlist li"))
    )
    assert "A user with that username already exists." in username_error.text


# Test case 22: Verify that a user can successfully log in with valid credentials.
def test_user_login_valid_credentials(driver):
    from helpers import login_user

    # Use the helper function for login
    login_user(driver, username="test", password="user12345")
    logout_button = driver.find_element(By.CSS_SELECTOR, "button.logout-button")

    # Verify the user is redirected to the correct page after login
    assert "/" in driver.current_url  # Verify Home page URL
    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.logout-button"))
    )
    assert logout_button.is_displayed()


# Test case 23: Verify that a user cannot log in with invalid credentials.
def test_user_login_invalid_credentials(driver):
    # Step 1: Open the Home page
    driver.get("http://localhost:8000/")  # Replace with your actual Home page URL

    # Step 2: Click the 'Login' button
    login_button = driver.find_element(By.LINK_TEXT, "Login")  # Adjust selector if needed
    login_button.click()

    # Step 3: Verify the Login page is opened
    assert "/auth/login/" in driver.current_url

    # Step 4: Enter invalid login credentials
    invalid_username = "invaliduser"  # Replace with an invalid username
    invalid_password = "wrongpassword"  # Replace with an incorrect password
    driver.find_element(By.ID, "username").send_keys(invalid_username)
    driver.find_element(By.ID, "password").send_keys(invalid_password)

    # Step 5: Click the 'Login' button to submit the login form
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    time.sleep(2)

    # Step 7: Verify the Login page is reloaded and fields are cleared
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    assert username_field.text == ""  # Ensure username field is cleared
    assert password_field.text == ""  # Ensure password field is cleared


# Test case 24: 
def test_user_logout(driver):
    # Step 1: Open the Home page
    driver.get("http://localhost:8000/")  # Replace with your actual Home page URL

    # Step 2: Click the 'Login' button
    login_button = driver.find_element(By.LINK_TEXT, "Login")  # Adjust selector if needed
    login_button.click()

    # Step 3: Verify the Login page is opened
    assert "/auth/login/" in driver.current_url

    # Step 4: Enter valid login credentials
    valid_username = "test"  # Replace with an actual valid username
    valid_password = "user12345"  # Replace with the actual password for the test user
    driver.find_element(By.ID, "username").send_keys(valid_username)
    driver.find_element(By.ID, "password").send_keys(valid_password)

    # Step 5: Click the 'Login' button to submit the login form
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Step 6: Ensure that the user is logged in
    # This can be done by checking the presence of the logout button (or other indicators)
    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.logout-button"))
    )
    assert logout_button.is_displayed()  # Ensure the user is logged in and logout button is present

    # Step 7: Click the 'Logout' button
    logout_button.click()

    # Step 8: Wait for the Home page to refresh (based on the assumption that the page reloads)
    WebDriverWait(driver, 10).until(
        EC.staleness_of(logout_button)  # Wait until the logout button is no longer attached (indicating page refresh)
    )

    # Step 9: Verify that the Home page is refreshed and the 'Login' button is displayed
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Login"))
    )
    assert login_button.is_displayed()  # Ensure the 'Login' button is visible on the page



