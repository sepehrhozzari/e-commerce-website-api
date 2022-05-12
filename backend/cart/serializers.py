from rest_framework import serializers
from .models import Item, CartItem


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
        fields = ("title", "image", "price", "discount_price")


class CartItemSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    item = BasicItemSerializer()

    class Meta:
        model = CartItem
        fields = ("user", "item", "quantity", "is_paid")
