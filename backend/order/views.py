from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from .serializers import OrderSerializer
from .models import Order, OrderItem
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED


class OrderViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin):
    permission_classes = [IsAuthenticated, ]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items").select_related("user")

    def create(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            raise ValidationError("شما سبد خریدی ندارید")

        if not cart.items.exists():
            raise ValidationError("سبد خرید شما خالی میباشد")

        order = Order(user=request.user)
        order.save()
        for cart_item in cart.items.select_related("user", "item"):
            order_item = OrderItem(
                user=cart_item.user, item=cart_item.item, quantity=cart_item.quantity)
            order_item.save()
            order.items.add(order_item)
            cart_item.delete()
        cart.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=HTTP_201_CREATED)
