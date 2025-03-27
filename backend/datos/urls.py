from django.urls import path, include
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
from . import views


router = DefaultRouter()
router.register('registros',RegistroViewset, basename ='registros' )

urlpatterns = [
    path('', include(router.urls)),  # Incluye todas las rutas del router
    path('ocupacion-list/', OcupacionView.as_view(), name='ocupacion-list'),  # Agrega la vista manualmente
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register_user, name='register_user'),
    path('vehiculos-hoy/', VehiculosHoyView.as_view(), name='vehiculos_hoy'),
    path('obtener-registros/', views.obtener_registro_por_id, name='obtener_registro_por_id'),
]
