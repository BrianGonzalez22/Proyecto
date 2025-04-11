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
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register_user, name='register_user'),
    path('obtener-registros/', obtener_registro_por_id, name='obtener_registro_por_id'),
    path('grafico-data/', GraficoData.as_view(), name='grafico_data'),
    path('obtener-datos/', obtener_datos, name='obtener_datos'),
    path('obtener-fechas-registros/', obtener_fechas_registros, name='obtener_fechas'),
    path('obtener-fechas-filtradas/', obtener_registros_filtrados, name='obtener_fechas_filtradas'),


]
