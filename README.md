Retail Stack E-Commerce Dashboard

A dynamic Django retail engine powered by MySQL/PostgreSQL, seamless CSV ingestion, and an interactive admin dashboard.

✨ What’s Inside

Experience a turnkey solution that:

Unifies data pipelines: One import_csv command ingests all your CSVs—categories, products, realistic 50 000 orders, 150 000 order items, and 4 000 user profiles—directly into the database.

Leverages relational power: Configurable for PostgreSQL or MySQL, optimized with bulk operations for blazing imports.

Delivers instant insights: Full CRUD & rich visualizations (charts, maps) in Django Admin.

Empowers manual tweaks: Modify any record—product prices, stock levels, order statuses, user addresses—right from the dashboard.

🚀 Quickstart

Clone & enter your project:

git clone <repo-url> && cd ecommerce

Set up a Python environment:

python -m venv venv
source venv/bin/activate    # Windows: venv\\Scripts\\activate

Install dependencies:

pip install -r requirements.txt

Configure DB in ecomm/settings.py:

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

Load everything:

python manage.py makemigrations
python manage.py migrate
python manage.py import_csv

Run the server & explore:

python manage.py runserver

Visit http://localhost:8000/admin/ with your superuser to dive into data.

🔧 Under the Hood

CSV to DB: Bulk create with minimal transaction overhead.

Auth Users: Auto-generates dummy users for your profiles.

Models:

Category: Slug, name, image, SEO

Product: Stock, prices, tags, rich metadata

Order & OrderItem: Full transaction lifecycle

Profile: Contact & location details

Admin Dashboard:

Order status donut charts

Customer location map

Revenue & profit summaries

🌈 Future Vision

Full e-commerce UX: Integrate a modern SPA frontend (React/Vue).

Real-time analytics: Live dashboards with WebSocket or streaming.

Role-based access: Granular permissions & multi-tenant support.

Public API: REST/GraphQL for mobile or partner apps.

🔮 Future Scope & Dashboard Integration

Automated Notifications: Dynamic order and email alert modules directly in the Admin dashboard.

Advanced BI Dashboards: Real‑time sales charts, conversion funnels, and geo‑performance heatmaps.

Payment & Shipping Insights: Stripe/PayPal statistics and shipment tracking statuses in dedicated panels.

Headless API Layer: REST/GraphQL endpoints powering future storefronts and mobile apps.

These enhancements will plug right into the Retail Stack backend dashboard, unifying operations, analytics, and customer interactions under one roof.

🏃 Running the Project

# Import all CSV data
env/bin/python manage.py import_csv

# Start the development server
env/bin/python manage.py runserver

Retail Stack merges database mastery with seamless backend workflows—your foundation for any scalable e-commerce endeavor.


