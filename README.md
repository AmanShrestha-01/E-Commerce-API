# E-Commerce REST API

A backend API for an online store with user authentication, product management, shopping cart, order processing, and Stripe payment integration.

## Tech Stack

- Python, Flask
- SQLAlchemy, SQLite
- JWT Authentication, Bcrypt
- Stripe Payments
- Swagger API Documentation

## Features

- User signup and login with hashed passwords
- JWT token-based authentication
- Product CRUD with categories
- Shopping cart (add, view, remove items)
- Order checkout with stock management
- Stripe payment intent integration
- Auto-generated API docs at /apidocs
- Automated test suite

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | /signup | Create account |
| POST | /login | Log in, get token |
| GET | /products | List all products |
| POST | /products | Create product |
| GET | /cart | View your cart |
| POST | /cart | Add to cart |
| DELETE | /cart/:id | Remove from cart |
| POST | /orders | Place order (Stripe) |
| GET | /orders | View order history |

## Run Locally
```bash
git clone https://github.com/AmanShrestha-01/E-Commerce-API.git
cd E-Commerce-API
pip install -r requirements.txt
python app.py
```

Visit API docs: http://127.0.0.1:8000/apidocs

## Run Tests
```bash
python test_app.py
```
