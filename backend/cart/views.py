from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Item
from .serializers import ItemDisplaySerializer, ItemSerializer
from rest_framework.permissions import IsAuthenticated
from account.permissions import IsAdminOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.prefetch_related("likes", "dislikes", "hits")
    filterset_fields = ("in_stock",)
    search_fields = ("title", "description")
    ordering_fields = ("in_stock",)

    def get_permissions(self):
        if self.action in ["like", "dislike"]:
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAdminOrReadOnly]
        return (permission() for permission in permission_classes)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ItemDisplaySerializer
        return ItemSerializer

    def retrieve(self, request, *args, **kwargs):
        item = self.get_object()
        if request.ip_address not in item.hits.all():
            item.hits.add(request.ip_address)
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=["get"])
    def like(self, request, pk=None):
        item = self.get_object()
        if request.user in item.dislikes.all():
            item.dislikes.remove(request.user)
            if request.user in item.likes.all():
                item.likes.remove(request.user)
                message += "لایک و دیس لایک برای محصول مورد نظر پاک شد"
            else:
                item.likes.add(request.user)
                message = "دیس لایک برای محصول مورد نظر پاک و لایک انجام شد"
        else:
            if request.user in item.likes.all():
                item.likes.remove(request.user)
                message = "لایک برای محصول مورد نظر برداشته شد"
            else:
                item.likes.add(request.user)
                message = "محصول مورد نظر لایک شد"
        return Response({"message": message}, status=HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def dislike(self, request, pk=None):
        item = self.get_object()
        if request.user in item.likes.all():
            item.likes.remove(request.user)
            if request.user in item.dislikes.all():
                item.dislikes.remove(request.user)
                message = "لایک و دیس لایک برای محصول مورد نظر برداشته شد"
            else:
                item.dislikes.add(request.user)
                message = "لایک برای محصول مورد نظر برداشته و دیس لاک شد"
        else:
            if request.user in item.dislikes.all():
                item.dislikes.remove(request.user)
                message = "دیس لایک برای محصول مورد نظر با موفقیت برداشته شد"
            else:
                item.dislikes.add(request.user)
                message = "محصول مورد نظر دیس لایک شد"
        return Response({"message": message}, status=HTTP_200_OK)
