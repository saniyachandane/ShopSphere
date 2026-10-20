# ShopSphere — Django + Django REST Framework

A responsive demo shopping website with product search, category filters, product details, session cart, quantity updates, checkout, customer registration/login, profile, order history, admin management, and REST API endpoints.

## 1. Setup (Windows PowerShell)

```powershell
cd ShopSphere
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Admin is at `http://127.0.0.1:8000/admin/`.
The project uses SQLite by default, so it starts without MySQL configuration. Add categories and products in Django Admin before shopping.

## 2. Optional MySQL setup

1. Create a database named `shopsphere_db` in MySQL.
2. Copy `.env.example` values into your terminal environment or configure equivalent environment variables.
3. Set `DB_ENGINE=mysql`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT`.
4. Install a MySQL driver compatible with your environment (`pip install mysqlclient`) and run `python manage.py migrate`.

Do not commit passwords or production secret keys. The default secret key and `DEBUG=True` are for local development only.

## 3. REST API (DRF)

| Method | Endpoint | Purpose | Access |
|---|---|---|---|
| GET | `/api/` | Router index | Public |
| GET | `/api/categories/` | List categories | Public |
| GET | `/api/categories/1/` | Category detail | Public |
| GET | `/api/products/` | Paginated product list | Public |
| GET | `/api/products/1/` | Product detail | Public |
| POST / PUT / PATCH / DELETE | `/api/products/1/` | Manage products | Staff/admin only |
| GET | `/api/orders/` | Current user's orders | Login required; staff can see all |
| GET | `/api/orders/1/` | Order detail | Login required and scoped to owner (staff can see all) |
| GET | `/api-auth/login/` | DRF browsable API login | Django session auth |

Example product search: `/api/products/?search=shirt`
Example ordering: `/api/products/?ordering=price` or `?ordering=-created_at`
Pagination uses page numbers, e.g. `/api/products/?page=2`.

Product writes require a staff account. Order endpoints are read-only so customers cannot spoof totals, prices, or order ownership through the API. Checkout creates orders through the validated website flow.

## 4. Main project structure

- `config/`: settings and URL routing
- `store/models.py`: Category, Product, Order, OrderItem
- `store/views.py`: website views and cart/checkout logic
- `store/serializers.py`: DRF serializers
- `store/api.py`: DRF viewsets and permissions
- `store/templates/`: responsive Bootstrap templates
- `static/css/style.css`: custom responsive styling
- `static/js/app.js`: small UI interactions

## 5. Notes

- This is a learning/demo project. Checkout does not process real payments.
- Use Django Admin to manage catalog records.
- For deployment, configure a strong `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS`, HTTPS, and a production database.
