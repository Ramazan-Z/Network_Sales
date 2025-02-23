from django.db import models

from network.models import NetworkElement


class Product(models.Model):
    """Модель сущности товара"""

    name: models.Field = models.CharField(
        max_length=150,
        verbose_name="Name",
        help_text="Название товара.",
    )
    model: models.Field = models.CharField(
        unique=True,
        max_length=200,
        verbose_name="Model",
        help_text="Модель или артикул товара.",
    )
    release_date: models.Field = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Release date",
        help_text="Дата выхода продукта на рынок.",
    )
    supplier: models.Field = models.ForeignKey(
        NetworkElement,
        on_delete=models.CASCADE,
        verbose_name="Supplier",
        help_text="Поставщик товара.",
        related_name="products",
    )

    def __str__(self):
        """Строковое представление модели"""
        return self.name

    class Meta:
        """Мета данные модели"""

        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("release_date",)
