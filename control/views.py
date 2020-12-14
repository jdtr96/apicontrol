from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, AllowAny
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status, viewsets
from .serializers import ProductoSerializer
from .models import Producto
from rest_framework.decorators import action
from django.db.models import Avg
# Create your views here.


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        per = ["GET", "PATCH"]
        return request.method in per


class ProductoViewset(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated | ReadOnly]

    def get_queryset(self, pk=None):
        queryset = Producto.objects.all()
        if self.request.user.id:
            print(self.request.user.id)
            print(self.kwargs.get('pk'))
            print(self.request.data)
            return queryset.filter(user=self.request.user.id)
        return queryset

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        data = request.data
        producto = self.get_object()
        producto.nombre = data["nombre"]
        producto.cantidad = data["cantidad"]
        producto.p_conpra = data["p_conpra"]
        producto.p_venta = data["p_venta"]
        producto.cantidad_vendidos = data["cantidad_vendidos"]

        resultado = Producto.objects.filter(
            id=self.kwargs.get('pk')).values('user')
        for id in resultado:
            res = id.get('user')
        if self.request.user.id == res:
            producto.save()
        return Response(ProductoSerializer(producto).data)

    def destroy(self, request, *args, **kwargs):
        producto = self.get_object()
        resultado = Producto.objects.filter(
            id=self.kwargs.get('pk')).values('user')
        for id in resultado:
            res = id.get('user')
        if self.request.user.id == res:
            self.perform_destroy(producto)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @ action(methods=['get'], detail=False)
    def reporte_venta_total(self, request):
        productos = Producto.objects.filter(user=self.request.user.id).values(
            'nombre', 'cantidad_vendidos', 'p_venta')
        return Response(data=productos)

    @ action(methods=['get'], detail=False)
    def venta_total(self, request):
        suma = 0
        productos = Producto.objects.filter(user=self.request.user.id).values(
            'nombre', 'cantidad_vendidos', 'p_venta')
        for dato in productos:
            mult = dato['cantidad_vendidos'] * dato['p_venta']
            suma = suma + mult
        return Response(data=suma)

    @ action(methods=['get'], detail=False)
    def promedio(self, request):
        promedio = Producto.objects.filter(
            user=self.request.user.id).aggregate(Avg('p_venta'))
        return Response(data=promedio)
