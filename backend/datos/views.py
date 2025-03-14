from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions
from .serializers import RegistrosSerializer
from .serializers import RolCountSerializer
from .serializers import OcupacionSerializer
from rest_framework.views import APIView
from .models import Registros
from rest_framework.response import Response
from django.db.models import Count, Max, Q
from .models import Usuarios
from rest_framework.decorators import action

class RegistroViewset(viewsets.ModelViewSet):  
    permission_classes = [permissions.AllowAny]
    queryset = Registros.objects.select_related("usuario").all()  
    serializer_class = RegistrosSerializer

    def list(self, request):
        queryset = self.get_queryset()  
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    

class RolCountView(viewsets.ViewSet):
    """
    ViewSet para contar los usuarios por rol.
    """

    def list(self, request):
        # Realizamos un conteo de los usuarios por rol
        roles = Usuarios.objects.values('rol').annotate(count=Count('rol'))

        # Convertimos los resultados a un formato adecuado para serializar
        data = [{'rol': item['rol'], 'count': item['count']} for item in roles]

        # Serializamos los datos
        serializer = RolCountSerializer(data, many=True)

        # Devolvemos la respuesta con los datos serializados
        return Response(serializer.data)
    

class OcupacionView(APIView):

    def get(self, request, *args, **kwargs):
        # Obtenemos todos los registros de entrada
        registros_entrada = Registros.objects.filter(movimiento='entrada')

        ultima_salida = Registros.objects.filter(movimiento='salida') \
            .values('usuario') \
            .annotate(ultima_salida=Max('fecha'))
        
        # Filtramos a los usuarios cuya última entrada no tenga una salida posterior
        usuarios_con_entrada_valida = registros_entrada.exclude(usuario__in=[usuario['usuario'] for usuario in ultima_salida]
        )

        # Realizamos el conteo de los roles de los usuarios válidos (que no tienen salida después de la entrada)
        rol_count = usuarios_con_entrada_valida.values('usuario__rol').annotate(count=Count('usuario__rol'))

        # Serializamos los datos
        data = [{'rol': item['usuario__rol'], 'count': item['count']} for item in rol_count]

        return Response(data)

    
        
