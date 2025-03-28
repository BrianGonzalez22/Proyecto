from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions
from .serializers import *
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
from .utils import obtener_inicio_y_fin_del_dia
from collections import defaultdict

class RegistroViewset(viewsets.ModelViewSet):  
    permission_classes = [permissions.AllowAny]
    queryset = Registros.objects.select_related("usuario").all()  
    serializer_class = RegistrosSerializer

    def list(self, request):
        queryset = self.get_queryset()  
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

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


@api_view(['GET'])
def obtener_registro_por_id(request):
    inicio_dia, fin_dia = obtener_inicio_y_fin_del_dia()

    # Obtener todas las entradas dentro del rango de la fecha
    entradas = Registros.objects.filter(
        fecha__gte=inicio_dia,
        fecha__lt=fin_dia,
        movimiento='entrada'
    )

    # Filtrar solo las entradas que no tienen una salida correspondiente
    registros_entrada_sin_salida = []
    for entrada in entradas:
        salida = Registros.objects.filter(
            movimiento='salida',
            usuario_id=entrada.usuario_id,
            vehiculo_id=entrada.vehiculo_id,
            fecha__gte=entrada.fecha,
            fecha__lt=fin_dia
        ).exists()

        # Si no existe una salida, se agrega a la lista
        if not salida:
            registros_entrada_sin_salida.append(entrada)

    # Agrupar por rol de usuario, combinando "docente" y "administrativo" en un solo grupo
    registros_agrupados = (
        Registros.objects.filter(id__in=[r.id for r in registros_entrada_sin_salida])
        .annotate(
            rol_agrupado=Case(
                When(usuario__rol='docente', then=Value('docente_admin')),
                When(usuario__rol='administrativo', then=Value('docente_admin')),
                default=F('usuario__rol'),
                output_field=CharField()
            )
        )
        .values('rol_agrupado')
        .annotate(count=Count('id'))
    )

    # Crear la respuesta de los registros agrupados
    resultados = [{'rol': registro['rol_agrupado'], 'count': registro['count']} for registro in registros_agrupados]

    return Response(resultados)

def obtener():
    inicio_dia, fin_dia = obtener_inicio_y_fin_del_dia()
    # Obtener todos los usuarios que tienen al menos una entrada registrada
    entradas = Registros.objects.filter(movimiento='entrada', fecha__gte=inicio_dia, fecha__lt=fin_dia)
    
    usuarios_con_entrada_y_salida = []

    # Iterar sobre las entradas
    for entrada in entradas:
        # Buscar si existe una salida para la misma entrada (mismo usuario y vehículo)
        salida = Registros.objects.filter(
            movimiento='salida',
            usuario_id=entrada.usuario_id,
            vehiculo_id=entrada.vehiculo_id,
            fecha__gt=entrada.fecha,
            fecha__gte=inicio_dia, 
            fecha__lt=fin_dia,
            
        )
        
        for salida in salida:
            # Si existe una salida correspondiente, agregar el usuario y el vehículo a la lista
            usuarios_con_entrada_y_salida.append({
                'usuario_id': entrada.usuario_id,
                'vehiculo_id': entrada.vehiculo_id,
                'entrada': entrada.fecha,
                'salida': salida.fecha
            })
    # Iterar sobre la lista y mostrar los resultados
    
    return usuarios_con_entrada_y_salida

@api_view(['GET'])
def obtener_datos_grafico(request):
    # Llamar a la función que calcula el promedio por 2 horas
    data = calcular_promedio_por_hora()
    
    # Usar el serializador para estructurar los datos, asegurándote de pasar los datos como 'data'
    serializer = PromedioEstanciaSerializer(data=data, many=True)
    
    # Validar y devolver los datos serializados en la respuesta
    if serializer.is_valid():
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)
    

def calcular_promedio_por_hora():
    # Obtener la lista de usuarios con entrada y salida
    usuarios_con_entrada_y_salida = obtener()

    # Crear una lista de estancias con sus intervalos de 1 hora
    estancias = []
    for usuario in usuarios_con_entrada_y_salida:
        entrada = usuario['entrada']
        salida = usuario['salida']
        
        # Calcular la duración de la estancia en minutos
        tiempo_estancia = (salida - entrada).total_seconds() / 60  # Convertir a minutos
        
        # Calcular el intervalo de 1 hora en el que cae la entrada
        hora_inicio_intervalo = entrada.hour  # Tomamos la hora completa para intervalos de 1 hora
        intervalo = f'{hora_inicio_intervalo}:00 - {hora_inicio_intervalo + 1}:00'  # Intervalo de 1 hora
        
        # Agregar la estancia con el intervalo y el tiempo de estancia
        estancias.append({
            'usuario_id': usuario['usuario_id'],
            'intervalo': intervalo,
            'tiempo_estancia': tiempo_estancia
        })
    
    # Agrupar las estancias por intervalo de 1 hora
    agrupados_por_intervalo = defaultdict(list)
    for estancia in estancias:
        agrupados_por_intervalo[estancia['intervalo']].append(estancia['tiempo_estancia'])

    # Calcular el promedio ponderado por intervalo de 1 hora
    promedio_ponderado_por_intervalo = []
    for intervalo, tiempos in agrupados_por_intervalo.items():
        total_tiempos = sum(tiempos)  # Sumar todos los tiempos de ocupación
        total_usuarios = len(tiempos)  # Número total de usuarios en el intervalo
        
        promedio = total_tiempos / total_usuarios if total_usuarios > 0 else 0  # Calcular el promedio ponderado
        
        promedio_ponderado_por_intervalo.append({
            'intervalo': intervalo,
            'tiempo_estancia_promedio': promedio
        })

    # Ordenar los intervalos por la hora de inicio del intervalo (numéricamente)
    promedio_ponderado_por_intervalo.sort(key=lambda x: x['intervalo'])
    
    return promedio_ponderado_por_intervalo




#PRUEBAS##
def usuario():
    inicio_dia, fin_dia = obtener_inicio_y_fin_del_dia()

    entradas = Registros.objects.filter(movimiento='entrada', fecha__gte=inicio_dia, fecha__lt=fin_dia)
    salidas = Registros.objects.filter(movimiento='salida', fecha__gte=inicio_dia, fecha__lt=fin_dia)

    for x in entradas:
        print(f"id: {x.usuario} entrada")

    for x in salidas:
        print(f"id: {x.usuario} salida")
#PRUEBAS##