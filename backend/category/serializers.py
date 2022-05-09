from rest_framework import serializers
from .models import Category


class CategoryDisplaySerializer(serializers.ModelSerializer):
    parent = serializers.CharField(source="parent.title")

    class Meta:
        model = Category
        exclude = ("is_active",)
