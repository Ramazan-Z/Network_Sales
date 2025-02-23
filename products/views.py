from rest_framework.viewsets import ModelViewSet

from products import models, serializers


class ProductsViewSet(ModelViewSet):
    """ViewSet для работы с товарами"""

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filterset_fields = ("supplier",)
    search_fields = ("name", "model")
    ordering_fields = ("release_date",)
