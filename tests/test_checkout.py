import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import time
import random
from selenium.common.exceptions import NoSuchElementException
from helpers import login_user, logout_user


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


# Test case 30: Verify that the user can complete the purchase and navigates to Order success page.
def test_complete_purchase(driver):
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
    driver.find_element(By.ID, "credit_card").click()  # Example: Selecting Credit Card
    time.sleep(1)  # Wait for the selection to register
    
    # Step 8: Click on the Place Order button to complete the purchase
    place_order_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-success.mt-4")
    place_order_button.click()


    # Step 9: Verify that the user is redirected to the Order Success page
    assert "Order Success" in driver.page_source  # Check if "Order Success" is in the page title or body

    print("Successfully completed the purchase and navigated to the Order Success page.")


# Test case 31: Verify that the user can continue shopping after checkout.
def test_continue_shopping_after_checkout(driver):
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
    driver.find_element(By.ID, "credit_card").click()  # Example: Selecting Credit Card
    time.sleep(1)  # Wait for the selection to register
    
    # Step 8: Click on the Place Order button to complete the purchase
    place_order_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-success.mt-4")
    place_order_button.click()

    # Step 11: Click the "Return to Home" button
    return_to_home_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary.mt-3")
    return_to_home_button.click()

    # Step 12: Verify that the user is redirected to the home page
    WebDriverWait(driver, 10).until(
        EC.url_to_be("http://127.0.0.1:8000/")  # Replace with your actual home page URL
    )
    assert driver.current_url == "http://127.0.0.1:8000/"  # Adjust as needed for the actual home page URL

    print("Successfully completed the purchase and returned to the home page.")

