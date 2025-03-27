from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions
from .serializers import RegistrosSerializer
from .serializers import RolCountSerializer
from .serializers import OcupacionSerializer
from rest_framework.views import APIView
from .models import Registros
from rest_framework.response import Response
from django.db.models import Count, Max, When, Case, Value, CharField, F
from .models import *
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.utils import timezone


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
        # Obtener la fecha actual con rango de tiempo (inicio y fin del día)
        today = timezone.now().date()
        start_of_day = timezone.make_aware(datetime.combine(today, datetime.min.time()))
        end_of_day = timezone.make_aware(datetime.combine(today, datetime.max.time()))

        # Obtener las últimas entradas y salidas por usuario (solo del día actual)
        ultimas_entradas = Registros.objects.filter(
            movimiento='entrada',
            fecha__range=(start_of_day, end_of_day)
        ).values('usuario').annotate(ultima_entrada=Max('fecha'))

        ultimas_salidas = Registros.objects.filter(
            movimiento='salida',
            fecha__range=(start_of_day, end_of_day)
        ).values('usuario').annotate(ultima_salida=Max('fecha'))

        # Crear un diccionario con las últimas salidas
        salidas_dict = {item['usuario']: item['ultima_salida'] for item in ultimas_salidas}

        # Hora actual para comparar con las salidas
        hora_actual = timezone.now()

        # Filtrar los usuarios cuya última entrada no tenga una salida posterior
        usuarios_con_entrada_ocupada = []
        usuarios_con_entrada_sin_salida = []

        for entrada in ultimas_entradas:
            usuario_id = entrada['usuario']
            ultima_entrada = entrada['ultima_entrada']
            ultima_salida = salidas_dict.get(usuario_id)

            # Si no hay salida o la última salida es en el futuro, consideramos la entrada como ocupada
            if not ultima_salida or ultima_salida > hora_actual:
                usuarios_con_entrada_ocupada.append(usuario_id)
            else:
                usuarios_con_entrada_sin_salida.append(usuario_id)

        # Realizar el conteo de roles de los usuarios ocupados
        rol_count_ocupados = Registros.objects.filter(
            usuario__in=usuarios_con_entrada_ocupada, 
            movimiento='entrada',
            fecha__range=(start_of_day, end_of_day)
        ).values('usuario__rol').annotate(count=Count('usuario__rol'))

        # Agrupar 'docente' y 'administrativo' bajo 'doc/adm'
        aggregated_data_ocupados = {}
        for item in rol_count_ocupados:
            rol = item['usuario__rol']
            count = item['count']

            if rol in ['docente', 'administrativo']:
                aggregated_data_ocupados['doc/adm'] = aggregated_data_ocupados.get('doc/adm', 0) + count
            else:
                aggregated_data_ocupados[rol] = aggregated_data_ocupados.get(rol, 0) + count

        # Formatear los resultados para entradas ocupadas
        data_ocupados = [{'rol': rol, 'count': count} for rol, count in aggregated_data_ocupados.items()]

        # Realizar el conteo de roles de los usuarios sin salida
        rol_count_sin_salida = Registros.objects.filter(
            usuario__in=usuarios_con_entrada_sin_salida,
            movimiento='entrada',
            fecha__range=(start_of_day, end_of_day)
        ).values('usuario__rol').annotate(count=Count('usuario__rol'))

        # Agrupar 'docente' y 'administrativo' bajo 'doc/adm'
        aggregated_data_sin_salida = {}
        for item in rol_count_sin_salida:
            rol = item['usuario__rol']
            count = item['count']

            if rol in ['docente', 'administrativo']:
                aggregated_data_sin_salida['doc/adm'] = aggregated_data_sin_salida.get('doc/adm', 0) + count
            else:
                aggregated_data_sin_salida[rol] = aggregated_data_sin_salida.get(rol, 0) + count

        # Formatear los resultados para entradas sin salida
        data_sin_salida = [{'rol': rol, 'count': count} for rol, count in aggregated_data_sin_salida.items()]

        # Combinar los resultados de las entradas ocupadas y sin salida
        data_final = {'ocupados': data_ocupados, 'sin_salida': data_sin_salida}

        return Response(data_final)

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


