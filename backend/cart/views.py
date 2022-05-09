from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Item
from .serializers import ItemDisplaySerializer, ItemSerializer
from account.permissions import IsAdminOrReadOnly


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.in_stock().prefetch_related("likes", "dislikes", "hits")
    permission_classes = [IsAdminOrReadOnly, ]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ItemDisplaySerializer
        return ItemSerializer