# Test case 32: Verify that the order success page displays the correct order details, such as items, billing, shipping address, and payment method. 
def test_order_success_page_with_logged_in_user(driver):
    fake = Faker()

    # Step 1: Log in the user
    driver.get("http://localhost:8000/")  # Replace with your actual Home page URL
    login_button = driver.find_element(By.LINK_TEXT, "Login")
    login_button.click()

    assert "/auth/login/" in driver.current_url

    valid_username = "test"  # Replace with an actual valid username
    valid_password = "user12345"  # Replace with the actual password for the test user
    driver.find_element(By.ID, "username").send_keys(valid_username)
    driver.find_element(By.ID, "password").send_keys(valid_password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    assert "/" in driver.current_url  # Verify Home page URL
    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.logout-button"))
    )
    assert logout_button.is_displayed()

    # Step 2: Add multiple products to the cart
    driver.get("http://localhost:8000")  # Navigate to home page again
    products = driver.find_elements(By.CSS_SELECTOR, ".product-card .add-to-cart-btn")
    added_product_names = []
    for product in products[:2]:  # Add first two products (or adjust as needed)
        try:
            product_name = product.find_element(By.XPATH, ".//ancestor::div[@class='product-card']//h3").text.strip()  # Get product name from card
            added_product_names.append(product_name)
            product.click()
        except NoSuchElementException as e:
            print(f"Product name not found for this product: {e}")

    # Step 3: Navigate to the Cart page
    cart_link = driver.find_element(By.CSS_SELECTOR, ".header-actions .cart-icon-container")
    cart_link.click()

    # Step 4: Navigate to the Checkout page
    checkout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/checkout/']"))
    )
    checkout_button.click()

    # Step 5: Fill in the Contact Information
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    phone = fake.phone_number()
    street_address = fake.street_address()
    city = fake.city()
    state = fake.state()
    postal_code = fake.postcode()

    driver.find_element(By.ID, "first_name").send_keys(first_name)
    driver.find_element(By.ID, "last_name").send_keys(last_name)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "phone").send_keys(phone)

    # Step 6: Fill in the Shipping Address
    driver.find_element(By.ID, "address").send_keys(street_address)
    driver.find_element(By.ID, "city").send_keys(city)
    driver.find_element(By.ID, "state").send_keys(state)
    driver.find_element(By.ID, "postal_code").send_keys(postal_code)

    # Step 7: Select Payment Method (Credit Card or PayPal)
    payment_methods = ["paypal", "credit_card"]  # Assuming the ID for PayPal and Credit Card are 'paypal' and 'credit_card'
    selected_payment_method_id = random.choice(payment_methods)  # Randomly choose between 'paypal' and 'credit_card'

    if selected_payment_method_id == "paypal":
        driver.find_element(By.ID, "paypal").click()  # Select PayPal
    elif selected_payment_method_id == "credit_card":
        driver.find_element(By.ID, "credit_card").click()  # Select Credit Card

    # Map internal IDs to UI names
    payment_method_ui_mapping = {
        "paypal": "PayPal",
        "credit_card": "Credit Card"
    }

    # Get the UI name for the selected payment method
    selected_payment_method_ui = payment_method_ui_mapping[selected_payment_method_id]


    # Step 8: Click on the Place Order button to complete the purchase
    place_order_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-success.mt-4")
    place_order_button.click()

    # Step 9: Wait for the Order Success page to load
    WebDriverWait(driver, 10).until(
        EC.url_contains("/order-success/")  # Adjust this based on the actual success page URL
    )

    # Step 10: Wait for the order success message to appear on the page
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Order Placed Successfully!')]"))
    )
    assert success_message.is_displayed()

    # Step 11: Verify the correct full text (including name) appears in the message
    expected_full_text = f"Thank you for placing your order, {first_name} {last_name}."
    actual_full_text = driver.find_element(By.CSS_SELECTOR, "p").text.strip()  # Get the full text of the paragraph
    assert expected_full_text == actual_full_text, f"Expected text '{expected_full_text}' not found. Actual text: '{actual_full_text}'"

    # Step 12: Verify that the products in the order summary match the order
    order_table_rows = driver.find_elements(By.CSS_SELECTOR, ".table tbody tr")
    for i, row in enumerate(order_table_rows):
        product_name = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip()
        assert product_name == added_product_names[i], f"Expected product name '{added_product_names[i]}', but got '{product_name}'"

    # Step 13: Verify that the Total price matches the sum of the products' total prices
    # Extract product prices from the table (assuming price is in the 4th column, i.e., "td" in the row)
    product_prices = driver.find_elements(By.XPATH, "//table[@class='table']//tbody//tr//td[4]")
    total_price = sum(float(price.text.strip().replace('$', '')) for price in product_prices)

    # Extract the displayed total price
    total_price_text = driver.find_element(By.CSS_SELECTOR, "h4.text-right").text.strip()
    # Extract numeric value from the total price text
    displayed_total_price = float(total_price_text.replace("Total: $", ""))

    # Verify that the calculated total price matches the displayed total price
    assert abs(total_price - displayed_total_price) < 0.01, f"Expected total price '{total_price:.2f}', but got '{displayed_total_price:.2f}'"


    # Step 14: Verify the shipping address
    shipping_address = driver.find_element(By.XPATH, "//p[strong[text()='Address:']]").text.strip()
    expected_address = f"Address: {street_address}, {city}, {state} - {postal_code}"
    assert shipping_address == expected_address, f"Expected address '{expected_address}', but got '{shipping_address}'"

    # Step 15: Verify the phone number
    phone_number = driver.find_element(By.XPATH, "//p[strong[text()='Phone:']]").text.strip()
    assert phone_number == f"Phone: {phone}", f"Expected phone number '{phone}', but got '{phone_number}'"

    # Step 16: Verify the payment method
    payment_method = driver.find_element(By.XPATH, "//h3[text()='Payment Method:']/following-sibling::p").text.strip()
    assert payment_method.title() ==  selected_payment_method_ui.title(), f"Expected payment method '{ selected_payment_method_ui.capitalize()}', but got '{payment_method}'"

    logout_user(driver)


