from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import User
from .serializers import UserSerializer, CustomizedUserDetailSerializer
from .permissions import IsAdmin
from dj_rest_auth.views import UserDetailsView


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin, ]
    filterset_fields = ("city", "is_staff", "is_superuser")
    search_fields = ("username", "first_name", "last_name", "email", "address")


class UserRetrieve(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin, ]


class CustomizedUserDetailsView(UserDetailsView):
    serializer_class = CustomizedUserDetailSerializer
