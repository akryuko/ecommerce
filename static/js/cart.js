document.addEventListener("DOMContentLoaded", function () {
    const addToCartButtons = document.querySelectorAll(".add-to-cart-btn");
    const cartCountElement = document.getElementById('cart-count');

    // Update the cart count when the page loads
    updateCartCount();

    // Event listener for adding products to the cart
    addToCartButtons.forEach((button) => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            console.log("Add to Cart button clicked");

            const productId = this.getAttribute("data-product-id");
            console.log(`Product ID: ${productId}`);

            const url = `/add_to_cart/${productId}/`;
            console.log(`Fetching URL: ${url}`);

            fetch(url, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                },
            })
            .then(response => response.json())
            .then(data => {
                console.log("Add to Cart Response:", data);
                if (data.cart_count !== undefined) {
                    // Ensure the cart count is updated after adding the item
                    updateCartCount();
                } else {
                    console.error("Unexpected response:", data);
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });

    // Function to fetch and update the cart count
    function updateCartCount() {
        console.log("Fetching cart count...");
        fetch('/get_cart_count/')  // Ensure the correct endpoint is used
            .then(response => response.json())
            .then(data => {
                console.log("Cart Count Response:", data);
                if (data.cart_count !== undefined) {
                    // Update the cart count in the DOM
                    cartCountElement.textContent = data.cart_count;

                    // Show or hide the cart count depending on the cart count
                    if (data.cart_count > 0) {
                        cartCountElement.style.display = 'inline';  // Show cart count if greater than 0
                    } else {
                        cartCountElement.style.display = 'none';  // Hide cart count if 0
                    }
                }
            })
            .catch(error => {
                console.error('Error updating cart count:', error);
            });
    }
});