# Test case 33: Verify that the "Return to Home" button works and redirects to the homepage.
def test_return_home(driver):
    fake = Faker()

    # Step 1: Log in the user
    driver.get("http://localhost:8000/")  # Replace with your actual Home page URL
    login_button = driver.find_element(By.LINK_TEXT, "Login")
    login_button.click()

    assert "/auth/login/" in driver.current_url

    valid_username = "test"  # Replace with an actual valid username
    valid_password = "user12345"  # Replace with the actual password for the test user
    driver.find_element(By.ID, "username").send_keys(valid_username)
    driver.find_element(By.ID, "password").send_keys(valid_password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    assert "/" in driver.current_url  # Verify Home page URL
    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.logout-button"))
    )
    assert logout_button.is_displayed()

    # Step 2: Add multiple products to the cart
    driver.get("http://localhost:8000")  # Navigate to home page again
    products = driver.find_elements(By.CSS_SELECTOR, ".product-card .add-to-cart-btn")
    added_product_names = []
    for product in products[:2]:  # Add first two products (or adjust as needed)
        try:
            product_name = product.find_element(By.XPATH, ".//ancestor::div[@class='product-card']//h3").text.strip()  # Get product name from card
            added_product_names.append(product_name)
            product.click()
        except NoSuchElementException as e:
            print(f"Product name not found for this product: {e}")

    # Step 3: Navigate to the Cart page
    cart_link = driver.find_element(By.CSS_SELECTOR, ".header-actions .cart-icon-container")
    cart_link.click()

    # Step 4: Navigate to the Checkout page
    checkout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/checkout/']"))
    )
    checkout_button.click()

    # Step 5: Fill in the Contact Information
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    phone = fake.phone_number()
    street_address = fake.street_address()
    city = fake.city()
    state = fake.state()
    postal_code = fake.postcode()

    driver.find_element(By.ID, "first_name").send_keys(first_name)
    driver.find_element(By.ID, "last_name").send_keys(last_name)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "phone").send_keys(phone)

    # Step 6: Fill in the Shipping Address
    driver.find_element(By.ID, "address").send_keys(street_address)
    driver.find_element(By.ID, "city").send_keys(city)
    driver.find_element(By.ID, "state").send_keys(state)
    driver.find_element(By.ID, "postal_code").send_keys(postal_code)

    # Step 7: Select Payment Method (Credit Card or PayPal)
    payment_methods = ["paypal", "credit_card"]  # Assuming the ID for PayPal and Credit Card are 'paypal' and 'credit_card'
    selected_payment_method_id = random.choice(payment_methods)  # Randomly choose between 'paypal' and 'credit_card'

    if selected_payment_method_id == "paypal":
        driver.find_element(By.ID, "paypal").click()  # Select PayPal
    elif selected_payment_method_id == "credit_card":
        driver.find_element(By.ID, "credit_card").click()  # Select Credit Card

    # Map internal IDs to UI names
    payment_method_ui_mapping = {
        "paypal": "PayPal",
        "credit_card": "Credit Card"
    }

    # Step 8: Click on the Place Order button to complete the purchase
    place_order_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-success.mt-4")
    place_order_button.click()

    # Step 9: Wait for the Order Success page to load
    WebDriverWait(driver, 10).until(
        EC.url_contains("/order-success/")  # Adjust this based on the actual success page URL
    )

    # Step 10: Wait for the order success message to appear on the page
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Order Placed Successfully!')]"))
    )
    assert success_message.is_displayed()

    # Step 11: Click the "Return to Home" button and verify redirection
    return_to_home_button = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-primary.mt-3")  # Locate the button
    return_to_home_button.click()

    # Step 12: Verify that the user is redirected to the homepage
    WebDriverWait(driver, 10).until(
        EC.url_to_be("http://localhost:8000/")  # Replace with your actual homepage URL
    )
    assert driver.current_url == "http://localhost:8000/"  # Verify the homepage URL


# Test case 35: Verify that a guest user can proceed to checkout without registering or logging in.
def test_guest_checkout(driver):
    fake = Faker()

    # Step 1: Navigate to the home page
    driver.get("http://localhost:8000")  # Replace with your actual Home page URL

    # Step 2: Add products to the cart
    products = driver.find_elements(By.CSS_SELECTOR, ".product-card .add-to-cart-btn")
    added_product_names = []
    for product in products[:5]:  # Add first two products (or adjust as needed)
        try:
            product_name = product.find_element(By.XPATH, ".//ancestor::div[@class='product-card']//h3").text.strip()
            added_product_names.append(product_name)
            product.click()
        except NoSuchElementException as e:
            print(f"Product name not found for this product: {e}")

    # Step 3: Navigate to the Cart page
    cart_link = driver.find_element(By.CSS_SELECTOR, ".header-actions .cart-icon-container")
    cart_link.click()

    # Step 4: Navigate to the Checkout page
    checkout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/checkout/']"))
    )
    checkout_button.click()

    # Step 5: Fill in the Contact Information (no login required)
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    phone = fake.phone_number()
    street_address = fake.street_address()
    city = fake.city()
    state = fake.state()
    postal_code = fake.postcode()

    driver.find_element(By.ID, "first_name").send_keys(first_name)
    driver.find_element(By.ID, "last_name").send_keys(last_name)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "phone").send_keys(phone)

    # Step 6: Fill in the Shipping Address
    driver.find_element(By.ID, "address").send_keys(street_address)
    driver.find_element(By.ID, "city").send_keys(city)
    driver.find_element(By.ID, "state").send_keys(state)
    driver.find_element(By.ID, "postal_code").send_keys(postal_code)

    # Step 7: Select Payment Method (Credit Card or PayPal)
    payment_methods = ["paypal", "credit_card"]  # Assuming the ID for PayPal and Credit Card are 'paypal' and 'credit_card'
    selected_payment_method_id = random.choice(payment_methods)  # Randomly choose between 'paypal' and 'credit_card'

    if selected_payment_method_id == "paypal":
        driver.find_element(By.ID, "paypal").click()  # Select PayPal
    elif selected_payment_method_id == "credit_card":
        driver.find_element(By.ID, "credit_card").click()  # Select Credit Card

    # Step 8: Click on the Place Order button to complete the purchase
    place_order_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-success.mt-4")
    place_order_button.click()

    # Step 9: Verify the Order Success message
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Order Placed Successfully!')]"))
    )
    assert success_message.is_displayed()

