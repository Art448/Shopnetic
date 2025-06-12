from flask import Flask, request, jsonify, render_template
from typing import Dict, Union, Optional

app = Flask(__name__, static_folder='static', template_folder='templates')

products = [
    {
        "product_id": "1",
        "name": "Physical Book",
        "type": "physical",
        "price": 9.99,
        "weight": 0.5,
        "quantity_available": 10
    },
    {
        "product_id": "2",
        "name": "E-book",
        "type": "digital",
        "price": 4.99,
        "download_link": "https://example.com/ebook-download",
        "quantity_available": 100
    }
]


# Product Classes (unchanged from your implementation)
class Product:
    def __init__(self, product_id: str, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price
    
    def to_dict(self) -> Dict:
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price
        }

class PhysicalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, weight: float):
        super().__init__(product_id, name, price)
        self.weight = weight
    
    def to_dict(self) -> dict:
        result = super().to_dict()
        result['weight'] = self.weight
        return result

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, download_size: float):
        super().__init__(product_id, name, price)
        self.download_size = download_size
    
    def to_dict(self) -> dict:
        result = super().to_dict()
        result['download_size'] = self.download_size
        return result

class CartItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
    
    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity
    
    def to_dict(self) -> Dict[str, Union[Dict, int]]:
        return {
            'product': self.product.to_dict(),
            'quantity': self.quantity,
            'subtotal': self.calculate_subtotal()
        }

class ShoppingCart:
    def __init__(self):
        self._items: Dict[str, CartItem] = {}
        self._product_catalog: Dict[str, Product] = {
            'prod1': PhysicalProduct('prod1', 'T-Shirt', 19.99, 0.5),
            'prod2': DigitalProduct('prod2', 'E-Book', 9.99, 2.5)
        }
    
    def get_items(self):
        return [item.to_dict() for item in self._items.values()]
    
    def add_item(self, product_id: str, quantity: int = 1):
        if product_id in self._product_catalog:
            if product_id in self._items:
                self._items[product_id].quantity += quantity
            else:
                self._items[product_id] = CartItem(self._product_catalog[product_id], quantity)
            return True
        return False

# Initialize the shopping cart
cart = ShoppingCart()


@app.route('/cart/items', methods=['GET'])
def get_cart_items():
    return jsonify(cart.get_items())

@app.route('/cart/add/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = request.json.get('quantity', 1)
    if cart.add_item(product_id, quantity):
        return jsonify({"status": "success", "message": "Item added to cart"})
    return jsonify({"status": "error", "message": "Product not found"}), 404

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/products')
def get_products():
    return jsonify([
        {"name": "Laptop", "price": 999.99, "image": "https://via.placeholder.com/200"},
        {"name": "Phone", "price": 499.99, "image": "https://via.placeholder.com/200"},
        {"name": "Headphones", "price": 199.99, "image": "https://via.placeholder.com/200"}
            
        
    ])

@app.route('/api/cart')
def get_cart():
    items = [item.to_dict() for item in cart.get_items()]
    total = 0.0
    for pid, quantity in cart.items():
        product = next((p for p in products if p['product_id'] == pid), None)
        if product:
            subtotal = product['price'] * quantity
            total += subtotal
            items.append({
                'product_details': product,
                'quantity': quantity,
                'subtotal': subtotal
            })

    return jsonify({'items': items, 'total': total})

@app.route('/api/cart/add', methods=['POST'])
def add_items_to_cart():
    data = request.get_json()
    pid = data.get('product_id')
    qty = int(data.get('quantity', 1))
    product = next((p for p in products if p['product_id'] == pid), None)

    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404

    available = product['quantity_available']
    existing_qty = cart.get(pid, 0)
    if qty + existing_qty > available:
        return jsonify({'success': False, 'message': 'Not enough stock'}), 400

    cart[pid] = existing_qty + qty
    return jsonify({'success': True})

# API: Update cart
@app.route('/api/cart/update', methods=['PUT'])
def update_cart():
    data = request.get_json()
    pid = data.get('product_id')
    qty = int(data.get('quantity'))
    product = next((p for p in products if p['product_id'] == pid), None)

    if not product:
        return jsonify({'success': False}), 404

    if qty > product['quantity_available'] + cart.get(pid, 0):
        return jsonify({'success': False, 'message': 'Exceeds stock'}), 400

    cart[pid] = qty
    return jsonify({'success': True})

# API: Remove from cart
@app.route('/api/cart/remove', methods=['DELETE'])
def remove_from_cart():
    pid = request.args.get('product_id')
    if pid in cart:
        del cart[pid]
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)