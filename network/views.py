from rest_framework import generics

from network import models, serializers


class NetworkElementList(generics.ListAPIView):
    """
    Принимает параметры пагинации, сортировки, фильтрации и поиска.
    Возвращает постраничный список элементов торговой сети.
    """

    queryset = models.NetworkElement.objects.all()
    serializer_class = serializers.NetworkElementSerializer
    ordering_fields = ("created_at",)
    search_fields = ("name",)
    filterset_fields = ("contact_data__city", "contact_data__country", "supplier")


class NewNetworkElement(generics.CreateAPIView):
    """
    Принимает набор данных для создания элемента торговой сети
    и возвращает JSON ответ с данными успешно созданного объекта.
    """

    queryset = models.NetworkElement.objects.all()
    serializer_class = serializers.NetworkElementSerializer


class RetrieveNetworkElement(generics.RetrieveAPIView):
    """Bозвращает JSON ответ с данными об указанном элементе торговой сети."""

    queryset = models.NetworkElement.objects.all()
    serializer_class = serializers.RetrieveNetworkElementSerializer


class UpdateNetworkElement(generics.UpdateAPIView):
    """
    Принимает набор данных для обновления элемента торговой сети
    и возвращает JSON ответ с данными успешно обновленного объекта.
    """

    queryset = models.NetworkElement.objects.all()
    serializer_class = serializers.NetworkElementSerializer


class DestroyNetworkElement(generics.DestroyAPIView):
    """Удаление указанного элемента торговой сети."""

    queryset = models.NetworkElement.objects.all()
    serializer_class = serializers.NetworkElementSerializer