# Test case 36: Verify that the user is prompted to create an account or register after completing a guest checkout.
def test_guest_checkout_prompt_to_create_account_or_login(driver):

    fake = Faker()
    
    # Step 1: Navigate to the home page
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

    # Step 2: Add products to the cart
    products = driver.find_elements(By.CSS_SELECTOR, ".product-card .add-to-cart-btn")
    added_product_names = []
    for product in products[:2]:  # Add first two products (or adjust as needed)
        try:
            product_name = product.find_element(By.XPATH, ".//ancestor::div[@class='product-card']//h3").text.strip()
            added_product_names.append(product_name)
            product.click()
        except NoSuchElementException as e:
            print(f"Product name not found for this product: {e}")

    # Step 3: Navigate to the Cart page
    cart_link = driver.find_element(By.CSS_SELECTOR, ".header-actions .cart-icon-container")
    cart_link.click()

    # Step 4: Navigate to the Checkout page
    checkout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/checkout/']"))
    )
    checkout_button.click()

    # Step 5: Fill in the Contact Information (no login required)
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    phone = fake.phone_number()
    street_address = fake.street_address()
    city = fake.city()
    state = fake.state()
    postal_code = fake.postcode()

    driver.find_element(By.ID, "first_name").send_keys(first_name)
    driver.find_element(By.ID, "last_name").send_keys(last_name)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "phone").send_keys(phone)

    # Step 6: Fill in the Shipping Address
    driver.find_element(By.ID, "address").send_keys(street_address)
    driver.find_element(By.ID, "city").send_keys(city)
    driver.find_element(By.ID, "state").send_keys(state)
    driver.find_element(By.ID, "postal_code").send_keys(postal_code)

    # Step 7: Select Payment Method (Credit Card or PayPal)
    payment_methods = ["paypal", "credit_card"]  # Assuming the ID for PayPal and Credit Card are 'paypal' and 'credit_card'
    selected_payment_method_id = random.choice(payment_methods)  # Randomly choose between 'paypal' and 'credit_card'

    if selected_payment_method_id == "paypal":
        driver.find_element(By.ID, "paypal").click()  # Select PayPal
    elif selected_payment_method_id == "credit_card":
        driver.find_element(By.ID, "credit_card").click()  # Select Credit Card

    # Step 8: Click on the Place Order button to complete the purchase
    place_order_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-success.mt-4")
    place_order_button.click()

    # Step 9: Verify the Order Success message
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Order Placed Successfully!')]"))
    )
    assert success_message.is_displayed()

    # Step 10: Verify that the user is prompted to create an account or log in
    # Check for "Create Account" button
    create_account_button = driver.find_element(By.CSS_SELECTOR, ".btn-create-account")
    assert create_account_button.is_displayed(), "'Create Account' button not found"

    # Check for "Login" link
    login_link = driver.find_element(By.CSS_SELECTOR, ".btn-login")
    assert login_link.is_displayed(), "'Login' link not found"

    # Step 11: Click on "Create Account" and verify redirection to the registration page
    create_account_button.click()
    WebDriverWait(driver, 10).until(
        EC.url_contains("/register/")  # Check if redirected to registration page
    )
    assert "/register/" in driver.current_url, "Failed to redirect to registration page after clicking 'Create Account'"

    # Step 12: Go back to the Order Success page using the browser's back action
    driver.back()

    # Step 13: Click on "Log in here" and verify redirection to the login page
    login_link.click()
    WebDriverWait(driver, 10).until(
        EC.url_contains("/auth/login/")  # Check if redirected to login page
    )
    assert "/auth/login/" in driver.current_url, "Failed to redirect to login page after clicking 'Log in here'"

