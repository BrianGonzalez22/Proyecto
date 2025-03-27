import random
from datetime import datetime, timedelta, time
from datos.models import Registros, Usuarios, Vehiculos
from django.utils import timezone

def generar_hora_aleatoria(hora_inicio, hora_fin):
    """Genera una hora aleatoria dentro del rango especificado, sin zona horaria."""
    # Crea fechas 'naive' (sin zona horaria)
    inicio = datetime.combine(datetime.today(), hora_inicio)
    fin = datetime.combine(datetime.today(), hora_fin)
    
    # Calcula el delta de tiempo entre el inicio y el fin
    delta = fin - inicio
    
    # Genera una hora aleatoria dentro del rango de tiempo
    return inicio + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

def insertar_registros(dias=5):
    usuarios = list(Usuarios.objects.all())
    vehiculos = list(Vehiculos.objects.all())

    if not usuarios or not vehiculos:
        print("No hay usuarios o vehículos registrados.")
        return

    for dia in range(dias):
        fecha_base = datetime.now() + timedelta(days=dia)
        registros_a_crear = []

        # Seleccionamos usuarios únicos para entradas (máximo 250 o menos)
        usuarios_para_entrada = random.sample(usuarios, min(len(usuarios), 250))

        # Crear entradas
        entradas = {}
        for usuario in usuarios_para_entrada:
            vehiculo = random.choice([v for v in vehiculos if v.usuario == usuario])
            hora_aleatoria = generar_hora_aleatoria(time(6, 0), time(12, 0))
            fecha_hora = fecha_base.replace(hour=hora_aleatoria.hour, minute=hora_aleatoria.minute, second=hora_aleatoria.second)

            registro = Registros(
                usuario=usuario,
                vehiculo=vehiculo,
                movimiento='entrada',
                fecha=fecha_hora
            )
            registros_a_crear.append(registro)
            entradas[usuario] = fecha_hora

        # Crear salidas solo para quienes tienen entrada
        for usuario, hora_entrada in entradas.items():
            vehiculo = random.choice([v for v in vehiculos if v.usuario == usuario])
            hora_salida = generar_hora_aleatoria((hora_entrada + timedelta(minutes=30)).time(), time(20, 0))
            fecha_salida = fecha_base.replace(hour=hora_salida.hour, minute=hora_salida.minute, second=hora_salida.second)

            if fecha_salida > fecha_hora:  # Validación para asegurar que la salida sea posterior
                registros_a_crear.append(Registros(
                    usuario=usuario,
                    vehiculo=vehiculo,
                    movimiento='salida',
                    fecha=fecha_salida
                ))

        print(f"Registros creados para el día: {fecha_base.date()} (Entradas: {len(entradas)}, Salidas: {len(registros_a_crear) - len(entradas)})")

        # Inserción masiva
        Registros.objects.bulk_create(registros_a_crear)

    print("Registros creados exitosamente.")

# Ejecutar la función
insertar_registros(30)
