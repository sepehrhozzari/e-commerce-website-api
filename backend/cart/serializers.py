from rest_framework import serializers
from .models import Item


class ItemDisplaySerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source="like_count")
    dislikes = serializers.IntegerField(source="dislike_count")
    hits = serializers.IntegerField(source="hits_count")
    category = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = "__all__"

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
