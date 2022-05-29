from rest_framework import routers
from .views import OrderViewSet


router = routers.SimpleRouter()
router.register("orders", OrderViewSet, basename="orders")

app_name = "order"

urlpatterns = router.urls
