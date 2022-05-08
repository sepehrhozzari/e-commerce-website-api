from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import User
from .serializers import UserSerializer, CustomizedUserDetailSerializer
from .permissions import IsSuperUserOrAdmin
from dj_rest_auth.views import UserDetailsView


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUserOrAdmin, ]


class UserRetrieve(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUserOrAdmin, ]


class CustomizedUserDetailsView(UserDetailsView):
    serializer_class = CustomizedUserDetailSerializer
