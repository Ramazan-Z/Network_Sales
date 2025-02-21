from rest_framework import serializers

from network import models, validators
from products.serializers import ProductSerializer


class ContactDataSerializer(serializers.ModelSerializer):
    """Сериализатор контактных данных"""

    class Meta:
        model = models.ContactData
        exclude = ("id",)


class NetworkElementSerializer(serializers.ModelSerializer):
    """Сериализатор элемента сети продаж"""

    contact_data = ContactDataSerializer(help_text="Контактные данные")
    level = serializers.SerializerMethodField(help_text="Уровень иерархии")

    @staticmethod
    def get_level(network_element) -> int | None:
        """Получение уровня иерархии"""
        if network_element.level:
            return int(network_element.level)
        return None

    def create(self, validated_data):
        """Создание объекта вложенного поля (контактных данных)"""
        contact_data = validated_data.pop("contact_data")
        contacts = models.ContactData.objects.create(**contact_data)
        return models.NetworkElement.objects.create(contact_data=contacts, **validated_data)

    def update(self, network_element, validated_data):
        """Обновление объекта вложенного поля (контактных данных)"""
        contact_data = validated_data.pop("contact_data", None)
        contacts = network_element.contact_data

        if contact_data:
            for field, value in contact_data.items():
                setattr(contacts, field, value)
            contacts.save()

        for field, value in validated_data.items():
            setattr(network_element, field, value)
        network_element.save()

        return network_element

    def get_validators(self):
        """Проверка рекурсии поставщика"""
        return [validators.SupplierValidator(self.context)]

    class Meta:
        model = models.NetworkElement
        fields = "__all__"
        read_only_fields = ("debt", "created_at")


class RetrieveNetworkElementSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра элемента сети продаж"""

    contact_data = ContactDataSerializer(help_text="Контактные данные")
    products = ProductSerializer(many=True, help_text="Товары")
    level = serializers.SerializerMethodField(help_text="Уровень иерархии")

    @staticmethod
    def get_level(network_element) -> int | None:
        """Получение уровня иерархии"""
        if network_element.level:
            return int(network_element.level)
        return None

    class Meta:
        model = models.NetworkElement
        fields = "__all__"
