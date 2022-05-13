from rest_framework import routers
from .views import ItemViewSet, CartItemViewSet


router = routers.SimpleRouter()
router.register("items", ItemViewSet, basename="items")
router.register("cart-items", CartItemViewSet, basename="cart_items")


urlpatterns = router.urls
