// cart.js

document.addEventListener("DOMContentLoaded", function () {
    const addToCartButtons = document.querySelectorAll(".add-to-cart-btn");

    addToCartButtons.forEach((button) => {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            const productId = this.getAttribute("data-product-id");
            const url = `/add_to_cart/${productId}/`;

            fetch(url, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.cart_count !== undefined) {
                    const cartCountElement = document.querySelector(".cart-count");
                    cartCountElement.textContent = data.cart_count;
                } else {
                    console.error("Unexpected response:", data);
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});
