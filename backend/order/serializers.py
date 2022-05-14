from rest_framework import serializers
from .models import OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")

    class Meta:
        model = OrderItem
        fields = ("user", "item", "quantity", "total_price",
                  "total_discount_price", "total_amount_saved")
