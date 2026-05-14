from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models import Client, Product, Order, OrderItem

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

# ===== CLIENTS =====

@bp.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json()

    if not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Імʼя та email обовʼязкові'}), 400

    if Client.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Клієнт з таким email вже існує'}), 400

    client = Client(name=data['name'], email=data['email'])
    db.session.add(client)
    db.session.commit()

    return jsonify(client.to_dict()), 201


# ===== PRODUCTS =====

@bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()

    if not data.get('name') or data.get('price') is None:
        return jsonify({'error': 'Назва та ціна обовʼязкові'}), 400

    if data['price'] <= 0:
        return jsonify({'error': 'Ціна має бути більше 0'}), 400

    product = Product(name=data['name'], price=data['price'])
    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201


# ===== ORDERS =====

@bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()

    # Перевірка клієнта
    client = Client.query.get(data.get('client_id'))
    if not client:
        return jsonify({'error': 'Клієнта не знайдено'}), 404

    # Перевірка товарів
    items = data.get('items', [])
    if not items:
        return jsonify({'error': 'Замовлення має містити хоча б один товар'}), 400

    # Створення замовлення
    order = Order(client_id=client.id)
    db.session.add(order)
    db.session.flush()

    # Додавання товарів
    for item in items:
        product = Product.query.get(item.get('product_id'))
        if not product:
            return jsonify({'error': f'Товар {item.get("product_id")} не знайдено'}), 404

        quantity = item.get('quantity', 1)
        if quantity <= 0:
            return jsonify({'error': 'Кількість має бути більше 0'}), 400

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=quantity
        )
        db.session.add(order_item)

    db.session.flush()
    order.calculate_total()
    db.session.commit()

    return jsonify(order.to_dict()), 201


@bp.route('/clients/<int:client_id>/orders', methods=['GET'])
def get_client_orders(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Клієнта не знайдено'}), 404

    orders = Order.query.filter_by(client_id=client_id).all()

    return jsonify({
        'client': client.to_dict(),
        'orders': [order.to_dict() for order in orders]
    }), 200