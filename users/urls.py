from django.urls import path, include
from users import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', views.UserViewset, basename="usuario")

urlpatterns = [
    path('', include(router.urls)),
]
