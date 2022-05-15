from django.urls import path, include
from rest_framework import routers
from .views import ItemViewSet, CartItemViewSet, CartRetrieve, CartList


router = routers.SimpleRouter()
router.register("items", ItemViewSet, basename="items")
router.register("cart-items", CartItemViewSet, basename="cart-items")


urlpatterns = [
    path('', include(router.urls)),
    path('carts/detail/', CartRetrieve.as_view(), name="cart-detail"),
    path('carts/', CartList.as_view(), name="cart-list"),
]
