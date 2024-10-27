document.addEventListener("DOMContentLoaded", () => {
  const products = [
    { id: 1, name: "cake", price: 1.99 },
    { id: 2, name: "pastry", price: 2.99 },
    { id: 3, name: "bread", price: 1.49 },
    { id: 4, name: "cookie", price: 0.99 },
    { id: 5, name: "muffin", price: 2.49 },
    { id: 6, name: "donut", price: 1.29 },
    { id: 7, name: "croissant", price: 2.19 },
  ];
  const cart = [];
  const productList = document.getElementById("product-list");
  const cartItems = document.getElementById("cart-items");
  const emptyCart = document.getElementById("empty-cart");
  const cartTotal = document.getElementById("cart-total");
  const totalPrice = document.getElementById("total-price");
  const checkoutBtn = document.getElementById("checkout-btn");

  products.forEach((product) => {
    const productDiv = document.createElement("div");
    productDiv.classList.add("product");
    productDiv.innerHTML = `
    <span>${product.name} - ${product.price.toFixed(2)}</span>
    <button data-id="${product.id}">Add to cart</button>
    `;
    productList.appendChild(productDiv);
  });

  productList.addEventListener("click", (event) => {
    if ((event.target.tagName === "BUTTON")) {
      console.log("clicked");
    }
  });
});
