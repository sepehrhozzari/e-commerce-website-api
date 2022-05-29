from django.urls import path
from .views import UserList, UserRetrieve

app_name = "ecommerce_account"
urlpatterns = [
    path('users/', UserList.as_view(), name="users-list"),
    path('users/<int:pk>/', UserRetrieve.as_view(), name="users-detail"),
]
