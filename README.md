# 🛍️ ShopSphere – Django E-Commerce Platform

🚀 **ShopSphere** is a web-based e-commerce application developed using **Python, Django, MySQL, HTML, CSS, JavaScript, and Bootstrap**. It provides a user-friendly shopping experience with product browsing, cart management, and order processing.

## ✨ Features

- 🔐 **User Authentication** – User registration, login, and logout.
- 🛒 **Product Catalog** – Browse products and view product details.
- 🔎 **Product Search** – Search for products by name.
- 🗂️ **Category Filtering** – Filter products by category.
- 🛍️ **Shopping Cart** – Add products, update quantities, and remove items.
- 📦 **Checkout System** – Enter customer details and place orders.
- 📊 **Stock Management** – Validate product availability and update stock after orders.
- 🧾 **Order History** – View previously placed orders.
- 👤 **User Profile** – Update profile information.
- 🔌 **REST API Support** – Django REST Framework is included in the project.

## 🧰 Technologies Used

| Technology | Purpose |
|---|---|
| 🐍 Python | Backend programming |
| 🎯 Django | Web application framework |
| 🔌 Django REST Framework | REST API development |
| 🗄️ MySQL | Database management |
| 🌐 HTML5 | Page structure |
| 🎨 CSS3 | Styling and layout |
| 📱 Bootstrap | Responsive user interface |
| ⚡ JavaScript | Frontend interactivity |
| 🐙 Git & GitHub | Version control and project hosting |

## 📁 Project Structure

```text
ShopSphere/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── templates/
├── static/
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

📌 *The exact folder structure may vary depending on the project files.*

## ⚙️ Installation and Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/saniyachandane/ShopSphere.git
cd ShopSphere
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3️⃣ Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4️⃣ Configure the MySQL Database

🗄️ Create a MySQL database named `shopsphere`.

Configure your local database credentials in Django settings or environment variables. 🔒 **Never upload database passwords or production secret keys to GitHub.**

### 5️⃣ Apply Database Migrations

```bash
python manage.py migrate
```

### 6️⃣ Create an Admin Account

```bash
python manage.py createsuperuser
```

### 7️⃣ Start the Development Server

```bash
python manage.py runserver
```

🌐 Open your browser and visit:

👉 http://127.0.0.1:8000/

## 🎓 Learning Outcomes

Through this project, I practiced:

- 🧩 Building web applications using Django.
- 🗄️ Connecting Django applications with MySQL.
- 🔐 Implementing user authentication.
- 🛒 Managing shopping carts using sessions.
- 📦 Processing orders and validating product stock.
- 🔌 Working with Django REST Framework.
- 🎨 Creating responsive pages using HTML, CSS, and Bootstrap.
- 🐙 Managing project code with Git and GitHub.

## 🚀 Future Enhancements

- 💳 Payment gateway integration.
- ⭐ Product ratings and reviews.
- ❤️ Wishlist functionality.
- 🚚 Order tracking.
- 🧪 Automated testing.
- 📚 REST API documentation.

## 👩‍💻 Author

**Saniya Chandane**

- 🐙 GitHub: [saniyachandane](https://github.com/saniyachandane)
- 💼 LinkedIn: [saniyachandane](https://linkedin.com/in/saniyachandane)

---

⭐ **If you find this project useful, consider giving the repository a star!**

💡 *Developed as a learning project to demonstrate full-stack web development using Python and Django.*
