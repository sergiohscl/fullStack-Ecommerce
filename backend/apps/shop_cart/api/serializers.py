from rest_framework import serializers
from apps.shop_cart.models import ShopCart


class ShopCartSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    customer = serializers.PrimaryKeyRelatedField(read_only=True)
    itens = serializers.JSONField()
    total = serializers.FloatField(required=False, allow_null=True)
    status = serializers.ChoiceField(
        choices=ShopCart.StatusShopCart.choices
    )
