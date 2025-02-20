from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Регистрация модели товара в админке"""

    list_display = ("id", "name", "model")
    search_fields = ("name", "model")
    list_filter = ("supplier",)
