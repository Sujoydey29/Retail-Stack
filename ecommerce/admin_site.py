# ecommerce/store/admin_site.py

import json
from datetime import timedelta

from django.utils import timezone
from django.contrib.admin import AdminSite
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Sum, F
from django.db.models.functions import TruncDay

from store.models import Order, OrderItem, Profile


class RetailAdminSite(AdminSite):
    site_header    = "Retail Stack Admin"
    site_title     = "Retail Dashboard"
    index_title    = "Key Performance Indicators"
    index_template = "admin/dashboard.html"

    def index(self, request, extra_context=None):
        now = timezone.now()

        # ── Row 1: KPIs ──
        total_orders    = Order.objects.count()
        total_revenue   = (
            OrderItem.objects
                     .aggregate(total=Sum(F("price") * F("quantity")))
                     .get("total") or 0
        )
        total_cost      = (
            OrderItem.objects
                     .aggregate(total=Sum(F("product__original_price") * F("quantity")))
                     .get("total") or 0
        )
        total_profit    = total_revenue - total_cost
        total_customers = Profile.objects.count()
        avg_order_value = (total_revenue / total_orders) if total_orders else 0

        # ── Row 2: period revenues ──
        start_day   = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_month = start_day.replace(day=1)
        start_year  = start_day.replace(month=1, day=1)

        daily_rev   = (
            Order.objects.filter(created_at__gte=start_day)
                 .aggregate(sum=Sum("total_price"))["sum"]
            or 0
        )
        monthly_rev = (
            Order.objects.filter(created_at__gte=start_month)
                 .aggregate(sum=Sum("total_price"))["sum"]
            or 0
        )
        annual_rev  = (
            Order.objects.filter(created_at__gte=start_year)
                 .aggregate(sum=Sum("total_price"))["sum"]
            or 0
        )

        max_rev     = max(daily_rev, monthly_rev, annual_rev, 1)
        daily_pct   = daily_rev   / max_rev * 100
        monthly_pct = monthly_rev / max_rev * 100
        annual_pct  = annual_rev  / max_rev * 100

        # ── 7-day trend (optional) ──
        week_ago    = now - timedelta(days=7)
        daily_qs    = (
            Order.objects.filter(created_at__gte=week_ago)
                         .annotate(day=TruncDay("created_at"))
                         .values("day")
                         .annotate(count=Count("id"))
                         .order_by("day")
        )
        chart_labels = [r["day"].strftime("%Y-%m-%d") for r in daily_qs]
        chart_data   = [r["count"] for r in daily_qs]

        # ── Doughnut: orders by status ──
        status_qs     = Order.objects.values("status").annotate(count=Count("id"))
        status_labels = [r["status"] for r in status_qs]
        status_data   = [r["count"]  for r in status_qs]

        # ── GeoChart: bucket orders by country (continent → state fallback) ──
        raw = Order.objects.values("country", "state").annotate(count=Count("id"))
        country_counts = {}
        for rec in raw:
            # Normalize incoming country/state to Title Case
            c = (rec["country"] or "").strip().title()

            # if they typed a continent (or left blank), fallback to state
            if c.lower() in [
                "north america", "south america",
                "europe", "asia", "africa", "australia"
            ] or not c:
                c = (rec["state"] or "").strip().title()

            # unify US variants
            if c.upper() in ("US", "USA", "UNITED STATES OF AMERICA"):
                c = "United States"
            if not c:
                c = "Unknown"

            country_counts[c] = country_counts.get(c, 0) + rec["count"]

        country_data = [
            [country, count]
            for country, count in country_counts.items()
        ]

        # ── Modal details: list every order per normalized country ──
        raw_orders = Order.objects.values(
            "country", "state", "city", "total_price", "created_at"
        )
        country_orders = {}
        for o in raw_orders:
            # same normalization logic as above
            c = (o["country"] or "").strip().title()
            if c.lower() == "north america":
                c = (o["state"] or "").strip().title()
            if c.upper() in ("US", "USA", "UNITED STATES OF AMERICA"):
                c = "United States"
            if not c:
                c = "Unknown"

            country_orders.setdefault(c, []).append({
                "city":      o["city"] or "",
                "state":     o["state"] or "",
                "amount":    o["total_price"],
                "timestamp": o["created_at"].strftime("%Y-%m-%d %H:%M"),
            })

        # ── Row 3: mini-stats ──
        payments_count  = Order.objects.exclude(payment_id__isnull=True).count()
        payments_amount = Order.objects.aggregate(sum=Sum("total_price"))["sum"] or 0
        avg_payment     = (payments_amount / payments_count) if payments_count else 0
        refund_count    = 0
        refund_amount   = 0
        avg_refund      = 0

        ctx = {
            # KPIs
            "total_orders":      total_orders,
            "total_revenue":     total_revenue,
            "total_profit":      total_profit,
            "total_customers":   total_customers,
            "avg_order_value":   avg_order_value,

            # period bars
            "daily_rev":         daily_rev,
            "monthly_rev":       monthly_rev,
            "annual_rev":        annual_rev,
            "daily_pct":         daily_pct,
            "monthly_pct":       monthly_pct,
            "annual_pct":        annual_pct,

            # optional 7-day trend
            "chart_labels":      chart_labels,
            "chart_data":        chart_data,

            # doughnut chart
            "status_labels":     status_labels,
            "status_data":       status_data,

            # geo chart
            "country_data":      country_data,
            "country_orders_json": json.dumps(country_orders, cls=DjangoJSONEncoder),

            # mini-stats
            "payments_count":    payments_count,
            "payments_amount":   payments_amount,
            "avg_payment":       avg_payment,
            "refund_count":      refund_count,
            "refund_amount":     refund_amount,
            "avg_refund":        avg_refund,
        }

        extra = extra_context or {}
        extra.update(ctx)
        return super().index(request, extra_context=extra)
