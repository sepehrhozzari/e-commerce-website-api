from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Item, CartItem, Cart
from .serializers import (
    ItemDisplaySerializer,
    ItemSerializer,
    CartItemSerializer,
    CartSerializer,
)
from rest_framework.permissions import IsAuthenticated
from account.permissions import IsAdminOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_206_PARTIAL_CONTENT,
    HTTP_204_NO_CONTENT,
)
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin
)
from rest_framework.viewsets import GenericViewSet
from .permissions import IsAdminOrCustomer
from rest_framework.generics import RetrieveDestroyAPIView


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


class CartItemViewSet(ListModelMixin, CreateModelMixin,
                      RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAdminOrCustomer, ]
    serializer_class = CartItemSerializer
    search_fields = ("item__title", "item__description",
                     "user__username", "user__first_name")

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related("user", "item")

    def create(self, request, *args, **kwargs):
        item = Item.objects.get(pk=request.data["item_pk"])
        try:
            cart_item = CartItem.objects.get(
                user=request.user, item=item)
            cart_item.quantity += 1
            cart_item.save()
            status = HTTP_206_PARTIAL_CONTENT
        except:
            cart_item = CartItem.objects.create(
                user=request.user, item=item)
            status = HTTP_201_CREATED
            try:
                cart = Cart.objects.get(user=request.user)
                cart.items.add(cart_item)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(user=request.user)
                cart.items.add(cart_item)

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status)

    @action(detail=True, methods=["delete"])
    def single_cart_item_delete(self, request, pk=None):
        cart_item = self.get_object()
        if cart_item.quantity == 1:
            cart_item.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            cart_item.quantity -= 1
            cart_item.save()
            return Response({"message": "تعداد سفارش برای محصول کم شد"}, status=HTTP_206_PARTIAL_CONTENT)


class CartRetrieve(RetrieveDestroyAPIView):
    permission_classes = [IsAdminOrCustomer, ]
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.prefetch_related("items").select_related("user")
