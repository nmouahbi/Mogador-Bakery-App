from flask import Blueprint, request, jsonify
from .models import db, Product
from flask import render_template


bp = Blueprint('main', __name__)
@bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.menu'))
    return render_template('index.html')

@bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    result = [{
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "price": p.price,
        "quantity": p.quantity,
        "category": p.category
    } for p in products]
    return jsonify(result)

@bp.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        quantity=data['quantity'],
        category=data.get('category', 'General')
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully!"}), 201

@bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.quantity = data.get('quantity', product.quantity)
    product.category = data.get('category', product.category)
    db.session.commit()
    return jsonify({"message": "Product updated successfully!"})

@bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully!"})