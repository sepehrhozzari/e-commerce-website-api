from rest_framework import routers
from .views import ItemViewSet


router = routers.SimpleRouter()
router.register("items", ItemViewSet, basename="items")


urlpatterns = router.urls
