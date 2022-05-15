from rest_framework import serializers
from .models import OrderItem, Order
from cart.serializers import BasicItemSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    item = BasicItemSerializer()

    class Meta:
        model = OrderItem
        fields = ("user", "item", "quantity", "total_price",
                  "total_discount_price", "total_amount_saved")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("user", "status", "items", "total_price",
                  "total_discount_price", "total_amount_saved")
