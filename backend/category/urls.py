from rest_framework import routers
from .views import CategoryViewSet


router = routers.SimpleRouter()
router.register("categories", CategoryViewSet, basename="categories")

app_name = "category"

urlpatterns = router.urls
