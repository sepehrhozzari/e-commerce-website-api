from rest_framework import serializers
from .models import OrderItem
from cart.serializers import BasicItemSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    item = BasicItemSerializer()

    class Meta:
        model = OrderItem
        fields = ("user", "item", "quantity", "total_price",
                  "total_discount_price", "total_amount_saved")
