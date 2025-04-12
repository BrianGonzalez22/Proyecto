import random
from faker import Faker
from .models import Vehiculos, Usuarios

fake = Faker()

def poblar_vehiculos(cantidad=250):
    usuarios_disponibles = list(Usuarios.objects.all())

    if cantidad > len(usuarios_disponibles):
        print("No hay suficientes usuarios únicos para asignar a cada vehículo.")
        return

    usuarios_seleccionados = random.sample(usuarios_disponibles, cantidad)

    colores = ['rojo', 'azul', 'blanco', 'negro', 'gris', 'verde', 'amarillo']
    tipos = ['sedán', 'camioneta', 'moto', 'SUV', 'pickup']

    for usuario in usuarios_seleccionados:
        Vehiculos.objects.create(
            placa=fake.unique.license_plate(),
            modelo=fake.word().capitalize() + f" {random.randint(2005, 2025)}",
            color=random.choice(colores),
            tipo=random.choice(tipos),
            estado=random.randint(0, 1),
            usuario=usuario
        )
    
    print(f"{cantidad} vehículos creados y asignados a usuarios únicos.")