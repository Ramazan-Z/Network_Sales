from rest_framework.serializers import ValidationError


class SupplierValidator:
    """Валидация случая рекурсии поставщика"""

    def __init__(self, context):
        self.view = context["view"]

    def __call__(self, data):
        instance = self.view.get_object() if "pk" in self.view.kwargs else None
        supplier = data.get("supplier")
        if instance and instance == supplier:
            raise ValidationError("An element of the sales network cannot be a supplier for itself.")
