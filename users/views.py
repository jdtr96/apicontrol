from rest_framework.permissions import BasePermission
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action


class IsPostRequest(BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST"


class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsPostRequest]

    @action(methods=["post"], detail=False)
    def verificar_token(self, request, *args, **kwargs):
        data = request.data
        iduser = Token.objects.all().filter(
            key=data["token"]).values("user")
        for id in iduser:
            res = id.get('user')
        user = User.objects.filter(id=res).values("username", "password")
        for u in user:
            use = u
        print(user)
        return Response(data=(data, use))

    @action(methods=["post"], detail=False)
    def verificar_login(self, request, *args, **kwargs):
        data = request.data
        idu = 0
        iduser = User.objects.filter(username=data["username"]).values("id")
        for item in iduser:
            idu = item.get("id")
        print(idu)
        token = Token.objects.all().filter(
            user=idu).values("key")
        for item in token:
            token = item
        print(token)
        return Response(data=(data, token))
