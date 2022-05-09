from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Category
from account.permissions import IsAdminOrReadOnly
from .serializers import CategoryDisplaySerializer, CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.is_active().select_related("parent")
    permission_classes = [IsAdminOrReadOnly, ]
    filterset_fields = ("position",)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CategoryDisplaySerializer
        return CategorySerializer
