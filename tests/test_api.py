import pytest
from app import create_app, db


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# ===== CLIENTS =====

def test_create_client(client):
    response = client.post('/clients', json={
        'name': 'Іван Петренко',
        'email': 'ivan@gmail.com'
    })
    assert response.status_code == 201
    assert response.get_json()['name'] == 'Іван Петренко'


def test_create_client_without_email(client):
    response = client.post('/clients', json={
        'name': 'Іван Петренко'
    })
    assert response.status_code == 400


# ===== PRODUCTS =====

def test_create_product(client):
    response = client.post('/products', json={
        'name': 'Ноутбук',
        'price': 25000.0
    })
    assert response.status_code == 201
    assert response.get_json()['price'] == 25000.0


def test_create_product_negative_price(client):
    response = client.post('/products', json={
        'name': 'Ноутбук',
        'price': -100
    })
    assert response.status_code == 400


# ===== ORDERS =====

def test_create_order(client):
    # Створюємо клієнта
    client.post('/clients', json={
        'name': 'Іван Петренко',
        'email': 'ivan@gmail.com'
    })

    # Створюємо товар
    client.post('/products', json={
        'name': 'Ноутбук',
        'price': 25000.0
    })

    # Створюємо замовлення
    response = client.post('/orders', json={
        'client_id': 1,
        'items': [{'product_id': 1, 'quantity': 2}]
    })
    assert response.status_code == 201
    assert response.get_json()['total'] == 50000.0


def test_create_order_without_client(client):
    response = client.post('/orders', json={
        'client_id': 999,
        'items': [{'product_id': 1, 'quantity': 1}]
    })
    assert response.status_code == 404


def test_create_order_without_items(client):
    client.post('/clients', json={
        'name': 'Іван Петренко',
        'email': 'ivan@gmail.com'
    })
    response = client.post('/orders', json={
        'client_id': 1,
        'items': []
    })
    assert response.status_code == 400


def test_get_client_orders(client):
    client.post('/clients', json={
        'name': 'Іван Петренко',
        'email': 'ivan@gmail.com'
    })
    client.post('/products', json={
        'name': 'Ноутбук',
        'price': 25000.0
    })
    client.post('/orders', json={
        'client_id': 1,
        'items': [{'product_id': 1, 'quantity': 1}]
    })

    response = client.get('/clients/1/orders')
    assert response.status_code == 200
    assert len(response.get_json()['orders']) == 1