from django.urls import path, include
from control import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'producto', views.ProductoViewset, basename="producto")


urlpatterns = [
    path('', include(router.urls)),
]
