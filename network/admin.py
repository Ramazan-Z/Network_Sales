from django.contrib import admin
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html

from network.models import ContactData, NetworkElement


@admin.register(ContactData)
class ContactDataAdmin(admin.ModelAdmin):
    """Регистрация модели контактов в админке"""

    list_display = ("email", "__str__")
    search_fields = ("country", "city", "street")
    list_filter = ("city",)


@admin.register(NetworkElement)
class NetworkElementAdmin(admin.ModelAdmin):
    """Регистрация модели сетевого звена в админке"""

    list_display = ("name", "level", "supplier_", "customers_", "debt")
    search_fields = ("name",)
    list_filter = ("contact_data__city", "supplier")
    actions = ("clear_debt",)

    def delete_queryset(self, request, queryset):
        """Переоределение метода для каскадного удаления контактов"""
        for item in queryset:
            self.delete_model(request, item)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Фильтрация занятых контактов из выпадающего списка"""
        if db_field.name == "contact_data":
            object_id = request.resolver_match.kwargs.get("object_id")
            kwargs["queryset"] = ContactData.objects.filter(Q(element=None) | Q(element=object_id))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.display(description="Level")
    def level(self, network_element):
        """Уровень в иерархической структуре"""
        return network_element.level

    @admin.display(description="Supplier")
    def supplier_(self, network_element):
        """Ссылка на поставщика"""
        supplier = network_element.supplier
        if supplier:
            link = reverse("admin:network_networkelement_change", args=[supplier.pk])
            return format_html("<a href='{}'>{}</a>", link, supplier)

    @admin.display(description="Customers")
    def customers_(self, network_element):
        """Ссылка на потребителей"""
        if network_element.customers.exists():
            link = reverse("admin:network_networkelement_changelist") + f"?supplier__id__exact={network_element.pk}"
            return format_html("<a href='{}'>{}</a>", link, "open")

    @admin.action(description="Clear the debt owed to the supplier by the selected objects.")
    def clear_debt(self, request, queryset):
        """ "Очистка задолженнностей перед поставщиком"""
        queryset.update(debt=0)
