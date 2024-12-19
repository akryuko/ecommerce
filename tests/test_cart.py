import random
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException


# Test case 14: Verify that products  can be added to the cart successfully.
def test_add_items_to_cart(driver):
    """
    Verify that 1 to 5 items can be added to the cart successfully.
    """
    # Step 1: Navigate to the e-commerce website's homepage
    driver.get("http://127.0.0.1:8000")

    # Step 2: Locate all products on the homepage
    products = driver.find_elements(By.CSS_SELECTOR, ".product-card .add-to-cart-btn")
    assert len(products) > 0, "No products found on the homepage."

    # Step 3: Randomly select 1 to 5 products to add to the cart
    num_products_to_add = random.randint(1, 5)
    selected_products = random.sample(products, num_products_to_add)

    for product in selected_products:
        product.click()

    # Step 4: Navigate to the Cart page
    cart_link = driver.find_element(By.CSS_SELECTOR, ".header-actions .cart-icon-container")
    cart_link.click()

    # Expected Results: Verify that the correct number of products appears in the cart
    cart_items = driver.find_elements(By.CSS_SELECTOR, "table.table-bordered tbody tr")
    assert len(cart_items) == num_products_to_add, f"Expected {num_products_to_add} items in the cart, but found {len(cart_items)}."

    # Verify each product's details in the cart
    for i, cart_item in enumerate(cart_items, start=1):
        product_name = cart_item.find_element(By.CSS_SELECTOR, "td:first-child").text
        product_quantity = cart_item.find_element(By.CSS_SELECTOR, "td:nth-child(4) span").text
        assert product_quantity == "1", f"Product {i} quantity in cart is incorrect."
        print(f"Product {i}: {product_name} added successfully with quantity {product_quantity}.")


# Test case 15: Verify that the cart displays the correct total price after items are added.
def test_cart_total_price(driver):
    # Step 1: Navigate to the e-commerce website's homepage
    driver.get("http://127.0.0.1:8000")

    # Step 2: Locate all products on the homepage
    products = driver.find_elements(By.CSS_SELECTOR, ".product-card")
    assert len(products) > 0, "No products found on the homepage."

    # Step 3: Add random products to the cart and calculate the expected total price
    total_expected_price = 0
    for i in range(3):  # Add exactly 3 items for this test
        product = products[i]
        price_element = product.find_element(By.CSS_SELECTOR, "p")
        product_price = float(price_element.text.replace("$", ""))
        total_expected_price += product_price

        add_to_cart_button = product.find_element(By.CSS_SELECTOR, ".add-to-cart-btn")
        add_to_cart_button.click()

    # Step 4: Navigate to the Cart page
    cart_link = driver.find_element(By.CSS_SELECTOR, ".header-actions .cart-icon-container")
    cart_link.click()

    # Step 5: Verify the total price in the cart
    cart_total_element = driver.find_element(By.CSS_SELECTOR, ".col-md-6.offset-md-6.text-right h4")
    cart_total_price = float(cart_total_element.text.replace("Total Cost: $", ""))
    
    # Round both totals to 2 decimal places for comparison
    total_expected_price = round(total_expected_price, 2)
    cart_total_price = round(cart_total_price, 2)
    
    assert cart_total_price == total_expected_price, f"Expected total price ${total_expected_price}, but got ${cart_total_price}."

# Test case 16: Verify that the cart updates the item quantity correctly when the quantity is changed.








