from rest_framework import serializers
from .models import Item, CartItem, Cart


class ItemDisplaySerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source="likes.count")
    dislikes = serializers.IntegerField(source="dislikes.count")
    hits = serializers.IntegerField(source="hits.count")
    category = serializers.SerializerMethodField()

    class Meta:
        model = Item
        exclude = ("created", "updated")

    def get_category(self, obj):
        return {
            "title": obj.category.title,
            "image": obj.category.image.url,
            "position": obj.category.position,
        }


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ("likes", "dislikes", "hits")


class BasicItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("pk", "title", "image", "price", "discount_price")


class CartItemSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    item = BasicItemSerializer()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=0)
    total_discount_price = serializers.DecimalField(
        max_digits=10, decimal_places=0)
    amount_saved = serializers.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        model = CartItem
        fields = ("user", "item", "quantity", "total_price",
                  "total_discount_price", "amount_saved")