class VehiculosHoyView(APIView):

    def get(self, request, *args, **kwargs):
        # Obtener la fecha actual (sin hora, solo la fecha)
        today = now().date()
        
        # Consulta usando Django ORM
        registros_hoy = Registros.objects.filter(
            fecha__date=today
        ).values('vehiculo__id')


        # Extraer los vehículos únicos
        vehiculos_ids = [registro['vehiculo__id'] for registro in registros_hoy]

        # Devolver los vehículos en formato de respuesta JSON
        return Response({'vehiculos_ids': vehiculos_ids})
    

@api_view(['GET'])
def obtener_registro_por_id(request):
    # Obtener la fecha y hora actual sin zona horaria
    fecha_objetivo = datetime.now()

    # Obtener la hora actual y crear el rango de fecha
    hora = fecha_objetivo.hour
    minuto = fecha_objetivo.minute
    segundo = fecha_objetivo.second
    microsegundo = fecha_objetivo.microsecond

    # Establecer el inicio y fin del día
    inicio_dia = fecha_objetivo.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_dia = fecha_objetivo.replace(hour=hora, minute=minuto, second=segundo, microsecond=microsegundo)

    # Filtrar los registros dentro del rango de la fecha
    registros_entrada_sin_salida = Registros.objects.filter(
        fecha__gte=inicio_dia,
        fecha__lt=fin_dia,
        movimiento='entrada'
    ).exclude(
    usuario_id__in=Registros.objects.filter(
        movimiento='salida',
        fecha__gte=inicio_dia,
        fecha__lt=fin_dia
    ).values('usuario_id')
)
    #print("Número de entradas encontradas:", registros_entrada_sin_salida.count())
    # Agrupar por rol de usuario, combinando "docente" y "administrativo" en un solo grupo
    registros_agrupados = registros_entrada_sin_salida.annotate(
        rol_agrupado=Case(
            When(usuario__rol='docente', then=Value('docente_admin')),
            When(usuario__rol='administrativo', then=Value('docente_admin')),
            default=F('usuario__rol'),
            output_field=CharField()
        )
    ).values('rol_agrupado').annotate(count=Count('id'))

    # Crear la respuesta de los registros agrupados
    resultados = [{'rol': registro['rol_agrupado'], 'count': registro['count']} for registro in registros_agrupados]

    return Response(resultados)




#PRUEBAS##
def obtener():

    fecha_objetivo = datetime.now()

    hora = fecha_objetivo.hour
    minuto = fecha_objetivo.minute
    segundo = fecha_objetivo.second
    microsegundo = fecha_objetivo.microsecond

    print(fecha_objetivo)

    inicio_dia = fecha_objetivo.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_dia = fecha_objetivo.replace(hour= hora, minute=minuto, second=segundo, microsecond=microsegundo)

    print(inicio_dia, fin_dia)
    # Filtrar los registros en el rango
    registros = Registros.objects.filter(fecha__gte=inicio_dia, fecha__lt=fin_dia)

    print(f"Se encontraron {registros.count()} registros con la fecha {fecha_objetivo.date()}")
    for registro in registros:
        print(f"ID: {registro.id}, Fecha: {registro.fecha}, Vehículo ID: {registro.vehiculo_id}")
#PRUEBAS##

def motos():
    fecha_objetivo = datetime.now()

    hora = fecha_objetivo.hour
    minuto = fecha_objetivo.minute
    segundo = fecha_objetivo.second
    microsegundo = fecha_objetivo.microsecond

    inicio_dia = fecha_objetivo.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_dia = fecha_objetivo.replace(hour= hora, minute=minuto, second=segundo, microsecond=microsegundo)

    # Filtrar los registros en el rango
    registros = Registros.objects.filter(fecha__gte=inicio_dia, fecha__lt=fin_dia, usuario__rol='moto')
    entradas = Registros.objects.filter(fecha__gte=inicio_dia, fecha__lt=fin_dia, usuario__rol='moto', movimiento='entrada').count()
    salidas = Registros.objects.filter(fecha__gte=inicio_dia, fecha__lt=fin_dia, usuario__rol='moto',movimiento='salida').count()
    
    print(f"Entradas: {entradas}")
    print(f"Salidas: {salidas}")
    print(f"Se encontraron {registros.count()} ")
    for registro in registros:
        print(f"ID: {registro.id}, Fecha: {registro.fecha},Movimiento : {registro.movimiento}, Vehículo ID: {registro.vehiculo_id}, Rol: {registro.usuario.rol}")