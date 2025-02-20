from typing import Self

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class ContactData(models.Model):
    """Контактные данные поставщика"""

    email: models.Field = models.EmailField(
        verbose_name="Email",
        help_text="Электронная почта",
    )
    country: models.Field = models.CharField(
        max_length=150,
        verbose_name="Country",
        help_text="Страна",
    )
    city: models.Field = models.CharField(
        max_length=150,
        verbose_name="City",
        help_text="Город",
    )
    street: models.Field = models.CharField(
        max_length=150,
        verbose_name="Street",
        help_text="Улица",
    )
    house_number: models.Field = models.CharField(
        max_length=10,
        verbose_name="House number",
        help_text="Номер дома",
    )

    def __str__(self):
        """Строковое представление модели"""
        return f"{self.country}, г.{self.city}, ул.{self.street}, д.{self.house_number}"

    class Meta:
        """Мета данные модели"""

        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ("country", "city", "street", "house_number")


class NetworkElement(models.Model):
    """Модель сетевого звена"""

    customers: models.query.QuerySet

    name: models.Field = models.CharField(
        max_length=150,
        verbose_name="Name",
        help_text="Название",
    )
    contact_data: models.Field | ContactData = models.OneToOneField(
        ContactData,
        on_delete=models.PROTECT,
        verbose_name="Contact data",
        help_text="Контактные данные",
        related_name="element",
    )
    supplier: models.Field | Self = models.ForeignKey(
        "NetworkElement",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Supplier",
        help_text="Поставщик",
        related_name="customers",
    )
    debt: models.Field = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Debt",
        help_text="Задолженность перед поставщиком",
        validators=(MinValueValidator(0),),
    )
    created_at: models.Field = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date of creation",
        help_text="Дата и время создания",
    )

    def __str__(self):
        """Строковое представление модели"""
        return self.name

    @property
    def level(self):
        """Получение уровня в иерархической структуре"""
        if not self.supplier and self.customers.exists():
            return 0  # Завод
        if self.supplier and self.customers.exists():
            return 1  # Розничная сеть
        if self.supplier and not self.customers.exists():
            return self.supplier.level + 1  # ИП
        return  # Без уровня, если нет ни поставщиков ни клиентов

    def clean(self):
        """Валидация случая рекурсии поставщика"""
        if self.supplier == self:
            raise ValidationError("An element of the sales network cannot be a supplier for itself.")

    def delete(self, *args, **kwargs):
        """Каскадное удаление контактов сетевого звена"""
        super().delete(*args, **kwargs)
        self.contact_data.delete()

    class Meta:
        """Мета данные модели"""

        verbose_name = "Network element"
        verbose_name_plural = "Network elements"
        ordering = ("created_at",)
