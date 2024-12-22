import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import time


# Test case 26: Verify that the checkout page loads correctly.
def test_checkout_page_loads_correctly(driver):
    # Step 1: Navigate to the e-commerce website's homepage
    driver.get("http://127.0.0.1:8000")  # Replace with your site URL

    # Step 2: Add a product to the cart
    product = driver.find_element(By.CSS_SELECTOR, ".product-card .add-to-cart-btn")
    product.click()

    # Step 3: Navigate to the Cart page
    cart_link = driver.find_element(By.CSS_SELECTOR, ".header-actions .cart-icon-container")
    cart_link.click()

    # Step 4: Locate and click the "Go to Checkout" button
    checkout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/checkout/']"))
    )
    checkout_button.click()

    # Step 5: Wait for the checkout page to load
    WebDriverWait(driver, 10).until(
        EC.url_contains("/checkout/")
    )

    # Step 6: Verify all required elements on the checkout page

    # Contact Information Fields
    assert driver.find_element(By.ID, "first_name"), "First Name field is missing."
    assert driver.find_element(By.ID, "last_name"), "Last Name field is missing."
    assert driver.find_element(By.ID, "email"), "Email field is missing."
    assert driver.find_element(By.ID, "phone"), "Phone field is missing."

    # Shipping Address Fields
    assert driver.find_element(By.ID, "address"), "Street Address field is missing."
    assert driver.find_element(By.ID, "city"), "City field is missing."
    assert driver.find_element(By.ID, "state"), "State field is missing."
    assert driver.find_element(By.ID, "postal_code"), "Postal Code field is missing."

    # Payment Method Options
    assert driver.find_element(By.ID, "credit_card"), "Credit Card payment option is missing."
    assert driver.find_element(By.ID, "paypal"), "PayPal payment option is missing."

    # Hidden Inputs for Cart Data
    cart_data_elements = driver.find_elements(By.NAME, "cart_data")
    assert len(cart_data_elements) > 0, "Hidden cart data inputs are missing."

    # Submit Button
    assert driver.find_element(By.CSS_SELECTOR, "button[type='submit']"), "Place Order button is missing."

    # Step 7: Confirm the URL
    assert "/checkout/" in driver.current_url, f"Expected URL to contain '/checkout/', but got {driver.current_url}"

    print("Checkout page loaded successfully with all required elements.")


# Test case 27: Verify that the order summary displays the correct items, quantities, and total price.
def test_order_summary_correctness(driver):
    # Step 1: Navigate to the e-commerce website's homepage
    driver.get("http://127.0.0.1:8000")  # Replace with your site URL

    # Step 2: Add multiple products to the cart
    products = driver.find_elements(By.CSS_SELECTOR, ".product-card .add-to-cart-btn")
    for product in products[:3]:  # Add first three products (or adjust as needed)
        product.click()

    # Step 3: Navigate to the Cart page
    cart_link = driver.find_element(By.CSS_SELECTOR, ".header-actions .cart-icon-container")
    cart_link.click()

    # Step 4: Extract cart data
    cart_rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
    cart_items = []
    for row in cart_rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        name = cells[0].text  # Product Name
        price = float(cells[2].text.replace("$", ""))  # Price
        quantity = int(cells[3].find_element(By.TAG_NAME, "span").text)  # Quantity
        total = float(cells[4].text.replace("$", ""))  # Total
        cart_items.append({"name": name, "price": price, "quantity": quantity, "total": total})

    # Calculate the expected total price from the cart page
    expected_total = sum(item["total"] for item in cart_items)

    # Step 5: Proceed to Checkout
    checkout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/checkout/']"))
    )
    checkout_button.click()

    # Step 6: Wait for the checkout page to load
    WebDriverWait(driver, 10).until(
        EC.url_contains("/checkout/")
    )

    # Step 7: Extract order summary data from the checkout page
    order_summary_rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
    for i, row in enumerate(order_summary_rows):
        cells = row.find_elements(By.TAG_NAME, "td")
        name = cells[0].text  # Product Name
        price = float(cells[3].text.replace("$", ""))  # Price
        quantity = int(cells[2].text)  # Quantity
        total = float(cells[4].text.replace("$", ""))  # Total

        # Compare with cart data
        assert name == cart_items[i]["name"], f"Expected product name '{cart_items[i]['name']}', but got '{name}'."
        assert price == cart_items[i]["price"], f"Expected price {cart_items[i]['price']}, but got {price}."
        assert quantity == cart_items[i]["quantity"], f"Expected quantity {cart_items[i]['quantity']}, but got {quantity}."
        assert total == cart_items[i]["total"], f"Expected total {cart_items[i]['total']}, but got {total}."

    # Step 8: Verify the total price on the checkout page
    checkout_total = float(driver.find_element(By.CSS_SELECTOR, "h3.text-right").text.replace("Total: $", ""))
    assert checkout_total == expected_total, f"Expected total price {expected_total}, but got {checkout_total}."

    print("Order summary dynamically verified with the cart data.")


