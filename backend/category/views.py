from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategoryDisplaySerializer, CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.is_active().select_related("parent")

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CategoryDisplaySerializer
        return CategorySerializer
