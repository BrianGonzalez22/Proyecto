from django.urls import path, include
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register('registros',RegistroViewset, basename ='registros' )
router.register('conteo',RolCountView, basename ='conteo' )


urlpatterns = [
    path('', include(router.urls)),  # Incluye todas las rutas del router
    path('ocupacion-list/', OcupacionView.as_view(), name='ocupacion-list'),  # Agrega la vista manualmente

  
]
