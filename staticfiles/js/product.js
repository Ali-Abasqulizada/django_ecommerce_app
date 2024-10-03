const addToCartCountEl = document.querySelector(".add_to_cart_count");
const operationsMinus = document.querySelector(".operations button:first-child");
const operationsPlus = document.querySelector(".operations button:last-child");
const cartCountInput = document.querySelector("#cart_count_input");

let addToCartCount = parseInt(addToCartCountEl.textContent);

const updateAddToCartCount = (newCount) => {
  addToCartCount = newCount;
  addToCartCountEl.textContent = addToCartCount;
  cartCountInput.value = addToCartCount;
};

// Event listener for minus button
operationsMinus.addEventListener("click", () => {
  if (addToCartCount > 1) {
    updateAddToCartCount(addToCartCount - 1);
  }
});

operationsPlus.addEventListener("click", () => {
  updateAddToCartCount(addToCartCount + 1);
});