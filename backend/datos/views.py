from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions
from .serializers import RegistrosSerializer
from .serializers import RolCountSerializer
from .serializers import OcupacionSerializer
from rest_framework.views import APIView
from .models import Registros
from rest_framework.response import Response
from django.db.models import Count, Max, Q, When, F, Case, Value
from .models import *
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status

class RegistroViewset(viewsets.ModelViewSet):  
    permission_classes = [permissions.AllowAny]
    queryset = Registros.objects.select_related("usuario").all()  
    serializer_class = RegistrosSerializer

    def list(self, request):
        queryset = self.get_queryset()  
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class OcupacionView(APIView):

    def get(self, request, *args, **kwargs):
        # Obtenemos todos los registros de entrada
        registros_entrada = Registros.objects.filter(movimiento='entrada')

        ultima_salida = Registros.objects.filter(movimiento='salida') \
            .values('usuario') \
            .annotate(ultima_salida=Max('fecha'))
        
        # Filtramos a los usuarios cuya última entrada no tenga una salida posterior
        usuarios_con_entrada_valida = registros_entrada.exclude(usuario__in=[usuario['usuario'] for usuario in ultima_salida])

        # Realizamos el conteo de los roles de los usuarios válidos (que no tienen salida después de la entrada)
        rol_count = usuarios_con_entrada_valida.values('usuario__rol').annotate(count=Count('usuario__rol'))

        # Ahora, vamos a modificar el conteo para que 'docente' y 'administrativo' se sumen
        # Modificamos la lógica para agrupar 'docente' y 'administrativo' bajo un solo nombre
        aggregated_data = {}

        for item in rol_count:
            rol = item['usuario__rol']
            count = item['count']
            
            # Si el rol es 'docente' o 'administrativo', los sumamos
            if rol == 'docente' or rol == 'administrativo':
                aggregated_data['doc/adm'] = aggregated_data.get('doc/adm', 0) + count
            else:
                # Para los demás roles, simplemente los agregamos como están
                aggregated_data[rol] = aggregated_data.get(rol, 0) + count

        # Convertimos los datos agregados a un formato adecuado para la serialización
        data = [{'rol': rol, 'count': count} for rol, count in aggregated_data.items()]

        # Serializamos los datos
        # Puedes usar un serializador adecuado o simplemente devolver la data
        # serializer = OcupacionSerializer(data, many=True)

        # Devolvemos la respuesta con los datos serializados
        return Response(data)

@api_view(['POST'])
def register_user(request):
    data = request.data
    # Validar si los campos existen
    if not data.get('username') or not data.get('password'):
        return Response({'error': 'Username y password son requeridos'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Validar si el usuario ya existe
    if User.objects.filter(username=data['username']).exists():
        return Response({'error': 'El usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Crear el usuario
    user = User.objects.create(
        username=data['username'],
        password=make_password(data['password']),
        email=data.get('email', '')
    )
    return Response({'message': 'Usuario creado exitosamente'}, status=status.HTTP_201_CREATED)
    
        