# Test case 28: Verify that the user can enter contact and shipping information.
def test_enter_contact_and_shipping_information(driver):
    fake = Faker()
    
    # Step 1:Generate fake data
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    phone = fake.phone_number()
    street_address = fake.street_address()
    city = fake.city()
    state = fake.state()
    postal_code = fake.postcode()

    driver.get("http://127.0.0.1:8000")  # Replace with your site URL

    # Step 2: Add multiple products to the cart
    products = driver.find_elements(By.CSS_SELECTOR, ".product-card .add-to-cart-btn")
    for product in products[:3]:  # Add first three products (or adjust as needed)
        product.click()

    # Step 3: Navigate to the Cart page
    cart_link = driver.find_element(By.CSS_SELECTOR, ".header-actions .cart-icon-container")
    cart_link.click()
    

    # Step 4: Navigate to the Checkout page
    checkout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/checkout/']"))
    )
    checkout_button.click()

    # Step 5: Fill in the Contact Information
    driver.find_element(By.ID, "first_name").send_keys(first_name)
    driver.find_element(By.ID, "last_name").send_keys(last_name)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "phone").send_keys(phone)
    
    time.sleep(2)

    # Step 6: Fill in the Shipping Address
    driver.find_element(By.ID, "address").send_keys(street_address)
    driver.find_element(By.ID, "city").send_keys(city)
    driver.find_element(By.ID, "state").send_keys(state)
    driver.find_element(By.ID, "postal_code").send_keys(postal_code)
        
    # Assert that the fields are filled correctly
    assert driver.find_element(By.ID, "first_name").get_attribute("value") == first_name
    assert driver.find_element(By.ID, "email").get_attribute("value") == email
    
    print("Successfully filled in contact and shipping information with dynamic data.")


# Test case 29: Verify that the user can select a payment method (Credit card / Paypal).
def test_select_payment_method(driver):
    fake = Faker()
    
    # Step 1: Generate fake data
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    phone = fake.phone_number()
    street_address = fake.street_address()
    city = fake.city()
    state = fake.state()
    postal_code = fake.postcode()

    driver.get("http://127.0.0.1:8000")  # Replace with your site URL

    # Step 2: Add multiple products to the cart
    products = driver.find_elements(By.CSS_SELECTOR, ".product-card .add-to-cart-btn")
    for product in products[:3]:  # Add first three products (or adjust as needed)
        product.click()

    # Step 3: Navigate to the Cart page
    cart_link = driver.find_element(By.CSS_SELECTOR, ".header-actions .cart-icon-container")
    cart_link.click()
    
    # Step 4: Navigate to the Checkout page
    checkout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/checkout/']"))
    )
    checkout_button.click()

    # Step 5: Fill in the Contact Information
    driver.find_element(By.ID, "first_name").send_keys(first_name)
    driver.find_element(By.ID, "last_name").send_keys(last_name)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "phone").send_keys(phone)
    
    time.sleep(2)

    # Step 6: Fill in the Shipping Address
    driver.find_element(By.ID, "address").send_keys(street_address)
    driver.find_element(By.ID, "city").send_keys(city)
    driver.find_element(By.ID, "state").send_keys(state)
    driver.find_element(By.ID, "postal_code").send_keys(postal_code)
        
    # Step 7: Select Payment Method (Credit Card or PayPal)
    # Select Credit Card payment method
    driver.find_element(By.ID, "credit_card").click()
    time.sleep(1)  # Wait for the selection to register
    
    # Assert that the Credit Card option is selected
    assert driver.find_element(By.ID, "credit_card").is_selected(), "Credit Card payment method was not selected."
    
    # Select PayPal payment method
    driver.find_element(By.ID, "paypal").click()
    time.sleep(1)  # Wait for the selection to register
    
    # Assert that the PayPal option is selected
    assert driver.find_element(By.ID, "paypal").is_selected(), "PayPal payment method was not selected."

    # Step 8: Assert that both options can be selected, but only one at a time
    assert not driver.find_element(By.ID, "credit_card").is_selected() or not driver.find_element(By.ID, "paypal").is_selected(), \
        "Both payment methods cannot be selected simultaneously."
    
    print("Successfully selected a payment method and verified the selection.")

