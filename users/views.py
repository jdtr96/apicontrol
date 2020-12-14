from rest_framework.permissions import BasePermission
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer
from .models import User


class IsPostRequest(BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST"


class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsPostRequest]
