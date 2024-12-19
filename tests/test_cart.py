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
