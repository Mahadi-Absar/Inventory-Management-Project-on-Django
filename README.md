# T-Shirt Inventory & Order Management System

A Django REST Framework backend for managing a T-shirt company's product
catalog, stock (per size/color), suppliers, customers, and orders.

## Problem Statement

Small apparel businesses need a way to track products across multiple
sizes and colors, know which supplier stocked which item, and manage
customer orders without overselling out-of-stock variants. This project
provides a complete REST API backend for exactly that.

## Features

- Product catalog organized by **Category**, sourced from **Suppliers**,
  labelled with **Tags** (many-to-many).
- Per-size/per-color stock tracking via **ProductVariant**.
- **Customer** profiles that extend Django's built-in `User` (one-to-one).
- **Order** and **OrderItem** management with automatic subtotal/total
  calculation and stock validation (can't order more than what's in stock).
- Full CRUD REST APIs for every model (ModelViewSet + DRF Router).
- Filtering, searching, and ordering on all list endpoints.
- Page-number pagination on all list endpoints.
- Django Admin fully customized (list_display, search_fields, list_filter,
  filter_horizontal for tags, inline variants/order items).
- Model-level and serializer-level validation with clear error messages.

## Technologies Used

- Python 3.12, Django 6.0
- Django REST Framework
- django-filter
- SQLite (default; PostgreSQL-ready)

## Project Structure

```
tshirt_inventory/
├── manage.py
├── requirements.txt
├── tshirt_inventory/       # project settings, root urls
├── inventory/              # Category, Supplier, Tag, Product, ProductVariant
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── filters.py
│   ├── admin.py
│   └── urls.py
└── orders/                 # Customer, Order, OrderItem
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── admin.py
    └── urls.py
```

## Data Model / Relationships

- `Product` → `Category` (ForeignKey)
- `Product` → `Supplier` (ForeignKey)
- `Product` ↔ `Tag` (ManyToMany)
- `ProductVariant` → `Product` (ForeignKey), unique on (product, size, color)
- `Customer` → `User` (OneToOne)
- `Order` → `Customer` (ForeignKey)
- `OrderItem` → `Order` (ForeignKey), `OrderItem` → `ProductVariant` (ForeignKey)

## Installation

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
```

## Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

## Create an Admin User

```bash
python manage.py createsuperuser
```

## Running the Project

```bash
python manage.py runserver
```

- API root: http://127.0.0.1:8000/api/
- Admin panel: http://127.0.0.1:8000/admin/
- Browsable API login: http://127.0.0.1:8000/api-auth/login/

## API Endpoint List

| Resource        | Endpoint                     |
|------------------|------------------------------|
| Categories       | `/api/categories/`           |
| Suppliers        | `/api/suppliers/`            |
| Tags             | `/api/tags/`                 |
| Products         | `/api/products/`             |
| Product Variants | `/api/variants/`             |
| Customers        | `/api/customers/`            |
| Orders           | `/api/orders/`               |
| Order Items      | `/api/order-items/`          |

All support: `GET` (list/retrieve), `POST` (create), `PUT`/`PATCH` (update),
`DELETE` (destroy).

### Filtering, Searching, Ordering examples

```
GET /api/products/?category=1
GET /api/products/?min_price=300&max_price=1000
GET /api/products/?search=Crew
GET /api/products/?ordering=-price
GET /api/orders/?status=PENDING
```

### Pagination

All list responses look like:

```json
{
  "count": 12,
  "next": "http://127.0.0.1:8000/api/products/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

## Sample API Requests and Responses

**Create a product**

```
POST /api/products/
{
  "name": "Classic Crew Tee",
  "sku": "tsh-001",
  "category": 1,
  "supplier": 1,
  "price": "599.00",
  "description": "100% cotton crew neck",
  "tags": [1]
}
```

Response `201 Created`:

```json
{
  "id": 1, "name": "Classic Crew Tee", "sku": "TSH-001",
  "category": 1, "category_name": "Round Neck", "supplier": 1,
  "price": "599.00", "description": "100% cotton crew neck",
  "tags": [1], "is_active": true,
  "created_at": "2026-07-18T05:19:17Z", "variants": []
}
```

**Validation error example**

```
POST /api/products/  { "price": "-10", ... }
```

```json
{ "price": ["Price must be greater than 0."] }
```

**Order with nested items**

```
GET /api/orders/1/
```

```json
{
  "id": 1, "customer": 1, "customer_name": "admin",
  "status": "PENDING", "shipping_address": "House 12, Road 4, Chattogram",
  "items": [
    {
      "id": 1, "product_variant": 1,
      "product_variant_detail": {"id": 1, "product": 1, "size": "M", "color": "Black", "stock_quantity": 50},
      "quantity": 2, "unit_price": "599.00", "subtotal": "1198.00"
    }
  ],
  "total_amount": "1198.00"
}
```

## API Testing

All endpoints were manually verified with `curl` (CRUD, validation errors,
filtering, searching, ordering, pagination). You can also test with the
DRF Browsable API (just open any endpoint URL in a browser while logged
in at `/api-auth/login/`) or import the endpoints into Postman.
