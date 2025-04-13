from flask import flash,Blueprint, request, jsonify, render_template, redirect, url_for
from .models import db, Product
from flask_login import current_user, login_required

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

@bp.route('/menu')
@login_required
def menu():
    products = Product.query.all()
    return render_template('menu.html', products=products)



@bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        # Update product with form data (adjust field names as needed)
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price', product.price))
        product.quantity = int(request.form.get('quantity', product.quantity))
        product.category = request.form.get('category')
        db.session.commit()
        flash('Product updated successfully!')
        return redirect(url_for('main.menu'))
    return render_template('edit_product.html', product=product)

@bp.route('/products/<int:id>/delete', methods=['POST'])
@login_required
def delete_product_form(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!')
    return redirect(url_for('main.menu'))

@bp.route('/products/new', methods=['GET', 'POST'])
@login_required
def new_product():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        description = request.form.get('description')
        try:
            price = float(request.form.get('price'))
        except (TypeError, ValueError):
            price = 0.0
        try:
            quantity = int(request.form.get('quantity', 0))
        except (TypeError, ValueError):
            quantity = 0
        category = request.form.get('category', 'General')
        
        # Create a new Product instance
        new_prod = Product(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category=category
        )
        db.session.add(new_prod)
        db.session.commit()
        flash("New product added successfully!")
        return redirect(url_for('main.menu'))
    
    # For GET request, render the new product form
    return render_template('new_product.html')


@bp.route('/category/<string:category>')
def category(category):
    # Use ilike for case-insensitive matching
    products = Product.query.filter(Product.category.ilike(category)).all()
    return render_template('category.html', category=category, products=products)