# Test case 17: Verify that an item can be removed from the cart successfully.
def test_remove_item_from_cart(driver):
    # Step 1: Navigate to the e-commerce website's homepage
    driver.get("http://127.0.0.1:8000")  # Replace with your site URL

    # Step 2: Add a product to the cart
    product = driver.find_element(By.CSS_SELECTOR, ".product-card .add-to-cart-btn")
    product.click()

    # Step 3: Wait for cart count to update after adding the product
    cart_count_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "cart-count"))
    )
    initial_cart_count = int(cart_count_element.text) if cart_count_element.text.isdigit() else 0

    # Step 4: Navigate to the Cart page
    cart_link = driver.find_element(By.CSS_SELECTOR, ".header-actions .cart-icon-container")
    cart_link.click()

    # Step 5: Wait for the cart page to load (Check if table is visible)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "table"))
    )

    # Step 6: Locate the product remove button within the form
    remove_button = driver.find_element(By.XPATH, "//form[./button[text()='Remove']]")

    # Step 7: Click the remove button
    remove_button.click()

    # Step 8: Wait for the cart to update (cart count should decrease)
    # If the cart is empty, the cart count element might be missing or show a different message
    try:
        cart_count_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cart-count"))
        )
        updated_cart_count = int(cart_count_element.text) if cart_count_element.text.isdigit() else 0
    except:
        # If the cart is empty, look for the empty cart message
        empty_cart_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".h4"))
        )
        assert "Your cart is empty." in empty_cart_message.text, "Cart is not empty after removal."

    # Step 9: Verify that the product is no longer in the cart (check if the product is not in the table)
    cart_items = driver.find_elements(By.XPATH, "//td[./button[text()='Remove']]")
    assert len(cart_items) == 0, "Product was not removed from the cart."

    print("Item successfully removed from the cart.")


# Test case 18: Verify that the "Go to Checkout" button works correctly and leads to the checkout page.
def test_go_to_checkout_button(driver):
    # Step 1: Navigate to the e-commerce website's homepage
    driver.get("http://127.0.0.1:8000")  # Replace with your site URL

    # Step 2: Add a product to the cart
    product = driver.find_element(By.CSS_SELECTOR, ".product-card .add-to-cart-btn")
    product.click()


    # Step 3: Navigate to the Cart page
    cart_link = driver.find_element(By.CSS_SELECTOR, ".header-actions .cart-icon-container")
    cart_link.click()

    # Step 4: Wait for the cart page to load (Check if table is visible)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "table"))
    )

    # Step 5: Locate the "Go to Checkout" button
    checkout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/checkout/']"))
    )

    # Step 6: Click the "Go to Checkout" button
    checkout_button.click()

    # Step 7: Wait for the checkout page to load (this could be a unique element in the checkout page)
    WebDriverWait(driver, 10).until(
        EC.url_contains("/checkout/")
    )

    # Step 8: Verify that the user is on the checkout page
    assert "/checkout/" in driver.current_url, f"Expected to be on checkout page, but found {driver.current_url}"

    print("Successfully redirected to the checkout page.")


# Test cas 19: Verify that the cart is persistent even if the user navigates away from the page
def test_cart_persistence(driver):
    # Step 1: Navigate to the e-commerce website's homepage
    driver.get("http://127.0.0.1:8000")  # Replace with your site URL

    # Step 2: Add a product to the cart
    product = driver.find_element(By.CSS_SELECTOR, ".product-card .add-to-cart-btn")
    product.click()

    # Step 3: Wait for cart count to update after adding the product
    cart_count_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "cart-count"))
    )
    initial_cart_count = int(cart_count_element.text) if cart_count_element.text.isdigit() else 0

    # Step 4: Navigate to a different page (e.g., homepage)
    driver.get("http://127.0.0.1:8000")  # Go to homepage or any other page

    # Step 5: Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "product-list"))
    )

    # Step 6: Navigate back to the Cart page
    cart_link = driver.find_element(By.CSS_SELECTOR, ".header-actions .cart-icon-container")
    cart_link.click()

    # Step 7: Wait for the cart page to load (check for table visibility)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "table"))
    )

    # Step 8: Check if the cart count is the same as before navigation
    cart_count_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "cart-count"))
    )
    updated_cart_count = int(cart_count_element.text) if cart_count_element.text.isdigit() else 0

    # Step 9: Verify that the cart count is the same (indicating persistence)
    assert updated_cart_count == initial_cart_count, f"Expected cart count to be {initial_cart_count}, but found {updated_cart_count}"

    print("Cart is persistent after navigating away from the page.")