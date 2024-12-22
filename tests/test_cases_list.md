# Test Case Title

## Homepage Tests (test_homepage.py)
1. Verify that the homepage loads successfully. ✅ 
2. Verify the title of the homepage is correct (e.g., "Welcome to Our Store"). ✅ 
3. Verify that products are displayed on the homepage. ✅ 
4. Verify that the cart icon is visible and displays the correct number of items in the cart. ✅ 
5. Verify the presence of sorting options for products (e.g., by price, name, etc.). ✅ 
6. Verify that the search bar is visible and functional. ✅ 
7. Verify that the "Add to Cart" buttons work correctly. ✅ 
8. Verify that the pagination works correctly (if there is pagination for products). ✅

## Product Page Tests (test_product_page.py)
9. Verify that the product page loads successfully when View button for product is clicked ✅
10. Verify the product image is displayed on the product detail page. ✅
11. Verify the correct product name, description, and price are displayed on the product detail page. ✅
12. Verify the "Add to Cart" button works on the product page. ✅
13. Verify the "Back" and "Go to Cart" buttons work on the product page. ✅

## Cart Functionality Tests
14. Verify that products can be added to the cart successfully. ✅
15. Verify that the cart displays the correct total price after items are added. ✅
16. Verify that the cart updates the item quantity correctly when the quantity is changed.
17. Verify that an item can be removed from the cart successfully. ✅
18. Verify that the "Go to Checkout" button works correctly and leads to the checkout page. ✅
19. Verify that the cart is persistent even if the user navigates away from the page. ✅

## User Registration and Login Tests
20. Verify that a user can successfully register with valid details. ✅
21. Verify that a user cannot register with invalid details (e.g., missing fields, invalid format, existing username). ✅
22. Verify that a user can successfully log in with valid credentials. ✅
23. Verify that a user cannot log in with invalid credentials.✅ 
24. Verify that the login page displays appropriate error messages for failed login attempts.
25. Verify that the user can log out successfully and is redirected to the homepage or login page. ✅ 

## Checkout Process Tests
26. Verify that the checkout page loads correctly. ✅ 
27. Verify that the order summary displays the correct items, quantities, and total price. ✅ 
28. Verify that the user can enter contact and shipping information. ✅
29. Verify that the user can select a payment method (Credit card / Paypal). ✅
30. Verify that the user can complete the purchase and receives an order confirmation.
31. Verify that the user can continue shopping after checkout.

## Order Success / Confirmation Page Tests
32. Verify that the order confirmation page displays the correct order details, such as items, billing, shipping address, and payment method.
33. Verify that the "Return to Home" button works and redirects to the homepage.
34. Verify that an order confirmation email is sent to the user after a successful purchase.

## Guest Checkout Tests
35. Verify that a guest user can proceed to checkout without registering or logging in.
36. Verify that the user is prompted to create an account after completing a guest checkout.
37. Verify that the guest order is linked to the guest user, allowing tracking of the order.

## Security and Session Tests
38. Verify that the session is maintained during navigation between pages for logged-in users.
39. Verify that sensitive data (like passwords) is securely handled during login and registration.
40. Verify that users are logged out after a period of inactivity.
41. Verify that the "Forgot Password" functionality works correctly.

## Responsive Design and UI Tests
42. Verify that the website is responsive on different screen sizes (desktop, tablet, mobile).
43. Verify that the header and footer are correctly displayed across all pages.
44. Verify that product images are displayed properly on all devices.
45. Verify that the "Add to Cart" button is functional on mobile devices.

## Miscellaneous Tests
46. Verify the presence of legal pages such as Terms and Conditions, Privacy Policy, and FAQ.
47. Verify that social media links in the footer work correctly.
48. Verify that the website displays a "404 Page Not Found" message for non-existent URLs.
49. Verify that the "Back to Home" button works on all pages.
