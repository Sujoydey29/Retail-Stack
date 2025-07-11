
# 🛒 Retail Stack E-Commerce Dashboard

### A dynamic Django retail engine powered by MySQL/PostgreSQL, seamless CSV ingestion, and an interactive admin dashboard.

---

## ✨ What’s Inside

Experience a turnkey solution that:

- 🔄 **Unifies data pipelines**: One `import_csv` command ingests **all** your CSVs—categories, products, realistic 50,000 orders, 150,000 order items, and 4,000 user profiles—directly into the database.
- 🧠 **Leverages relational power**: Configurable for **PostgreSQL** or **MySQL**, optimized with bulk operations for blazing imports.
- 📊 **Delivers instant insights**: Full CRUD & rich visualizations (charts, maps) in Django Admin.
- ✍️ **Empowers manual tweaks**: Modify product prices, stock levels, order statuses, user addresses—all from the dashboard.

---

## 🛠️ Tech Stack

- **Backend:** Django 4.x
- **Database:** PostgreSQL / MySQL (switchable in `settings.py`)
- **Frontend (Admin):** Django Admin with customization
- **Data Ingestion:** CSV Bulk Loader via `import_csv`
- **Visualization:** Admin UI dashboard with filters & search

---

## 📂 CSV Dataset Structure

All data lives in the `data/cvs/` folder:

| File               | Rows      | Description                              |
|--------------------|-----------|------------------------------------------|
| `categories.csv`   | ~10       | Category metadata & images               |
| `products.csv`     | 1,000     | Product details, stock, pricing, SEO     |
| `orders_fixed.csv` | 50,000    | Realistic orders with real-world places  |
| `order_items.csv`  | ~150,000  | Line-items per order                     |
| `profiles.csv`     | 4,000     | User profiles (address, phone, location) |

---

## ⚡ Quickstart

### 1. Clone & Setup
```bash
git clone <your-repo-url>
cd ecommerce
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Database
Edit `ecomm/settings.py`:
```python
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',  # or 'django.db.backends.mysql'
    'NAME': 'ecommdb',
    'USER': 'your_user',
    'PASSWORD': 'your_password',
    'HOST': 'localhost',
    'PORT': '5432',  # MySQL default: 3306
  }
}
```

### 3. Load Everything
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py import_csv
```

### 4. Start the Server
```bash
python manage.py runserver
```

Now visit 👉 `http://localhost:8000/admin/` and log in with your Django superuser.

---

## 📈 Admin Dashboard Features

- 🔍 **View & search** products, categories, orders, customers
- 📤 **Edit** product prices, stock, and descriptions manually
- 📦 **Update** order statuses (Pending, Completed, Shipping)
- 🧾 **User Profiles** with city, country, phone, and addresses

---

## 🔮 Future Scope & Dashboard Integration

Your project lays the **foundation** for a full-scale, modular e-commerce platform with database-first logic.

Here’s where we can go next:

- 📩 **Automated Notifications**: Push alerts when order status updates
- 📈 **Real-time Analytics**: Dashboards powered by WebSockets or Kafka
- 🌍 **Geo & Payment Insights**: Visualize top cities, payment trends
- 🔐 **Role-based Admin**: Staff vs superuser panels
- 💳 **Integrated Checkout**: Stripe/PayPal flow with live tracking
- 🌐 **Public API**: REST or GraphQL for external access

These enhancements will plug right into the Retail Stack backend dashboard, unifying operations, analytics, and customer interactions under one roof.

---

## 🧪 Sample Run Commands

```bash
# Step 1: Import data
python manage.py import_csv

# Step 2: Run the dev server
python manage.py runserver
```

---

## 🏁 Final Thoughts

> This Retail Stack project isn’t just a demo — it’s a scalable foundation. From database structure to user experience, it sets the groundwork for a full-fledged production-grade e-commerce engine. Whether you scale it into a microservices backend, plug in a mobile app, or turn it into a B2C portal, the architecture is ready.
