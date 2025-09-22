from django.contrib import admin

# Register your models here.
# products/admin.py
from django.contrib import admin
from .models import TrendingProduct

@admin.register(TrendingProduct)
class TrendingProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "marketplace",
        "category",
        "current_price",
        "previous_price",
        "price_drop",
        "updated_at",
    )
    search_fields = ("title", "category", "marketplace")
    list_filter = ("marketplace", "category")
    ordering = ("-updated_at",)
