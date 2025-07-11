import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model
from store.models import Category, Product, Order, OrderItem, Profile

User = get_user_model()

class Command(BaseCommand):
    help = 'Import CSVs into Postgres, including dummy Users for Profiles'

    def handle(self, *args, **options):
        base = 'data/csv/'  # adjust if your folder differs

        with transaction.atomic():
            # 0️⃣ Create dummy Users for each Profile
            with open(base + 'profiles.csv', newline='') as f:
                reader = csv.DictReader(f)
                user_ids = {int(row['user_id']) for row in reader}

            users_to_create = []
            for uid in user_ids:
                if not User.objects.filter(pk=uid).exists():
                    u = User(pk=uid,
                             username=f'user{uid}',
                             email=f'user{uid}@example.com')
                    u.set_unusable_password()
                    users_to_create.append(u)
            User.objects.bulk_create(users_to_create)

            # 1️⃣ Categories
            Category.objects.all().delete()
            with open(base + 'categories.csv', newline='') as f:
                reader = csv.DictReader(f)
                objs = [Category(
                    id=row['id'], slug=row['slug'], name=row['name'],
                    image=row['image'], description=row['description'],
                    status=row['status'], trending=row['trending'],
                    meta_title=row['meta_title'],
                    meta_keywords=row['meta_keywords'],
                    meta_description=row['meta_description'],
                ) for row in reader]
                Category.objects.bulk_create(objs, batch_size=500)

            # 2️⃣ Products
            Product.objects.all().delete()
            with open(base + 'products.csv', newline='') as f:
                reader = csv.DictReader(f)
                objs = [Product(
                    id=row['id'],
                    category_id=row['category_id'],
                    slug=row['slug'],
                    name=row['name'],
                    product_image=row['image'],    # match your model field
                    small_description=row['small_description'],
                    quantity=row['quantity'],
                    description=row['description'],
                    original_price=row['original_price'],
                    selling_price=row['selling_price'],
                    status=row['status'],
                    trending=row['trending'],
                    tag=row['tag'],
                    meta_title=row['meta_title'],
                    meta_keywords=row['meta_keywords'],
                    meta_description=row['meta_description'],
                ) for row in reader]
                Product.objects.bulk_create(objs, batch_size=500)

            # 3️⃣ Orders
            Order.objects.all().delete()
            with open(base + 'orders.csv', newline='') as f:
                reader = csv.DictReader(f)
                objs = [Order(
                    id=row['id'],
                    user_id=row['user_id'],
                    fname=row['fname'],
                    lname=row['lname'],
                    email=row['email'],
                    phone=row['phone'],
                    address=row['address'],
                    city=row['city'],
                    state=row['state'],
                    country=row['country'],
                    pincode=row['pincode'],
                    total_price=row['total_price'],
                    payment_mode=row['payment_mode'],
                    payment_id=row['payment_id'],
                    status=row['status'],
                    message=row['message'],
                    tracking_no=row['tracking_no'],
                ) for row in reader]
                Order.objects.bulk_create(objs, batch_size=500)

            # 4️⃣ OrderItems
            OrderItem.objects.all().delete()
            with open(base + 'order_items.csv', newline='') as f:
                reader = csv.DictReader(f)
                objs = [OrderItem(
                    order_id=row['order_id'],
                    product_id=row['product_id'],
                    price=row['price'],
                    quantity=row['quantity'],
                ) for row in reader]
                OrderItem.objects.bulk_create(objs, batch_size=500)

            # 5️⃣ Profiles
            Profile.objects.all().delete()
            with open(base + 'profiles.csv', newline='') as f:
                reader = csv.DictReader(f)
                prof_objs = [Profile(
                    user_id=row['user_id'],
                    phone=row['phone'],
                    address=row['address'],
                    city=row['city'],
                    state=row['state'],
                    country=row['country'],
                    pincode=row['pincode'],
                ) for row in reader]
                Profile.objects.bulk_create(prof_objs, batch_size=500)

        self.stdout.write(self.style.SUCCESS('✅ All CSVs and Profiles imported!'))
