from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import RegistrosSerializer
from .models import Registros
from rest_framework.response import Response
from rest_framework.decorators import action

class RegistroViewset(viewsets.ModelViewSet):  # Cambiado a ModelViewSet para optimizar
    permission_classes = [permissions.AllowAny]
    queryset = Registros.objects.select_related("usuario").all()  # Optimiza la consulta
    serializer_class = RegistrosSerializer

    def list(self, request):
        queryset = self.get_queryset()  # Obtiene los registros con usuario relacionado
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    


    @action(detail=False, methods=['get'])
    def contar_registros(self,request):
        entradas = Registros.objects.filter(movimiento="entrada").count()
        salidas = Registros.objects.filter(movimiento="salida").count()

        return Response({
            "total_entradas": entradas,
            "total_salidas": salidas
        })
        
