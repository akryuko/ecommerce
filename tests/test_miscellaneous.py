import time
import pytest
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests


# Test case 46: Verify the presence of legal pages such as Terms and Conditions, Privacy Policy, and FAQ.
def test_legal_pages_present(driver):
    """
    Verify the presence of legal pages such as Terms and Conditions, FAQ, and About Us.
    """
    # Step 1: Navigate to the homepage
    driver.get("http://127.0.0.1:8000")

    # Step 2: Locate the footer section and its links
    footer = driver.find_element(By.CSS_SELECTOR, ".footer")
    assert footer, "Footer section is not found."

    # Step 3: Verify presence of the legal page links
    legal_pages_links = {
        "FAQ": "/faq",
        "About Us": "/about",  # Updated link for About Us
        "Terms and Conditions": "/terms"
    }

    for page_name, page_url in legal_pages_links.items():
        link = footer.find_element(By.PARTIAL_LINK_TEXT, page_name)
        assert link.is_displayed(), f"'{page_name}' link is not visible in the footer."
        assert link.get_attribute("href") == f"http://127.0.0.1:8000{page_url}/" or link.get_attribute("href") == f"http://127.0.0.1:8000{page_url}", f"'{page_name}' link is incorrect."

    # Step 4: Optionally, verify that the links are working by opening them
    for page_name, page_url in legal_pages_links.items():
        link = footer.find_element(By.PARTIAL_LINK_TEXT, page_name)
        link.click()

        # Normalize URLs by removing the trailing slash for comparison
        current_url = driver.current_url.rstrip('/')
        expected_url = f"http://127.0.0.1:8000{page_url}".rstrip('/')

        assert current_url == expected_url, f"'{page_name}' page did not load correctly. Expected {expected_url} but got {current_url}."
        driver.back()  # Go back to the previous page (home page)

# Test case 47: Verify that social media links in the footer work correctly.
def test_social_media_links(driver):
    """
    Verify that social media links in the footer work correctly.
    """
    # Step 1: Navigate to the homepage
    driver.get("http://127.0.0.1:8000")

    # Step 2: Locate the footer section and its social media links
    footer = driver.find_element(By.CSS_SELECTOR, ".footer")
    assert footer, "Footer section is not found."

    # Step 3: Verify presence of social media links
    social_media_links = {
        "Instagram": "https://instagram.com",
        "Facebook": "https://facebook.com"
    }

    for platform, url in social_media_links.items():
        link = footer.find_element(By.PARTIAL_LINK_TEXT, platform)
        assert link.is_displayed(), f"'{platform}' link is not visible in the footer."
        
        # Normalize URLs by removing the trailing slash (if any) and comparing
        expected_url = url.rstrip('/')
        actual_url = link.get_attribute("href").rstrip('/')
        
        # Ensure comparison ignores 'www' in URLs
        expected_netloc = urlparse(expected_url).netloc
        actual_netloc = urlparse(actual_url).netloc
        
        # Strip out 'www' if present
        expected_netloc = expected_netloc.lstrip('www.')
        actual_netloc = actual_netloc.lstrip('www.')

        assert expected_netloc == actual_netloc, f"'{platform}' link is incorrect. Expected {expected_url}, but got {actual_url}."

    # Step 4: Optionally, verify that the links are working by opening them in a new tab
    for platform, url in social_media_links.items():
        link = footer.find_element(By.PARTIAL_LINK_TEXT, platform)
        link.click()

        # Wait for the new tab to open and switch to the new tab
        time.sleep(2)  # You might want to use WebDriverWait here for better reliability
        driver.switch_to.window(driver.window_handles[1])

        # Verify that the URL of the social media page is correct (check the netloc part of the URL)
        expected_netloc = urlparse(url).netloc
        actual_netloc = urlparse(driver.current_url).netloc

        # Strip out 'www' if present
        expected_netloc = expected_netloc.lstrip('www.')
        actual_netloc = actual_netloc.lstrip('www.')

        assert expected_netloc == actual_netloc, f"'{platform}' social media page did not load correctly. Expected {url}, but got {driver.current_url}"

        # Close the new tab and switch back to the main window
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

# Test case 48: Verify that the website displays a "404 Page Not Found" message for non-existent URLs.
def test_404_page_not_found():
    """
    Verify that the website returns a 404 status code for non-existent URLs.
    """
    # Define the non-existent URL
    non_existent_url = "http://127.0.0.1:8000/non-existent-page/"

    # Make a GET request to the non-existent URL
    response = requests.get(non_existent_url)

    # Verify that the response status code is 404
    assert response.status_code == 404, f"Expected 404, but got {response.status_code}."

# Test case 49: Verify that the "Back to Home" button works on all pages. 
@pytest.mark.parametrize("url", [
    "/",               # Homepage
    "/cart/",          # Cart page
    "/product_detail/1/",  # Product detail page (example, you can parameterize for all products)
    "/faq/",           # FAQ page
    "/about/",         # About Us page
    "/terms/",         # Terms and Conditions page
])
def test_back_to_home_button(driver, url):
    """
    Verify that the 'Back to Home' button works correctly on all pages.
    """
    # Step 1: Navigate to the specified page
    driver.get(f"http://127.0.0.1:8000{url}")

    # Step 2: Find the 'Back to Home' button (assumed to be a link or button)
    try:
        back_to_home_button = driver.find_element(By.CSS_SELECTOR, "a[href='/']")
    except:
        pytest.fail("'Back to Home' button/link not found.")

    # Step 3: Click the 'Back to Home' button
    back_to_home_button.click()

    # Step 4: Verify that the page has redirected to the homepage
    assert driver.current_url == "http://127.0.0.1:8000/", "The 'Back to Home' button did not redirect to the homepage."

    print(f"Back to Home button worked on {url} page.")