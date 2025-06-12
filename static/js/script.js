document.addEventListener('DOMContentLoaded', () => {
    const products = [
        { id: 1, name: "Laptop", price: 999.99, stock: 10, image: "https://via.placeholder.com/200" },
        { id: 2, name: "Phone", price: 499.99, stock: 15, image: "https://via.placeholder.com/200" },
        { id: 3, name: "Headphones", price: 199.99, stock: 20, image: "https://via.placeholder.com/200" }
    ];

    const cart = [];

    const productsContainer = document.getElementById('productsContainer');
    const cartItemsContainer = document.getElementById('cartItemsContainer');
    const cartCount = document.getElementById('cartCount');
    const cartTotal = document.getElementById('cartTotal');
    const cartSection = document.getElementById('cartSection');
    const productsSection = document.getElementById('productsSection');

    const productModal = new bootstrap.Modal(document.getElementById('productModal'));
    const productModalTitle = document.getElementById('productModalTitle');
    const productModalBody = document.getElementById('productModalBody');
    const productQuantity = document.getElementById('productQuantity');
    const addToCartBtn = document.getElementById('addToCartBtn');

    let selectedProduct = null;

    function renderProducts() {
        productsContainer.innerHTML = '';
        products.forEach(product => {
            const col = document.createElement('div');
            col.className = 'col-md-4';
            col.innerHTML = `
                <div class="card product-card">
                    <img src="${product.image}" class="card-img-top" alt="${product.name}">
                    <div class="card-body">
                        <h5 class="card-title">${product.name}</h5>
                        <p class="card-text">$${product.price.toFixed(2)}</p>
                        <p>Available: ${product.stock}</p>
                        <button class="btn btn-primary view-details" data-id="${product.id}">View Details</button>
                    </div>
                </div>
            `;
            productsContainer.appendChild(col);
        });

        document.querySelectorAll('.view-details').forEach(button => {
            button.addEventListener('click', (e) => {
                const id = parseInt(e.target.getAttribute('data-id'));
                selectedProduct = products.find(p => p.id === id);
                if (selectedProduct) {
                    productModalTitle.textContent = selectedProduct.name;
                    productModalBody.innerHTML = `
                        <img src="${selectedProduct.image}" class="img-fluid mb-3" alt="${selectedProduct.name}">
                        <p><strong>Price:</strong> $${selectedProduct.price.toFixed(2)}</p>
                        <p><strong>Available Stock:</strong> ${selectedProduct.stock}</p>
                    `;
                    productQuantity.value = 1;
                    productModal.show();
                }
            });
        });
    }

    function updateCart() {
        cartItemsContainer.innerHTML = '';
        let total = 0;
        cart.forEach((item, index) => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            const div = document.createElement('div');
            div.className = 'cart-item d-flex justify-content-between align-items-center';
            div.innerHTML = `
                <div>
                    <strong>${item.name}</strong> - $${item.price.toFixed(2)} x ${item.quantity}
                </div>
                <div class="quantity-controls">
                    <button class="btn btn-sm btn-outline-secondary decrease" data-index="${index}">-</button>
                    <input type="text" value="${item.quantity}" readonly>
                    <button class="btn btn-sm btn-outline-secondary increase" data-index="${index}">+</button>
                </div>
            `;
            cartItemsContainer.appendChild(div);
        });
        cartCount.textContent = cart.reduce((sum, item) => sum + item.quantity, 0);
        cartTotal.textContent = total.toFixed(2);

        // Quantity buttons
        document.querySelectorAll('.increase').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const index = parseInt(e.target.getAttribute('data-index'));
                if (cart[index].quantity < products.find(p => p.id === cart[index].id).stock) {
                    cart[index].quantity++;
                    updateCart();
                }
            });
        });

        document.querySelectorAll('.decrease').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const index = parseInt(e.target.getAttribute('data-index'));
                if (cart[index].quantity > 1) {
                    cart[index].quantity--;
                } else {
                    cart.splice(index, 1);
                }
                updateCart();
            });
        });
    }

    addToCartBtn.addEventListener('click', () => {
        const quantity = parseInt(productQuantity.value);
        if (selectedProduct && quantity > 0) {
            const existing = cart.find(item => item.id === selectedProduct.id);
            if (existing) {
                if (existing.quantity + quantity <= selectedProduct.stock) {
                    existing.quantity += quantity;
                } else {
                    alert("Not enough stock");
                    return;
                }
            } else {
                cart.push({
                    id: selectedProduct.id,
                    name: selectedProduct.name,
                    price: selectedProduct.price,
                    quantity
                });
            }
            updateCart();
            productModal.hide();
        }
    });

    document.getElementById('viewCartBtn').addEventListener('click', () => {
        cartSection.classList.remove('d-none');
        productsSection.classList.add('d-none');
        updateCart();
    });

    document.getElementById('closeCartBtn').addEventListener('click', () => {
        cartSection.classList.add('d-none');
        productsSection.classList.remove('d-none');
    });

    renderProducts();
});
