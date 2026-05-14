# K2 ERP Orders

Модуль обліку замовлень для бізнес-системи K2 ERP.
Реалізований на Flask + SQLAlchemy + PostgreSQL + Docker.

## Стек

- Python 3.11
- Flask
- SQLAlchemy
- PostgreSQL
- Docker + Docker Compose
- pytest

## Структура проєкту

k2-erp-orders/
├── app/
│   ├── __init__.py      # Ініціалізація Flask та БД
│   ├── models.py        # Моделі: Client, Product, Order, OrderItem
│   └── routes.py        # API ендпоінти
├── tests/
│   └── test_api.py      # Тести
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py
└── README.md

## Запуск через Docker

1. Клонуй репозиторій:
git clone https://github.com/michxdr/k2-erp-orders.git
cd k2-erp-orders

2. Запусти контейнери:
docker-compose up --build

3. Додаток доступний на: http://localhost:5000

## Запуск локально

1. Створи віртуальне середовище:
python -m venv .venv
.venv\Scripts\activate

2. Встанови залежності:
pip install -r requirements.txt

3. Запусти PostgreSQL та створи базу k2_orders

4. Запусти додаток:
python run.py

## API ендпоінти

### Клієнти

POST /clients — створити клієнта
{
    "name": "Іван Петренко",
    "email": "ivan@gmail.com"
}

### Товари

POST /products — створити товар
{
    "name": "Ноутбук",
    "price": 25000.0
}

### Замовлення

POST /orders — створити замовлення
{
    "client_id": 1,
    "items": [
        {"product_id": 1, "quantity": 2}
    ]
}

GET /clients/<id>/orders — отримати замовлення клієнта

## Запуск тестів

pip install pytest
pytest tests/

## Чому такий підхід

- Flask — легкий фреймворк, ідеальний для REST API
- SQLAlchemy — зручна ORM, дозволяє працювати з БД через Python об'єкти
- PostgreSQL — надійна реляційна БД для бізнес-даних
- Docker — однаковий запуск на будь-якому середовищі
- Структура проєкту розрахована на масштабування — легко додавати нові модулі