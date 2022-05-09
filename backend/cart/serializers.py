from rest_framework import serializers
from .models import Item


class ItemDisplaySerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source="like_count")
    dislikes = serializers.IntegerField(source="dislike_count")
    hits = serializers.IntegerField(source="hits_count")

    class Meta:
        model = Item
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ("likes", "dislikes", "hits")
