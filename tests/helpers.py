from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_user(driver, username, password):
    # Step 1: Open the Home page
    driver.get("http://localhost:8000/")  # Replace with your actual Home page URL

    # Step 2: Click the 'Login' button
    login_button = driver.find_element(By.LINK_TEXT, "Login")
    login_button.click()

    # Step 3: Verify the Login page is opened
    assert "/auth/login/" in driver.current_url

    # Step 4: Enter valid login credentials
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)

    # Step 5: Click the 'Login' button to submit the login form
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Step 6: Verify the user is redirected to the correct page after login
    assert "/" in driver.current_url
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.logout-button"))
    )

def logout_user(driver):
    """
    Logs out the user from the application.
    :param driver: WebDriver instance.
    """
    # Find and click the logout button
    logout_button = driver.find_element(By.CSS_SELECTOR, "button.logout-button")
    logout_button.click()

    # Verify that the user is redirected to the login page or the login button is visible
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Login"))
    )
    login_button = driver.find_element(By.LINK_TEXT, "Login")
    assert login_button.is_displayed(), "Login button not visible after logout."
